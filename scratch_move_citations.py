import os

# 1. Update PALABRAS_PREVIAS_borrador.md
preface_path = '/home/jaime/Descargas/colapso-probatorio/PALABRAS_PREVIAS_borrador.md'
with open(preface_path, 'r', encoding='utf-8') as f:
    preface = f.read()

# Replace symbols
preface = preface.replace('financiamiento¹', 'financiamiento [1]')
preface = preface.replace('absurdo²', 'absurdo [2]')
preface = preface.replace('nadan³', 'nadan [3]')

# Remove the footnotes at the bottom
lines = preface.split('\n')
new_lines = []
for line in lines:
    if line.startswith('¹ McCarthy, J.') or line.startswith('² Turing, A.') or line.startswith('³ Dijkstra, E.'):
        continue
    new_lines.append(line)

with open(preface_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines).strip() + '\n')

# 2. Add Anexo C to PAPER_v3_trabajo.md
paper_path = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(paper_path, 'r', encoding='utf-8') as f:
    paper = f.read()

anexo_text = """

<div style="page-break-before: always;"></div>

<a id="anexo-citas"></a>

## Anexo C: Referencias Bibliográficas del Prefacio

[1] McCarthy, J. et al., *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*, 1955.

[2] Turing, A. M., *«Computing Machinery and Intelligence»*, Mind, 1950.

[3] Dijkstra, E. W., *«The threats to computing science» (EWD898)*, 1984.

"""

if "Anexo C: Referencias Bibliográficas del Prefacio" not in paper:
    paper = paper.rstrip() + anexo_text

with open(paper_path, 'w', encoding='utf-8') as f:
    f.write(paper)
