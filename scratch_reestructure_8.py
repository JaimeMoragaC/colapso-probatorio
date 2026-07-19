import os
import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Helper to extract blocks
def get_block(start_marker, end_marker):
    start_idx = text.find(start_marker)
    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        return text[start_idx:end_idx]
    return text[start_idx:]

b_intro = get_block('## 8. El Frente Jurisdiccional y Estatal', '#### 8.1.1 El "firmware" medieval')
b_firmware = get_block('#### 8.1.1 El "firmware" medieval', '### 8.2 Neurobiología del fallador')
b_neuro = get_block('### 8.2 Neurobiología del fallador', '#### 8.2.8 La colisión de lógicas')
b_limites = get_block('#### 8.2.8 La colisión de lógicas', '### 8.3 La sana crítica')
b_bft = get_block('### 8.3 La sana crítica', '### 8.4 El juez como periférico')
b_periferico = get_block('### 8.4 El juez como periférico', '### 8.5 La IA agéntica')
b_exploit = get_block('### 8.5 La IA agéntica', '### 8.6 El colapso constitucional')
b_rest = get_block('### 8.6 El colapso constitucional', '## 9.')

# Modify headers and references in blocks
b_limites = b_limites.replace('#### 8.2.8 La colisión', '### 8.2 Límites termodinámicos y cibernéticos\n\n*En una frase: la física de la información establece límites duros que ninguna voluntad biológica puede superar.*\n\n#### 8.2.1 La colisión')
b_limites = b_limites.replace('#### 8.2.9 Límites termodinámicos', '#### 8.2.2 Límites termodinámicos')

b_bft = b_bft.replace('### 8.3 La sana crítica', '#### 8.2.3 La sana crítica como algoritmo de consenso bizantino')
b_bft = b_bft.replace('§8.5.1', '§8.6.1') # reference to perfilamiento
b_bft = b_bft.replace('§8.2.4', '§8.3.4') # reference to anclaje
b_bft = b_bft.replace('§8.2.3', '§8.3.3') # reference to memoria
b_bft = b_bft.replace('ataque cognitivo de §8.5', 'ataque cognitivo de §8.6')

b_neuro = b_neuro.replace('### 8.2 Neurobiología', '### 8.3 Neurobiología')
b_neuro = b_neuro.replace('#### 8.2.1', '#### 8.3.1')
b_neuro = b_neuro.replace('#### 8.2.2', '#### 8.3.2')
b_neuro = b_neuro.replace('#### 8.2.3', '#### 8.3.3')
b_neuro = b_neuro.replace('#### 8.2.4', '#### 8.3.4')
b_neuro = b_neuro.replace('#### 8.2.5', '#### 8.3.5')
b_neuro = b_neuro.replace('#### 8.2.6', '#### 8.3.6')
b_neuro = b_neuro.replace('#### 8.2.7', '#### 8.3.7')
b_neuro = b_neuro.replace('Síntesis de §8.2', 'Síntesis de §8.3')
b_neuro = b_neuro.replace('§8.5.1', '§8.6.1') # prior
b_neuro = b_neuro.replace('§8.2.1', '§8.3.1')
b_neuro = b_neuro.replace('§8.2.2', '§8.3.2')

b_firmware = b_firmware.replace('#### 8.1.1', '### 8.4')

b_periferico = b_periferico.replace('### 8.4', '### 8.5')
b_periferico = b_periferico.replace('limitaciones biológicas (§8.2)', 'limitaciones biológicas (§8.3)')

b_exploit = b_exploit.replace('### 8.5', '### 8.6')
b_exploit = b_exploit.replace('#### 8.5.1', '#### 8.6.1')
b_exploit = b_exploit.replace('#### 8.5.2', '#### 8.6.2')
b_exploit = b_exploit.replace('#### 8.5.3', '#### 8.6.3')
b_exploit = b_exploit.replace('vulnerabilidad de §8.2', 'vulnerabilidad de §8.3')
b_exploit = b_exploit.replace('§8.2.1', '§8.3.1')
b_exploit = b_exploit.replace('§8.2.2', '§8.3.2')
b_exploit = b_exploit.replace('§8.2.3', '§8.3.3')
b_exploit = b_exploit.replace('§8.2.4', '§8.3.4')
b_exploit = b_exploit.replace('§8.2.5', '§8.3.5')

b_rest = b_rest.replace('### 8.6', '### 8.8')
b_rest = b_rest.replace('### 8.7', '### 8.9')
b_rest = b_rest.replace('§8.3, §8.6', '§8.2.3, §8.8')
b_rest = b_rest.replace('§8.4', '§8.5')
b_rest = b_rest.replace('§8.5', '§8.6')
b_rest = b_rest.replace('§8.2.9', '§8.2.2')

b_isomorfismo = """### 8.7 El Isomorfismo del Colapso: De Ring-0 a la Sana Crítica

*En una frase: la caída del ente regulado corporativo y el colapso del juez son exactamente la misma falla estructural ocurriendo en sustratos distintos; cuando el primero falla, el segundo es su escenario de contingencia ciego.*

El argumento de este trabajo está dividido en dos grandes bloques: la vulnerabilidad de las infraestructuras corporativas (Parte I) y la vulnerabilidad del sistema de justicia (Parte II). Hasta este punto, podrían parecer dos fenómenos paralelos. No lo son. Comparten un isomorfismo estructural perfecto y operan en una secuencia fatal.

El fraude corporativo TOCTOU en Ring-0 (§4) y el engaño cognitivo al sentenciador biológico (§8.6) son iteraciones de la misma negligencia arquitectónica: **confiar en el motor de procesamiento asumiendo ciegamente la integridad de la entrada**.
- En la **Capa de Silicio (Ente Regulado):** Se audita el *software* (motor) leyendo sus propios *logs* (entradas), sin exigir atestación criptográfica desde el hardware (TPM). El sistema cree estar seguro porque sus reportes falsificados le dicen que lo está.
- En la **Capa Biológica (Juez):** Se blinda la imparcialidad de la sana crítica (motor) leyendo el expediente (entradas), sin exigir un "Firewall Epistemológico". El juez cree descubrir la verdad porque sus heurísticas le inyectan dopamina ante una narrativa coherente.

#### 8.7.1 El colapso de la cadena de auditoría

La conexión crítica es que el tribunal es el **escenario de contingencia** de la ciberseguridad corporativa. Cuando un banco o infraestructura crítica sufre un ataque de máxima profundidad (Ring-0) y el atacante borra sus huellas alterando los *logs* desde el núcleo, el conflicto inevitablemente se judicializa.

En ese instante, el ente corporativo inundará el tribunal con miles de fojas de reportes técnicos adulterados. Y el sistema procesal, asumiendo su premisa silenciosa, le exigirá al juez —un procesador biológico agotado, sometido a la Ley de Miller y a su fatiga decisional— que audite manualmente un ataque de nivel kernel. El magistrado carece del ancho de banda y de las herramientas para lograrlo. Al enfrentarse a una evidencia sintética hiper-estructurada (la "Emulación Emergente"), el juez aplicará su sana crítica y terminará validando la falsedad, simplemente porque es la narrativa más "redonda" y libre de fricciones que su cerebro puede procesar. La trampa se cierra: el fraude tecnológico corporativo se blanquea mediante una sentencia judicial.

#### 8.7.2 Verdad empírica vs. verdad estocástica

Este isomorfismo revela la grieta en la epistemología jurídica contemporánea. Doctrinadores como Taruffo o Ferrer sostienen que el proceso busca aproximarse a una **"verdad empírica"** —un encadenamiento causal real de los hechos—. Pero, como demuestra Judea Pearl en sus trabajos sobre inferencia causal (2018), los grandes modelos de lenguaje y arquitecturas conexionistas no comprenden la causalidad; optimizan puramente la asociación estocástica (la probabilidad de que un *token* siga a otro). 

El adversario agéntico no le entrega al juez una verdad empírica; le entrega una **"verdad sintáctica"** inmaculada, estadísticamente indistinguible de la realidad, pero vaciada de todo nexo causal con los hechos históricos. Al procesar esta verdad sintáctica, el "firmware medieval" del juez (§8.4) encuentra la paz moral que busca, cerrando el caso y consumando el *probatory suicide*.

#### 8.7.3 La única salida: el Firewall Epistemológico

Pedirle al magistrado "más cuidado" en la valoración probatoria frente a la IA polimórfica es tan inútil arquitectónicamente como auditar un malware de kernel instalando más software antivirus. Ningún sistema de Capa 7 (lógica humana, apelaciones) detecta una alteración de Capa 0 (datos inyectados en la raíz).

La única salida es establecer un **Firewall Epistemológico**. Así como la ciberseguridad corporativa debe anclarse en la Atestación de Silicio (Hardware Root of Trust), el derecho procesal debe exigir la **validación criptográfica** de la evidencia *antes* de que ingrese a la carga cognitiva del juzgador. Toda prueba que carezca de atestación física inmutable de origen debe ser bloqueada en la entrada, porque una vez que penetra el entorno perceptivo del juez biológico, la física de la información (Ashby, Shannon) garantiza que el fallo será predecible, determinista y falso.

"""

new_text = (
    text[:text.find('## 8. El Frente Jurisdiccional')] +
    b_intro + 
    b_limites +
    b_bft +
    b_neuro +
    b_firmware +
    b_periferico +
    b_exploit +
    b_isomorfismo +
    b_rest
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Reestructuración completa y guardada en PAPER_v3_trabajo.md")
