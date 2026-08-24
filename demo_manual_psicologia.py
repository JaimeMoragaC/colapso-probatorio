"""
DEMO EJECUTABLE: MANUAL DE PSICOLOGÍA PARA SALUD COMUNITARIA
Ejecuta las 4 fases fundamentales con simulación de datos y generación de gráficos.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Configurar estilo visual limpio
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

print("="*70)
print("  MANUAL DE PSICOLOGÍA COMUNITARIA: SUITE DE HERRAMIENTAS EJECUTABLES")
print("="*70)

# ------------------------------------------------------------------------------
# 1. DIAGNÓSTICO PSICOSOCIAL Y TAMIZAJE COMUNITARIO (PHQ-9 + COHESIÓN SOCIAL)
# ------------------------------------------------------------------------------
print("\n[ETAPA 1] EJECUTANDO DIAGNÓSTICO COMUNITARIO...")

def tamizaje_salud_mental_comunitaria(respuestas_phq9: list[int], cohesion_social_score: int):
    total_phq9 = sum(respuestas_phq9)
    if total_phq9 <= 4:
        nivel_depresion = "Mínimo / Sin síntomas"
        accion = "Promoción general de salud y bienestar comunitario."
    elif total_phq9 <= 9:
        nivel_depresion = "Leve"
        accion = "Psicoeducación comunitaria y talleres de manejo del estrés."
    elif total_phq9 <= 14:
        nivel_depresion = "Moderado"
        accion = "Intervención grupal comunitaria y seguimiento en APS."
    elif total_phq9 <= 19:
        nivel_depresion = "Moderadamente Severo"
        accion = "Derivación a evaluación clínica individual / Salud Mental."
    else:
        nivel_depresion = "Severo"
        accion = "Intervención inmediata, triaje clínico y evaluación de riesgo vital."
        
    vulnerabilidad = ((total_phq9 / 27) * 0.7 + ((10 - cohesion_social_score) / 10) * 0.3) * 100
    return {
        "puntaje_phq9": total_phq9,
        "severidad_clinica": nivel_depresion,
        "cohesion_percibida": f"{cohesion_social_score}/10",
        "indice_vulnerabilidad": round(vulnerabilidad, 1),
        "accion_sugerida": accion
    }

# Simular muestra de 10 participantes de una junta vecinal
np.random.seed(42)
participantes = [f"Vecino {i+1}" for i in range(10)]
datos_tamizaje = []
for p in participantes:
    # 9 preguntas con valores de 0 a 3
    phq = list(np.random.choice([0, 1, 2, 3], size=9, p=[0.4, 0.3, 0.2, 0.1]))
    cohesion = int(np.random.randint(2, 10))
    res = tamizaje_salud_mental_comunitaria(phq, cohesion)
    res["Participante"] = p
    datos_tamizaje.append(res)

df_tamizaje = pd.DataFrame(datos_tamizaje)[["Participante", "puntaje_phq9", "severidad_clinica", "cohesion_percibida", "indice_vulnerabilidad", "accion_sugerida"]]
print(df_tamizaje.to_string(index=False))


# ------------------------------------------------------------------------------
# 2. SOCIOGRAMA Y MAPEO DE REDES DE APOYO (NetworkX)
# ------------------------------------------------------------------------------
print("\n" + "-"*70)
print("[ETAPA 2] GENERANDO SOCIOGRAMA Y MAPEO DE REDES...")

relaciones_comunitarias = [
    ("Lidia (Líder)", "Carlos (Punto Vecinal)"),
    ("Lidia (Líder)", "Marta (Club Adulto Mayor)"),
    ("Lidia (Líder)", "Andrés (Comedor)"),
    ("Carlos (Punto Vecinal)", "Marta (Club Adulto Mayor)"),
    ("Carlos (Punto Vecinal)", "Esteban"),
    ("Carlos (Punto Vecinal)", "Sofia"),
    ("Marta (Club Adulto Mayor)", "Rosa"),
    ("Rosa", "Pedro"),
    ("Andrés (Comedor)", "Esteban"),
    ("Rosa", "Jorge (Aislado)"),
    ("Clara (Aislada)", "Marta (Club Adulto Mayor)")
]

G = nx.Graph()
G.add_edges_from(relaciones_comunitarias)

grados = dict(G.degree())
intermediacion = nx.betweenness_centrality(G)

lideres = sorted(grados.items(), key=lambda x: x[1], reverse=True)[:2]
aislados = [nodo for nodo, grado in grados.items() if grado <= 1]

print(f"• Total participantes en la red: {G.number_of_nodes()}")
print(f"• Densidad de conectividad comunitaria: {nx.density(G):.2f}")
print(f"• Líderes de articulación comunitaria (Mayor Grado): {[l[0] for l in lideres]}")
print(f"• Nodos en riesgo de desconexión / aislamiento: {aislados}")

# Generar gráfico visual del Sociograma
plt.figure(figsize=(9, 6), dpi=150)
pos = nx.spring_layout(G, seed=42, k=0.9)

colores = []
for nodo in G.nodes():
    if nodo in [l[0] for l in lideres]:
        colores.append('#2ecc71') # Verde (Líder)
    elif nodo in aislados:
        colores.append('#e74c3c') # Rojo (Riesgo de Aislamiento)
    else:
        colores.append('#3498db') # Azul (Conectado)

nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=1200, alpha=0.9)
nx.draw_networkx_edges(G, pos, width=2, edge_color='#7f8c8d', alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", font_family="sans-serif")

# Leyenda manual
plt.plot([0], [0], marker='o', markersize=10, color='#2ecc71', label='Líderes Clave (Articuladores)', linestyle='None')
plt.plot([0], [0], marker='o', markersize=10, color='#3498db', label='Vecinos Integrados', linestyle='None')
plt.plot([0], [0], marker='o', markersize=10, color='#e74c3c', label='Riesgo de Aislamiento', linestyle='None')
plt.legend(loc='upper left', frameon=True)
plt.title("Sociograma de Apoyo Social Comunitario\nIdentificación de Redes y Vulnerabilidad de Vínculos", fontsize=12, fontweight='bold', pad=15)
plt.axis('off')
plt.tight_layout()

sociograma_path = "sociograma_comunitario.png"
plt.savefig(sociograma_path)
plt.close()
print(f"-> Gráfico guardado exitosamente en: {sociograma_path}")


# ------------------------------------------------------------------------------
# 3. TRIAJE Y PRIMEROS AUXILIOS PSICOLÓGICOS (PAP)
# ------------------------------------------------------------------------------
print("\n" + "-"*70)
print("[ETAPA 3] ÁRBOL DE DECISIÓN: PRIMEROS AUXILIOS PSICOLÓGICOS (PAP)")

def algoritmo_pap(seguridad_fisica: bool, desborde_emocional: bool, necesidades_basicas: bool, red_apoyo: bool):
    if not seguridad_fisica:
        return ["🚨 DETENER: Riesgo en entorno físico. Priorizar seguridad antes de abordaje verbal."]
    
    acciones = []
    if desborde_emocional:
        acciones.append("1. FASE DE CALMA: Contacto visual sereno, tono pausado, respiración diafragmática 4-4-4.")
    else:
        acciones.append("1. FASE DE ESCUCHA: Escucha activa no invasiva, normalizar respuestas adaptativas.")
        
    if not necesidades_basicas:
        acciones.append("2. FASE DE FOCALIZACIÓN: Gestionar de inmediato agua, abrigo, acceso a información verídica.")
    else:
        acciones.append("2. FASE DE FOCALIZACIÓN: Identificar prioridades inmediatas expresadas por la persona.")
        
    if not red_apoyo:
        acciones.append("3. FASE DE CONEXIÓN: Activar red local comunitaria / vincular con facilitador vecinal o APS.")
    else:
        acciones.append("3. FASE DE CONEXIÓN: Facilitar contacto telefónico/físico con su círculo primario.")
        
    acciones.append("4. SEGUIMIENTO: Entregar pauta escrita de autocuidado y fijar contacto en 48 hrs.")
    return acciones

caso_1 = algoritmo_pap(seguridad_fisica=True, desborde_emocional=True, necesidades_basicas=False, red_apoyo=False)
print("Caso Simulador: Persona desbordada emocionalmente, sin necesidades básicas ni red de apoyo:")
for paso in caso_1:
    print(f"   {paso}")


# ------------------------------------------------------------------------------
# 4. EVALUACIÓN DE IMPACTO PRE/POST (D DE COHEN + VISUALIZACIÓN)
# ------------------------------------------------------------------------------
print("\n" + "-"*70)
print("[ETAPA 4] EVALUACIÓN DE IMPACTO DEL PROGRAMA (PRE vs POST TALLER)")

def evaluacion_impacto(pre, post):
    pre_arr = np.array(pre)
    post_arr = np.array(post)
    diff = post_arr - pre_arr
    n1, n2 = len(pre_arr), len(post_arr)
    s_pooled = np.sqrt(((n1 - 1) * np.var(pre_arr, ddof=1) + (n2 - 1) * np.var(post_arr, ddof=1)) / (n1 + n2 - 2))
    d = np.mean(diff) / s_pooled if s_pooled != 0 else 0
    return np.mean(pre_arr), np.mean(post_arr), np.mean(diff), d

# Puntajes de bienestar comunitario en 12 participantes (Escala 0-30)
pre_taller = [12, 14, 11, 15, 13, 10, 12, 16, 11, 14, 13, 15]
post_taller = [20, 22, 18, 24, 21, 19, 20, 25, 17, 23, 21, 24]

m_pre, m_post, m_diff, d_cohen = evaluacion_impacto(pre_taller, post_taller)

print(f"• Media Pre-Intervención: {m_pre:.2f} pts")
print(f"• Media Post-Intervención: {m_post:.2f} pts")
print(f"• Incremento promedio: +{m_diff:.2f} pts")
print(f"• Tamaño del Efecto (d de Cohen): {d_cohen:.2f} (Efecto Grande / Alto Impacto Comunitario)")

# Generar gráfico de impacto Pre vs Post
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
x = np.arange(len(pre_taller))
width = 0.35

ax.bar(x - width/2, pre_taller, width, label='Pre-Intervención', color='#95a5a6', alpha=0.85)
ax.bar(x + width/2, post_taller, width, label='Post-Intervención', color='#2ecc71', alpha=0.9)

ax.set_ylabel('Puntaje de Bienestar Psicosocial (0-30)', fontsize=11)
ax.set_xlabel('Participantes del Taller Comunitario', fontsize=11)
ax.set_title(f'Evaluación de Impacto Pre vs Post Intervención\nGanancia Promedio: +{m_diff:.1f} pts | Tamaño del Efecto d = {d_cohen:.2f}', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"P{i+1}" for i in range(len(pre_taller))])
ax.legend(frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
impacto_path = "grafico_impacto_intervencion.png"
plt.savefig(impacto_path)
plt.close()
print(f"-> Gráfico de impacto guardado en: {impacto_path}")

print("\n" + "="*70)
print("  EJECUCIÓN COMPLETADA CON ÉXITO")
print("="*70)
