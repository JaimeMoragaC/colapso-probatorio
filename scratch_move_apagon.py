import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = r"### El apagón jurisdiccional del 12 de junio de 2026"
end_marker = r"proyectadas por una caja negra controlada por el adversario."
target_marker = r"# 1\. El Falso Consenso de la Seguridad Cloud: Anatomía de un Fracaso Normativo"

# Build pattern to capture the block
pattern = re.compile(rf"({start_marker}.*?{end_marker}\n+)", re.DOTALL)
match = pattern.search(text)

if match:
    block = match.group(1)
    
    # Remove the block from its original position
    text = text.replace(block, "")
    
    # Insert the block just before the target marker
    # Ensure there's enough spacing
    block_with_spacing = f"{block.strip()}\n\n"
    text = re.sub(rf"({target_marker})", rf"{block_with_spacing}\1", text)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Block moved successfully.")
else:
    print("Could not find the block to move.")
