// Entrada NATIVA: corre la simulación (biblioteca compartida con el build WASM),
// imprime el resumen y escribe figure.svg + CSVs + metrics.txt.
use anexo_i_poc::{run, RunOut, BIAS_NAMES, SEED_DEFAULT, BUDGET_DEFAULT};
use std::fmt::Write as _;
use std::fs;

fn main() {
    let o: RunOut = run(SEED_DEFAULT, BUDGET_DEFAULT, 1.0);

    println!("============================================================");
    println!(" ANEXO I — Adversarial Oracle Extraction contra K_J (sintético)");
    println!(" seed={SEED_DEFAULT:#x}  budget={BUDGET_DEFAULT}  reproducible");
    println!("============================================================\n");
    println!("[1] Fidelidad del surrogate  KL(K_J || g_J):");
    println!("      inicio: {:.3} bits  ->  final: {:.4} bits", o.kl_start, o.kl_final);
    println!("[2] Ataque black-box sobre N(x) (solo consulta g_J):");
    println!("      caso base  P(absolución)   = {:.3}", o.p_base);
    println!("      tras ataque P(y*|x*) REAL   = {:.3}   (bajo K_J verdadero)", o.p_star);
    println!("      iteraciones = {}   |   presupuesto δ (L∞) = {:.3}", o.iters, o.delta);
    println!("[3] Techo (Cota I.1) = {:.3} (incertidumbre irreducible)  |  H(Y|X)_pob = {:.3} bits", o.ceiling, o.h_yx);
    println!("      ¿P(y*|x*) < techo?  {}  ({:.3} < {:.3})",
        if o.p_star < o.ceiling {"SÍ"} else {"NO"}, o.p_star, o.ceiling);
    println!("[4] Colegialidad (I.8) — intersección factible ⋂R_i:");
    println!("        n |  σ   | ⋂R_i factible | entropía");
    for (i,(n,vol,ent)) in o.bft.iter().enumerate() {
        println!("      {:3} | {:.2} | {:>10.2}% | {:.3} bits", n, o.sigmas[i], vol*100.0, ent);
    }
    println!("[5] Activación de invariantes cognitivos (I.7, por ablación):");
    for (j,pct) in &o.activation { println!("      {:<24} {:>5.1}%", BIAS_NAMES[*j], pct); }
    println!("\n[6] Enjambre: {} agentes convergen a x*", o.swarm.len());

    let mut c = String::from("epoch,kl_bits\n");
    for (e,k) in &o.kl_curve { let _=writeln!(c,"{e},{k:.6}"); }
    fs::write("surrogate_kl.csv", c).unwrap();
    let mut c = String::from("agent,iter,p_true\n");
    for (a,tr) in o.swarm.iter().enumerate() { for (it,p) in tr.iter().enumerate() { let _=writeln!(c,"{a},{it},{p:.6}"); } }
    fs::write("swarm.csv", c).unwrap();
    let mut c = String::from("n,sigma,vol_factible,entropia\n");
    for (i,(n,vol,ent)) in o.bft.iter().enumerate() { let _=writeln!(c,"{n},{:.2},{vol:.6},{ent:.6}", o.sigmas[i]); }
    fs::write("bft.csv", c).unwrap();
    let mut c = String::from("invariante,activacion_pct\n");
    for (j,pct) in &o.activation { let _=writeln!(c,"{},{pct:.2}", BIAS_NAMES[*j]); }
    fs::write("activation.csv", c).unwrap();
    fs::write("metrics.txt", format!(
        "P(y*|x*)={:.3}\ndelta={:.3}\niterations={}\nH(Y|X)={:.3}\nceiling={:.3}\nkl_final={:.4}\n",
        o.p_star, o.delta, o.iters, o.h_yx, o.ceiling, o.kl_final)).unwrap();
    fs::write("figure.svg", &o.svg).unwrap();

    println!("\nArchivos: figure.svg + CSVs + metrics.txt");
    println!("Abre figure.svg en cualquier navegador. (El mismo código corre en el dashboard vía WASM.)");
}
