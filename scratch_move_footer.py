import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# The block to move
block_start = "*Fuentes y Verificabilidad Jurisprudencial (Anexo del Capítulo 8):*"
block_end_pattern = r"(<p id=\"fn313\">.*?</p>)"

match = re.search(re.escape(block_start) + r"(.*?)" + block_end_pattern, text, re.DOTALL)

if match:
    full_block = match.group(0)
    # Remove it from its current location
    text = text.replace(full_block, "")
    
    # Append it to the very end of the document
    text = text.strip() + "\n\n---\n" + full_block + "\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Block moved to the end of the document.")
else:
    print("Block not found!")
