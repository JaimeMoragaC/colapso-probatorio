import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PALABRAS_PREVIAS_borrador.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace judge/justice references with corporate/regulatory ones
replacements = {
    r"nuestra «sana crítica» o nuestro celo de \*compliance\*": r"nuestras auditorías forenses y nuestros programas de *compliance*",
    r"a los jueces y directores corporativos": r"a los directores corporativos, a los CISOs y al propio regulador",
    r"guardián de la justicia": r"garante de la fe pública documental",
    r"Para un jurista, la duda adquiere entonces una gravedad absoluta:": r"Para el Directorio y el oficial de cumplimiento, la duda adquiere entonces una gravedad patrimonial y penal extrema:",
    r"el atacante hackee a la máquina": r"el atacante comprometa a la máquina",
    r"este documento demuestra": r"este análisis demuestra",
    r"pero que jueces, reguladores y auditores": r"pero que reguladores, directorios y auditores",
    r"y su sana crítica": r"y sus métricas de control superficial",
    r"la democratización del ataque que aquí describo": r"la escalada del ataque que aquí describo",
    r"el abandono ciego del raciocinio humano": r"la delegación ciega de la responsabilidad humana"
}

for old, new in replacements.items():
    text = re.sub(old, new, text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Palabras previas refactorizadas (enfoque corporativo).")
