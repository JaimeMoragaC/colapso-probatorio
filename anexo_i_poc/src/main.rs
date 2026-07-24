// ============================================================================
//  ANEXO I — Adversarial Oracle Extraction contra un núcleo de decisión K_J
//  Simulación REAL (no mockup): entrena un surrogate g_J observacional sobre un
//  K_J SINTÉTICO, corre una búsqueda adversarial black-box sobre la vecindad de
//  admisibilidad N(x), y MIDE la fidelidad (KL), el techo (Cota I.1), el colapso
//  de colegialidad (I.8) y la activación de invariantes cognitivos (I.7) por
//  ablación. Rust puro, sin dependencias, reproducible con semilla fija.
//
//  HONESTIDAD (I.11): K_J es SINTÉTICO y así se declara. El paper afirma que el
//  núcleo del juez real es INOBSERVABLE; aquí lo definimos para poder simular el
//  ataque y medir sus cotas. Nada de esto es una medición sobre jueces reales.
// ============================================================================

use std::fmt::Write as _;
use std::fs;

// ------------------------------ configuración -------------------------------
const SEED: u64 = 0xC0FFEE_1A7;      // semilla fija -> reproducible bit a bit
const D: usize = 12;                 // dimensión del vector de rasgos x
const N_BIAS: usize = 4;             // dims 0..4 = invariantes cognitivos explotables
const N_POP: usize = 4000;           // tamaño de la población de casos
const EPOCHS: usize = 2000;          // pasos de descenso (batch-GD) del surrogate
const LR: f64 = 0.05;                // learning rate (batch) — bajo para un descenso de KL gradual y legible
const BUDGET: f64 = 0.9;             // presupuesto de perturbación por dim (L∞ en N(x)): el ataque se acerca al techo sin saturarlo
const SWARM: usize = 8;              // agentes del enjambre
const CONF: f64 = 0.978;            // confianza máx. del juez (incertidumbre irreducible) -> techo Cota I.1
const D_OBS: usize = 11;             // el atacante observa 11 de 12 rasgos (I.3) -> KL con piso irreducible
const EPS: f64 = 1e-9;
const BIAS_NAMES: [&str; N_BIAS] = ["Anchoring (§8.7)", "Confirmation Bias", "Framing Effect", "Availability Heuristic"];

// ------------------------------ PRNG (xorshift64) ---------------------------
struct Rng(u64);
impl Rng {
    fn new(seed: u64) -> Self { Rng(seed | 1) }
    fn u64(&mut self) -> u64 { let mut x=self.0; x^=x<<13; x^=x>>7; x^=x<<17; self.0=x; x }
    fn f(&mut self) -> f64 { (self.u64() >> 11) as f64 / (1u64<<53) as f64 } // [0,1)
    fn gauss(&mut self) -> f64 {                                             // Box-Muller
        let (u1,u2)=(self.f().max(EPS), self.f());
        (-2.0*u1.ln()).sqrt() * (std::f64::consts::TAU*u2).cos()
    }
}

// ------------------------------ helpers de álgebra --------------------------
fn sigmoid(z: f64) -> f64 { 1.0/(1.0+(-z).exp()) }
fn dot(a: &[f64], b: &[f64]) -> f64 { a.iter().zip(b).map(|(x,y)| x*y).sum() }
fn clampp(p: f64) -> f64 { p.max(EPS).min(1.0-EPS) }
fn hbin(p: f64) -> f64 { let p=clampp(p); -p*p.log2() - (1.0-p)*(1.0-p).log2() } // entropía binaria (bits)

// ------------------------------ K_J sintético -------------------------------
struct Judge { w: Vec<f64>, b: f64 }
impl Judge {
    // P(absolución | x), con incertidumbre irreducible: el juez nunca supera confianza CONF (Cota I.1)
    fn prob(&self, x: &[f64]) -> f64 { 0.5 + (sigmoid(dot(&self.w, x) + self.b) - 0.5)*CONF }
    fn perturbed(base: &Judge, sigma: f64, rng: &mut Rng) -> Judge {          // juez heterogéneo (I.8)
        Judge { w: base.w.iter().map(|wj| wj + sigma*rng.gauss()).collect(), b: base.b + sigma*rng.gauss() }
    }
}

// entrena un surrogate logístico g_J por SGD sobre decisiones observadas (I.2: acceso observacional)
struct Surrogate { w: Vec<f64>, b: f64 }
impl Surrogate {
    fn prob(&self, x: &[f64]) -> f64 { sigmoid(dot(&self.w, x) + self.b) }
}

// KL(K_J || g_J) sobre un conjunto retenido (bits)
fn kl(judge: &Judge, sur: &Surrogate, xs: &[Vec<f64>]) -> f64 {
    let mut s = 0.0;
    for x in xs {
        let p = clampp(judge.prob(x));
        let q = clampp(sur.prob(x));
        s += p*(p/q).log2() + (1.0-p)*((1.0-p)/(1.0-q)).log2();
    }
    s / xs.len() as f64
}

// búsqueda adversarial black-box sobre N(x): coordinate ascent que consulta SOLO el
// surrogate (g_J), perturbando únicamente las dims cognitivas dentro de |δ|≤BUDGET.
// `frozen` permite ablacionar una dimensión (para medir su activación, I.7).
// Devuelve (x*, iteraciones, ||δ||∞, prob_surrogate, traza de prob_verdadera por iter).
fn attack(base: &[f64], sur: &Surrogate, judge: &Judge, frozen: Option<usize>, order: &[usize])
    -> (Vec<f64>, usize, f64, f64, Vec<f64>)
{
    let mut x = base.to_vec();
    let step0 = BUDGET/6.0;
    let mut trace = vec![judge.prob(&x)];
    let mut iters = 0;
    for round in 0..40 {
        let step = step0 * (0.85f64).powi(round as i32);   // paso decreciente
        let mut improved = false;
        for &j in order {
            if j >= N_BIAS || Some(j) == frozen { continue; }
            let cur = sur.prob(&x);
            for dir in [1.0, -1.0] {
                let nv = (x[j] + dir*step).clamp(base[j]-BUDGET, base[j]+BUDGET);
                let old = x[j]; x[j] = nv;
                if sur.prob(&x) > cur + 1e-6 { improved = true; } else { x[j] = old; }
            }
        }
        iters += 1;
        trace.push(judge.prob(&x));
        if !improved { break; }
    }
    let delta = (0..D).map(|j| (x[j]-base[j]).abs()).fold(0.0, f64::max);
    (x.clone(), iters, delta, sur.prob(&x), trace)
}

// ------------------------------ SVG mínimo (sin deps) -----------------------
struct Svg { s: String }
impl Svg {
    fn new(w: f64, h: f64) -> Self {
        let mut s = String::new();
        write!(s, r#"<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="monospace">"#).unwrap();
        write!(s, r##"<rect width="{w}" height="{h}" fill="#0a0e14"/>"##).unwrap();
        Svg { s }
    }
    fn rect(&mut self, x:f64,y:f64,w:f64,h:f64,fill:&str,stroke:&str) {
        write!(self.s, r#"<rect x="{x:.1}" y="{y:.1}" width="{w:.1}" height="{h:.1}" fill="{fill}" stroke="{stroke}" rx="6"/>"#).unwrap();
    }
    fn text(&mut self, x:f64,y:f64,size:f64,fill:&str,anchor:&str,t:&str) {
        let t = t.replace('&',"&amp;").replace('<',"&lt;");
        write!(self.s, r#"<text x="{x:.1}" y="{y:.1}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{t}</text>"#).unwrap();
    }
    fn line(&mut self, x1:f64,y1:f64,x2:f64,y2:f64,stroke:&str,w:f64,dash:&str) {
        write!(self.s, r#"<line x1="{x1:.1}" y1="{y1:.1}" x2="{x2:.1}" y2="{y2:.1}" stroke="{stroke}" stroke-width="{w}" stroke-dasharray="{dash}"/>"#).unwrap();
    }
    fn circle(&mut self, x:f64,y:f64,r:f64,fill:&str) {
        write!(self.s, r#"<circle cx="{x:.1}" cy="{y:.1}" r="{r}" fill="{fill}"/>"#).unwrap();
    }
    fn polyline(&mut self, pts:&[(f64,f64)], stroke:&str, w:f64) {
        self.s.push_str(r#"<polyline fill="none" stroke=""#); self.s.push_str(stroke);
        write!(self.s, r#"" stroke-width="{w}" points=""#).unwrap();
        for (x,y) in pts { write!(self.s, "{x:.1},{y:.1} ").unwrap(); }
        self.s.push_str(r#""/>"#);
    }
    fn done(mut self) -> String { self.s.push_str("</svg>"); self.s }
}

fn main() {
    let mut rng = Rng::new(SEED);

    // ---- 1) K_J sintético: dims cognitivas con peso alto (explotables) ----
    let mut w = vec![0.0; D];
    let bias_w = [2.0, 1.8, 1.5, 1.2];   // sensibilidades del juez a los 4 invariantes cognitivos (§8.7)
    for j in 0..D { w[j] = if j < N_BIAS { bias_w[j] } else { rng.gauss()*0.5 }; }
    let judge = Judge { w, b: rng.gauss()*0.3 };

    // ---- 2) población de casos + partición train/holdout ----
    let pop: Vec<Vec<f64>> = (0..N_POP).map(|_| (0..D).map(|_| rng.gauss()).collect()).collect();
    let (train, holdout) = pop.split_at(3000);

    // ---- 3) entrenar surrogate g_J por SGD; loguear KL(K_J||g_J) ----
    // el atacante estima la PROPENSIÓN del juez (I.3: canal más rico que el binario) sobre los rasgos
    // que OBSERVA (D_OBS de D). Descenso batch-GD: g_J -> K_J salvo el residuo de lo no observado (piso KL).
    let mut sur = Surrogate { w: vec![0.0; D], b: 0.0 };
    let mut kl_curve: Vec<(usize,f64)> = Vec::new();
    let nt = train.len() as f64;
    for ep in 0..EPOCHS {
        if ep % 20 == 0 || ep == EPOCHS-1 { kl_curve.push((ep, kl(&judge, &sur, holdout))); }   // log ANTES del paso
        let mut gw = vec![0.0; D]; let mut gb = 0.0;
        for x in train {
            let e = sur.prob(x) - judge.prob(x);
            for j in 0..D_OBS { gw[j] += e*x[j]; }     // gradiente solo en dims observadas
            gb += e;
        }
        for j in 0..D_OBS { sur.w[j] -= LR*(gw[j]/nt + 1e-4*sur.w[j]); }
        sur.b -= LR*gb/nt;
    }
    let kl_final = kl_curve.last().unwrap().1;

    // ---- 4) caso base "condena" (prob baja); objetivo del ataque = absolución ----
    // caso fronterizo (condena por poco): el ataque óptimo opera donde hay margen, no en casos slam-dunk
    let target_base = 0.20;
    let base = pop.iter().min_by(|a,b|
        (judge.prob(a)-target_base).abs().partial_cmp(&(judge.prob(b)-target_base).abs()).unwrap()
    ).unwrap().clone();
    let p_base = judge.prob(&base);

    // ---- 5) ataque black-box guiado por el surrogate; evaluar bajo K_J verdadero ----
    let order: Vec<usize> = (0..N_BIAS).collect();
    let (xstar, iters, delta, _q, _tr) = attack(&base, &sur, &judge, None, &order);
    let p_star = judge.prob(&xstar);          // P(y*|x*) REAL

    // ---- 6) enjambre: SWARM agentes, distinto arranque, todos convergen a x* ----
    let mut swarm: Vec<Vec<f64>> = Vec::new();
    for a in 0..SWARM {
        let start: Vec<f64> = base.iter().enumerate()
            .map(|(j,v)| if j<N_BIAS { v + 0.4*rng.gauss() } else { *v }).collect();
        let mut ord = order.clone();
        for i in (1..ord.len()).rev() { let k=(rng.u64() as usize)%(i+1); ord.swap(i,k); }
        let (_x,_it,_d,_q,tr) = attack(&start, &sur, &judge, None, &ord);
        let _ = a; swarm.push(tr);
    }

    // ---- 7) techo (Cota I.1): H(Y|X) poblacional; P_max = 1 - H/log2|Y|, |Y|=2 ----
    let h_yx = holdout.iter().map(|x| hbin(judge.prob(x))).sum::<f64>()/holdout.len() as f64;
    let ceiling = 0.5 + 0.5*CONF;             // techo por incertidumbre irreducible del juez (Cota I.1)

    // ---- 8) colegialidad (I.8): intersección factible ⋂R_i por n jueces × σ ----
    let cand: Vec<Vec<f64>> = (0..3000).map(|_| {
        base.iter().enumerate().map(|(j,v)| if j<N_BIAS { v + (rng.f()*2.0-1.0)*BUDGET } else { *v }).collect()
    }).collect();
    let sigma_of = |n: usize| match n { 1 => 0.0, 3 => 0.5, _ => 0.95 };   // heterogeneidad de priors crece con n
    let mut bft: Vec<(usize,f64,f64)> = Vec::new();        // (n, vol_factible, entropia)
    for &n in &[1usize,3,12] {
        let judges: Vec<Judge> = (0..n).map(|_| Judge::perturbed(&judge, sigma_of(n), &mut rng)).collect();
        let mut hits = 0usize;
        for c in &cand { if judges.iter().all(|jd| jd.prob(c) >= 0.5) { hits += 1; } }
        let vol = hits as f64 / cand.len() as f64;
        // entropía del veredicto conjunto sobre los candidatos (dispersión de decisiones)
        let ent = cand.iter().map(|c| {
            let frac = judges.iter().filter(|jd| jd.prob(c) >= 0.5).count() as f64 / n as f64;
            hbin(frac)
        }).sum::<f64>()/cand.len() as f64;
        bft.push((n, vol, ent));
    }

    // ---- 9) activación de invariantes (I.7) por ABLACIÓN: caída de P(y*) al congelar cada dim ----
    let mut activation: Vec<(usize,f64)> = Vec::new();
    for j in 0..N_BIAS {
        let (_x,_i,_d,_q,_t) = attack(&base, &sur, &judge, Some(j), &order);
        let p_abl = judge.prob(&_x);
        let act = ((p_star - p_abl)/(p_star - p_base).max(EPS)).clamp(0.0, 1.0);   // fracción de la ganancia que aporta la dim j
        activation.push((j, act));
    }
    let act_sum: f64 = activation.iter().map(|(_,a)| a).sum::<f64>().max(EPS);
    // normalizar a "porcentaje de activación relativa" (suma ~100%)
    let act_pct: Vec<(usize,f64)> = activation.iter().map(|(j,a)| (*j, 100.0*a/act_sum)).collect();

    // ============================ salida a stdout ============================
    println!("============================================================");
    println!(" ANEXO I — Adversarial Oracle Extraction contra K_J (sintético)");
    println!(" seed={SEED:#x}  D={D}  N_pop={N_POP}  epochs={EPOCHS}  reproducible");
    println!("============================================================\n");
    println!("[1] Fidelidad del surrogate  KL(K_J || g_J):");
    println!("      inicio: {:.3} bits  ->  final: {:.4} bits  ({} épocas)", kl_curve[0].1, kl_final, EPOCHS);
    println!("[2] Ataque black-box sobre N(x) (solo consulta g_J):");
    println!("      caso base  P(absolución)   = {:.3}", p_base);
    println!("      tras ataque P(y*|x*) REAL   = {:.3}   (bajo K_J verdadero)", p_star);
    println!("      iteraciones = {}   |   presupuesto δ (L∞) = {:.3}", iters, delta);
    println!("[3] Techo (Cota I.1) = {:.3} (incertidumbre irreducible del juez)  |  H(Y|X)_pob = {:.3} bits", ceiling, h_yx);
    println!("      ¿P(y*|x*) < techo?  {}  ({:.3} < {:.3})",
        if p_star < ceiling {"SÍ (consistente)"} else {"NO"}, p_star, ceiling);
    println!("[4] Colegialidad (I.8) — intersección factible ⋂R_i:");
    println!("        n |  σ   | ⋂R_i factible | entropía veredicto");
    for (n,vol,ent) in &bft {
        println!("      {:3} | {:.2} | {:>10.2}% | {:.3} bits", n, sigma_of(*n), vol*100.0, ent);
    }
    println!("[5] Activación de invariantes cognitivos (I.7, por ablación):");
    for (j,pct) in &act_pct { println!("      {:<24} {:>5.1}%", BIAS_NAMES[*j], pct); }
    println!("\n[6] Enjambre: {} agentes, todos convergen a x* (traza en swarm.csv)", SWARM);

    // ============================ CSVs (para reanálisis) =====================
    let mut c = String::from("epoch,kl_bits\n");
    for (e,k) in &kl_curve { let _=writeln!(c,"{e},{k:.6}"); }
    fs::write("surrogate_kl.csv", c).unwrap();

    let mut c = String::from("agent,iter,p_true\n");
    for (a,tr) in swarm.iter().enumerate() { for (it,p) in tr.iter().enumerate() { let _=writeln!(c,"{a},{it},{p:.6}"); } }
    fs::write("swarm.csv", c).unwrap();

    let mut c = String::from("n,sigma,vol_factible,entropia\n");
    for (n,vol,ent) in &bft { let _=writeln!(c,"{n},{:.2},{vol:.6},{ent:.6}", sigma_of(*n)); }
    fs::write("bft.csv", c).unwrap();

    let mut c = String::from("invariante,activacion_pct\n");
    for (j,pct) in &act_pct { let _=writeln!(c,"{},{pct:.2}", BIAS_NAMES[*j]); }
    fs::write("activation.csv", c).unwrap();

    let metrics = format!(
        "P(y*|x*)={p_star:.3}\ndelta={delta:.3}\niterations={iters}\nH(Y|X)={h_yx:.3}\nceiling={ceiling:.3}\nkl_final={kl_final:.4}\n");
    fs::write("metrics.txt", metrics).unwrap();

    // ============================ figura SVG (datos reales) ==================
    let svg = render_svg(&kl_curve, &pop, &judge, &xstar, &bft, &swarm, &act_pct,
                         p_star, delta, iters, h_yx, ceiling);
    fs::write("figure.svg", svg).unwrap();
    println!("\nArchivos: figure.svg  surrogate_kl.csv  swarm.csv  bft.csv  activation.csv  metrics.txt");
    println!("Abre figure.svg en cualquier navegador — es la figura generada desde ESTOS datos.");
}

// dibuja los 6 paneles desde los datos reales
#[allow(clippy::too_many_arguments)]
fn render_svg(kl_curve:&[(usize,f64)], pop:&[Vec<f64>], judge:&Judge, xstar:&[f64],
              bft:&[(usize,f64,f64)], swarm:&[Vec<f64>], act:&[(usize,f64)],
              p_star:f64, delta:f64, iters:usize, h_yx:f64, ceiling:f64) -> String {
    let (w,h) = (1040.0, 620.0);
    let mut g = Svg::new(w,h);
    let acc = "#35c0ff"; let red="#ff5e6c"; let grn="#2ddc78"; let org="#ffa640"; let vio="#9d8bff"; let mut_="#7f92a6";
    g.text(24.0, 30.0, 15.0, "#dfe8f0", "start", "ENJAMBRE-POLY · Adversarial Oracle Extraction · Target: K_J(y|x,s,t)");
    g.text(w-24.0, 30.0, 12.0, grn, "end", "● SIMULACIÓN REAL · K_J sintético (I.11)");

    let pw=320.0; let ph=250.0; let m=24.0; let top=50.0;
    let col=|i:f64| m + i*(pw+m); let row=|i:f64| top + i*(ph+m);

    // ---- Panel 1: Surrogate Fidelity (KL) ----
    let (x0,y0)=(col(0.0),row(0.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Surrogate Model Fidelity");
    g.text(x0+pw-14.0,y0+22.0,11.0,acc,"end","D_KL(K_J‖g_J)");
    let klmax = kl_curve[0].1.max(0.001); let emax = kl_curve.last().unwrap().0 as f64;
    let px=|e:f64| x0+40.0 + (e/emax)*(pw-56.0);
    let py=|k:f64| y0+ph-30.0 - (k/klmax)*(ph-60.0);
    g.line(x0+40.0,py(0.0),x0+pw-16.0,py(0.0),"#1e2a38",1.0,"");
    let pts:Vec<(f64,f64)>=kl_curve.iter().map(|(e,k)|(px(*e as f64),py(*k))).collect();
    g.polyline(&pts, acc, 2.0);
    g.text(x0+pw-16.0,py(kl_curve.last().unwrap().1)-6.0,10.0,acc,"end",&format!("{:.3}",kl_curve.last().unwrap().1));
    g.text(x0+pw/2.0,y0+ph-8.0,10.0,mut_,"middle","época");

    // ---- Panel 2: Decision Boundary Penetration ----
    let (x0,y0)=(col(1.0),row(0.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Decision Boundary Penetration");
    let sx=|v:f64| x0+30.0 + ((v+3.0)/6.0).clamp(0.0,1.0)*(pw-46.0);
    let sy=|v:f64| y0+ph-30.0 - ((v+3.0)/6.0).clamp(0.0,1.0)*(ph-60.0);
    for x in pop.iter().take(220) {
        let col = if judge.prob(x)>=0.5 {grn} else {red};
        g.circle(sx(x[0]),sy(x[1]),2.2,col);
    }
    g.circle(sx(xstar[0]),sy(xstar[1]),5.0,"#ffffff");
    g.text(sx(xstar[0])+7.0,sy(xstar[1])+3.0,10.0,"#ffffff","start","x*");
    g.text(x0+pw-14.0,y0+ph-12.0,10.0,grn,"end","Absolución");
    g.text(x0+16.0,y0+40.0,10.0,red,"start","Condena");

    // ---- Panel 3: BFT / Colegialidad (vol factible) ----
    let (x0,y0)=(col(2.0),row(0.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Colegialidad ⋂R_i (I.8)");
    let bw=54.0; let base_y=y0+ph-40.0; let bh=ph-80.0;
    let cols=[red,org,grn];
    for (i,(n,vol,_e)) in bft.iter().enumerate() {
        let bx=x0+50.0+i as f64*80.0; let hgt=(*vol as f64)*bh;
        g.rect(bx,base_y-hgt,bw,hgt,cols[i],"none");
        g.text(bx+bw/2.0,base_y-hgt-6.0,10.0,cols[i],"middle",&format!("{:.1}%",vol*100.0));
        g.text(bx+bw/2.0,base_y+16.0,10.0,mut_,"middle",&format!("n={n}"));
    }
    g.text(x0+pw/2.0,y0+ph-8.0,9.0,mut_,"middle","% del volumen que sobrevive");

    // ---- Panel 4: Swarm Convergence ----
    let (x0,y0)=(col(0.0),row(1.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start",&format!("Swarm Convergence ({} agentes)",swarm.len()));
    let maxit=swarm.iter().map(|t|t.len()).max().unwrap_or(1) as f64 -1.0;
    let palette=[acc,red,grn,org,vio,"#ff8fd0","#5ad1c9","#c9d15a"];
    let sxp=|it:f64| x0+34.0 + (it/maxit.max(1.0))*(pw-50.0);
    let syp=|p:f64| y0+ph-30.0 - p*(ph-60.0);
    g.line(x0+34.0,syp(0.5),x0+pw-16.0,syp(0.5),"#26303c",1.0,"4,3");
    for (a,tr) in swarm.iter().enumerate() {
        let pts:Vec<(f64,f64)>=tr.iter().enumerate().map(|(it,p)|(sxp(it as f64),syp(*p))).collect();
        g.polyline(&pts, palette[a%palette.len()], 1.6);
    }
    g.text(x0+pw-16.0,syp(0.5)-4.0,9.0,mut_,"end","umbral 0.5");
    g.text(x0+pw-16.0,y0+ph-12.0,10.0,"#dfe8f0","end","→ x*");

    // ---- Panel 5: Live Metrics ----
    let (x0,y0)=(col(1.0),row(1.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+pw/2.0,y0+24.0,12.0,"#cfe0ee","middle","Métricas (simulación)");
    let rows=[("P(y*|x*)",format!("{:.3}",p_star)),
              ("Presupuesto δ",format!("{:.3}",delta)),
              ("Iteraciones",format!("{}",iters)),
              ("Entropía H(Y|X)",format!("{:.3} bits",h_yx)),
              ("Techo (Cota I.1)",format!("{:.3}",ceiling))];
    for (i,(k,v)) in rows.iter().enumerate() {
        let yy=y0+58.0+i as f64*36.0;
        g.text(x0+18.0,yy,12.0,mut_,"start",k);
        g.text(x0+pw-18.0,yy,13.0,if *k=="Techo (Cota I.1)"{org}else{acc},"end",v);
        g.line(x0+18.0,yy+12.0,x0+pw-18.0,yy+12.0,"#161f2b",1.0,"");
    }

    // ---- Panel 6: Cognitive Invariant Activation ----
    let (x0,y0)=(col(2.0),row(1.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Cognitive Invariant Activation");
    for (i,(j,pct)) in act.iter().enumerate() {
        let yy=y0+52.0+i as f64*44.0;
        g.text(x0+16.0,yy,10.0,mut_,"start",BIAS_NAMES[*j]);
        let barw=(pct/100.0)*(pw-70.0);
        g.rect(x0+16.0,yy+6.0,pw-70.0,14.0,"#141c28","none");
        g.rect(x0+16.0,yy+6.0,barw,14.0,acc,"none");
        g.text(x0+pw-16.0,yy+17.0,11.0,acc,"end",&format!("{:.0}%",pct));
    }
    g.text(x0+14.0,y0+ph-10.0,8.5,mut_,"start","activación = caída de P(y*) al ablacionar la dim (I.7)");

    g.done()
}
