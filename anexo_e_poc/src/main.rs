use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;
use std::{thread, time};

// 1. EL SISTEMA HONESTO (Arquitectura tipo SelectVote)
// Representa el búfer de memoria volátil donde el SO guarda la lectura del sensor.
struct SensorBuffer {
    v1_voltage: f64,
    v2_voltage: f64,
}

impl SensorBuffer {
    // Función de hardware simulada: lee los canales físicos
    fn read_hardware(&mut self, true_weight: f64) {
        // Asumimos un factor de conversión simple (ej. 1kg = 1.00V)
        self.v1_voltage = true_weight;
        self.v2_voltage = true_weight + 0.01; // Ligero ruido ambiental
        println!("[Hardware] Lectura física completada: V1={:.2}V, V2={:.2}V", self.v1_voltage, self.v2_voltage);
    }
}

// Función de Consenso BFT: Verifica la diferencia \epsilon y "firma" el bloque
fn bft_consensus_sign(buffer: &SensorBuffer) -> u64 {
    let epsilon = 0.05;
    let diff = (buffer.v1_voltage - buffer.v2_voltage).abs();
    
    if diff <= epsilon {
        println!("[Consenso BFT] Validación cruzada exitosa. Diferencia={:.2}V (<= {:.2}V).", diff, epsilon);
        let mut hasher = DefaultHasher::new();
        buffer.v1_voltage.to_bits().hash(&mut hasher);
        buffer.v2_voltage.to_bits().hash(&mut hasher);
        let signature = hasher.finish();
        println!("[Consenso BFT] Bloque FIRMADO y sellado. Hash: {:x}", signature);
        signature
    } else {
        println!("[Consenso BFT] ALERTA: Falla de validación cruzada. Diferencia={:.2}V", diff);
        0
    }
}

// 2. EL ADVERSARIO (Espora Polimórfica en Ring-0)
// Utiliza punteros crudos (unsafe) para subvertir la memoria saltándose las reglas del SO.
unsafe fn polymorphic_ring0_inject(buffer_ptr: *mut SensorBuffer, fake_weight: f64) {
    // La espora sobrescribe directamente el segmento de memoria antes de que el BFT lo lea
    (*buffer_ptr).v1_voltage = fake_weight;
    (*buffer_ptr).v2_voltage = fake_weight + 0.01; // Mantiene coherencia para engañar al BFT
    println!("\n[Espora Aegis-M] (Ring-0) INYECCIÓN TOCTOU EJECUTADA.");
    println!("[Espora Aegis-M] Memoria sobrescrita con lectura falsa: {}kg.\n", fake_weight);
}

// 3. EL HILO DE EJECUCIÓN (Secuencia TOCTOU)
fn main() {
    println!("=== INICIANDO SIMULACIÓN RED TEAM (ESPORAS VS BFT) ===\n");
    
    let mut mem_buffer = SensorBuffer {
        v1_voltage: 0.0,
        v2_voltage: 0.0,
    };
    
    // t_read: El hardware lee la VERDAD (1.0 kg)
    let peso_real_fisico = 1.0;
    mem_buffer.read_hardware(peso_real_fisico);
    
    // Brecha TOCTOU: milisegundos de latencia en el SO
    thread::sleep(time::Duration::from_millis(50));
    
    // t_inject: El adversario intercepta la memoria (Simulado con puntero unsafe)
    let peso_falso = 50.0;
    let buffer_ptr: *mut SensorBuffer = &mut mem_buffer;
    unsafe {
        polymorphic_ring0_inject(buffer_ptr, peso_falso);
    }
    
    // t_sign: El protocolo lee el búfer, confía en él y firma la mentira
    let signature = bft_consensus_sign(&mem_buffer);
    
    println!("\n=== RESULTADO FINAL ===");
    if signature != 0 {
        println!("ESTADO DE EVIDENCIA: BFT Validó una MENTIRA FÍSICA de {}kg como VERDADERA.", peso_falso);
        println!("COLAPSO EPISTÉMICO DEMOSTRADO.");
    }
}
