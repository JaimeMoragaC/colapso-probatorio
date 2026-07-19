import os

# 1. Revert PALABRAS_PREVIAS_borrador.md
preface_path = '/home/jaime/Descargas/colapso-probatorio/PALABRAS_PREVIAS_borrador.md'
with open(preface_path, 'r', encoding='utf-8') as f:
    preface = f.read()

preface = preface.replace('financiamiento [1]', 'financiamiento¹')
preface = preface.replace('absurdo [2]', 'absurdo²')
preface = preface.replace('nadan [3]', 'nadan³')

footnotes = """
¹ McCarthy, J. et al., A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence, 1955.  
² Turing, A. M., «Computing Machinery and Intelligence», Mind, 1950.  
³ Dijkstra, E. W., «The threats to computing science» (EWD898), 1984.
"""

if '¹ McCarthy' not in preface:
    preface = preface.rstrip() + '\n\n' + footnotes.strip() + '\n'

with open(preface_path, 'w', encoding='utf-8') as f:
    f.write(preface)


# 2. Revert PAPER_v3_trabajo.md
paper_path = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(paper_path, 'r', encoding='utf-8') as f:
    paper = f.read()

anexo_text_start = '<div style="page-break-before: always;"></div>\n\n<a id="anexo-citas"></a>\n\n## Anexo C: Referencias Bibliográficas del Prefacio'

if anexo_text_start in paper:
    paper = paper.split(anexo_text_start)[0].rstrip() + '\n'
    
with open(paper_path, 'w', encoding='utf-8') as f:
    f.write(paper)
