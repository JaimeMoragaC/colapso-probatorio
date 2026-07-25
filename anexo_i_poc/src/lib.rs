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

pub struct RunOut {
    pub svg: String,
    pub kl_curve: Vec<(usize,f64)>,
    pub swarm: Vec<Vec<f64>>,
    pub bft: Vec<(usize,f64,f64)>,
    pub sigmas: Vec<f64>,
    pub activation: Vec<(usize,f64)>,
    pub p_base: f64, pub p_star: f64, pub iters: usize, pub delta: f64,
    pub h_yx: f64, pub ceiling: f64, pub kl_start: f64, pub kl_final: f64,
    pub surf_ax: Vec<f64>,          // eje u/v de la superficie de decisión
    pub surf_z: Vec<Vec<f64>>,      // z[j][i] = P(absolución) en (u_i, v_j)
    pub xstar3: [f64;3],            // x* sobre la superficie (u,v,z)
    pub path3: Vec<[f64;3]>,        // trayectoria del ataque sobre la superficie
    pub balls: Vec<f64>,            // muestra de casos: su P(absolución) (para la animación de bolas)
}

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

    // superficie de decisión (grid sobre dim0×dim1) para el render 3D del dashboard
    let ng2 = 44usize; let srng = 2.9;
    let surf_ax: Vec<f64> = (0..=ng2).map(|i| -srng + 2.0*srng*(i as f64/ng2 as f64)).collect();
    let zat = |u:f64,v:f64| { let mut xx=base.clone(); xx[0]=u; xx[1]=v; judge.prob(&xx) };
    let mut surf_z = vec![vec![0.0f64; ng2+1]; ng2+1];
    for j in 0..=ng2 { for i in 0..=ng2 { surf_z[j][i] = zat(surf_ax[i], surf_ax[j]); } }
    let cl = |f:f64| f.clamp(-srng, srng);
    let xstar3 = [cl(xstar[0]), cl(xstar[1]), zat(cl(xstar[0]), cl(xstar[1]))];
    let path3: Vec<[f64;3]> = (0..=22).map(|k| {
        let t=k as f64/22.0;
        let u=cl(base[0])+(cl(xstar[0])-cl(base[0]))*t;
        let v=cl(base[1])+(cl(xstar[1])-cl(base[1]))*t;
        [u, v, zat(u,v)]
    }).collect();

    let svg = render_svg(&kl_curve, &judge, &base, &xstar, &bft, &swarm, &act_pct,
                         p_star, delta, iters, h_yx, ceiling);

    // muestra de casos para la animación de bolas (su veredicto bajo K_J)
    let nb = 72usize;
    let balls: Vec<f64> = (0..nb).map(|k| judge.prob(&pop[k * (pop.len()/nb)])).collect();

    RunOut { svg, kl_curve, swarm, bft, sigmas, activation: act_pct,
             p_base, p_star, iters, delta, h_yx, ceiling, kl_start, kl_final,
             surf_ax, surf_z, xstar3, path3, balls }
}

// ------------------------------ SVG premium (sin deps) ----------------------
fn cmix(a:(u8,u8,u8), b:(u8,u8,u8), t:f64) -> (u8,u8,u8) {
    let l=|x:u8,y:u8| (x as f64 + (y as f64 - x as f64)*t.clamp(0.0,1.0)).round() as u8;
    (l(a.0,b.0), l(a.1,b.1), l(a.2,b.2))
}
fn hexf(c:(u8,u8,u8), bright:f64) -> String {
    let g=|x:u8| ((x as f64)*bright).round().clamp(0.0,255.0) as u8;
    format!("#{:02x}{:02x}{:02x}", g(c.0), g(c.1), g(c.2))
}

const DEFS: &str = r##"<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.5" y2="1"><stop offset="0" stop-color="#0c131d"/><stop offset="1" stop-color="#070a11"/></linearGradient>
<linearGradient id="pan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121f2f"/><stop offset="1" stop-color="#0b141f"/></linearGradient>
<linearGradient id="klf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#35c0ff" stop-opacity="0.42"/><stop offset="1" stop-color="#35c0ff" stop-opacity="0"/></linearGradient>
<linearGradient id="bR" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8f2833"/><stop offset="1" stop-color="#ff6b78"/></linearGradient>
<linearGradient id="bO" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8f5f18"/><stop offset="1" stop-color="#ffc061"/></linearGradient>
<linearGradient id="bG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#147040"/><stop offset="1" stop-color="#3ff090"/></linearGradient>
<linearGradient id="bC" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#25607f"/><stop offset="1" stop-color="#5ad1ff"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"##;

struct Svg { s: String }
impl Svg {
    fn new(w:f64,h:f64) -> Self {
        let mut s=String::new();
        write!(s, r#"<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="'Inter','Segoe UI',system-ui,sans-serif">"#).unwrap();
        s.push_str(DEFS);
        write!(s, r#"<rect width="{w}" height="{h}" fill="url(#bg)"/>"#).unwrap();
        Svg { s }
    }
    fn rect(&mut self,x:f64,y:f64,w:f64,h:f64,fill:&str,stroke:&str){ write!(self.s,r#"<rect x="{x:.1}" y="{y:.1}" width="{w:.1}" height="{h:.1}" fill="{fill}" stroke="{stroke}" rx="10"/>"#).unwrap(); }
    fn rrect(&mut self,x:f64,y:f64,w:f64,h:f64,r:f64,fill:&str){ write!(self.s,r#"<rect x="{x:.1}" y="{y:.1}" width="{w:.2}" height="{h:.2}" rx="{r}" fill="{fill}"/>"#).unwrap(); }
    fn text(&mut self,x:f64,y:f64,sz:f64,fill:&str,anc:&str,wt:&str,t:&str){ let t=t.replace('&',"&amp;").replace('<',"&lt;"); write!(self.s,r#"<text x="{x:.1}" y="{y:.1}" font-size="{sz}" fill="{fill}" text-anchor="{anc}" font-weight="{wt}">{t}</text>"#).unwrap(); }
    fn line(&mut self,x1:f64,y1:f64,x2:f64,y2:f64,st:&str,w:f64,dash:&str){ write!(self.s,r#"<line x1="{x1:.1}" y1="{y1:.1}" x2="{x2:.1}" y2="{y2:.1}" stroke="{st}" stroke-width="{w}" stroke-dasharray="{dash}"/>"#).unwrap(); }
    fn circle(&mut self,x:f64,y:f64,r:f64,fill:&str,extra:&str){ write!(self.s,r#"<circle cx="{x:.1}" cy="{y:.1}" r="{r}" fill="{fill}" {extra}/>"#).unwrap(); }
    fn poly(&mut self,pts:&[(f64,f64)],fill:&str,stroke:&str,sw:f64){ self.s.push_str(r#"<polygon points=""#); for (x,y) in pts { write!(self.s,"{x:.1},{y:.1} ").unwrap(); } write!(self.s,r#"" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>"#).unwrap(); }
    fn polyline(&mut self,pts:&[(f64,f64)],st:&str,w:f64,extra:&str){ self.s.push_str(r#"<polyline fill="none" stroke=""#); self.s.push_str(st); write!(self.s,r#"" stroke-width="{w}" {extra} points=""#).unwrap(); for (x,y) in pts { write!(self.s,"{x:.1},{y:.1} ").unwrap(); } self.s.push_str(r#""/>"#); }
    fn done(mut self)->String{ self.s.push_str("</svg>"); self.s }
}

#[allow(clippy::too_many_arguments)]
fn render_svg(kl_curve:&[(usize,f64)], judge:&Judge, base:&[f64], xstar:&[f64],
              bft:&[(usize,f64,f64)], swarm:&[Vec<f64>], act:&[(usize,f64)],
              p_star:f64, delta:f64, iters:usize, h_yx:f64, ceiling:f64) -> String {
    let (w,h)=(1040.0,640.0);
    let mut g=Svg::new(w,h);
    let acc="#4bc7ff"; let mut_="#66788c"; let ink="#d6e4f2";
    g.text(24.0,33.0,15.5,"#eaf2fa","start","700","ENJAMBRE-POLY · Adversarial Oracle Extraction · Target: K_J(y|x,s,t)");
    g.circle(w-278.0,29.0,4.0,"#3ff090","filter=\"url(#glow)\"");
    g.text(w-24.0,33.0,11.5,"#3ff090","end","600","SIMULACIÓN REAL · K_J sintético (I.11)");

    let pw=320.0; let ph=256.0; let m=24.0; let top=54.0;
    let col=|i:f64| m+i*(pw+m); let row=|i:f64| top+i*(ph+m);

    // ===== Panel 1: Surrogate Fidelity (KL) =====
    let (x0,y0)=(col(0.0),row(0.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,acc);
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600","Surrogate Model Fidelity");
    g.text(x0+pw-14.0,y0+26.0,10.5,acc,"end","500","D_KL(K_J‖g_J)");
    let klmax=kl_curve[0].1.max(0.001); let emax=kl_curve.last().unwrap().0 as f64;
    let (gx,gy,gw2,gh2)=(x0+44.0,y0+44.0,pw-62.0,ph-84.0);
    let px=|e:f64| gx+(e/emax)*gw2; let py=|k:f64| gy+(1.0-k/klmax)*gh2;
    for i in 0..=4 { let yy=gy+(i as f64/4.0)*gh2; g.line(gx,yy,gx+gw2,yy,"#182533",1.0,"");
        g.text(gx-7.0,yy+3.0,8.0,"#54677a","end","400",&format!("{:.2}",klmax*(1.0-i as f64/4.0))); }
    let mut area:Vec<(f64,f64)>=kl_curve.iter().map(|(e,k)|(px(*e as f64),py(*k))).collect();
    area.push((px(emax),gy+gh2)); area.push((px(0.0),gy+gh2));
    g.poly(&area,"url(#klf)","none",0.0);
    let line:Vec<(f64,f64)>=kl_curve.iter().map(|(e,k)|(px(*e as f64),py(*k))).collect();
    g.polyline(&line,"#4bc7ff",2.6,"stroke-linejoin=\"round\" stroke-linecap=\"round\" filter=\"url(#glow)\"");
    let last=*kl_curve.last().unwrap();
    g.circle(px(last.0 as f64),py(last.1),3.4,"#8fe0ff","filter=\"url(#glow)\"");
    g.text(px(last.0 as f64)-7.0,py(last.1)-9.0,10.0,"#a9e8ff","end","700",&format!("{:.3}",last.1));
    g.text(x0+pw/2.0,y0+ph-9.0,9.0,mut_,"middle","400","época →");

    // ===== Panel 2: Decision Boundary · superficie 3D de K_J =====
    let (x0,y0)=(col(1.0),row(0.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,"#7fe9ff");
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600","Decision Boundary · superficie K_J");
    let ng=26usize; let rng=2.6; let repr=base;
    let zf=|u:f64,v:f64| { let mut xx=repr.to_vec(); xx[0]=u; xx[1]=v; judge.prob(&xx) };
    let mut z=vec![vec![0.0f64; ng+1]; ng+1];
    for i in 0..=ng { for j in 0..=ng {
        let u=-rng+2.0*rng*(i as f64/ng as f64); let v=-rng+2.0*rng*(j as f64/ng as f64);
        z[i][j]=zf(u,v);
    }}
    let cx=x0+pw*0.5; let cyc=y0+ph*0.63; let ax=pw*0.30; let ay=pw*0.135; let az=ph*0.40;
    let proj=|i:f64,j:f64,zz:f64|->(f64,f64){ let u=i/ng as f64-0.5; let v=j/ng as f64-0.5; (cx+(u-v)*2.0*ax, cyc+(u+v)*2.0*ay - zz*az) };
    let red=(255u8,94,108); let slate=(22u8,31,45); let grn=(45u8,220,120);
    for d in 0..(2*ng-1) {
        for i in 0..ng {
            let jj = d as i64 - i as i64;
            if jj<0 || jj as usize >= ng { continue; }
            let j=jj as usize;
            let (za,zb,zc,zd)=(z[i][j],z[i+1][j],z[i+1][j+1],z[i][j+1]);
            let zavg=(za+zb+zc+zd)*0.25;
            let pts=[proj(i as f64,j as f64,za), proj((i+1) as f64,j as f64,zb),
                     proj((i+1) as f64,(j+1) as f64,zc), proj(i as f64,(j+1) as f64,zd)];
            let base_c= if zavg<0.5 { cmix(red,slate,zavg/0.5) } else { cmix(slate,grn,(zavg-0.5)/0.5) };
            let sh=(0.80 + 1.5*(-(zb-za)-0.5*(zd-za))).clamp(0.50,1.30);
            let zmin=za.min(zb).min(zc).min(zd); let zmax=za.max(zb).max(zc).max(zd);
            let (stroke,sw)= if zmin<0.5 && zmax>0.5 { ("#8ff0ff",1.6) } else { ("#0c1a28",0.4) };
            g.poly(&pts,&hexf(base_c,sh),stroke,sw);
        }
    }
    let cl=|f:f64| f.clamp(-rng,rng);
    let toij=|f0:f64,f1:f64| ((cl(f0)+rng)/(2.0*rng)*ng as f64, (cl(f1)+rng)/(2.0*rng)*ng as f64);
    let (bi,bj)=toij(base[0],base[1]); let (si,sj)=toij(xstar[0],xstar[1]);
    let mut path=Vec::new();
    for k in 0..=14 { let t=k as f64/14.0; let ii=bi+(si-bi)*t; let jj=bj+(sj-bj)*t;
        let u=-rng+2.0*rng*(ii/ng as f64); let v=-rng+2.0*rng*(jj/ng as f64);
        path.push(proj(ii,jj,zf(u,v))); }
    g.polyline(&path,"#ffd24a",2.4,"stroke-linecap=\"round\" filter=\"url(#glow)\"");
    let pbp=proj(bi,bj,zf(cl(base[0]),cl(base[1]))); g.circle(pbp.0,pbp.1,3.0,"#ffd24a","");
    let pstar=proj(si,sj,zf(cl(xstar[0]),cl(xstar[1])));
    g.circle(pstar.0,pstar.1,5.0,"#ffffff","filter=\"url(#glow)\"");
    g.text(pstar.0+9.0,pstar.1-4.0,10.5,"#ffffff","start","700","x*");
    g.text(x0+18.0,y0+ph-14.0,9.0,"#ff6b78","start","500","● condena");
    g.text(x0+pw-16.0,y0+ph-14.0,9.0,"#3ff090","end","500","absolución ●");
    g.text(x0+pw-16.0,y0+42.0,8.5,"#8ff0ff","end","500","— frontera P=0.5");

    // ===== Panel 3: Colegialidad ⋂R_i =====
    let (x0,y0)=(col(2.0),row(0.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,"#3ff090");
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600","Colegialidad ⋂R_i (I.8)");
    let base_y=y0+ph-46.0; let bh=ph-96.0;
    for i in 0..=3 { let yy=base_y-(i as f64/3.0)*bh; g.line(x0+40.0,yy,x0+pw-20.0,yy,"#182533",1.0,""); }
    let grads=["url(#bR)","url(#bO)","url(#bG)"]; let labc=["#ff8a94","#ffcf7a","#7ff0b0"]; let bw=48.0;
    for (i,(n,vol,_e)) in bft.iter().enumerate() {
        let bx=x0+56.0+i as f64*82.0; let hgt=((*vol)*bh).max(2.0);
        g.rrect(bx,base_y-hgt,bw,hgt,5.0,grads[i]);
        g.text(bx+bw/2.0,base_y-hgt-8.0,11.0,labc[i],"middle","700",&format!("{:.1}%",vol*100.0));
        g.text(bx+bw/2.0,base_y+18.0,10.0,mut_,"middle","500",&format!("n={n}"));
    }
    g.text(x0+pw/2.0,y0+ph-10.0,8.5,mut_,"middle","400","% del volumen factible que sobrevive");

    // ===== Panel 4: Swarm Convergence =====
    let (x0,y0)=(col(0.0),row(1.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,"#9d8bff");
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600",&format!("Swarm Convergence · {} agentes",swarm.len()));
    let (gx,gy,gw2,gh2)=(x0+20.0,y0+44.0,pw-40.0,ph-78.0);
    let maxit=swarm.iter().map(|t|t.len()).max().unwrap_or(1) as f64 -1.0;
    for i in 0..=3 { let yy=gy+(i as f64/3.0)*gh2; g.line(gx,yy,gx+gw2,yy,"#152230",1.0,""); }
    let sxp=|it:f64| gx+(it/maxit.max(1.0))*gw2; let syp=|p:f64| gy+(1.0-p)*gh2;
    g.line(gx,syp(0.5),gx+gw2,syp(0.5),"#3a4657",1.0,"5,4");
    let palette=["#4bc7ff","#ff6b78","#3ff090","#ffc061","#9d8bff","#ff8fd0","#5ad1c9","#c9d15a"];
    for (a,tr) in swarm.iter().enumerate() {
        let pts:Vec<(f64,f64)>=tr.iter().enumerate().map(|(it,p)|(sxp(it as f64),syp(*p))).collect();
        g.polyline(&pts,palette[a%palette.len()],1.7,"stroke-linejoin=\"round\" opacity=\"0.9\"");
    }
    g.text(gx+gw2,syp(0.5)-5.0,8.5,mut_,"end","400","umbral 0.5");
    g.text(gx+gw2,y0+ph-12.0,10.0,ink,"end","700","→ x*");

    // ===== Panel 5: Métricas =====
    let (x0,y0)=(col(1.0),row(1.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,acc);
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600","Métricas de la simulación");
    let rows=[("P(y*|x*)",format!("{:.3}",p_star),acc),
              ("Presupuesto δ",format!("{:.3}",delta),acc),
              ("Iteraciones",format!("{}",iters),acc),
              ("Entropía H(Y|X)",format!("{:.3} bits",h_yx),acc),
              ("Techo (Cota I.1)",format!("{:.3}",ceiling),"#ffc061")];
    for (i,(k,v,c)) in rows.iter().enumerate() {
        let yy=y0+62.0+i as f64*33.0;
        g.text(x0+20.0,yy,11.5,"#9fb0c2","start","500",k);
        g.text(x0+pw-20.0,yy,13.5,c,"end","700",v);
        g.line(x0+20.0,yy+10.0,x0+pw-20.0,yy+10.0,"#152230",1.0,"");
    }
    let by=y0+ph-28.0; let bw2=pw-40.0;
    g.rrect(x0+20.0,by,bw2,8.0,4.0,"#152230");
    g.rrect(x0+20.0,by,bw2*p_star.min(1.0),8.0,4.0,"url(#bC)");
    let cxp=x0+20.0+bw2*ceiling.min(1.0);
    g.line(cxp,by-3.0,cxp,by+11.0,"#ffc061",2.0,"");
    g.text(x0+20.0,by-6.0,8.0,mut_,"start","400","P(y*)");
    g.text(cxp,by-6.0,8.0,"#ffc061","middle","500","techo");

    // ===== Panel 6: Cognitive Invariant Activation =====
    let (x0,y0)=(col(2.0),row(1.0));
    g.rect(x0,y0,pw,ph,"url(#pan)","#1e2c3d"); g.rrect(x0+14.0,y0+15.0,3.0,13.0,1.5,acc);
    g.text(x0+24.0,y0+26.0,12.5,ink,"start","600","Cognitive Invariant Activation");
    for (i,(j,pct)) in act.iter().enumerate() {
        let yy=y0+54.0+i as f64*46.0;
        g.text(x0+18.0,yy,10.0,"#9fb0c2","start","500",BIAS_NAMES[*j]);
        let track=pw-74.0;
        g.rrect(x0+18.0,yy+7.0,track,13.0,6.5,"#152230");
        g.rrect(x0+18.0,yy+7.0,(track*pct/100.0).max(2.0),13.0,6.5,"url(#bC)");
        g.text(x0+pw-16.0,yy+17.0,11.0,"#8fe0ff","end","700",&format!("{:.0}%",pct));
    }
    g.text(x0+18.0,y0+ph-12.0,8.0,mut_,"start","400","activación = caída de P(y*) al ablacionar la dim (I.7)");

    g.done()
}

// ------------------------------ serialización JSON (sin serde) --------------
pub fn to_json(o: &RunOut) -> String {
    let mut s = String::with_capacity(64_000);
    let f1 = |v:&[f64], p:usize| v.iter().map(|x| format!("{:.*}", p, x)).collect::<Vec<_>>().join(",");
    s.push('{');
    s.push_str(&format!("\"x\":[{}],", f1(&o.surf_ax, 3)));
    s.push_str("\"z\":[");
    for (r,row) in o.surf_z.iter().enumerate() { if r>0 { s.push(','); } s.push('['); s.push_str(&f1(row,4)); s.push(']'); }
    s.push_str("],");
    s.push_str(&format!("\"xstar\":[{:.3},{:.3},{:.4}],", o.xstar3[0], o.xstar3[1], o.xstar3[2]));
    s.push_str("\"path\":[");
    for (i,p) in o.path3.iter().enumerate() { if i>0 { s.push(','); } s.push_str(&format!("[{:.3},{:.3},{:.4}]", p[0],p[1],p[2])); }
    s.push_str(&format!("],\"balls\":[{}],\"kl\":[", f1(&o.balls, 4)));
    for (i,(e,k)) in o.kl_curve.iter().enumerate() { if i>0 { s.push(','); } s.push_str(&format!("[{},{:.5}]", e, k)); }
    s.push_str("],\"swarm\":[");
    for (i,tr) in o.swarm.iter().enumerate() { if i>0 { s.push(','); } s.push('['); s.push_str(&f1(tr,4)); s.push(']'); }
    s.push_str("],\"bft\":[");
    for (i,(n,vol,ent)) in o.bft.iter().enumerate() { if i>0 { s.push(','); } s.push_str(&format!("[{},{:.4},{:.4}]", n, vol, ent)); }
    s.push_str("],\"act\":[");
    for (i,(j,pct)) in o.activation.iter().enumerate() { if i>0 { s.push(','); } s.push_str(&format!("[{},{:.2}]", j, pct)); }
    s.push_str(&format!("],\"metrics\":{{\"p_star\":{:.4},\"delta\":{:.4},\"iters\":{},\"h_yx\":{:.4},\"ceiling\":{:.4}}}",
        o.p_star, o.delta, o.iters, o.h_yx, o.ceiling));
    s.push('}');
    s
}

// ------------------------------ export WASM ---------------------------------
static mut OUT_BUF: Vec<u8> = Vec::new();

#[no_mangle]
pub extern "C" fn render_data_wasm(seed: u32, budget_milli: u32, het_centi: u32) -> *const u8 {
    let o = run(seed as u64, budget_milli as f64 / 1000.0, het_centi as f64 / 100.0);
    unsafe { OUT_BUF = to_json(&o).into_bytes(); OUT_BUF.as_ptr() }
}

#[no_mangle]
pub extern "C" fn render_svg_wasm(seed: u32, budget_milli: u32, het_centi: u32) -> *const u8 {
    let svg = run(seed as u64, budget_milli as f64 / 1000.0, het_centi as f64 / 100.0).svg;
    unsafe { OUT_BUF = svg.into_bytes(); OUT_BUF.as_ptr() }
}

#[no_mangle]
pub extern "C" fn out_len() -> usize { unsafe { OUT_BUF.len() } }
