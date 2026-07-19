import os
import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace <p id="fnX"> with <p><a name="fnX" id="fnX"></a>
for i in range(301, 311):
    old_p = f'<p id="fn{i}">'
    new_p = f'<p><a name="fn{i}" id="fn{i}"></a>'
    text = text.replace(old_p, new_p)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Footnotes anchors arreglados")
