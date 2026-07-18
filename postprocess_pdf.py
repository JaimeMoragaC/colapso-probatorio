#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-procesa PAPER_v3_Formato_Institucional.pdf (generado por Chrome, que no
fija Author/Subject/Keywords ni marcadores): inyecta metadata del documento y un
esquema de marcadores (outline) construido desde los encabezados H2 (## ) del
markdown, localizados por su página real en el PDF. Se ejecuta como paso final
del build (después de Chrome)."""
import re, subprocess, sys
from pathlib import Path
import pikepdf

HERE = Path(__file__).resolve().parent
MD  = HERE / "PAPER_v3_trabajo.md"
PDF = HERE / "PAPER_v3_Formato_Institucional.pdf"

TITLE   = ("La Ficción de la Ciberseguridad Corporativa: Certificaciones de papel, "
           "CISOs silenciados y la indefensión de los Directorios. El secreto que su Gerencia de Seguridad barre bajo la alfombra.")
AUTHOR  = "Jaime Marcelo Moraga Carrasco"
SUBJECT = ("Dictamen en derecho: fiabilidad de la evidencia digital, soberanía "
           "tecnológica y límites de la potestad sancionatoria (Leyes 21.663, "
           "21.719 y 21.459; Boletín 16821-19)")
KEYWORDS = ("evidencia digital, atestación remota, ciberseguridad, Ley 21.663, "
            "Ley 21.719, protección de datos, inteligencia artificial, ANCI, "
            "soberanía tecnológica, carga de la prueba, cómputo confidencial, TPM, "
            "cadena de custodia, OIV, Boletín 16821-19")

def clean(h):
    h = re.sub(r"<[^>]+>", "", h)          # tags html
    h = h.replace("↩", "").replace("#", "")
    h = re.sub(r"\*+", "", h)
    h = re.sub(r"\{[^}]*\}", "", h)     # atributos pandoc {.clase}
    return re.sub(r"\s+", " ", h).strip()

def heading_key(h):
    # substring distintivo para buscar en el texto del PDF (sin nº de nota final)
    k = clean(h)
    k = re.sub(r"\d+$", "", k).strip()      # quita superíndice de nota pegado
    return k[:38]

def main():
    if not PDF.exists():
        sys.exit("Falta el PDF; corre ./build_pdf.sh primero.")
    md = MD.read_text(encoding="utf-8").split("\n")
    pref_path = HERE / "preface.md"          # front matter inyectado antes del índice
    pref = pref_path.read_text(encoding="utf-8").split("\n") if pref_path.exists() else []
    headings = [ln[3:] for ln in (pref + md) if ln.startswith("## ")]

    pages = subprocess.run(["pdftotext","-enc","UTF-8",str(PDF),"-"],
                           capture_output=True, text=True).stdout.split("\f")
    norm = [re.sub(r"\s+"," ", p) for p in pages]
    # Inicio del cuerpo, TRAS el TOC (Escenario I, marcado por "03:14"): las búsquedas de
    # encabezados arrancan aquí para no confundirlos con sus entradas del índice.
    body0 = next((i for i,p in enumerate(norm) if "03:14" in p), 0)
    # El prefacio es front matter ANTES del TOC; se ubica aparte por su epígrafe.
    pref_pg = next((i for i,p in enumerate(norm) if "no admite primera persona" in p), None)

    outline, cur, missing = [], body0, []
    for h in headings:
        key = heading_key(h)
        if key.startswith("Palabras previas"):
            if pref_pg is not None:
                outline.append((re.sub(r"\s*\d+$","",clean(h)).strip(), pref_pg))
            else:
                missing.append(clean(h))
            continue
        pg = next((i for i in range(cur, len(norm)) if key and key in norm[i]), None)
        if pg is None:
            missing.append(clean(h)); continue
        title = re.sub(r"\s*\d+$", "", clean(h)).strip()   # quita superíndice de nota
        outline.append((title, pg)); cur = pg

    pdf = pikepdf.open(str(PDF), allow_overwriting_input=True)
    with pdf.open_metadata() as m:
        m["dc:title"] = TITLE
        m["dc:creator"] = [AUTHOR]
        m["dc:description"] = SUBJECT
        m["pdf:Keywords"] = KEYWORDS
    pdf.docinfo["/Title"]    = TITLE
    pdf.docinfo["/Author"]   = AUTHOR
    pdf.docinfo["/Subject"]  = SUBJECT
    pdf.docinfo["/Keywords"] = KEYWORDS

    with pdf.open_outline() as ol:
        ol.root.clear()
        for title, pg in outline:
            ol.root.append(pikepdf.OutlineItem(title, pg))

    pdf.save(str(PDF))
    pdf.close()
    print(f"Metadata fijada (Author/Subject/Keywords). Marcadores: {len(outline)}.")
    for title, pg in outline:
        print(f"  p{pg+1:>3}  {title[:60]}")
    if missing:
        print("SIN UBICAR (revisar):", missing)

if __name__ == "__main__":
    main()
