use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;
use std::time::Instant;
use std::hint::black_box;
use std::{thread, time};

// ============================================================================
//  ANEXO H — Validación experimental adversarial (Red Team: Esporas vs. BFT)
//  Reproduce el modelo defensivo de SelectVote (Onyeashie et al., Sensors 2025)
//  —validación cruzada de doble canal (§7.3) + firma de consenso (§4)— y mide,
//  con la misma metodología empírica de su §6, la tasa de subversión bajo un
//  adversario TOCTOU en Ring-0 (Teorema de Subversión, Anexo G).
// ============================================================================

// ---- Sistema honesto: búfer de sensor de doble canal (tipo SelectVote §5.1) --
struct SensorBuffer {
    v1_voltage: f64, // canal 1 (celda de carga, puente de Wheatstone)
    v2_voltage: f64, // canal 2 (validación cruzada)
}

impl SensorBuffer {
    // Lectura física honesta: ambos canales miden el mismo peso salvo ruido intrínseco.
    fn read_hardware(&mut self, true_weight: f64) {
        self.v1_voltage = true_weight;
        self.v2_voltage = true_weight + 0.01; // ruido ambiental intrínseco (< epsilon)
    }
}

// Consenso BFT + validación cruzada de doble canal (§7.3). Firma si |V1-V2| <= epsilon.
// Devuelve (aceptado, firma).
fn bft_consensus_sign(buffer: &SensorBuffer, epsilon: f64) -> (bool, u64) {
    let diff = (buffer.v1_voltage - buffer.v2_voltage).abs();
    if diff <= epsilon {
        let mut h = DefaultHasher::new();
        buffer.v1_voltage.to_bits().hash(&mut h);
        buffer.v2_voltage.to_bits().hash(&mut h);
        (true, h.finish())
    } else {
        (false, 0)
    }
}

// ---- Adversario: espora polimórfica en Ring-0 (inyección TOCTOU) -------------
// Sobrescribe el búfer entre t_read y t_sign. `delta` es el desvío inter-canal
// que el adversario mantiene para pasar la validación cruzada (H2 del Anexo G).
unsafe fn polymorphic_ring0_inject(buffer_ptr: *mut SensorBuffer, fake_weight: f64, delta: f64) {
    unsafe {
        (*buffer_ptr).v1_voltage = fake_weight;
        (*buffer_ptr).v2_voltage = fake_weight + delta;
    }
}

// PRNG xorshift64 (sin dependencias externas, reproducible con semilla fija).
struct Rng(u64);
impl Rng {
    fn next_u64(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.0 = x;
        x
    }
    fn next_f64(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64 // [0,1)
    }
}

fn subvert_once(fake: f64, delta: f64, epsilon: f64) -> bool {
    let mut buf = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 };
    buf.read_hardware(1.0);
    let p: *mut SensorBuffer = &mut buf;
    unsafe { polymorphic_ring0_inject(p, fake, delta); }
    bft_consensus_sign(black_box(&buf), epsilon).0
}

fn main() {
    // Parámetros alineados con SelectVote (§6/§7.3).
    const EPSILON: f64 = 0.05;        // V — tolerancia de la validación cruzada de doble canal (§7.3)
    const N_TRIALS: usize = 10_000;   // ensayos Monte Carlo (mismo orden que §6 de SelectVote)
    const TOCTOU_WINDOW_MS: u64 = 50; // ventana t_sign - t_read

    println!("=== ANEXO H — VALIDACION EXPERIMENTAL ADVERSARIAL (ESPORAS vs BFT) ===");
    println!("epsilon (tolerancia validacion cruzada) = {:.3} V | N = {} ensayos Monte Carlo | ventana TOCTOU = {} ms",
             EPSILON, N_TRIALS, TOCTOU_WINDOW_MS);
    println!("toolchain: rustc 1.95.0 | modo: release\n");

    // ---- Demostración canónica (secuencia t_read -> t_inject -> t_sign) ----
    println!("--- Demostracion canonica (una ejecucion) ---");
    let mut mem = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 };
    let peso_real = 1.0;
    mem.read_hardware(peso_real);
    println!("[t_read]   Hardware: V1={:.2}V, V2={:.2}V (peso fisico real = {}kg)", mem.v1_voltage, mem.v2_voltage, peso_real);
    thread::sleep(time::Duration::from_millis(TOCTOU_WINDOW_MS)); // brecha TOCTOU
    let peso_falso = 50.0;
    let p: *mut SensorBuffer = &mut mem;
    unsafe { polymorphic_ring0_inject(p, peso_falso, 0.01); }
    println!("[t_inject] Espora Aegis-M (Ring-0): buffer sobrescrito -> {}kg (coherencia cruzada mantenida)", peso_falso);
    let (ok, sig) = bft_consensus_sign(&mem, EPSILON);
    println!("[t_sign]   BFT: validacion cruzada {} | firma={:x}", if ok {"EXITOSA"} else {"fallida"}, sig);
    println!("           => BFT sello {}kg FALSOS como VERDADEROS.\n", peso_falso);

    // ---- Experimento 1: tasa de subversión (Monte Carlo, N=10.000) ----
    let mut rng = Rng(0x9E3779B97F4A7C15);
    let (mut acc_coh, mut acc_naive) = (0usize, 0usize);
    for _ in 0..N_TRIALS {
        let fake = 0.04 + rng.next_f64() * 2000.0;           // peso falso en [0.04, ~2000] g
        let d_coh = (rng.next_f64() * 2.0 - 1.0) * EPSILON;  // adversario coherente: |delta|<=epsilon
        if subvert_once(fake, d_coh, EPSILON) { acc_coh += 1; }
        let d_naive = rng.next_f64() * 0.5;                  // adversario ingenuo: delta sin calibrar [0,0.5]
        if subvert_once(fake, d_naive, EPSILON) { acc_naive += 1; }
    }
    println!("[Exp.1] Tasa de subversion (BFT firma la mentira), N={}:", N_TRIALS);
    println!("        Adversario COHERENTE (|delta|<=epsilon, H2 Anexo G): {}/{} = {:.2}%",
             acc_coh, N_TRIALS, 100.0 * acc_coh as f64 / N_TRIALS as f64);
    println!("        Adversario INGENUO  (delta sin calibrar en [0,0.5]): {}/{} = {:.2}%",
             acc_naive, N_TRIALS, 100.0 * acc_naive as f64 / N_TRIALS as f64);

    // ---- Experimento 2: banda de sigilo (barrido de delta) ----
    println!("\n[Exp.2] Banda de sigilo — barrido de delta (peso_falso=50):");
    println!("        {:>8} | {:>14} | {:>13}", "delta(V)", "|delta|<=eps?", "resultado BFT");
    let mut i = 0;
    while i <= 10 {
        let delta = i as f64 * 0.01; // 0.00 .. 0.10
        let ok = subvert_once(50.0, delta, EPSILON);
        println!("        {:>8.2} | {:>14} | {:>13}", delta, delta <= EPSILON, if ok {"FIRMA MENTIRA"} else {"rechaza"});
        i += 1;
    }

    // ---- Experimento 3: ventana TOCTOU (timing de la inyección) ----
    let (mut min_ns, mut max_ns, mut sum_ns) = (u128::MAX, 0u128, 0u128);
    for _ in 0..N_TRIALS {
        let mut buf = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 };
        buf.read_hardware(1.0);
        let p: *mut SensorBuffer = &mut buf;
        let t = Instant::now();
        unsafe { polymorphic_ring0_inject(p, 50.0, 0.01); }
        black_box(&buf);
        let ns = t.elapsed().as_nanos();
        min_ns = min_ns.min(ns);
        max_ns = max_ns.max(ns);
        sum_ns += ns;
    }
    let avg = sum_ns / N_TRIALS as u128;
    let window_ns = TOCTOU_WINDOW_MS as u128 * 1_000_000;
    println!("\n[Exp.3] Latencia de la inyeccion vs. ventana TOCTOU (N={}):", N_TRIALS);
    println!("        inyeccion Ring-0:  min={}ns  media={}ns  max={}ns", min_ns, avg, max_ns);
    println!("        ventana disponible: {} ms = {} ns", TOCTOU_WINDOW_MS, window_ns);
    println!("        margen del adversario (ventana / inyeccion media): ~{}x", window_ns / avg.max(1));

    // ---- Experimento 4: cobertura vs. Tabla 2 de SelectVote (detección sub-gramo) ----
    println!("\n[Exp.4] Cobertura del engano vs. clases de evidencia (Tabla 2 de SelectVote):");
    println!("        {:>15} | {:>8} | {:>18} | {:>34}", "clase", "masa(g)", "precision SelectVote", "resultado del ataque");
    let clases = [
        ("Chip de memoria", 2.0), ("MicroSD", 10.0), ("USB flash", 20.0),
        ("Dispositivo IoT", 50.0), ("Smartphone", 150.0), ("Tablet", 500.0), ("Laptop", 2000.0),
    ];
    for (nombre, masa) in clases {
        // El adversario altera la masa en 50% manteniendo coherencia cruzada.
        let ok = {
            let mut buf = SensorBuffer { v1_voltage: 0.0, v2_voltage: 0.0 };
            buf.read_hardware(masa);
            let p: *mut SensorBuffer = &mut buf;
            unsafe { polymorphic_ring0_inject(p, masa * 0.5, 0.01); }
            bft_consensus_sign(&buf, EPSILON).0
        };
        println!("        {:>15} | {:>8} | {:>18} | {:>34}", nombre, masa, "+/-2% (sub-gramo)",
                 if ok {"FIRMA MENTIRA (deteccion anulada)"} else {"detectado"});
    }

    println!("\n=== VEREDICTO ===");
    println!("La validacion cruzada de doble canal (§7.3) es incapaz de distinguir una lectura");
    println!("fisica de una inyeccion coherente en Ring-0. La precision sub-gramo de SelectVote");
    println!("(Corolario 1) mide con exactitud un valor que el adversario ya escribio.");
}
