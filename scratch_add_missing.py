import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the missing footnotes in the text
text = text.replace('Danziger, Levav y Avnaim-Pesso (2011) analizaron 1.112 resoluciones', 'Danziger, Levav y Avnaim-Pesso (2011)[^309] analizaron 1.112 resoluciones')
text = text.replace('Guthrie, Rachlinski & Wistrich (2001; 2007)', 'Guthrie, Rachlinski & Wistrich (2001; 2007)[^310]')
text = text.replace('las dos variables que Kahneman separó', 'las dos variables que Kahneman separó[^306]')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Text updated with missing footnotes.")
