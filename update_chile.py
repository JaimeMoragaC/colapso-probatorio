import re

with open('PAPER_v3_trabajo.md', 'r') as f:
    content = f.read()

# Buscamos la sección exacta para reemplazarla de forma segura
start_marker = "### Traducción a la sana crítica chilena."
end_marker = "#### El precedente doméstico: la Corte Suprema chilena ya rechaza el registro autodeclarado en sede de consumo financiero"

if start_marker in content and end_marker in content:
    before = content.split(start_marker)[0]
    after = end_marker + content.split(end_marker)[1]
    
    new_section = """### Traducción a la Sana Crítica Chilena y el Suicidio Probatorio bajo la Ley 21.595

En este punto, el ordenamiento chileno juega a favor de la tesis, no en contra. A diferencia del *common law* inglés pre-Horizon, el proceso penal chileno no consagra una presunción legal de que "los computadores funcionan correctamente". En Chile rige la libre valoración conforme a la **sana crítica** (Arts. 295 a 297 del Código Procesal Penal), que obliga al tribunal a ponderar la prueba según la lógica, las máximas de la experiencia y los conocimientos científicamente afianzados.

De ello se desprenden consecuencias letales para la ciberseguridad corporativa tradicional, especialmente bajo el nuevo régimen de responsabilidad penal de las personas jurídicas:

**1. La carga de la prueba en el Modelo de Prevención de Delitos (Ley 21.595):**
No hay presunción legal que la fiscalía o los demandantes deban destruir. En el contexto de un ciberincidente mayor bajo la Ley 21.595, es la corporación quien invoca sus registros para defenderse, alegando que su Modelo de Prevención de Delitos (MPD) funcionó adecuadamente y que el ataque era técnicamente irresistible. Al invocar esta eximente, **la carga de la prueba recae sobre el directorio**. Si la empresa presenta *logs* extraídos de un entorno opaco (caja negra) carente de atestación criptográfica, fracasa en su propia carga probatoria. La entidad se auto-condena, pues sus evidencias son incapaces de persuadir bajo el rigor de la sana crítica.

**2. La máxima de la experiencia (el *software* es maleable):**
La objeción probatoria no exige probar la alteración específica del registro corporativo. Basta acreditar —como un hecho notorio y máxima de la experiencia, hoy respaldada empíricamente por el caso *Horizon*— que los sistemas complejos fallan y admiten alteraciones silenciosas. Si el entorno de captura carece de una atestación anclada en hardware (RATS/SCITT) que permita descartar esa manipulación algorítmica, la duda es insalvable. Despejar esa duda probatoria es obligación exclusiva de quien dispone —o debió disponer— de la atestación.

**3. Valoración (Art. 297) y el riesgo de Exclusión (Art. 276):**
El vehículo idóneo para atacar esta deficiencia técnica es la derrota en la valoración de la prueba (Art. 297 CPP). Un registro sin cadena de custodia íntegra ni atestación de su entorno de ejecución carece del sustento científico exigido para formar convicción. Sin embargo, presentar un *log* de caja negra no atestado no solo tiene valor probatorio cero en la sentencia, sino que roza la exclusión en la audiencia preparatoria por manifiesta impertinencia o falta de idoneidad (Art. 276 CPP). Esto se debe a que priva a la contraparte de escrutar técnicamente el origen de la prueba, vulnerando el debido proceso.

**4. El estándar científico exige atestación, no intuición del juez (Art. 314 CPP):**
El límite negativo de la sana crítica es que el tribunal no puede resolver *contra* la ciencia consolidada, ni suplir con "saber privado" una cuestión técnica (lo cual violaría el principio de contradicción). La fiabilidad de un ecosistema informático no es un hecho que el juez pueda deducir empíricamente; requiere conocimiento pericial (Art. 314 CPP). Quien presenta el registro corporativo debe acreditar su fiabilidad mediante un perito. Si el entorno es opaco y carece de firmas RATS/SCITT ancladas en hardware, el perito se encuentra ante una caja negra y solo podrá declarar bajo juramento que es imposible dar fe técnica de la integridad del *log*. Sin atestación, no hay base fáctica pericial; sin perito, la prueba carece de valor científico afianzado.

**5. El "Vector Inverso": Evidencia IA y la ceguera del Tribunal:**
La sana crítica enfrenta, además, una perturbación epistémica de sentido inverso. El adversario asimétrico puede generar evidencia sintética —*logs* fabricados, trazas de red reconstituidas, reportes forenses alucinados— con calidad técnica IA capaz de superar filtros estáticos. 
En octubre de 2025, un tribunal federal de Estados Unidos estableció criterios de admisibilidad específicos para prueba digital manipulada con IA, reforzando la necesidad de autenticación técnica (*Diario Constitucional*, 11-oct-2025). Paralelamente, la Academia Judicial de Chile reconoció formalmente en abril de 2026 que la Inteligencia Artificial opera en los tribunales nacionales "de manera asistemática, irregular e invisible, sin protocolos" (Lillo, *Inteligencia Artificial en la Justicia*). Esto significa que el tribunal chileno, en su rol de *gatekeeper*, carece hoy de los instrumentos empíricos para distinguir un *log* corporativo auténtico de uno sintético.
La atestación de *hardware* continua resuelve estructuralmente el problema: una cadena de atestación en tiempo real no puede ser inyectada con datos fabricados *ex post* sin romper físicamente la raíz criptográfica de confianza. La atestación bilateral (del OIV y del entorno) es la única arquitectura que restaura el control de la sana crítica ante amenazas hiperpolimórficas.

La tesis de este documento no descansa en una conjetura especulativa sobre vulnerabilidades teóricas, sino en una regla de distribución probatoria inexcusable bajo el estándar procesal chileno: Quien presenta un registro generado por un sistema complejo soporta la carga de acreditar la integridad irrefutable del entorno que lo produjo. En ausencia de atestación anclada en hardware, esa carga no se satisface y el registro es anulado, certificando procesalmente el suicidio probatorio del directorio.

"""
    
    with open('PAPER_v3_trabajo.md', 'w') as f:
        f.write(before + new_section + after)
    print("Reemplazo exitoso.")
else:
    print("No se encontraron los marcadores.")
