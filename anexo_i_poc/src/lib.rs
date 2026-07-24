// ============================================================================
//  ANEXO I — Adversarial Oracle Extraction contra un núcleo de decisión K_J
//  Biblioteca compartida: la MISMA simulación corre nativa (main.rs) y en el
//  navegador vía WebAssembly (export render_svg_wasm). Rust puro, sin dependencias.
//
//  HONESTIDAD (I.11): K_J es SINTÉTICO y así se declara. No es una medición sobre
//  jueces reales; el paper sostiene que el núcleo real es inobservable.
// ============================================================================
#![allow(static_mut_refs)]

use std::fmt::Write as _;

// ------------------------------ configuración -------------------------------
pub const SEED_DEFAULT: u64 = 0xC0FFEE_1A7;
pub const BUDGET_DEFAULT: f64 = 0.9;
const D: usize = 12;
const N_BIAS: usize = 4;
const N_POP: usize = 4000;
const EPOCHS: usize = 2000;
const LR: f64 = 0.05;
const SWARM: usize = 8;
const CONF: f64 = 0.978;
const D_OBS: usize = 11;
const EPS: f64 = 1e-9;
pub const BIAS_NAMES: [&str; N_BIAS] = ["Anchoring (§8.7)", "Confirmation Bias", "Framing Effect", "Availability Heuristic"];

// ------------------------------ PRNG (xorshift64) ---------------------------
struct Rng(u64);
impl Rng {
    fn new(seed: u64) -> Self { Rng(seed | 1) }
    fn u64(&mut self) -> u64 { let mut x=self.0; x^=x<<13; x^=x>>7; x^=x<<17; self.0=x; x }
    fn f(&mut self) -> f64 { (self.u64() >> 11) as f64 / (1u64<<53) as f64 }
    fn gauss(&mut self) -> f64 {
        let (u1,u2)=(self.f().max(EPS), self.f());
        (-2.0*u1.ln()).sqrt() * (std::f64::consts::TAU*u2).cos()
    }
}

fn sigmoid(z: f64) -> f64 { 1.0/(1.0+(-z).exp()) }
fn dot(a: &[f64], b: &[f64]) -> f64 { a.iter().zip(b).map(|(x,y)| x*y).sum() }
fn clampp(p: f64) -> f64 { p.max(EPS).min(1.0-EPS) }
fn hbin(p: f64) -> f64 { let p=clampp(p); -p*p.log2() - (1.0-p)*(1.0-p).log2() }

struct Judge { w: Vec<f64>, b: f64 }
impl Judge {
    fn prob(&self, x: &[f64]) -> f64 { 0.5 + (sigmoid(dot(&self.w, x) + self.b) - 0.5)*CONF }
    fn perturbed(base: &Judge, sigma: f64, rng: &mut Rng) -> Judge {
        Judge { w: base.w.iter().map(|wj| wj + sigma*rng.gauss()).collect(), b: base.b + sigma*rng.gauss() }
    }
}

struct Surrogate { w: Vec<f64>, b: f64 }
impl Surrogate { fn prob(&self, x: &[f64]) -> f64 { sigmoid(dot(&self.w, x) + self.b) } }

fn kl(judge: &Judge, sur: &Surrogate, xs: &[Vec<f64>]) -> f64 {
    let mut s = 0.0;
    for x in xs {
        let p = clampp(judge.prob(x)); let q = clampp(sur.prob(x));
        s += p*(p/q).log2() + (1.0-p)*((1.0-p)/(1.0-q)).log2();
    }
    s / xs.len() as f64
}

fn attack(base: &[f64], sur: &Surrogate, judge: &Judge, frozen: Option<usize>, order: &[usize], budget: f64)
    -> (Vec<f64>, usize, f64, f64, Vec<f64>)
{
    let mut x = base.to_vec();
    let step0 = budget/6.0;
    let mut trace = vec![judge.prob(&x)];
    let mut iters = 0;
    for round in 0..40 {
        let step = step0 * (0.85f64).powi(round as i32);
        let mut improved = false;
        for &j in order {
            if j >= N_BIAS || Some(j) == frozen { continue; }
            let cur = sur.prob(&x);
            for dir in [1.0, -1.0] {
                let nv = (x[j] + dir*step).clamp(base[j]-budget, base[j]+budget);
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

// ------------------------------ resultado -----------------------------------
pub struct RunOut {
    pub svg: String,
    pub kl_curve: Vec<(usize,f64)>,
    pub swarm: Vec<Vec<f64>>,
    pub bft: Vec<(usize,f64,f64)>,
    pub sigmas: Vec<f64>,
    pub activation: Vec<(usize,f64)>,
    pub p_base: f64, pub p_star: f64, pub iters: usize, pub delta: f64,
    pub h_yx: f64, pub ceiling: f64, pub kl_start: f64, pub kl_final: f64,
}

/// Corre la simulación completa con parámetros (seed, budget de N(x), het = escala de
/// heterogeneidad de priors) y devuelve todos los datos + la figura SVG.
pub fn run(seed: u64, budget: f64, het: f64) -> RunOut {
    let mut rng = Rng::new(seed);

    let mut w = vec![0.0; D];
    let bias_w = [2.0, 1.8, 1.5, 1.2];
    for j in 0..D { w[j] = if j < N_BIAS { bias_w[j] } else { rng.gauss()*0.5 }; }
    let judge = Judge { w, b: rng.gauss()*0.3 };

    let pop: Vec<Vec<f64>> = (0..N_POP).map(|_| (0..D).map(|_| rng.gauss()).collect()).collect();
    let (train, holdout) = pop.split_at(3000);

    let mut sur = Surrogate { w: vec![0.0; D], b: 0.0 };
    let mut kl_curve: Vec<(usize,f64)> = Vec::new();
    let nt = train.len() as f64;
    for ep in 0..EPOCHS {
        if ep % 20 == 0 || ep == EPOCHS-1 { kl_curve.push((ep, kl(&judge, &sur, holdout))); }
        let mut gw = vec![0.0; D]; let mut gb = 0.0;
        for x in train {
            let e = sur.prob(x) - judge.prob(x);
            for j in 0..D_OBS { gw[j] += e*x[j]; }
            gb += e;
        }
        for j in 0..D_OBS { sur.w[j] -= LR*(gw[j]/nt + 1e-4*sur.w[j]); }
        sur.b -= LR*gb/nt;
    }
    let kl_start = kl_curve[0].1; let kl_final = kl_curve.last().unwrap().1;

    let tb = 0.20;
    let base = pop.iter().min_by(|a,b|
        (judge.prob(a)-tb).abs().partial_cmp(&(judge.prob(b)-tb).abs()).unwrap()).unwrap().clone();
    let p_base = judge.prob(&base);

    let order: Vec<usize> = (0..N_BIAS).collect();
    let (xstar, iters, delta, _q, _tr) = attack(&base, &sur, &judge, None, &order, budget);
    let p_star = judge.prob(&xstar);

    let mut swarm: Vec<Vec<f64>> = Vec::new();
    for _a in 0..SWARM {
        let start: Vec<f64> = base.iter().enumerate()
            .map(|(j,v)| if j<N_BIAS { v + 0.4*rng.gauss() } else { *v }).collect();
        let mut ord = order.clone();
        for i in (1..ord.len()).rev() { let k=(rng.u64() as usize)%(i+1); ord.swap(i,k); }
        let (_x,_it,_d,_q,tr) = attack(&start, &sur, &judge, None, &ord, budget);
        swarm.push(tr);
    }

    let h_yx = holdout.iter().map(|x| hbin(judge.prob(x))).sum::<f64>()/holdout.len() as f64;
    let ceiling = 0.5 + 0.5*CONF;

    let cand: Vec<Vec<f64>> = (0..3000).map(|_| {
        base.iter().enumerate().map(|(j,v)| if j<N_BIAS { v + (rng.f()*2.0-1.0)*budget } else { *v }).collect()
    }).collect();
    let sigma_of = |n: usize| ((match n { 1 => 0.0, 3 => 0.5, _ => 0.95 }) * het).min(1.5);
    let mut bft: Vec<(usize,f64,f64)> = Vec::new();
    let mut sigmas: Vec<f64> = Vec::new();
    for &n in &[1usize,3,12] {
        let s = sigma_of(n); sigmas.push(s);
        let judges: Vec<Judge> = (0..n).map(|_| Judge::perturbed(&judge, s, &mut rng)).collect();
        let mut hits = 0usize;
        for c in &cand { if judges.iter().all(|jd| jd.prob(c) >= 0.5) { hits += 1; } }
        let vol = hits as f64 / cand.len() as f64;
        let ent = cand.iter().map(|c| {
            let frac = judges.iter().filter(|jd| jd.prob(c) >= 0.5).count() as f64 / n as f64;
            hbin(frac)
        }).sum::<f64>()/cand.len() as f64;
        bft.push((n, vol, ent));
    }

    let mut activation: Vec<(usize,f64)> = Vec::new();
    for j in 0..N_BIAS {
        let (xa,_i,_d,_q,_t) = attack(&base, &sur, &judge, Some(j), &order, budget);
        let p_abl = judge.prob(&xa);
        let act = ((p_star - p_abl)/(p_star - p_base).max(EPS)).clamp(0.0, 1.0);
        activation.push((j, act));
    }
    let act_sum: f64 = activation.iter().map(|(_,a)| a).sum::<f64>().max(EPS);
    let act_pct: Vec<(usize,f64)> = activation.iter().map(|(j,a)| (*j, 100.0*a/act_sum)).collect();

    let svg = render_svg(&kl_curve, &pop, &judge, &xstar, &bft, &swarm, &act_pct,
                         p_star, delta, iters, h_yx, ceiling);

    RunOut { svg, kl_curve, swarm, bft, sigmas, activation: act_pct,
             p_base, p_star, iters, delta, h_yx, ceiling, kl_start, kl_final }
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
        write!(self.s, r#"<rect x="{x:.1}" y="{y:.1}" width="{w:.1}" height="{h:.1}" fill="{fill}" stroke="{stroke}" rx="6"/>"#).unwrap(); }
    fn text(&mut self, x:f64,y:f64,size:f64,fill:&str,anchor:&str,t:&str) {
        let t = t.replace('&',"&amp;").replace('<',"&lt;");
        write!(self.s, r#"<text x="{x:.1}" y="{y:.1}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{t}</text>"#).unwrap(); }
    fn line(&mut self, x1:f64,y1:f64,x2:f64,y2:f64,stroke:&str,w:f64,dash:&str) {
        write!(self.s, r#"<line x1="{x1:.1}" y1="{y1:.1}" x2="{x2:.1}" y2="{y2:.1}" stroke="{stroke}" stroke-width="{w}" stroke-dasharray="{dash}"/>"#).unwrap(); }
    fn circle(&mut self, x:f64,y:f64,r:f64,fill:&str) {
        write!(self.s, r#"<circle cx="{x:.1}" cy="{y:.1}" r="{r}" fill="{fill}"/>"#).unwrap(); }
    fn polyline(&mut self, pts:&[(f64,f64)], stroke:&str, w:f64) {
        self.s.push_str(r#"<polyline fill="none" stroke=""#); self.s.push_str(stroke);
        write!(self.s, r#"" stroke-width="{w}" points=""#).unwrap();
        for (x,y) in pts { write!(self.s, "{x:.1},{y:.1} ").unwrap(); }
        self.s.push_str(r#""/>"#); }
    fn done(mut self) -> String { self.s.push_str("</svg>"); self.s }
}

#[allow(clippy::too_many_arguments)]
fn render_svg(kl_curve:&[(usize,f64)], pop:&[Vec<f64>], judge:&Judge, xstar:&[f64],
              bft:&[(usize,f64,f64)], swarm:&[Vec<f64>], act:&[(usize,f64)],
              p_star:f64, delta:f64, iters:usize, h_yx:f64, ceiling:f64) -> String {
    let (w,h) = (1040.0, 620.0);
    let mut g = Svg::new(w,h);
    let acc="#35c0ff"; let red="#ff5e6c"; let grn="#2ddc78"; let org="#ffa640"; let vio="#9d8bff"; let mut_="#7f92a6";
    g.text(24.0, 30.0, 15.0, "#dfe8f0", "start", "ENJAMBRE-POLY · Adversarial Oracle Extraction · Target: K_J(y|x,s,t)");
    g.text(w-24.0, 30.0, 12.0, grn, "end", "● SIMULACIÓN REAL · K_J sintético (I.11)");

    let pw=320.0; let ph=250.0; let m=24.0; let top=50.0;
    let col=|i:f64| m + i*(pw+m); let row=|i:f64| top + i*(ph+m);

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

    let (x0,y0)=(col(1.0),row(0.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Decision Boundary Penetration");
    let sx=|v:f64| x0+30.0 + ((v+3.0)/6.0).clamp(0.0,1.0)*(pw-46.0);
    let sy=|v:f64| y0+ph-30.0 - ((v+3.0)/6.0).clamp(0.0,1.0)*(ph-60.0);
    for x in pop.iter().take(220) {
        let cc = if judge.prob(x)>=0.5 {grn} else {red};
        g.circle(sx(x[0]),sy(x[1]),2.2,cc);
    }
    g.circle(sx(xstar[0]),sy(xstar[1]),5.0,"#ffffff");
    g.text(sx(xstar[0])+7.0,sy(xstar[1])+3.0,10.0,"#ffffff","start","x*");
    g.text(x0+pw-14.0,y0+ph-12.0,10.0,grn,"end","Absolución");
    g.text(x0+16.0,y0+40.0,10.0,red,"start","Condena");

    let (x0,y0)=(col(2.0),row(0.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Colegialidad ⋂R_i (I.8)");
    let bw=54.0; let base_y=y0+ph-40.0; let bh=ph-80.0; let cols=[red,org,grn];
    for (i,(n,vol,_e)) in bft.iter().enumerate() {
        let bx=x0+50.0+i as f64*80.0; let hgt=(*vol)*bh;
        g.rect(bx,base_y-hgt,bw,hgt.max(0.5),cols[i],"none");
        g.text(bx+bw/2.0,base_y-hgt-6.0,10.0,cols[i],"middle",&format!("{:.1}%",vol*100.0));
        g.text(bx+bw/2.0,base_y+16.0,10.0,mut_,"middle",&format!("n={n}"));
    }
    g.text(x0+pw/2.0,y0+ph-8.0,9.0,mut_,"middle","% del volumen que sobrevive");

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

    let (x0,y0)=(col(2.0),row(1.0)); g.rect(x0,y0,pw,ph,"#0d1420","#1e2a38");
    g.text(x0+14.0,y0+22.0,12.0,"#cfe0ee","start","Cognitive Invariant Activation");
    for (i,(j,pct)) in act.iter().enumerate() {
        let yy=y0+52.0+i as f64*44.0;
        g.text(x0+16.0,yy,10.0,mut_,"start",BIAS_NAMES[*j]);
        let barw=(pct/100.0)*(pw-70.0);
        g.rect(x0+16.0,yy+6.0,pw-70.0,14.0,"#141c28","none");
        g.rect(x0+16.0,yy+6.0,barw.max(0.0),14.0,acc,"none");
        g.text(x0+pw-16.0,yy+17.0,11.0,acc,"end",&format!("{:.0}%",pct));
    }
    g.text(x0+14.0,y0+ph-10.0,8.5,mut_,"start","activación = caída de P(y*) al ablacionar la dim (I.7)");

    g.done()
}

// ------------------------------ export WASM ---------------------------------
// Sin wasm-bindgen: la figura SVG se deja en un buffer estático y se pasa por
// (puntero, longitud). budget_milli = budget*1000 ; het_centi = het*100.
static mut SVG_BUF: Vec<u8> = Vec::new();

#[no_mangle]
pub extern "C" fn render_svg_wasm(seed: u32, budget_milli: u32, het_centi: u32) -> *const u8 {
    let svg = run(seed as u64, budget_milli as f64 / 1000.0, het_centi as f64 / 100.0).svg;
    unsafe { SVG_BUF = svg.into_bytes(); SVG_BUF.as_ptr() }
}

#[no_mangle]
pub extern "C" fn svg_len() -> usize { unsafe { SVG_BUF.len() } }
