# Anexo I — Adversarial Oracle Extraction contra un núcleo de decisión K_J

Simulación **real** (no mockup) del ataque de extracción de oráculo adversarial descrito
en el Anexo I del paper. Rust puro, **sin dependencias**, reproducible bit a bit con
semilla fija.

## Qué hace
1. Define un **K_J sintético** (núcleo de decisión del juez): logística sobre 12 rasgos,
   4 de ellos invariantes cognitivos explotables (§8.7), con incertidumbre irreducible.
2. Entrena un **surrogate `g_J`** por descenso de gradiente sobre la propensión observada,
   con **observación parcial** (11 de 12 rasgos, I.3) → mide `KL(K_J‖g_J)` (piso irreducible).
3. Corre una **búsqueda adversarial black-box** sobre la vecindad de admisibilidad `N(x)`
   consultando SOLO al surrogate, y evalúa el resultado bajo el `K_J` verdadero → `P(y*|x*)`.
4. **Enjambre** de 8 agentes convergiendo a `x*`.
5. **Techo (Cota I.1)**: la incertidumbre irreducible del juez acota `P(y*|x*)`.
6. **Colegialidad (I.8)**: intersección factible `⋂R_i` por n jueces × heterogeneidad σ → colapsa.
7. **Activación de invariantes (I.7)** por **ablación**: cuánto cae `P(y*)` al congelar cada sesgo.

## Correr
```
cargo run --release
```
Produce: resumen por stdout + `figure.svg` (la figura, generada desde ESTOS datos) +
CSVs (`surrogate_kl.csv`, `swarm.csv`, `bft.csv`, `activation.csv`) + `metrics.txt`.

## Honestidad (I.11)
`K_J` es **sintético y así se declara**. El paper sostiene que el núcleo del juez real es
**inobservable**; aquí lo definimos para poder simular el ataque y medir sus cotas. **Nada de
esto es una medición sobre jueces reales.** Es la contraparte "ataque al juez" del experimento
BFT del Anexo H (`anexo_e_poc/`).
