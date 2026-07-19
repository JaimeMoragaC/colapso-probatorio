import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Targeted replacements in HEADINGS ONLY (lines starting with #)
heading_replacements = {
    r"El colapso de la defensa": "La vulnerabilidad de la defensa",
    r"Anatomía del Colapso Probatorio": "Anatomía de la Falla Probatoria",
    r"colapso metodológico": "error metodológico",
    r"el colapso del mapa cartesiano": "la obsolescencia del mapa cartesiano",
    r"El secuestro de la Ley": "La subversión de la Ley",
    r"el colapso de la cobertura": "la anulación de la cobertura",
    r"secuestro del plano de control": "compromiso del plano de control",
    r"El colapso del plano de control": "El compromiso del plano de control",
    r"El Secuestro Epistemológico": "La Subversión Cognitiva",
    r"El colapso de las cláusulas": "La inviabilidad de las cláusulas",
    r"Colapso del esquema": "Falla estructural del esquema",
    r"El colapso estocástico": "La vulnerabilidad inminente",
    r"La anatomía del colapso": "La anatomía de la brecha",
    r"El colapso del modelo criminal": "La evolución del modelo criminal",
    r"El colapso de las pólizas": "La ineficacia de las pólizas",
    r"el colapso probatorio": "el vacío probatorio",
    r"el colapso de la defensa garantista": "la neutralización de la defensa garantista",
    r"El colapso del \"estoppel": "La ineficacia del \"estoppel",
    r"El colapso documental": "La fragilidad documental",
    r"El colapso físico": "La vulnerabilidad física",
    r"El colapso de la presunción": "El fin de la presunción",
    r"El Colapso Empírico": "La Falla Empírica",
    r"el colapso del \"Log Retention": "la insuficiencia del \"Log Retention",
    r"El Suicidio Económico": "El Perjuicio Económico",
    r"El Colapso Epistémico Total": "La Ceguera Tecnológica",
    r"El colapso del agente": "La vulnerabilidad del agente",
    r"La ficción de la": "La insuficiencia de la",
    r"La Ficción de la": "La Ineficacia de la",
    r"la ficción de la": "la insuficiencia de la",
    r"La ilusión de": "La falsa promesa de",
    r"la ilusión de": "la falsa promesa de",
    r"El teatro criptográfico: La farsa del": "La falsa seguridad criptográfica: La insuficiencia del",
    r"El colapso de la potestad": "La neutralización de la potestad"
}

lines = text.split('\n')
new_lines = []
for line in lines:
    if line.startswith('#'):
        for old, new in heading_replacements.items():
            # Use regex for case-insensitive replacement in headings if needed, or exact match
            line = re.sub(old, new, line, flags=re.IGNORECASE)
    new_lines.append(line)

text = '\n'.join(new_lines)

# 2. Global replacements in text (for the most apocalyptic words)
global_replacements = {
    r"\bsuicidio probatorio\b": "indefensión probatoria",
    r"\bSuicidio probatorio\b": "Indefensión probatoria",
    r"\bhemorragia cognitiva\b": "exposición sistémica",
    r"\bhemorragia en VRAM\b": "fuga de memoria (VRAM)",
    r"\bfutilidad\b": "ineficacia",
    r"\bFutilidad\b": "Ineficacia",
    r"\bsecuestrado por\b": "comprometido por",
    r"\bsecuestran\b": "subvierten",
    r"\bapocalipsis\b": "falla sistémica",
    r"\bletal\b": "crítico"  # "letal" is used a lot (as "efecto letal"), we'll change it to "crítico" to be more objective
}

for old, new in global_replacements.items():
    text = re.sub(old, new, text)

# One specific fix: "El hito de Claude Mythos: El colapso de la defensa corporativa"
text = text.replace("El hito de Claude Mythos: El colapso de la defensa corporativa", "El hito de Claude Mythos: La obsolescencia de la defensa corporativa")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tono apocalíptico mitigado.")
