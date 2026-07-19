import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith("### Como leer este Documento"):
        skip = True
    if skip and line.startswith("## Arquitectura del Documento: El Frente Corporativo y Regulatorio"):
        skip = False
    
    if not skip:
        if line.startswith("Ambas disciplinas convergen, hacia el final del documento, en una solución arquitectónica idónea mandatorio: la Soberanía Forense anclada en hardware."):
            new_lines.append(line)
            new_lines.append("\nSe incorpora un Glosario interdisciplinario (Anexo A) que traduce cada término técnico a su relevancia jurídica y viceversa. Una convicción atraviesa el documento: ningún lector necesita ser experto en las dos disciplinas para seguir el argumento; solo necesita aceptar que el problema no respeta la frontera entre ellas.\n")
        else:
            new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
