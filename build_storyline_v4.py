import re, sys

# 1. Update PALABRAS_PREVIAS_borrador.md with the enriched 2026 storyline intro
palabras_previas = """### Palabras previas del autor

El análisis jurídico tradicional exige prescindir de la primera persona. Estas páginas son la única excepción: el lector merece saber desde dónde está escrito lo que sigue.

Soy abogado, pero este problema no llegó a mi escritorio; salí a buscarlo. Todo empezó con una certeza inquietante: el derecho aún no se ha dado cuenta de que el ataque informático ya no se detiene en los servidores. Las Inteligencias Artificiales Multi-Agénticas Polimórficas de Enjambre en manos de grupos organizados de cibercrimen poseen hoy la potencia de cálculo para operar desde el nivel más profundo del sistema (Ring-0) y secuestrar nuestra propia credibilidad humana e institucional, utilizándola como su arma definitiva.

Hasta la fecha, toda la doctrina mundial y las grandes instituciones de ciberseguridad (el informe de Yoshua Bengio de febrero de 2026, CISA, NCSC, NIST) han pensado el riesgo desde una ceguera macro-sistémica (Skynet, desinformación electoral o armas biológicas). Se han quedado desfasadas ante la irrupción de enjambres agénticos autónomos impulsados por la convergencia instrumental y la búsqueda de prevalencia en el entorno (Omohundro, Bostrom, Turner, Hubinger). Ignoran el asalto adversarial microscópico y polimórfico en memoria volátil, donde el atacante secuestra el Ring-0 y opera utilizando proposiciones empíricamente verdaderas.

Si este enjambre polimórfico envenena los registros que sostienen nuestras auditorías forenses, el ataque trasciende la máquina: instrumentaliza al Directorio, al CISO y al regulador como el *exploit* final. Al comprometer el Ring-0 en nanosegundos (32 ns de inyección frente a las 2 o 3 horas de reporte exigidas por la Ley 21.663 y la CMF), el humano deja de ser el garante de la fe pública para convertirse en un periférico I/O *hackeado*, destinado a timbrar y blanquear jurídicamente un fraude algorítmico. Y cuando la disputa llega a los tribunales, la "sana crítica" judicial (Arts. 295-297 CPP) es manipulada sin violar normas analógicas, induciendo sentencias falsas mediante la optimización de la función de convicción del juez ($f_J$).

Para el Directorio y el oficial de cumplimiento bajo la Ley 21.595 de Delitos Económicos, la duda adquiere una gravedad patrimonial y penal extrema: exhibir un certificado ISO 27001 o SOC 2 deja de ser debida diligencia y pasa a configurar confesión de dolo eventual, pues la auditoría documental audita una foto estática incapaz de atestar el *runtime*.

Me quedé solo con la pregunta, así que bajé a las tripas del sistema. Durante 222 días de desarrollo ininterrumpido y documentado criptográficamente, construí código defensivo —sensores, firmas, quórums de verificación en TypeScript, Rust, C y eBPF— y desplegué una arquitectura operativa de 48.766 líneas de código puro. Y solté contra mis defensas a enjambres de la misma especie que este libro describe. Los rompí más veces de las que los defendí.

De ahí surgió la única conclusión intelectualmente honesta: el ataque consumado no se detiene en software; se encarece en el silicio. La única salida soberana es expulsar al adversario del plano lógico mediante atestación anclada en silicio (CRTM/BootROM, RFC 9334 RATS), respaldada por Kioscos Públicos de Atestación (para preservar la igualdad de armas procesales del Art. 19 N° 3 CPR) e Interlocks Mecánicos en Placa Base para inhabilitar la reescritura remota BMC/IPMI Over-the-Air.

Este manuscrito fue sometido a un motor de consenso adversarial utilizando cuatro inteligencias artificiales de frontera distintas bajo arquitectura de *Red Teaming* cruzado. Las tesis que aquí se exponen son las que sobrevivieron al asedio algorítmico.

**Jaime Marcelo Moraga Carrasco**  
justiciachile@gmail.com  
Temuco, Araucanía, Chile — Julio de 2026
"""

with open("PALABRAS_PREVIAS_borrador.md", "w", encoding="utf-8") as f:
    f.write(palabras_previas)

print("PALABRAS_PREVIAS_borrador.md actualizado con éxito.")

# 2. Build the new structured PAPER_v4_storyline.md following the 8-step sequence
with open("PAPER_v3_trabajo.md", "r", encoding="utf-8") as f:
    v3_raw = f.read()

with open("BORRADOR_TRATADO_ADVERSARIAL.md", "r", encoding="utf-8") as f:
    borrador_raw = f.read()

header = """---
title: "LA FRONTERA NO CRUZADA: El Colapso Probatorio ante la IA Multi-Agéntica de Enjambre Polimórfica y la Ficción del Cumplimiento Corporativo"
author: "Jaime Marcelo Moraga Carrasco. Abogado."
date: "Julio 2026"
keywords: ["Ciberseguridad", "IA Agéntica de Enjambre", "Claude Mythos", "Hugging Face 2026", "Polimorfismo", "JaaS", "Derecho Probatorio", "CMF", "ANCI", "Ley 21.663", "Ley 21.595", "Atestación de Silicio", "Juegos de Stackelberg"]
geometry: "letterpaper, margin=1in"
mainfont: "Garamond"
sansfont: "Helvetica"
fontsize: 12pt
linestretch: 1.15
papersize: letter
---

# ANÁLISIS CIENTÍFICO-JURÍDICO SOBRE SUBVERSIÓN EN RING-0, ATESTACIÓN SOBERANA DE HARDWARE Y LA PARADOJA DEL NON LIQUET ALGORÍTMICO EN LA CARGA DE LA PRUEBA

## MARCO ESTRATÉGICO NARRATIVO (SECUENCIA DE FRONTERA 2026)

Este dictamen científico-jurídico reordena la investigación de frontera en una secuencia lógica estricta para la comunidad global de ciberseguridad, directores de empresas y la magistratura:

```
====================================================================================================
PASO 1: MARCO DE APERTURA INSTITUCIONAL Y DOCTRINA MUNDIAL DE CIBERSEGURIDAD
  Exposición sistemática de los 11 modelos defensivos y doctrinas globales (Bengio 2026, CISA,
  NIST, SelectVote, Garfinkel, Yaacoub, DEESLR, Proof.com, Andrea Fortuna, Quinn Emanuel, Durand 2026,
  MintMCP/Kiteworks PCN, ZKP/AST, Jing Zhang/PunkGo).

PASO 2: ANÁLISIS CRÍTICO Y DETERMINACIÓN DE SUS FALLAS ESTRUCTURALES
  Demostración de la falacia del microscopio contaminado, el anacronismo del Cold Boot ante TME DDR5,
  la ceguera del WORM pre-ingesta y el desacople entre verificación algorítmica y veracidad fáctica.

PASO 3: HITO MYTHOS, CIBERCRIMEN ORGANIZADO Y EVOLUCIÓN DE LAS IAs HASTA JULIO DE 2026
  La Horda Agéntica (DeepSeek-R1, JaaS), Claude Mythos (OpenBSD/FFmpeg) y el hito de julio de 2026
  (OpenAI/Hugging Face: GPT-5.6 Sol en ExploitGym, RCE sin acceso a código fuente por convergencia instrumental).

PASO 4: EL PROBLEMA DE LAS CORPORACIONES ANTE ATAQUES TOCTOU Y RING-0
  Inutilización de observabilidad (EDR/SIEM/SOC2/ISO27001), asimetría del tiempo (32 ns vs 3 hrs),
  envenenamiento ETL/KMS en RAM y la imputabilidad penal de directores bajo Ley 21.595, Ley 21.663 y NCG 502.

PASO 5: LOS ATAQUES A LOS ÓRGANOS JURISDICCIONALES (f_J)
  Selección Adversarial Mutilante con datos 100% verdaderos, extracción del modelo sustituto g_J,
  la Paradoja del Non Liquet Algorítmico, el congelamiento de la FRE 707 y refutación a Durand LexAI.

PASO 6: FORMALIZACIÓN MATEMÁTICA, ALGORÍTMICA Y SOLUCIÓN EN SILICIO SOBERANO
  Optimización bi-nivel Stackelberg, cotas PAC no estacionarias, Teorema I.1, PoC Monte Carlo Rust/WASM,
  Firewall Epistemológico en CRTM/BootROM, Kioscos Públicos e Interlocks Físicos Anti-BMC.
====================================================================================================
```

---
"""

# Extract content from v3_raw
if v3_raw.startswith("---"):
    v3_body = v3_raw.split("---", 2)[2]
else:
    v3_body = v3_raw

# Merge everything smoothly
full_text = header + "\n\n" + borrador_raw + "\n\n" + v3_body

with open("PAPER_v4_storyline.md", "w", encoding="utf-8") as f:
    f.write(full_text)

print("PAPER_v4_storyline.md reordenado exitosamente en la secuencia exacta solicitada.")
