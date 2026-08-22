#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LexControl - Motor de Inteligencia y Ordenamiento Taxonómico de Expedientes (v2.0 PRO REAL)
============================================================================================
Arquitectura de 5 Niveles COMPLETA Y FUNCIONAL:
1. Consolidación en Raíz Original (/media/jaime/c11cad3b-.../Casos2023).
2. Aspiradora Forense de archivos sueltos desde Descargas y carpetas dispersas.
3. Jerarquía Taxonómica: Cliente -> Causa/Expediente -> Categorías procesales.
4. Bandeja de Contención: /_Documentos_Generales_Sin_Rol/ para archivos de cliente sin causa.
5. Deduplicación inteligente por Hash SHA-256 para eliminar copias repetidas y Cuarentena segura.
"""

import os
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import json
import urllib.request
try:
    import fitz
except ImportError:
    fitz = None

GEMINI_API_KEY = "TU_API_KEY_AQUI_POR_SEGURIDAD"

def extraer_caratula_ia(ruta_pdf):
    if not fitz:
        print("   ⚠️ [ERROR] PyMuPDF (fitz) no instalado. No se puede hacer Micro-Auditoría.")
        return None
        
    try:
        doc = fitz.open(ruta_pdf)
        texto = ""
        # Extraer max 2 páginas
        for i in range(min(2, doc.page_count)):
            texto += doc[i].get_text("text") + "\n"
        doc.close()
        
        texto_limpio = texto.strip()[:1500]
        if len(texto_limpio) < 50:
            return None
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        schema = {
            "type": "object",
            "properties": {
                "rol_rit": {"type": "string", "description": "Ej: C-1234-2023 o O-123-2024"},
                "ruc": {"type": "string"},
                "competencia": {"type": "string", "description": "Civil, Penal, Laboral, Familia o Cobranza"},
                "tribunal": {"type": "string"},
                "demandante_querellante": {"type": "string"},
                "demandado_imputado": {"type": "string"},
                "materia": {"type": "string"}
            },
            "required": ["rol_rit", "tribunal", "demandante_querellante", "demandado_imputado", "competencia"]
        }
        
        prompt = f"""
Eres un oficinista experto del Poder Judicial. Analiza el siguiente texto de la carátula o primeras páginas de un expediente judicial y extrae los datos estructurales solicitados en JSON estricto.
Si falta un dato, déjalo vacío o nulo, pero asegúrate de extraer el ROL/RIT, las partes y el tribunal.

TEXTO:
{texto_limpio}
"""
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            texto_respuesta = res['candidates'][0]['content']['parts'][0]['text']
            return json.loads(texto_respuesta)
            
    except Exception as e:
        print(f"   ⚠️ [IA FALLA] Error al procesar Micro-Auditoría: {e}")
        return None


# 1. CONFIGURACIÓN DE RUTAS RAÍZ
DISCO_CASOS_RAIZ = Path("/media/jaime/c11cad3b-6d38-462a-9c2e-49c33f1f6c18/Casos2023")
CARPETAS_ASPIRAR = [
    Path("/home/jaime/Descargas"),
    Path("/home/jaime/Descargas/colapso-probatorio"),
]

# Si el disco externo no está conectado, creamos una raíz consolidada en Descargas para probar
if not DISCO_CASOS_RAIZ.exists():
    DISCO_CASOS_RAIZ = Path("/home/jaime/Descargas/Casos2023-Consolidados")
    print(f"⚠️ Nota: Disco externo /media/... no detectado. Usando raíz consolidada local: {DISCO_CASOS_RAIZ}")

# 2. BASE DE CONOCIMIENTO: CLIENTES Y SUS CAUSAS
CLIENTES_DB = {
    "moraga": {
        "nombre": "Jaime Marcelo Moraga Carrasco (Socio - Autodefensa)",
        "rut": "8.328.581-8",
        "keywords": ["moraga", "saldivia", "medina", "1869-2026", "temuco", "digüeñes", "1869", "389-2024", "quater"],
        "causas": {
            "1869-2026": {"rol": "ROL C-1869-2026", "caratula": "MEDINA con MORAGA (3º Civil Temuco)", "keywords": ["1869", "medina", "saldivia", "temuco"]},
            "389-2024": {"rol": "ROL C-389-2024", "caratula": "Arrendamiento 389-2024", "keywords": ["389-2024", "quater", "recibe causa"]}
        }
    },
    "welt": {
        "nombre": "Ópticas Welt SpA",
        "rut": "77.176.965-K",
        "keywords": ["welt", "optica", "opticas", "1604-2025"],
        "causas": {
            "1604-2025": {"rol": "ROL C-1604-2025", "caratula": "Cobranza Ópticas Welt", "keywords": ["1604", "welt", "cobranza"]}
        }
    },
    "cuevas": {
        "nombre": "Froilán Cuevas",
        "rut": "12.057.371-5",
        "keywords": ["cuevas", "froilan", "25727-2026", "suprema"],
        "causas": {
            "25727-2026": {"rol": "ROL 25727-2026", "caratula": "Corte Suprema Cuevas Froilán", "keywords": ["25727", "suprema", "cuevas"]}
        }
    },
    "inzunza": {
        "nombre": "Juanico - Inzunza",
        "rut": "Sin RUT",
        "keywords": ["inzunza", "juanico", "1000-2023", "absolucion"],
        "causas": {
            "1000-2023": {"rol": "ROL C-1000-2023", "caratula": "JUANICO con INZUNZA", "keywords": ["1000", "inzunza"]}
        }
    },
    "laboral_penal": {
        "nombre": "Litigios Laborales y Penales Diversos",
        "rut": "Múltiples Mandantes",
        "keywords": ["84-2025", "estafa", "casas", "canete", "cañete", "304-2025", "1050-2025", "valparaiso", "125-2025"],
        "causas": {
            "84-2025": {"rol": "RIT 84-2025", "caratula": "Sentencia RIT 84-2025", "keywords": ["84-2025"]},
            "304-2025": {"rol": "ROL C-304-2025", "caratula": "Juzgado Letras Cañete - Absolución", "keywords": ["304-2025", "canete", "cañete"]},
            "4019-2025": {"rol": "RIT P-4019-2025", "caratula": "Querella Estafa Casas", "keywords": ["estafa", "casas", "acoge a tramitacion"]},
            "1050-2025": {"rol": "ROL C-1050-2025", "caratula": "Reposición y Apelación", "keywords": ["1050-22025", "1050-2025", "reposicion y apelacion"]},
            "125-2025": {"rol": "ROL 125-2025", "caratula": "Corte Apelaciones Valparaíso", "keywords": ["125-2025", "valparaiso"]}
        }
    }
}

# Subcarpetas taxonómicas estándar por expediente
CATEGORIAS_PROCESALES = {
    "demanda": "01_Demandas_y_Contestaciones",
    "contestacion": "01_Demandas_y_Contestaciones",
    "reconven": "01_Demandas_y_Contestaciones",
    "resolucion": "02_Resoluciones_OJV",
    "recibe_causa": "02_Resoluciones_OJV",
    "recibe causa": "02_Resoluciones_OJV",
    "sentencia": "02_Resoluciones_OJV",
    "acoge": "02_Resoluciones_OJV",
    "folio": "02_Resoluciones_OJV",
    "transferencia": "03_Prueba_Documental_y_Finanzas",
    "pago": "03_Prueba_Documental_y_Finanzas",
    "comprobante": "03_Prueba_Documental_y_Finanzas",
    "posiciones": "03_Prueba_Documental_y_Finanzas",
    "boleta": "03_Prueba_Documental_y_Finanzas",
    "acompaña": "04_Escritos_y_Mero_Tramite",
    "escrito": "04_Escritos_y_Mero_Tramite",
    "anuncio": "04_Escritos_y_Mero_Tramite",
    "alegato": "04_Escritos_y_Mero_Tramite",
    "reposicion": "04_Escritos_y_Mero_Tramite",
    "audiencia": "05_Audiencias_y_Actas",
    "acta": "05_Audiencias_y_Actas",
    "comparecencia": "05_Audiencias_y_Actas",
    "certificacion": "05_Audiencias_y_Actas",
    "canete": "05_Audiencias_y_Actas"
}

def calcular_hash_sha256(ruta_archivo):
    """Calcula el hash SHA-256 de un archivo para detectar duplicados idénticos."""
    hasher = hashlib.sha256()
    with open(ruta_archivo, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def clasificar_y_consolidar():
    print("="*80)
    print("⚡ [NIVEL 1] Inicializando Consolidación en Raíz:", DISCO_CASOS_RAIZ)
    print("="*80)
    DISCO_CASOS_RAIZ.mkdir(parents=True, exist_ok=True)
    
    hashes_existentes = set()
    archivos_procesados = 0
    archivos_duplicados = 0
    archivos_sin_causa = 0

    # 1. Mapear hashes de los archivos que YA están en Casos2023 para evitar duplicarlos
    for root, _, files in os.walk(DISCO_CASOS_RAIZ):
        for file in files:
            ruta_comp = Path(root) / file
            if ruta_comp.is_file():
                try:
                    hashes_existentes.add(calcular_hash_sha256(ruta_comp))
                except Exception:
                    pass

    # 2. Aspirar archivos de las carpetas dispersas (Descargas, colapso-probatorio, etc.)
    carpetas_a_procesar = [p for p in CARPETAS_ASPIRAR if p.exists()]

    for carpeta_origen in carpetas_a_procesar:
        print(f"\n🌪️ [NIVEL 2] Aspirando y escaneando carpeta: {carpeta_origen}")
        for root, _, files in os.walk(carpeta_origen):
            # No escanear carpetas de nodo, git o nuestra raíz de destino
            if any(ign in str(root) for ign in ["node_modules", ".git", "Casos2023", "LexControl-"]):
                continue

            for file in files:
                # Filtrar archivos temporales o irrelevantes (.js, .html, .css, etc.) para centrarse en documentos legales
                if file.startswith('.') or not file.lower().endswith(('.pdf', '.docx', '.doc', '.xlsx', '.xls', '.png', '.jpg', '.jpeg')):
                    continue

                ruta_orig = Path(root) / file
                if not ruta_orig.is_file():
                    continue

                nombre_lower = file.lower()

                # [NIVEL 4] Deduplicación: Si es idéntico a uno ya almacenado, se omite
                try:
                    file_hash = calcular_hash_sha256(ruta_orig)
                    if file_hash in hashes_existentes:
                        print(f"   🗑️ [DUPLICADO IGNORADO] '{file}' ya está archivado en Casos2023 (Hash idéntico).")
                        archivos_duplicados += 1
                        continue
                    hashes_existentes.add(file_hash)
                except Exception:
                    pass

                # Identificar Cliente y Causa en nuestra base de conocimiento
                cliente_encontrado = None
                causa_encontrada = None

                for cl_key, cl_info in CLIENTES_DB.items():
                    if any(kw in nombre_lower for kw in cl_info["keywords"]):
                        cliente_encontrado = cl_info
                        for c_key, c_info in cl_info["causas"].items():
                            if any(ckw in nombre_lower for ckw in c_info["keywords"]):
                                causa_encontrada = c_info
                                break
                        if causa_encontrada or cliente_encontrado:
                            break

                # Casos especiales de nombres cifrados o escaneos
                if not cliente_encontrado:
                    if any(sp in nombre_lower for sp in ["04-04-2025", "20250727", "medina"]):
                        cliente_encontrado = CLIENTES_DB["moraga"]
                        causa_encontrada = CLIENTES_DB["moraga"]["causas"]["1869-2026"]
                    elif "optica" in nombre_lower or "welt" in nombre_lower:
                        cliente_encontrado = CLIENTES_DB["welt"]
                        causa_encontrada = CLIENTES_DB["welt"]["causas"]["1604-2025"]

                # [NIVEL 3 y 5] Determinar Ruta Destino
                if cliente_encontrado and causa_encontrada:
                    # Nivel 3.B: Causa Específica
                    cat_proc = "04_Escritos_y_Mero_Tramite"
                    for kw, cat in CATEGORIAS_PROCESALES.items():
                        if kw in nombre_lower:
                            cat_proc = cat
                            break
                    ruta_destino = DISCO_CASOS_RAIZ / f"[{cliente_encontrado['rut']}] {cliente_encontrado['nombre']}" / f"[{causa_encontrada['rol']}] {causa_encontrada['caratula']}" / cat_proc
                elif cliente_encontrado and not causa_encontrada:
                    # Nivel 3.C: [TU PROPUESTA BRILLANTE] Bandeja General de Cliente sin Rol Específico
                    ruta_destino = DISCO_CASOS_RAIZ / f"[{cliente_encontrado['rut']}] {cliente_encontrado['nombre']}" / "_Documentos_Generales_Sin_Rol"
                    archivos_sin_causa += 1
                else:
                    # Fallback: Usar IA de Micro-Auditoría para Extraer Datos si es un PDF judicial desconocido
                    if file.lower().endswith('.pdf'):
                        print(f"   🤖 [IA ACTIVA] Documento desconocido. Iniciando Micro-Auditoría de Carátula: {file}")
                        datos_ia = extraer_caratula_ia(ruta_orig)
                        if datos_ia and datos_ia.get("rol_rit") and datos_ia.get("demandante_querellante"):
                            # Limpiar strings para carpetas
                            rol_limpio = re.sub(r'[^a-zA-Z0-9_-]', '', datos_ia["rol_rit"])
                            dem_limpio = re.sub(r'[^a-zA-Z0-9_ -]', '', datos_ia["demandante_querellante"])
                            def_limpio = re.sub(r'[^a-zA-Z0-9_ -]', '', datos_ia.get("demandado_imputado", "Desconocido"))
                            
                            caratula_ia = f"{dem_limpio} con {def_limpio}".strip()
                            # Crear carpeta en la nueva jerarquía de "NUEVOS"
                            cat_proc = "01_Expediente"
                            ruta_destino = DISCO_CASOS_RAIZ / f"[NUEVOS] {dem_limpio}" / f"[{rol_limpio}] {caratula_ia}" / cat_proc
                            print(f"      ✨ [IA ÉXITO] Identificado: ROL {rol_limpio} - {caratula_ia}")
                        else:
                            # Si la IA falla o no encuentra el ROL, a cuarentena
                            if any(jk in nombre_lower for jk in ["sentencia", "resolucion", "corte", "juzgado", "demanda", "querella", "absolucion", "alegato"]):
                                ruta_destino = DISCO_CASOS_RAIZ / "_Cuarentena_Para_Revisar_Abogado"
                            else:
                                continue # No es legal
                    else:
                        if any(jk in nombre_lower for jk in ["sentencia", "resolucion", "corte", "juzgado", "demanda", "querella", "absolucion", "alegato"]):
                            ruta_destino = DISCO_CASOS_RAIZ / "_Cuarentena_Para_Revisar_Abogado"
                        else:
                            continue # No es un documento legal de nuestros clientes

                ruta_destino.mkdir(parents=True, exist_ok=True)

                # Renombrar estandarizado
                fecha_mtime = datetime.fromtimestamp(ruta_orig.stat().st_mtime).strftime('%Y-%m-%d')
                nombre_limpio = re.sub(r'[^a-zA-Z0-9_.-]', '_', file)
                nuevo_nombre = f"{fecha_mtime}_{nombre_limpio}"
                ruta_final_archivo = ruta_destino / nuevo_nombre

                # Copiar archivo a la estructura consolidada
                try:
                    shutil.copy2(ruta_orig, ruta_final_archivo)
                    print(f"   ✅ [CLASIFICADO] {file} \n      --> {ruta_final_archivo.relative_to(DISCO_CASOS_RAIZ)}")
                    archivos_procesados += 1
                except Exception as e:
                    print(f"   ❌ Error copiando {file}: {e}")

    print("\n" + "="*80)
    print("🎉 ¡ORDENAMIENTO FORENSE DE 5 NIVELES FINALIZADO CON ÉXITO!")
    print(f"📂 Raíz Consolidada en : {DISCO_CASOS_RAIZ}")
    print(f"✅ Archivos Clasificados y Trasladados a Expedientes: {archivos_procesados - archivos_sin_causa}")
    print(f"🗂️ Archivos en Bandeja General de Cliente (Sin Rol): {archivos_sin_causa}")
    print(f"🗑️ Duplicados Exactos Ignorados/Deduplicados       : {archivos_duplicados}")
    print("="*80)

if __name__ == "__main__":
    clasificar_y_consolidar()
