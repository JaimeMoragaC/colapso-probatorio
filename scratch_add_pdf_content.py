import os
import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add 8.6.4 El salto epistémico
insert_salto = """
#### 8.6.4 El salto epistémico: Del "ruido biológico" a la inyección polimórfica en Ring-0

La dogmática jurídica contemporánea y la economía conductual han logrado un avance histórico al desmantelar el mito del magistrado infalible. Los estudios empíricos sobre el condicionamiento metabólico del fallo y las heurísticas judiciales (§8.3) han probado, sin margen de duda, que la "sana crítica" opera en la realidad como un algoritmo biológico inestable, ruidoso y susceptible de manipulación por variables físicas triviales.

Sin embargo, el estado del arte de la academia jurídica actual padece de una ceguera arquitectónica fatal. Los debates contemporáneos sobre el impacto de la Inteligencia Artificial en los tribunales se encuentran estancados en la Capa de Aplicación (Capa 7): discuten los sesgos discriminatorios de los sistemas de evaluación de riesgo (como COMPAS) o el peligro de que un litigante presente un video *Deepfake* que engañe al sentenciador. Asumen, erróneamente, que el terminal de trabajo del juez sigue siendo una fortaleza inexpugnable.

Este documento postula que dicho enfoque doctrinal es asimétrico y anacrónico. El vacío fundamental en la literatura radica en la incapacidad de prever qué sucede cuando el vector de ataque abandona la interfaz visual y desciende al silicio. Las IAs agénticas polimórficas no necesitan generar complejos videos falsos para convencer al intelecto del magistrado; les basta con ejecutar un ataque de concurrencia temporal (TOCTOU) y alterar el hash de una resolución en el nivel de máximos privilegios del procesador (Ring-0) milisegundos antes de que el token criptográfico del juez la selle.

El cruce interdisciplinario arroja una conclusión forense ineludible: si la ciencia cognitiva ya demostró que el magistrado carece de las herramientas fisiológicas para superar sus propios sesgos en un entorno de papel, resulta matemáticamente imposible exigirle que su "intuición moral" detecte una inyección de código ejecutada en la memoria viva de su equipo. El ruido biológico del siglo XX acaba de ser reemplazado por el secuestro algorítmico del siglo XXI.
"""

text = text.replace('devuelviéndoles un canal de verdad que la máquina no controle.', 'devuelviéndoles un canal de verdad que la máquina no controle.\n' + insert_salto)

# 2. Add 8.8 Herramientas de Supervivencia Jurisdiccional and renumber 8.8 -> 8.9, 8.9 -> 8.10
insert_herramientas = """### 8.8 Herramientas de Supervivencia Jurisdiccional

*En una frase: la única forma en que el juez recupera el control de su tribunal frente al peritaje corporativo es exigiendo atestación de silicio bajo apercibimiento de exclusión por prueba ilícita.*

Frente a la ceguera forense descrita, el juez no está indefenso si comprende que el problema dejó de ser jurídico y pasó a ser de arquitectura de sistemas. Para evitar actuar como un periférico ciego que blanquea fraudes corporativos, la judicatura dispone de tres herramientas procesales destructivas para neutralizar la evidencia sintética:

1. **La Exclusión por Prueba Ilícita (La inconstitucionalidad de la Caja Negra):** 
Si una corporación o el Estado aporta prueba digital extraída de un sistema que carece de atestación de estado (hardware ciego), el juez debe excluirla (e.g., Art. 276 CPP chileno). Admitir un *log* inauditable vulnera el derecho al debido proceso (Art. 19 N° 3 CPR) al imponerle a la contraparte una *probatio diabolica*: la imposibilidad técnica de auditar un sistema cerrado. Rechazar esta prueba no es obstruir la justicia; es proteger la pureza del sistema constitucional.

2. **La Inversión Táctica de la Carga de la Prueba:** 
El juez no debe exigirle al ciudadano que pruebe que el *software* del banco falló. La carga de probar la inmutabilidad física del registro recae sobre quien controla el servidor. Si el banco presenta un registro y no posee un enclave de hardware (TPM/TEE) que certifique criptográficamente su integridad en el Ring-0, su prueba no goza de presunción de veracidad.

3. **El Test de Atestación Jurisdiccional:** 
El escrutinio judicial sobre la prueba digital debe mutar hacia un test de tres pasos inapelables para el perito:
   - *Test de Origen Físico:* ¿La evidencia proviene de un entorno de ejecución confiable (TEE) o de un sistema operativo de propósito general manipulable?
   - *Test de Visibilidad de Kernel:* ¿El perito puede probar la integridad de la memoria en el milisegundo exacto de la captura (T=0) o solo ofrece registros posteriores (T+1)?
   - *Test de Soberanía:* ¿La institución controla las llaves criptográficas a nivel de silicio o depende de los registros opacos de un hiperescalar?

Si el perito informático responde negativamente a cualquiera de estas preguntas, el juez recupera el control: la prueba es declarada inatestable a nivel de silicio y, por tanto, jurídicamente irrelevante.

"""

text = text.replace('### 8.8 El colapso constitucional', insert_herramientas + '### 8.9 El colapso constitucional')
text = text.replace('### 8.9 El espejo comparado', '### 8.10 El espejo comparado')
text = text.replace('§8.2.3, §8.8', '§8.3.3, §8.9') # Update internal reference for probatio diabolica

# 3. Expand El espejo comparado
text = text.replace('**Alemania — el *Staatstrojaner*', '**India — Caso Bhima Koregaon y la inyección remota (2021).** Activistas fueron encarcelados bajo leyes antiterroristas usando como prueba documentos hallados en sus discos duros. El juez asumió la validez de los metadatos. Años después, la firma *Arsenal Consulting* demostró que un atacante usó malware (NetWire RAT) para inyectar 52 documentos incriminatorios remotamente, alterando el Master File Table (MFT) para que pareciera que el usuario los redactó. *Lección:* confiar en la carpeta del sistema sin atestación de origen permite a un atacante construir una "realidad procesal" entera a espaldas del usuario.\n\n**España — STS 300/2015 y la manipulación visual.** El Tribunal Supremo de España dictó una jurisprudencia implacable (Ponente: Manuel Marchena) estableciendo que un pantallazo (e.g., WhatsApp, redes sociales) carece de todo valor probatorio sin peritaje del terminal físico, advirtiendo sobre la intrínseca manipulabilidad de la interfaz visual. *Lección:* lo que el juez ve en la Capa 7 (pantalla) no es prueba de lo que ocurrió en el servidor.\n\n**Alemania — el *Staatstrojaner*')

text = text.replace('El mismo patrón, con idéntica raíz', '**Estados Unidos — *State v. Loomis* (2016).** La Corte Suprema de Wisconsin validó una condena penal basada en un software privado (COMPAS) que denegó la libertad condicional evaluando un "riesgo de reincidencia". Se denegó el acceso al código fuente por "secreto comercial". *Lección:* es el colapso de la motivación de la sentencia; el juez abdica de la sana crítica delegándola en una caja negra algorítmica corporativa.\n\nEl mismo patrón, con idéntica raíz')

# 4. Update references and bibliography
text = text.replace('| Ashby (1956)', '| Susskind (2019) | *Online Courts and the Future of Justice* | Obsolescencia del periférico humano (§8.3) |\n| Posner (2008) | *How Judges Think* | Formalismo jurídico como blanqueamiento heurístico (§8.3) |\n| Ashby (1956)')


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Actualización completada y guardada en PAPER_v3_trabajo.md")
