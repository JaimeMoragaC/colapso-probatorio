import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replacements to tone down the "messianic" and "oracle" language
replacements = {
    r"\bmanifiesto\b": "dictamen",
    r"\bManifiesto\b": "Dictamen",
    r"\bineludible\b": "mandatorio",
    r"\bIneludible\b": "Mandatorio",
    r"\bunabomber\b": "teórico",
    r"\bUnabomber\b": "Teórico",
    r"Estructura de Manifiesto de Unabomber": "Exceso de Dogmática y Falta de Validación Empírica",
    r"manifiesto de un teórico conspirativo del silicio": "documento estrictamente teórico",
    r"\bverdad absoluta\b": "certeza empírica",
    r"\bVerdad absoluta\b": "Certeza empírica",
    r"\bimplacablemente\b": "estrictamente",
    r"\bsalvación\b": "mitigación",
    r"\búnica solución arquitectónica\b": "solución arquitectónica idónea",
    r"la franqueza brutal que aterra a los directorios": "la realidad estructural que expone a los directorios",
    r"aniquilarte desde adentro": "comprometer la red desde adentro"
}

for old, new in replacements.items():
    text = re.sub(old, new, text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tono mesiánico mitigado.")
