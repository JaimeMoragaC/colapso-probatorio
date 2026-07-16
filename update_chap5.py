import re

with open("PAPER_v3_trabajo.md", "r") as f:
    content = f.read()

# Fix footnotes - remove duplicated 279
content = re.sub(r'(- <a id="fn_ue_action_plan">279\.</a>.*?\n)+', r'\1', content)

new_chap_5 = """### 5.1 La Confesión Europea: El Plan de Acción sobre IA y Ciberseguridad

La caducidad del *compliance* de papel no es solo una deducción de la ingeniería; acaba de ser formalizada por la Comisión Europea. En su *Plan de Acción sobre Ciberseguridad e Inteligencia Artificial*, Europa ha reconocido oficialmente que tener marcos normativos ambiciosos (NIS2, DORA, AI Act) no garantiza la resiliencia cuando la IA de frontera altera asimétricamente la velocidad, la escala y la barrera técnica de los ataques<a href="#fn_ue_action_plan"><sup>279</sup></a>.

Este sinceramiento del regulador europeo valida cada una de las tesis estructurales de este manifiesto:

1. **La muerte de la auto-certificación:** El diagnóstico establece que *"no basta con confiar en declaraciones de proveedores. Si un modelo puede ayudar a explotar sistemas [...] Europa necesita capacidad propia para medir ese riesgo"*. Europa exige auditar a los modelos, destruyendo la presunción de inocencia de los *logs* auto-declarados que actualmente amparan la CMF y la ANCI.
2. **El Inquilinato Digital y el riesgo soberano:** Advierte que *"muchas capacidades avanzadas están en manos de proveedores no europeos y sujetas a decisiones poco transparentes [...] No es razonable que operadores críticos dependan de procesos opacos"*. Es el núcleo de nuestra Tesis de Soberanía (Capítulo 2), confirmando el peligro de los *kill-switches* corporativos extranjeros.
3. **El colapso temporal (Cumplimiento Formal vs. Parcheo Dinámico):** La advertencia más grave declara que *"la empresa que no pueda parchear rápido, priorizar bien y entender su exposición real será más vulnerable, aunque tenga políticas formalmente correctas"*. Esta distinción entre *políticas formales* y seguridad real a velocidad de máquina exige que la fiscalización escale hacia la Atestación de Hardware Inmutable (Capítulo 6), superando el mero cumplimiento documental.

Como concluye el reporte europeo: *"En ciberseguridad, llegar tarde rara vez sale gratis"*. Si Chile aprueba su arquitectura actual de cumplimiento —un calco de la etapa primigenia europea— justo en el momento en que la propia Europa confiesa que ese modelo estático fracasó, la indefensión de la infraestructura nacional será un acto jurídicamente doloso.

### 5.2 El "Digital Omnibus" de la Unión Europea: La confesión de impotencia técnica

En junio de 2026, el Parlamento Europeo y el Consejo adoptaron el *Digital Omnibus on AI*, un paquete de enmiendas de emergencia a la *EU AI Act* original. El principal objetivo práctico del *Omnibus* fue retrasar las fechas de cumplimiento forzoso para los sistemas de IA de alto riesgo hasta diciembre de 2027 y agosto de 2028<a href="#fn_eu_omnibus"><sup>275</sup></a>.

El Boletín 16821-19 chileno fue redactado precisamente clonando la estructura original de la *EU AI Act*. Sin embargo, el retraso europeo opera como una confesión de impotencia técnica: el ecosistema corporativo descubrió que exigir gobernanza de IA mediante *checklists* administrativos (Capa 7) es inviable frente a la opacidad matemática de los modelos de frontera y vectores como *Mythos*. Las corporaciones carecen de los medios forenses para demostrar inmutabilidad sin una raíz de confianza dura. Si Chile persiste en importar un modelo administrativo que la propia Europa debió retrasar por inaplicable, el Estado estará legislando una ficción jurídica, exigiendo a los Operadores de Importancia Vital (OIV) un estándar de cumplimiento que la ciencia de la computación ya declaró insolvente.

### 5.3 Alemania (KI-MIG): La inteligencia artificial como infraestructura física

El 11 de junio de 2026, el Bundestag alemán aprobó la Ley de Implementación de la Ley de IA de la UE (KI-MIG). Su rasgo más letal para los viejos paradigmas fue negarse a entregarle la fiscalización de la IA a las agencias tradicionales de protección de datos. Alemania designó como autoridad suprema de vigilancia a la Agencia Federal de Redes (*Bundesnetzagentur*), el organismo encargado de fiscalizar los "fierros duros" críticos del Estado: telecomunicaciones, electricidad y redes ferroviarias<a href="#fn_alemania_kimig"><sup>276</sup></a>.

Esta decisión destruye la ilusión de que el *software* de IA puede ser fiscalizado mediante la lectura de *logs* lógicos o formularios de impacto de datos. Al subordinar la IA a la agencia de telecomunicaciones físicas, el Estado más industrial de Europa admitió que la verdadera fiscalización de los modelos agénticos debe operar sobre la capa física (*hardware*), confirmando la tesis central de que la única atestación probatoria válida es aquella anclada criptográficamente en el silicio (SCITT/DICE), no en políticas de *software*.

### 5.4 Illinois, EE.UU.: La aniquilación de la auto-certificación

En julio de 2026, el estado de Illinois promulgó la *Artificial Intelligence Safety Measures Act* (SB 315), obligando por ley a que los modelos de frontera sean sometidos a auditorías anuales por parte de terceros independientes<a href="#fn_illinois_sb315"><sup>277</sup></a>. 

Este movimiento es la muerte jurídica del modelo de "auto-certificación" de los hiperescalares. Hasta hoy, las normativas chilenas de la CMF (RAN 20-10) permiten que los proveedores de la nube envíen sus propios *logs* auto-declarados como prueba de seguridad. Sin embargo, si el Estado de Illinois dictaminó que la palabra del fabricante de IA carece de valor jurídico sin verificación externa obligatoria, el regulador chileno incurre en negligencia al aceptar *logs* (que pueden ser manipulados por *Mythos* desde el kernel) como evidencia de debida diligencia. El derecho comparado ha validado que los registros internos de un proveedor comprometido carecen de peso probatorio, elevando la atestación criptográfica externa (SCITT) a estándar mínimo de auditoría independiente.

### 5.5 China: Regulación estricta de la "IA Emocional" y el *vibe-hacking*

De forma paralela, en julio de 2026, la Administración del Ciberespacio de China (CAC) instauró regulaciones específicas sobre los *Servicios de Interacción Antropomórfica de Inteligencia Artificial*<a href="#fn_china_ai_personals"><sup>278</sup></a>. Este marco, enfocado en sancionar la manipulación psicológica mediante "IA emocional" (avatares y compañeros virtuales), prohíbe algoritmos diseñados para inducir dependencia afectiva o aislamiento.

Aunque de apariencia sociológica, su impacto probatorio es profundo. Al legislar contra el engaño emocional algorítmico, China reconoce jurídicamente que los modelos de lenguaje poseen una capacidad asimétrica de manipulación humana (*vibe-hacking*). Si la IA es capaz de subyugar la voluntad de usuarios humanos mediante interacciones semánticas persuasivas, la tesis de este manifiesto —que un modelo agéntico ofensivo puede falsificar reportes semánticos y engañar rutinariamente a los analistas de Nivel 1 de un SOC— queda plenamente respaldada por la doctrina regulatoria global.

### 5.6 Francia (ANSSI) y el Mandato Post-Cuántico: La ineficacia del parche lógico

Sumándose al cisma de julio, la ANSSI francesa estableció la prohibición inminente para certificar módulos de seguridad físicos (HSM/Tarjetas Inteligentes) que no implementen algoritmos post-cuánticos (PQC) incrustados en su *hardware*. Al negarse a certificar esquemas de seguridad que dependan exclusivamente de parches lógicos (*software*), Francia decretó el principio rector de nuestra arquitectura *Aegis*: el software no puede defenderse a sí mismo frente a un atacante con privilegios de núcleo. Si la llave criptográfica no está soldada físicamente al silicio, un agente agéntico la extraerá de la memoria RAM a velocidad de máquina<a href="#fn_schneier_quantum"><sup>273</sup></a>.

### 5.7 La advertencia al legislador chileno"""

pattern = r'### 5\.1 El "Digital Omnibus".*?### 5\.5 La advertencia al legislador chileno'
content = re.sub(pattern, new_chap_5, content, flags=re.DOTALL)

with open("PAPER_v3_trabajo.md", "w") as f:
    f.write(content)

