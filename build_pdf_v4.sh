#!/usr/bin/env bash
# Regenera PAPER_v4_Formato_Institucional.pdf desde PAPER_v4_storyline.md
# Usa template.html (portada diseñada + style.css) y toc-depth=4.
set -euo pipefail
cd "$(dirname "$0")"

INCLUDE_BEFORE=""
if [ -f PALABRAS_PREVIAS_borrador.md ]; then
  pandoc PALABRAS_PREVIAS_borrador.md -o .preface.fragment.html
  INCLUDE_BEFORE="--include-before-body=.preface.fragment.html"
fi

echo "Generando HTML intermedio para PAPER_v4_storyline.md..."
pandoc PAPER_v4_storyline.md -o PAPER_v4_Formato_Institucional.html --standalone --self-contained \
  --template=template.html \
  $INCLUDE_BEFORE \
  -V lang=es --toc --toc-depth=4

rm -f .preface.fragment.html

echo "Compilando PDF con Google Chrome Headless..."
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=PAPER_v4_Formato_Institucional.pdf \
  --print-to-pdf-no-header --no-pdf-header-footer \
  PAPER_v4_Formato_Institucional.html

python3 postprocess_pdf.py || echo 'WARN: postprocess (metadata/marcadores) omitido — pikepdf no disponible'

echo "=========================================================="
echo "ÉXITO: PAPER_v4_Formato_Institucional.pdf compilado."
echo "Páginas: $(pdfinfo PAPER_v4_Formato_Institucional.pdf 2>/dev/null | awk '/Pages/{print $2}')"
echo "=========================================================="
