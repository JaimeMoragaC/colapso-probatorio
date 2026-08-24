import sys
from auto_organizar_expedientes import extraer_caratula_ia

ruta = "/home/jaime/Descargas/017) 24-04 SENTENCIA RIT 84-2025.pdf"
print(f"Probando IA con: {ruta}")
res = extraer_caratula_ia(ruta)
print(f"Resultado:\n{res}")
