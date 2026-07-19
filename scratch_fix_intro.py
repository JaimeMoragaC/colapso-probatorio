import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

old_block = r"""## Arquitectura del Documento: Los Dos Frentes del Colapso

Este documento aborda una única falla estructural —la ceguera forense derivada de la falta de atestación en silicio— y los efectos de esta vulnerabilidad ante ataques de IA Poliformica , pero la disecciona en los dos ecosistemas institucionales donde su impacto es definitivo e irreversible.

Para garantizar la claridad y el rigor analítico, la exposición de este manifiesto se ha dividido deliberadamente en dos grandes frentes. Aunque la física del ataque (Ring-0, subversión de memoria, ataques TOCTOU) es idéntica en ambos, el bien jurídico destruido y los sujetos expuestos son diametralmente distintos:

1. El Frente Corporativo y Regulatorio (La responsabilidad fiduciaria)
La primera parte de esta obra se enfoca estrictamente en el mercado financiero y los Operadores de Importancia Vital (OIV). Aquí analizaremos cómo la ceguera del cloud computing aniquila el valor de las certificaciones de ciberseguridad (ISO 27001, SOC 2) y hace materialmente incumplibles los deberes de reporte exigidos por la ANCI (Ley 21.663) y la CMF (NCG 502). En esta sección, el foco recae sobre el Directorio y el Oficial de Cumplimiento, demostrando cómo la arquitectura actual los arrastra hacia la responsabilidad penal personal por negligencia inexcusable bajo la Ley 21.595.

2. El Frente Jurisdiccional y Estatal (El secuestro del debido proceso)
Una vez establecido el diagnóstico corporativo, la segunda parte del documento traslada esta misma vulnerabilidad arquitectónica a los órganos con potestad decisional del Estado (tribunales y entes sancionadores). En este frente, el análisis abandona el riesgo financiero para centrarse en el riesgo institucional: cómo un ataque a nivel de kernel convierte la presunción de legalidad de la Firma Electrónica Avanzada en un arma de falsificación perfecta. Aquí demostraremos cómo el sistema instrumentaliza al Juez y a la Autoridad Administrativa, convirtiéndolos en simples periféricos hackeados que blanquean fraudes algorítmicos mediante su "sana crítica".

Es en este segundo frente donde el trabajo hace su aportación más singular. La Sección 8 modela la \*sana crítica\* del juez como un algoritmo de consenso biológico y demuestra —trasladando el teorema de tolerancia a fallos bizantinos \(Lamport, 1982\) del sistema distribuido al proceso probatorio— que ese algoritmo fracasa por diseño cuando todas sus fuentes digitales pueden estar comprometidas. En la intersección exacta que ese capítulo ocupa —la sana crítica del juez humano leída como consenso bizantino bajo el modelo de amenazas de la IA agéntica— no existe, hasta donde alcanza esta investigación, literatura previa: es una contribución pionera —un \*first-mover\* genuino—, cuyo aporte no reside en la metáfora sino en haberla convertido en un modelo con condición de falla, umbral y remedio \(§8\.3\).

Guía de lectura:
La vulnerabilidad técnica subyacente actúa como el hilo conductor de toda la obra. Sin embargo, el lector proveniente del mundo corporativo \(CEOs, directores, auditores\) encontrará el núcleo de su exposición legal en la primera mitad, mientras que el lector del mundo jurídico y procesal \(magistrados, litigantes, legisladores\) verá el colapso de su liturgia institucional expuesto con crudeza en la segunda. Ambos frentes convergen, hacia el final del documento, en una única solución arquitectónica ineludible: la Soberanía Forense anclada en hardware\."""

new_block = """## Arquitectura del Documento: El Frente Corporativo y Regulatorio

Este documento aborda una única falla estructural —la ceguera forense derivada de la falta de atestación en silicio— y los efectos letales de esta vulnerabilidad ante ataques de IA Polimórfica. 

Para garantizar el máximo impacto y rigor analítico, la exposición de este manifiesto se concentra deliberadamente en un único ecosistema institucional: el mercado financiero y los Operadores de Importancia Vital (OIV). Analizaremos cómo la ceguera del *cloud computing* aniquila el valor de las certificaciones de ciberseguridad tradicionales (ISO 27001, SOC 2) y hace materialmente incumplibles los deberes de reporte exigidos por la ANCI (Ley 21.663) y la CMF (NCG 502).

El foco de este documento recae implacablemente sobre el Directorio, el CISO y el Oficial de Cumplimiento, demostrando cómo la arquitectura actual los arrastra hacia la responsabilidad penal personal por negligencia inexcusable bajo la Ley 21.595.

> **Nota de Alcance Jurisdiccional:** Aunque la física del ataque (Ring-0, subversión de memoria, ataques TOCTOU) descrita aquí secuestra inevitablemente el debido proceso, la dimensión de **valoración judicial** —el deber del adjudicador, el colapso de la "sana crítica" y el juez como periférico vulnerable— ha sido deliberadamente extraída de este dictamen. Ese frente se desarrolla a profundidad en el volumen complementario de esta serie: *La valoración judicial de la evidencia digital en la era de la IA generativa*.

### Guía de lectura táctica interdisciplinaria

La vulnerabilidad técnica subyacente (TOCTOU, carencia de SCITT) actúa como el hilo conductor de toda la obra. Sin embargo, para evitar la fatiga interdisciplinaria del lector, el documento permite las siguientes rutas de lectura acelerada:

- 🚦 **Para perfiles de Ingeniería y CISO:** El núcleo de su exposición técnica reside en el **Capítulo 2** (Modelo de Amenaza) y el **Capítulo 4** (Análisis Crítico de Defensas Hiperescalares). Para avanzar ágilmente, el autor autoriza leer "en diagonal" las extensas minucias de derecho procesal chileno detalladas en la **Sección 3.8**, sin que ello quiebre el hilo conductor de la vulnerabilidad arquitectónica.
- ⚖️ **Para Fiscales (Legal) y el Directorio Corporativo:** Su exposición fiduciaria y patrimonial se desglosa con absoluta crudeza en el **Capítulo 3** (Especialmente la Sección 3.8 sobre la Inversión de la Carga de la Prueba Penal) y el **Capítulo 6** (Requisitos de evidencia idónea frente al regulador). 

Ambas disciplinas convergen, hacia el final del documento, en una única solución arquitectónica ineludible: la Soberanía Forense anclada en hardware."""

# Replace the block using a regex to ignore exact whitespace/newlines
import re
pattern = re.compile(r'## Arquitectura del Documento: Los Dos Frentes del Colapso.*?Soberanía Forense anclada en hardware\.', re.DOTALL)
text = pattern.sub(new_block, text)

# Ensure "## PRIMERA PARTE" is removed since there is no SEGUNDA PARTE anymore
text = re.sub(r'## PRIMERA PARTE — El sospechoso firma su propia coartada \{\.parte\}\n', '', text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Architecture section updated.")
