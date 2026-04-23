"""
TERMINAL BAIRES — Diagrama de proceso
Flujo operativo de un barco en el puerto de La Plata.

Genera: informe/assets/diagrama_proceso.png

Dependencias:
    - Binario Graphviz instalado en el sistema (apt, brew, winget).
    - pip install graphviz
"""

from graphviz import Digraph
from pathlib import Path

# ── Config de salida ──────────────────────────────────────────────
OUT_DIR = Path("informe/assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_NAME = "diagrama_proceso"

# ── Paleta ────────────────────────────────────────────────────────
C_BG         = "#FFFFFF"
C_START_END  = "#D3D1C7"
C_PROCESS    = "#E6F1FB"
C_DECISION   = "#FAEEDA"
C_QUEUE      = "#F5C4B3"
C_EVENT      = "#FAD4CC"
C_MUELLE     = "#F0E6D2"
C_EDGE       = "#2C2C2A"
C_EVENT_EDG  = "#C0392B"
C_OK         = "#1D9E75"
C_MUELLE_EDG = "#A8956A"

# ── Grafo ─────────────────────────────────────────────────────────
dot = Digraph("terminal_baires_proceso", format="png")
dot.attr(rankdir="LR", bgcolor=C_BG, dpi="180", pad="0.4",
         nodesep="0.45", ranksep="0.75")
dot.attr("node", fontname="Helvetica", fontsize="11",
         color=C_EDGE, penwidth="1.3")
dot.attr("edge", fontname="Helvetica", fontsize="9", color=C_EDGE)

# Título
dot.attr(label=("<<B>TERMINAL BAIRES — Diagrama de proceso</B><BR/>"
                "<FONT POINT-SIZE='10'>Flujo operativo de un barco en el puerto</FONT>>"),
         labelloc="t", fontname="Helvetica", fontsize="14")

# ── Nodos del flujo principal ─────────────────────────────────────
dot.node("llegada",
         "Barco llega\n(≈10 barcos/mes)",
         shape="oval", style="filled", fillcolor=C_START_END)

dot.node("antepuerto",
         "Antepuerto (cola FIFO)\nBarco informa datos\n(nº y ubicación de cont.)",
         shape="box3d", style="filled", fillcolor=C_QUEUE)

dot.node("dec_muelle",
         "¿Muelle\nlibre?",
         shape="diamond", style="filled", fillcolor=C_DECISION)

dot.node("dec_clima",
         "¿Clima\napto?",
         shape="diamond", style="filled", fillcolor=C_DECISION)

# ── Cluster del muelle ────────────────────────────────────────────
with dot.subgraph(name="cluster_muelle") as c:
    c.attr(label="Recurso: Muelle (ocupado durante todo este tramo)",
           labelloc="t", style="rounded,filled", fillcolor=C_MUELLE,
           color=C_MUELLE_EDG, fontname="Helvetica-Bold",
           fontsize="10", fontcolor="#5F4F2F", penwidth="1.5")

    c.node("amarre",
           "Amarre\n[Recurso: Práctico]",
           shape="box", style="rounded,filled", fillcolor=C_PROCESS)

    c.node("descarga",
           "Descarga\n[Recurso: Grúa]\n5–10 contenedores\n(20% medios)",
           shape="box", style="rounded,filled", fillcolor=C_PROCESS)

    c.node("carga",
           "Carga\n[Recurso: Grúa]\n10–15 contenedores\n(20% medios)",
           shape="box", style="rounded,filled", fillcolor=C_PROCESS)

    c.node("desamarre",
           "Desamarre\n[Recurso: Práctico]",
           shape="box", style="rounded,filled", fillcolor=C_PROCESS)

dot.node("partida", "Barco parte", shape="oval",
         style="filled", fillcolor=C_START_END)

# ── Flujo principal ───────────────────────────────────────────────
dot.edge("llegada", "antepuerto")
dot.edge("antepuerto", "dec_muelle")
dot.edge("dec_muelle", "dec_clima", label="SÍ", fontcolor=C_OK)
dot.edge("dec_clima", "amarre", label="SÍ", fontcolor=C_OK)
dot.edge("amarre", "descarga")
dot.edge("descarga", "carga")
dot.edge("carga", "desamarre")
dot.edge("desamarre", "partida")

# ── Retornos NO ───────────────────────────────────────────────────
dot.edge("dec_muelle", "antepuerto", label="NO",
         fontcolor=C_EVENT_EDG, color=C_EVENT_EDG,
         constraint="false", style="dashed")
dot.edge("dec_clima", "antepuerto", label="NO",
         fontcolor=C_EVENT_EDG, color=C_EVENT_EDG,
         constraint="false", style="dashed")

# ── Eventos estocásticos ──────────────────────────────────────────
with dot.subgraph(name="cluster_eventos") as e:
    e.attr(label="Eventos estocásticos globales",
           style="dashed,rounded", color="#888888",
           fontname="Helvetica-Bold", fontsize="10",
           fontcolor="#555555")

    e.node("clima_evento",
           "Clima adverso\n(el puerto no opera)",
           shape="box", style="rounded,filled,dashed",
           fillcolor=C_EVENT)

    e.node("falla_evento",
           "Falla de grúa\n(≈15% del tiempo\noperativo)",
           shape="box", style="rounded,filled,dashed",
           fillcolor=C_EVENT)

# Influencias (no afectan layout)
dot.edge("clima_evento", "dec_clima", style="dotted",
         color=C_EVENT_EDG, arrowhead="none",
         label="condiciona", fontcolor=C_EVENT_EDG,
         constraint="false")
dot.edge("falla_evento", "descarga", style="dotted",
         color=C_EVENT_EDG, arrowhead="none",
         label="interrumpe", fontcolor=C_EVENT_EDG,
         constraint="false")
dot.edge("falla_evento", "carga", style="dotted",
         color=C_EVENT_EDG, arrowhead="none",
         constraint="false")

# Nota: no usamos rank=same ni edges invisibles para posicionar el
# cluster de eventos. Graphviz lo ubicará naturalmente abajo cuando
# las flechas de influencia (constraint=false) no fuercen su posición.

# ── Render ────────────────────────────────────────────────────────
out_path = dot.render(filename=OUT_NAME, directory=str(OUT_DIR),
                      cleanup=True)
print(f"Diagrama guardado: {out_path}")
