#!/usr/bin/env bash
# Regenera PAPER_v3_Formato_Institucional.pdf desde PAPER_v3_trabajo.md
# Usa template.html (portada diseñada + style.css) y toc-depth=4.
# Para el índice analítico: ./build_pdf.sh → python3 gen_indice.py → ./build_pdf.sh
set -euo pipefail
cd "$(dirname "$0")"

# Prefacio: AHORA vive integrado en el cuerpo de PAPER_v3_trabajo.md (antes de
# Escenario I), no como fragmento front-matter inyectado. Se desactiva la inyección
# separada de PALABRAS_PREVIAS_borrador.md para evitar que el prefacio salga DUPLICADO.
INCLUDE_BEFORE=""
# if [ -f PALABRAS_PREVIAS_borrador.md ]; then
#   pandoc PALABRAS_PREVIAS_borrador.md -o .preface.fragment.html
#   INCLUDE_BEFORE="--include-before-body=.preface.fragment.html"
# fi

pandoc PAPER_v3_trabajo.md -o PAPER_v3_Formato_Institucional.html --standalone \
  --template=template.html \
  $INCLUDE_BEFORE \
  -V lang=es --toc --toc-depth=4

rm -f .preface.fragment.html

google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=PAPER_v3_Formato_Institucional.pdf \
  --print-to-pdf-no-header --no-pdf-header-footer \
  PAPER_v3_Formato_Institucional.html

# Metadata (Author/Subject/Keywords) + marcadores/outline desde los encabezados H2.
# Chrome no los genera; pikepdf los inyecta sin re-rasterizar.
python3 postprocess_pdf.py || echo 'WARN: postprocess (metadata/marcadores) omitido — pikepdf no disponible'

echo "PDF: $(pdfinfo PAPER_v3_Formato_Institucional.pdf 2>/dev/null | awk '/Pages/{print $2}') páginas"
