import re
import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
extract_path = '/home/jaime/Descargas/colapso-probatorio/CAPITULO_8_VALORACION_JUDICIAL_EXTRAIDO.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract Chapter 8 body
ch8_start = r'<div style="page-break-before: always;"></div>\s*## SEGUNDA PARTE — La máquina firma por el juez'
ch8_end = r'## Profundizaciones en la frontera'
ch8_pattern = re.compile(f'({ch8_start}.*?)(?={ch8_end})', re.DOTALL)

ch8_match = ch8_pattern.search(text)
ch8_content = ""
if ch8_match:
    ch8_content = ch8_match.group(1)
    
    # Create the corollary
    corolario = """<div style="page-break-before: always;"></div>

## Corolario Jurisdiccional: El juez como periférico vulnerable

> *Como se demuestra extensamente en el trabajo complementario de esta serie ("La valoración judicial de la evidencia digital en la era de la IA generativa"), la mente del juez humano opera con recursos finitos (racionalidad limitada). Frente a un registro digital opaco, originado en Ring-0 y no atestado criptográficamente en origen, el sistema procesal de "Sana Crítica" colapsa. El tribunal se convierte en un periférico cognitivo vulnerable que procesará ciegamente la falsificación algorítmica (Mythos) como verdad empírica, consolidando la indefensión probatoria de la víctima y la impunidad corporativa.*

"""
    text = text[:ch8_match.start()] + corolario + text[ch8_match.end():]
else:
    print("Chapter 8 body not found.")

# 2. Extract Chapter 8 footer
footer_start = r'\*Fuentes y Verificabilidad Jurisprudencial'
footer_end = r'(<p id=\"fn313\">.*?</p>)'
footer_pattern = re.compile(f'({footer_start}.*?{footer_end})', re.DOTALL)

footer_match = footer_pattern.search(text)
footer_content = ""
if footer_match:
    footer_content = footer_match.group(1)
    
    # Remove footer from text, including the preceding ---
    text = re.sub(r'---\s*' + re.escape(footer_content) + r'\s*', '', text, flags=re.DOTALL)
else:
    print("Chapter 8 footer not found.")

# Write extracted content
if ch8_content or footer_content:
    with open(extract_path, 'w', encoding='utf-8') as f:
        f.write("# SECCIÓN EXTRAÍDA: FRENTE JURISDICCIONAL Y VALORACIÓN JUDICIAL\n\n")
        if ch8_content:
            f.write(ch8_content)
        if footer_content:
            f.write("\n\n---\n")
            f.write(footer_content)
            f.write("\n")
    print(f"Extracted to {extract_path}")

# Save the new markdown
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated PAPER_v3_trabajo.md")
