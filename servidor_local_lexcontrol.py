#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LexControl - Servidor Lanzador Forense y Gestor de Archivos Locales
===================================================================
Servidor HTTP ligero en Python (Puerto 8888) que permite a la aplicación web
React abrir archivos directamente en el escritorio Linux (mediante xdg-open)
o servirlos para su visualización en pestañas del navegador.
"""

import os
import sys
import urllib.parse
import mimetypes
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PUERTO = 8888
HOST = "localhost"

class LexControlFileHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # ENDPOINT 1: /abrir?ruta=/path/al/archivo.pdf (Abre en escritorio Linux nativo)
        if parsed_url.path == "/abrir":
            ruta = query_params.get("ruta", [""])[0]
            if not ruta or not os.path.exists(ruta):
                self.send_response(404)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Archivo no encontrado en disco"}')
                return

            try:
                # Ejecutar orden nativa de apertura en Linux (xdg-open)
                subprocess.Popen(["xdg-open", ruta], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok", "message": "Abierto en escritorio Linux"}')
                print(f"🖥️ [DESCRITORIO LINUX] Abierto nativo: {ruta}")
            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode('utf-8'))

        # ENDPOINT 2: /ver?ruta=/path/al/archivo.pdf (Sirve bytes para ver en pestaña web)
        elif parsed_url.path == "/ver":
            ruta = query_params.get("ruta", [""])[0]
            if not ruta or not os.path.exists(ruta):
                self.send_response(404)
                self._send_cors_headers()
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Error 404: Archivo judicial no encontrado en disco.")
                return

            try:
                mime_type, _ = mimetypes.guess_type(ruta)
                if not mime_type:
                    mime_type = "application/octet-stream"

                with open(ruta, "rb") as f:
                    contenido = f.read()

                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Length", str(len(contenido)))
                self.send_header("Content-Disposition", f'inline; filename="{os.path.basename(ruta)}"')
                self.end_headers()
                self.wfile.write(contenido)
                print(f"🌐 [NAVEGADOR WEB] Servido en pestaña: {os.path.basename(ruta)}")
            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(f"Error sirviendo archivo: {str(e)}".encode('utf-8'))

        # ENDPOINT 3: /sincronizar_ojv (Forzar ejecución del Motor OJV con ventana visible en tu escritorio)
        elif parsed_url.path == "/sincronizar_ojv":
            try:
                print("⚡ [SINCRONIZACIÓN VISIBLE OJV] Abriendo ventana de tu navegador en el escritorio para login y control seguro...")
                subprocess.Popen(["python3", "/home/jaime/Descargas/colapso-probatorio/motor_ojv_diferencial.py", "--login-humano"])
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok", "message": "Ventana judicial abierta en tu escritorio. Ingresa tranquilamente con tu clave."}')
            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode('utf-8'))

        # ENDPOINT 4: /login_humano (Abrir ventana visible para Opción A)
        elif parsed_url.path == "/login_humano":
            try:
                print("🔑 [OPCIÓN A] Abriendo Chromium visible para login y resolución de CAPTCHA...")
                subprocess.Popen(["python3", "/home/jaime/Descargas/colapso-probatorio/motor_ojv_diferencial.py", "--login-humano"])
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok", "message": "Ventana interactiva abierta en el escritorio Linux"}')
            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode('utf-8'))

        # ENDPOINT 5: /status (Verificación de salud del puente)
        elif parsed_url.path == "/status" or parsed_url.path == "/":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "activo", "motor": "LexControl File Launcher v2.2 (Opcion A)", "puerto": 8888}')

        else:
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()

    def log_message(self, format, *args):
        # Silenciar logs ruidosos para no saturar terminal
        pass

def iniciar_servidor():
    print("="*75)
    print(f"⚡ SERVIDOR LANZADOR FORENSE LEXCONTROL INICIADO EN http://{HOST}:{PUERTO}")
    print("👉 Listo para abrir tus 17.742 archivos en tu escritorio Linux nativo.")
    print("="*75)
    servidor = HTTPServer((HOST, PUERTO), LexControlFileHandler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor lanzador detenido por el usuario.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()
