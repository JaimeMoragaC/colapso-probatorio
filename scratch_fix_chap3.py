with open("PAPER_v3_trabajo.md", "r") as f:
    content = f.read()

import re

target_start = "### 3.8.3 La trampa doméstica: el colapso de la defensa garantista"
target_end = "### 3.8.2 Proyección al proceso penal: cadena de custodia, prueba ilícita y sana crítica"

if target_start in content and target_end in content:
    start_idx = content.find(target_start)
    end_idx = content.find(target_end)
    
    new_text = """### 3.8.3 El colapso del placebo comercial: la trampa del *Compliance* ante el *enforcement* internacional

Frente a este cerco transnacional, resulta natural que las gerencias legales busquen resguardo en el pilar histórico del derecho sancionador chileno: la exigencia de que el Estado pruebe la infracción, o en su defecto, en el cumplimiento documental de los estándares de la industria. 

Sin embargo, esta aproximación encierra una trampa contraintuitiva. Desde una perspectiva corporativa, parece lógico asumir que comprar las herramientas más costosas del mercado (EDR, SIEM) y certificarse bajo los estándares de gestión más reconocidos (ISO 27001, SOC 2) opera como un escudo legal infalible. El peligro letal de esta premisa es ignorar que el propio "negocio de la ciberseguridad" se basa en la mercantilización de la ceguera arquitectónica, y que los reguladores de primer mundo han dejado de ser complacientes frente a esta ficción.

#### 1. El Complejo Industrial de la Ciberseguridad y la mercantilización de la ceguera.

Para entender la trampa en la que caen los directorios, hay que diseccionar el modelo de negocio. La industria tradicional de ciberseguridad lucra vendiendo soluciones basadas en software (antivirus, agentes EDR, *logs* de hipervisor) que operan bajo la falsa presunción de que el sistema operativo está intacto. Se comercializa la ilusión de control, ocultando deliberadamente que todas estas herramientas son arquitectónicamente ciegas ante un ataque de Ring 0 (el nivel de privilegios del hipervisor).

El directorio adquiere estos costosos servicios y auditorías documentales creyendo que compra "seguridad", cuando en realidad está adquiriendo un placebo comercial. Las grandes consultoras y los proveedores *cloud* amparan esta ilusión mediante el "modelo de responsabilidad compartida": el hiperescalador entrega una infraestructura opaca, la firma auditora certifica la existencia de procesos administrativos en papel, y el riesgo físico residual se transfiere silenciosamente, y sin mitigar, al cliente final.

#### 2. El giro del *enforcement* internacional: cazar la asimetría, no el hackeo.

Los reguladores internacionales ya han despertado a esta farsa comercial. Ya no sancionan a la empresa por ser "víctima" técnica de un incidente, sino por la asimetría de información que genera el placebo corporativo. En EE.UU., la Comisión de Bolsa y Valores (SEC) ha establecido un precedente implacable al imputar por fraude a altos directivos (ej. caso SolarWinds, 2023)<a href="#fn_sec_solarwinds" id="fnref_sec_solarwinds"><sup>286</sup></a>.

La acción de la SEC no se fundamentó en la incapacidad de la empresa para detener un ataque estatal avanzado (SUNBURST). El ilícito se configuró por la discrepancia dolosa entre las declaraciones públicas —que aseguraban altos estándares de ciberseguridad apoyados en el marketing de la industria— y la realidad interna de una arquitectura con vulnerabilidades inmanejables. La doctrina es directa: es un fraude regulatorio utilizar el *compliance* de papel para encubrir la falta de integridad real de la arquitectura. En paralelo, las autoridades europeas de protección de datos (DPAs) aplican multas bajo el principio de Seguridad desde el Diseño (Art. 32 GDPR) con la misma lógica<a href="#fn_gdpr_art32" id="fnref_gdpr_art32"><sup>287</sup></a>: la sanción recae sobre la negligencia inexcusable de operar bajo arquitecturas inherentemente opacas.

#### 3. La tenaza doméstica y el suicidio por telemetría.

Al importar este placebo comercial al ordenamiento chileno, el operador activa una bomba de tiempo. Atrapado entre la Ley 21.663 (obligación de reportar con información veraz) y la Ley 21.719 (deber de *poder demostrar* diligencia), el operador se ve forzado a entregar a la autoridad la misma telemetría *cloud* por la que pagó millones.

Y aquí se cierra la tenaza probatoria: como se analizó en §3.3, un *log* de nube carente de anclaje en *hardware* (TPM/DICE) es matemáticamente inacreditable. El responsable envía a la ANCI telemetría firmada que, por la vulnerabilidad inherente del problema TOCTOU, no puede garantizar el estado del entorno en que se generó. La misma herramienta comercial que el directorio adquirió para defenderse se convierte en la prueba material de su negligencia. No se le castiga por el hackeo; se le castiga porque su defensa es criptográficamente ciega, consumando un suicidio probatorio.

#### 4. El colapso de las últimas defensas: la falacia de la "imposibilidad" y el *estoppel*.

Frente a esta encerrona, las gerencias legales suelen recurrir a dos defensas de manual que hoy colapsan ante el rigor técnico:
1. **La excusa de la imposibilidad técnica (*ad impossibilia*):** Argumentar que la atestación de hardware es inaccesible es fáctica y jurídicamente falso. El mercado *sí ofrece* soluciones comerciales (ej. *Confidential Computing*). Ignorar deliberadamente estas tecnologías para operar en nubes estándar (más baratas y ciegas), y luego alegar "imposibilidad", no es una defensa; es la confesión de una decisión financiera que priorizó el ahorro por sobre la integridad, manteniendo en cualquier escenario la vulnerabilidad de la estructura de datos ante Ring 0.
2. **El espejismo del *estoppel* regulatorio:** Argumentar que si la ANCI históricamente ha aceptado certificaciones en papel, no puede sancionarlos ahora por "confianza legítima". Esta premisa es nula. La confianza legítima ampara la buena fe, no el uso de una pauta administrativa desfasada para enmascarar riesgos estructurales. El deber de prevención de delitos económicos (Ley 21.595) es muy superior a cualquier desfase temporal del regulador.

### La única salida del cepo.

De lo anterior se sigue una conclusión que no es defensiva sino arquitectónica: apostar por el placebo comercial del *compliance* de *software* garantiza la condena. Solo la evidencia atestable —atestación por un tercero anclada en *hardware*, bajo claves del responsable y con continuidad bajo control del obligado— satisface a la vez los regímenes chilenos y sobrevive al implacable escrutinio internacional, donde la ceguera tecnológica ya no es atenuante, sino el cuerpo del delito.

Quien la adopta hoy convierte el cepo en piso firme; quien persiste en el cumplimiento meramente documental queda dentro cuando la tenaza se cierra. El catálogo normativo concreto para incorporar esta exigencia al régimen —reporte atestable, puerto seguro probatorio, continuidad bajo control del obligado y un estándar único de evidencia— se desarrolla en §6.3.


"""
    
    fixed_end = target_end.replace("### 3.8.2", "### 3.8.4")
    
    with open("PAPER_v3_trabajo.md", "w") as f:
        f.write(content[:start_idx] + new_text + fixed_end + content[end_idx + len(target_end):])
    print("Replacement successful")
else:
    print("Target strings not found")
