#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LexControl - Puente de Sincronización Disco Real -> Web App
===========================================================
Escanea la jerarquía real en /media/jaime/.../Casos2023 y genera el catálogo
data/realDiskData.json, que el servidor local sirve a LexControl para que muestre
en el navegador los archivos reales de cada cliente y causa.
"""

import os
import sys
from pathlib import Path

APP_LEXCONTROL = Path("/home/jaime/Descargas/lex-control-casos")
sys.path.insert(0, str(APP_LEXCONTROL))
import catalogos  # noqa: E402  (necesita el sys.path de arriba)

DISCO_CASOS_RAIZ = Path("/media/jaime/c11cad3b-6d38-462a-9c2e-49c33f1f6c18/Casos2023")

if not DISCO_CASOS_RAIZ.exists():
    DISCO_CASOS_RAIZ = Path("/home/jaime/Descargas/Casos2023-Consolidados")

def escanear_disco_a_json():
    print(f"⚡ Escaneando árbol real en disco: {DISCO_CASOS_RAIZ}")
    
    estructura_clientes = []
    total_archivos = 0

    if not DISCO_CASOS_RAIZ.exists():
        print("❌ No se encontró la carpeta raíz en disco.")
        return

    # Iterar por carpetas de Cliente (Nivel A)
    for carpeta_cliente in sorted(DISCO_CASOS_RAIZ.iterdir()):
        if not carpeta_cliente.is_dir() or carpeta_cliente.name.startswith('.'):
            continue
        
        nombre_cliente_dir = carpeta_cliente.name
        # Extraer RUT si viene en formato [RUT] Nombre
        rut = "Sin RUT"
        nombre = nombre_cliente_dir
        if "[" in nombre_cliente_dir and "]" in nombre_cliente_dir:
            partes = nombre_cliente_dir.split("]", 1)
            rut = partes[0].replace("[", "").strip()
            nombre = partes[1].strip()

        datos_cliente = {
            "folderName": nombre_cliente_dir,
            "rut": rut,
            "nombre": nombre,
            "path": str(carpeta_cliente),
            "documentosGenerales": [],
            "causas": []
        }

        # Iterar dentro del cliente (Causas Nivel B o Bandeja General Nivel C)
        for sub_dir in sorted(carpeta_cliente.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name.startswith('.'):
                if sub_dir.is_file() and not sub_dir.name.startswith('.'):
                    # Archivos sueltos directamente bajo cliente
                    datos_cliente["documentosGenerales"].append({
                        "name": sub_dir.name,
                        "size": f"{round(sub_dir.stat().st_size / 1024, 1)} KB",
                        "path": str(sub_dir)
                    })
                    total_archivos += 1
                continue

            nombre_sub = sub_dir.name
            
            # Si es la bandeja general de documentos sin rol
            if "General" in nombre_sub or "Sin_Rol" in nombre_sub or "Sin Rol" in nombre_sub:
                for archivo in sorted(sub_dir.iterdir()):
                    if archivo.is_file() and not archivo.name.startswith('.'):
                        datos_cliente["documentosGenerales"].append({
                            "name": archivo.name,
                            "size": f"{round(archivo.stat().st_size / 1024, 1)} KB",
                            "path": str(archivo)
                        })
                        total_archivos += 1
            else:
                # Es una Causa / Expediente judicial
                rol = "Sin ROL"
                caratula = nombre_sub
                if "[" in nombre_sub and "]" in nombre_sub:
                    c_partes = nombre_sub.split("]", 1)
                    rol = c_partes[0].replace("[", "").strip()
                    caratula = c_partes[1].strip()

                datos_causa = {
                    "folderName": nombre_sub,
                    "rol": rol,
                    "caratula": caratula,
                    "path": str(sub_dir),
                    "categorias": [],
                    "totalArchivos": 0
                }

                # Categorías procesales dentro del expediente
                for cat_dir in sorted(sub_dir.iterdir()):
                    if cat_dir.is_dir() and not cat_dir.name.startswith('.'):
                        cat_items = []
                        for f in sorted(cat_dir.iterdir()):
                            if f.is_file() and not f.name.startswith('.'):
                                cat_items.append({
                                    "name": f.name,
                                    "size": f"{round(f.stat().st_size / 1024, 1)} KB",
                                    "path": str(f)
                                })
                                total_archivos += 1
                        
                        if cat_items:
                            datos_causa["categorias"].append({
                                "nombre": cat_dir.name,
                                "archivos": cat_items
                            })
                            datos_causa["totalArchivos"] += len(cat_items)
                    elif cat_dir.is_file() and not cat_dir.name.startswith('.'):
                        # Archivo directamente bajo la causa sin categoría
                        if not any(c["nombre"] == "00_General_Expediente" for c in datos_causa["categorias"]):
                            datos_causa["categorias"].append({"nombre": "00_General_Expediente", "archivos": []})
                        
                        datos_causa["categorias"][0]["archivos"].append({
                            "name": cat_dir.name,
                            "size": f"{round(cat_dir.stat().st_size / 1024, 1)} KB",
                            "path": str(cat_dir)
                        })
                        datos_causa["totalArchivos"] += 1
                        total_archivos += 1

                datos_cliente["causas"].append(datos_causa)

        if datos_cliente["causas"] or datos_cliente["documentosGenerales"]:
            estructura_clientes.append(datos_cliente)

    # Escribir el catálogo que sirve el servidor local a la app React
    destino = catalogos.guardar(catalogos.DISCO, {
        "totalArchivos": total_archivos,
        "raizDisco": str(DISCO_CASOS_RAIZ),
        "clientes": estructura_clientes,
    })

    print(f"✅ ¡Puente de datos exitoso! {len(estructura_clientes)} clientes y {total_archivos} archivos sincronizados en {destino}")

if __name__ == "__main__":
    escanear_disco_a_json()
