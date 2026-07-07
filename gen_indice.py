#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera el «## Índice analítico» (índice de materias con páginas) al final de
PAPER_v3_trabajo.md, leyendo la paginación REAL de PAPER_v3_Formato_Institucional.pdf.

FLUJO DE 2 PASADAS (los números de página son fijos, así que el orden importa):
  1) ./build_pdf.sh         # asegura que exista el heading «## Índice analítico»
                            #   (aunque sea con contenido viejo) y fija la paginación
  2) python3 gen_indice.py  # recalcula páginas desde el PDF y reescribe el índice
  3) ./build_pdf.sh         # PDF final (el índice crece sólo al final: no desplaza
                            #   las páginas del cuerpo, así que las referencias siguen válidas)

Coincidencia con límites de palabra (\\b) para evitar falsos positivos por subcadena
(p. ej. NIST≠"administrativo", ANCI≠"financiero", Horizon≠"horizonte").
«passim» para términos que aparecen en más de PASSIM páginas.
"""
import re, sys, subprocess, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
MD   = HERE / "PAPER_v3_trabajo.md"
PDF  = HERE / "PAPER_v3_Formato_Institucional.pdf"
PASSIM = 16

# término visible -> patrones a buscar (en minúsculas, con acentos exactos)
TERMS = {
"Agencia de Protección de Datos (APDP)":["agencia de protección de datos","apdp"],
"AI Act (Reglamento UE 2024/1689)":["ai act","2024/1689"],
"AI Liability Directive (COM(2022)496)":["ai liability directive","com(2022)496"],
"ANCI (Agencia Nacional de Ciberseguridad)":["anci"],
"Anthropic":["anthropic"],
"APT28 (PROMPTSTEAL/LAMEHUG)":["apt28"],
"Árboles de Merkle":["merkle"],
"Arranque medido (measured boot)":["measured boot","arranque medido"],
"Atestación remota (RATS, RFC 9334)":["rats","rfc 9334","atestación remota"],
"BadRAM / Battering RAM":["badram","battering ram"],
"BancoEstado / Sodinokibi (2020)":["bancoestado","sodinokibi"],
"Bates v Post Office (escándalo Horizon)":["bates","post office","horizon"],
"BlackMamba":["blackmamba"],
"Boletín 16821-19 (proyecto de ley de IA)":["16821-19"],
"BSI (Alemania)":["bsi"],
"Bullcoming v. New Mexico":["bullcoming"],
"Cadena de custodia":["cadena de custodia"],
"Capital One / AWS (IMDSv1)":["capital one"],
"Carga de la prueba / carga probatoria":["carga de la prueba","carga probatoria"],
"Cifrado homomórfico (FHE)":["homomórfico","homomórfica","fhe"],
"CISA / NSA":["cisa"],
"Claude Fable 5":["fable 5"],
"Claude Mythos":["mythos"],
"Clínica Dávila / Devman":["dávila","devman"],
"CLOUD Act":["cloud act"],
"CMF (Comisión para el Mercado Financiero)":["cmf"],
"Cómputo confidencial (SEV-SNP, TDX, SGX)":["sev-snp","tdx","sgx","cómputo confidencial"],
"Confused deputy (diputado confundido)":["confused deputy"],
"Continuidad operacional / soberana":["continuidad operacional","continuidad soberana"],
"Convenio de Budapest":["budapest"],
"Crawford v. Washington":["crawford"],
"CSIRT Nacional":["csirt"],
"Daubert (fiabilidad pericial)":["daubert"],
"Debido proceso (Art. 19 N°3 CPR)":["19 n°3","19 n° 3","debido proceso"],
"DeepSeek-R1":["deepseek"],
"Delegado de Protección de Datos (DPO)":["delegado de protección de datos","dpo"],
"DICE (Device Identifier Composition Engine)":["device identifier","dice ("],
"eBPF":["ebpf"],
"ECRA (Export Control Reform Act)":["ecra","export control reform"],
"EDPB":["edpb"],
"EDR (detección y respuesta en endpoint)":["edr"],
"eIDAS (Reglamento UE 910/2014)":["eidas","910/2014"],
"EMCO / Guacamaya (2022)":["guacamaya","emco"],
"Encargado de Ciberseguridad":["encargado de ciberseguridad"],
"Equilibrio de Nash / market for lemons":["equilibrio de nash","market for lemons","lemons"],
"Evidencia con proveniencia atestada":["proveniencia atestada"],
"FedRAMP":["fedramp"],
"FISA 702":["fisa 702"],
"FraudGPT":["fraudgpt"],
"FRE 901(b)(9)":["901(b)(9)","fre 901"],
"FTC (Federal Trade Commission)":["ftc"],
"GDPR / RGPD":["gdpr","rgpd"],
"Grupo GTD (2023)":["grupo gtd","gtd"],
"GTIG / Mandiant (Google)":["gtig","mandiant","m-trends"],
"IFX Networks / ChileCompra (2023)":["ifx networks","chilecompra"],
"IMA (Integrity Measurement Architecture)":["integrity measurement"],
"IMDSv1 / IMDSv2 (AWS)":["imdsv1","imdsv2"],
"In re McDonald's":["mcdonald"],
"Indelegabilidad de la responsabilidad":["indelegable","indelegabilidad"],
"InfoStealer":["infostealer"],
"Instituto de Salud Pública (ISP, 2025)":["instituto de salud pública","isp"],
"KRITIS / § 8a BSIG (Alemania)":["kritis","bsig"],
"Ley 19.880 (Procedimiento Administrativo)":["ley 19.880","19.880"],
"Ley 20.009 / Ley 21.234 (medios de pago)":["ley 20.009","ley 21.234"],
"Ley 21.459 (Delitos Informáticos)":["ley 21.459"],
"Ley 21.595 (Delitos Económicos)":["ley 21.595"],
"Ley 21.663 (Marco de Ciberseguridad)":["ley 21.663"],
"Ley 21.719 (Protección de Datos Personales)":["ley 21.719"],
"Lorraine v. Markel":["lorraine v. markel","lorraine v markel"],
"Machine unlearning / supresión exacta":["machine unlearning","unlearning","exact deletion"],
"Malware polimórfico / polimorfismo":["polimórfico","polimórfica","polimorfismo","polymorphism"],
"Mamba / SSM (modelos de espacio de estados)":["mamba","espacio de estados","ssm"],
"Marchand v. Barnhill":["marchand"],
"MAS (Monetary Authority of Singapore)":["monetary authority","principios feat","feat framework"],
"Melendez-Diaz v. Massachusetts":["melendez"],
"MITRE ATT&CK / ATLAS":["mitre att","atlas"],
"NCSC (Reino Unido)":["ncsc"],
"NetFlow / Windows Event Forwarding (WEF)":["netflow","windows event forwarding"],
"NIS2 (Directiva UE 2022/2555)":["nis2","2022/2555"],
"NIST":["nist"],
"Operador de Importancia Vital (OIV)":["operador de importancia vital","oiv"],
"PDPC / IMDA (Singapur)":["pdpc","imda"],
"Plano de control (Control Plane)":["control plane","plano de control"],
"Pliny the Liberator":["pliny"],
"Problema de los Generales Bizantinos":["bizantino","bizantinos","bizantina"],
"Project Glasswing":["glasswing"],
"Prompt injection (inyección de instrucciones)":["prompt injection","inyección de instrucciones"],
"PROMPTFLUX":["promptflux"],
"PROMPTSTEAL / LAMEHUG":["promptsteal","lamehug"],
"ProxyShell (CVE-2021-34473 y rel.)":["proxyshell"],
"Prueba diabólica":["diabólica"],
"Puerto seguro probatorio":["puerto seguro"],
"Ransomware 3.0":["ransomware 3.0"],
"Res ipsa loquitur":["res ipsa"],
"Responsabilidad proactiva (accountability)":["responsabilidad proactiva","accountability"],
"Sana crítica (arts. 295-297 CPP)":["sana crítica"],
"Sandbox regulatorio":["sandbox"],
"Schrems II (C-311/18)":["schrems"],
"SCITT (cadena de suministro / transparencia)":["scitt"],
"SEC (Securities and Exchange Commission)":["sec v","securities and exchange"],
"Servicio de Salud Araucanía Sur (2026)":["araucanía sur"],
"State v. Pickett (TrueAllele)":["pickett"],
"TOCTOU (time-of-check / time-of-use)":["toctou"],
"TPM (Trusted Platform Module)":["tpm"],
"WormGPT":["wormgpt"],
"XBOW":["xbow"],
# --- términos añadidos ---
"NCG 502 (CMF, obligaciones Fintec)":["ncg 502"],
"RAN 20-7 / 20-8 / 20-10 (normativa CMF)":["ran 20-7","ran 20-8","ran 20-9","ran 20-10","capítulo 20-7","capítulo 20-8","capítulo 20-10"],
"Banco de Chile / Redbanc (Lazarus, 2018)":["banco de chile","redbanc","powerratankba"],
"Preservación provisoria (Art. 218 bis CPP)":["218 bis","preservación provisoria"],
"Incidente (reporte y gestión de)":["reporte de incidente","reporte del incidente","reporte de incidentes","gestión de incidentes","notificación de incidente","deber de reporte"],
"Responsable de la información / del tratamiento":["responsable de la información","responsable del tratamiento","responsable de datos","responsable de la informacion"],
"Teoría de juegos de la atestación":["teoría de juegos","juegos de la atestación"],
# --- referencias cruzadas (véase) ---
"Bizantino, problema de los Generales":("SEE","Problema de los Generales Bizantinos"),
"Guacamaya (hackeo)":("SEE","EMCO / Guacamaya (2022)"),
"Horizon (escándalo)":("SEE","Bates v Post Office (escándalo Horizon)"),
"Mythos":("SEE","Claude Mythos"),
"Sodinokibi":("SEE","BancoEstado / Sodinokibi (2020)"),
"Teoría de juegos / equilibrio de Nash":("SEE","Equilibrio de Nash / market for lemons"),
}

def page_texts():
    txt = subprocess.run(["pdftotext","-enc","UTF-8",str(PDF),"-"],
                         capture_output=True, text=True).stdout
    return [p.lower() for p in txt.split("\f")]

def rx(p): return re.compile(r"(?<!\w)"+re.escape(p.lower())+r"(?!\w)", re.UNICODE)

def fold(s):
    s = s.lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"^[«\"'\(¿¡]+", "", s).strip()

def main():
    if not PDF.exists():
        sys.exit("Falta PAPER_v3_Formato_Institucional.pdf — corre ./build_pdf.sh primero.")
    P = page_texts()
    # Acotar la búsqueda al CUERPO: excluir el TOC del frente y el propio índice del final,
    # para no citar ni la tabla de contenidos ni el propio índice analítico.
    marker = "términos clave y las páginas del pdf"
    cutoff = next((i for i, p in enumerate(P) if marker in p), len(P))
    # Marcador de inicio del cuerpo: el subtítulo (texto que NO está en el TOC; el título
    # de la H1 sí aparece listado en el TOC, así que no sirve como marcador).
    start  = next((i for i, p in enumerate(P)
                   if "por qué la evidencia digital delegada en la nube" in p), 0)
    entries = []
    for label, pats in TERMS.items():
        if isinstance(pats, tuple) and pats and pats[0] == "SEE":
            entries.append((label, None, pats[1]))          # referencia cruzada «véase»
            continue
        comps = [rx(p) for p in pats]
        hits = sorted(i+1 for i in range(start, cutoff) if any(c.search(P[i]) for c in comps))
        entries.append((label, hits, None))
    missing = [l for l, h, s in entries if h is not None and not h]
    entries.sort(key=lambda e: fold(e[0]))

    out = ["## Índice analítico", "",
           "*Índice de materias: términos clave y las páginas del PDF donde aparecen. "
           "Las entradas «*véase*» remiten al término principal. Los números corresponden a "
           "la paginación de esta versión; si el documento se reedita, el índice debe "
           "regenerarse (`python3 gen_indice.py`).*"]
    cur = None
    for label, hits, see in entries:
        L = fold(label)[0].upper()
        if L != cur:
            cur = L; out.append(f"\n**{L}**\n")
        ref = f"*véase* {see}" if see is not None else (", ".join(map(str, hits)) or "—")
        out.append(f"- **{label},** {ref}")
    block = "\n".join(out) + "\n"

    src = MD.read_text(encoding="utf-8")
    if "## Índice analítico" not in src:
        src = src.rstrip() + "\n\n" + block          # primera vez: añade al final
    else:
        idx = src.index("## Índice analítico")
        after = src[idx:]
        colofon = ""
        if "<!-- COLOFON -->" in after:
            colofon = "\n\n<!-- COLOFON -->" + after.split("<!-- COLOFON -->", 1)[1].rstrip() + "\n"
        src = src[:idx] + block.rstrip() + "\n" + colofon  # reemplaza el índice, conserva el colofón
    MD.write_text(src, encoding="utf-8")
    print(f"Índice regenerado: {len(entries)} términos | sin ocurrencia: {missing or 'ninguno'}")
    print("Ahora corre ./build_pdf.sh para el PDF final.")

if __name__ == "__main__":
    main()
