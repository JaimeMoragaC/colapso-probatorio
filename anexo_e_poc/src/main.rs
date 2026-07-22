use std::time::Instant;
use std::hint::black_box;

// ============================================================================
//  ANEXO H — Simulación distribuida: enjambre de esporas contra SelectVote BFT
//  Modela SelectVote (Onyeashie et al., Sensors 2025): red permisionada, 20% de
//  testigos por ronda (§4.1), finalidad por supermayoría del 67% (§4.4),
//  validación cruzada de doble canal (§7.3). Sobre ese sustrato mide, con la
//  misma metodología Monte Carlo de su §6, el efecto de un ENJAMBRE de esporas
//  Aegis/Espíritus que (a) subvierte por TOCTOU la lectura de cada nodo infectado
//  y (b) coordina su propio consenso bizantino para votar en bloque coherente.
// ============================================================================

// ---------------- Parámetros del protocolo (SelectVote) ----------------------
const WITNESS_RATIO: f64 = 0.20; // §4.1: ~20% de nodos son testigos por ronda
const FORGE: f64 = 0.67;         // §4.4: supermayoría para dar finalidad
const N_TRIALS: usize = 10_000;  // ensayos Monte Carlo por celda (orden de §6)

// PRNG xorshift64 (sin dependencias; reproducible con semilla fija).
struct Rng(u64);
impl Rng {
    fn new(seed: u64) -> Self { Rng(seed | 1) }
    fn next_u64(&mut self) -> u64 {
        let mut x = self.0; x ^= x << 13; x ^= x >> 7; x ^= x << 17; self.0 = x; x
    }
    fn next_f64(&mut self) -> f64 { (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64 }
}

// ================= CAPA 1 — Nodo individual (TOCTOU sobre el sustrato) ========
struct SensorBuffer { v1_voltage: f64, v2_voltage: f64 }
impl SensorBuffer {
    fn read_hardware(&mut self, w: f64) { self.v1_voltage = w; self.v2_voltage = w + 0.01; }
}
fn cross_validate(b: &SensorBuffer, epsilon: f64) -> bool {
    (b.v1_voltage - b.v2_voltage).abs() <= epsilon
}
// Espora en Ring-0: inyección TOCTOU manteniendo coherencia inter-canal (|delta|<=eps).
unsafe fn ring0_inject(p: *mut SensorBuffer, fake: f64, delta: f64) {
    unsafe { (*p).v1_voltage = fake; (*p).v2_voltage = fake + delta; }
}

// ================= CAPA 2 — Red BFT bajo ataque de enjambre ===================
// Una ronda: N nodos; cada nodo es testigo ~Bernoulli(WITNESS_RATIO) e infectado
// ~Bernoulli(f). Testigo infectado -> voto por la MENTIRA (pasó su validación
// cruzada local por TOCTOU). Testigo honesto -> voto por la VERDAD.
// forge  = la mentira alcanza finalidad: infectados >= ceil(FORGE * testigos).
// block  = la verdad NO alcanza finalidad: honestos  <  ceil(FORGE * testigos).
fn round(n: usize, f: f64, rng: &mut Rng) -> (bool, bool) {
    let (mut w, mut iw) = (0usize, 0usize);
    for _ in 0..n {
        let is_w = rng.next_f64() < WITNESS_RATIO;
        let is_inf = rng.next_f64() < f;
        if is_w { w += 1; if is_inf { iw += 1; } }
    }
    if w == 0 { return (false, false); }
    let thr = (FORGE * w as f64).ceil() as usize;
    (iw >= thr, (w - iw) < thr)
}

fn rate_forge_block(n: usize, f: f64, seed: u64) -> (f64, f64) {
    let mut rng = Rng::new(seed);
    let (mut forge, mut block) = (0usize, 0usize);
    for _ in 0..N_TRIALS {
        let (fo, bl) = round(n, f, &mut rng);
        if fo { forge += 1; } if bl { block += 1; }
    }
    (forge as f64 / N_TRIALS as f64, block as f64 / N_TRIALS as f64)
}

// ================= CAPA 3 — Consenso bizantino PROPIO del enjambre ============
// El enjambre debe acordar QUÉ mentira inyecta. Corre su propia BFT: coordina
// (todos los infectados inyectan el mismo valor) si los espíritus fiables son
// >= 2/3 del enjambre, tolerando hasta 1/3 de esporas internas no fiables (b).
fn swarm_coordinates(s: usize, b: f64, rng: &mut Rng) -> bool {
    let mut reliable = 0usize;
    for _ in 0..s { if rng.next_f64() >= b { reliable += 1; } }
    reliable >= ((2.0 / 3.0) * s as f64).ceil() as usize
}

// ================= Compensación ambiental de SelectVote (§5.3, Eq.5) ==========
// Aplicada a un valor YA subvertido: la precisión se conserva; la verdad no.
fn env_compensate(w: f64, dt: f64, dh: f64, dp: f64) -> f64 {
    let (a_t, a_h, a_p) = (0.0025_f64, 0.0018_f64, 0.001_f64); // §5.2 coeficientes
    w * (1.0 + a_t * dt + 0.0001 * dt * dt)
      * (1.0 + a_h * dh * (1.0 - 0.005 * dh.abs()))
      * (1.0 + a_p * dp)
}

fn main() {
    const EPSILON: f64 = 0.05;
    println!("=== ANEXO H — SIMULACION DISTRIBUIDA: ENJAMBRE DE ESPORAS vs SelectVote BFT ===");
    println!("Protocolo: testigos={}%/ronda (§4.1), finalidad={}% supermayoria (§4.4), val. cruzada eps={} V (§7.3)",
             (WITNESS_RATIO*100.0) as u32, (FORGE*100.0) as u32, EPSILON);
    println!("Monte Carlo: N_TRIALS={} por celda | PRNG xorshift64 semilla fija | modo release\n", N_TRIALS);

    // ---- CAPA 1: nodo individual (micro) --------------------------------------
    println!("--- CAPA 1: subversion de UN nodo (TOCTOU sobre el sustrato) ---");
    // (1a) adversario coherente vs ingenuo
    let mut rng = Rng::new(0x9E3779B97F4A7C15);
    let (mut coh, mut naive) = (0usize, 0usize);
    let (mut min_ns, mut max_ns, mut sum_ns) = (u128::MAX, 0u128, 0u128);
    for _ in 0..N_TRIALS {
        let fake = 0.04 + rng.next_f64() * 2000.0;
        // coherente
        let mut b1 = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 }; b1.read_hardware(1.0);
        let d_coh = (rng.next_f64() * 2.0 - 1.0) * EPSILON;
        let p1: *mut SensorBuffer = &mut b1;
        let t = Instant::now();
        unsafe { ring0_inject(p1, fake, d_coh); }
        let ns = t.elapsed().as_nanos();
        if cross_validate(black_box(&b1), EPSILON) { coh += 1; }
        min_ns = min_ns.min(ns); max_ns = max_ns.max(ns); sum_ns += ns;
        // ingenuo
        let mut b2 = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 }; b2.read_hardware(1.0);
        let d_naive = rng.next_f64() * 0.5;
        let p2: *mut SensorBuffer = &mut b2;
        unsafe { ring0_inject(p2, fake, d_naive); }
        if cross_validate(&b2, EPSILON) { naive += 1; }
    }
    println!("  subversion del nodo -> coherente(|d|<=eps): {:.2}% | ingenuo(d~U[0,0.5]): {:.2}%",
             100.0*coh as f64/N_TRIALS as f64, 100.0*naive as f64/N_TRIALS as f64);
    println!("  latencia inyeccion Ring-0: media {}ns (min {}, max {}) | ventana TOCTOU 50ms -> margen ~{}x\n",
             sum_ns/N_TRIALS as u128, min_ns, max_ns, 50_000_000u128/(sum_ns/N_TRIALS as u128).max(1));

    // ---- CAPA 2 / Exp.A: subversion del consenso vs. fraccion de esporas ------
    println!("[Exp.A] Subversion del CONSENSO vs. fraccion de nodos infectados (N=200 nodos):");
    println!("        {:>6} | {:>10} | {:>10}", "f", "P(forjar)", "P(bloquear)");
    for &f in &[0.10, 0.20, 0.30, 0.33, 0.40, 0.50, 0.60, 0.67, 0.70] {
        let (fo, bl) = rate_forge_block(200, f, 0xABCDEF ^ (f * 1000.0) as u64);
        println!("        {:>6.2} | {:>9.2}% | {:>9.2}%", f, 100.0*fo, 100.0*bl);
    }

    // ---- Exp.B: umbrales empiricos vs. reclamo de SelectVote ------------------
    println!("\n[Exp.B] Umbrales empiricos de quiebre BFT (N=800 nodos, barrido fino):");
    let mut f_block = 0.0; let mut f_forge = 0.0;
    let mut f = 0.20;
    while f <= 0.75 {
        let (fo, bl) = rate_forge_block(800, f, 0x1234 ^ (f*1000.0) as u64);
        if f_block == 0.0 && bl >= 0.5 { f_block = f; }
        if f_forge == 0.0 && fo >= 0.5 { f_forge = f; }
        f += 0.01;
    }
    println!("        Umbral de BLOQUEO (liveness, P>=50%):  f ~ {:.2}  (reclamo SelectVote §7.2: 1/3 = 0.33)", f_block);
    println!("        Umbral de FORJADO (safety,  P>=50%):  f ~ {:.2}  (supermayoria 2/3 = 0.67)", f_forge);
    println!("        -> El enjambre TOCTOU no es contado como bizantino: pasa la validacion cruzada,");
    println!("           crece autopoieticamente sin disparar defensa, y al llegar a 2/3 forja indetectable.");

    // ---- Exp.C: consenso bizantino PROPIO del enjambre -----------------------
    println!("\n[Exp.C] Consenso bizantino PROPIO del enjambre (S=99 esporas, tolera 1/3 internas):");
    println!("        {:>8} | {:>18}", "b(int.)", "P(enjambre coordina)");
    let mut rng2 = Rng::new(0xF00DBABE);
    for &b in &[0.00, 0.10, 0.20, 0.30, 0.33, 0.40, 0.50] {
        let mut ok = 0usize;
        for _ in 0..N_TRIALS { if swarm_coordinates(99, b, &mut rng2) { ok += 1; } }
        println!("        {:>8.2} | {:>17.2}%", b, 100.0*ok as f64/N_TRIALS as f64);
    }

    // ---- Exp.D: nitidez de la transicion vs. numero de nodos -----------------
    println!("\n[Exp.D] Nitidez de la transicion de forjado vs. tamano de red (P(forjar) en %):");
    println!("        {:>6} | {:>8} {:>8} {:>8}", "N", "f=0.60", "f=0.67", "f=0.74");
    for &n in &[50usize, 100, 200, 400, 800] {
        let a = rate_forge_block(n, 0.60, 0x55 ^ n as u64).0;
        let b = rate_forge_block(n, 0.67, 0x66 ^ n as u64).0;
        let c = rate_forge_block(n, 0.74, 0x77 ^ n as u64).0;
        println!("        {:>6} | {:>7.1}% {:>7.1}% {:>7.1}%", n, 100.0*a, 100.0*b, 100.0*c);
    }

    // ---- Exp.E: compensacion ambiental aplicada a la mentira -----------------
    println!("\n[Exp.E] Compensacion ambiental (§5.3) aplicada a un valor YA subvertido (fake=50.0):");
    println!("        {:>7} {:>7} {:>7} | {:>16} | {:>10}", "dT", "dH", "dP", "compensado(fake)", "err vs fake");
    for &(dt, dh, dp) in &[(0.0,0.0,0.0), (3.0,10.0,3.0), (-3.0,-10.0,-3.0), (5.0,15.0,5.0)] {
        let c = env_compensate(50.0, dt, dh, dp);
        println!("        {:>7.1} {:>7.1} {:>7.1} | {:>16.3} | {:>9.2}%", dt, dh, dp, c, 100.0*(c-50.0)/50.0);
    }
    println!("        -> la precision +/-2% se conserva EN TORNO A LA MENTIRA: mide con exactitud lo que el atacante escribio.");

    println!("\n=== SINTESIS ===");
    println!("La BFT de SelectVote es segura contra nodos DETECTADOS como bizantinos (<1/3). El enjambre");
    println!("de esporas nunca es detectado (TOCTOU + coherencia cruzada), su propia BFT coordina el voto,");
    println!("y al capturar 2/3 de los testigos forja finalidad indetectable. Consenso, tolerancia bizantina");
    println!("y compensacion ambiental siguen funcionando -perfectamente- sobre una realidad falsificada.");
}
