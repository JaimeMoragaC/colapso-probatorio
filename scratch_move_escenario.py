import os

paper_path = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
cap8_path = '/home/jaime/Descargas/colapso-probatorio/CAPITULO_8_VALORACION_JUDICIAL_EXTRAIDO.md'

with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if line.startswith("### Escenario III. El ataque Ring-0 y la autoridad decisional"):
        # Go back one line to include empty lines if any
        start_idx = i - 1 if i > 0 and lines[i-1].strip() == "" else i
    if start_idx != -1 and line.startswith("### Como leer este Documento"):
        # Go back to the '---' line
        for j in range(i, start_idx, -1):
            if lines[j].strip() == "---":
                end_idx = j
                break
        break

if start_idx != -1 and end_idx != -1:
    extracted_text = "".join(lines[start_idx:end_idx])
    
    # Delete from paper
    new_paper_lines = lines[:start_idx] + lines[end_idx:]
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.writelines(new_paper_lines)
        
    # Append to CAPITULO_8 before the Bibliography
    with open(cap8_path, 'r', encoding='utf-8') as f:
        cap8_content = f.read()
        
    bib_tag = "### Bibliografía específica de §8"
    if bib_tag in cap8_content:
        cap8_parts = cap8_content.split(bib_tag)
        new_cap8 = cap8_parts[0] + "\n\n" + extracted_text + "\n\n" + bib_tag + cap8_parts[1]
        with open(cap8_path, 'w', encoding='utf-8') as f:
            f.write(new_cap8)
        print("Escenario III movido exitosamente al capítulo extraído.")
    else:
        print("No se encontró la bibliografía en CAPITULO_8.")
else:
    print(f"No se pudo encontrar los índices. Start: {start_idx}, End: {end_idx}")
