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

# ── Paleta ────────────────────────────────────────────────────────
C_BG           = "#FFFFFF"
C_START_END    = "#D3D1C7"
C_PROCESS      = "#E6F1FB"   # fondo actividades
C_PROCESS_EDG  = "#5DADE2"   # borde actividades
C_DECISION     = "#FAEEDA"
C_QUEUE        = "#FCE6E0"   # antepuerto
C_QUEUE_EDG    = "#C0392B"
C_RESOURCE     = "#F4FAFE"   # fondo cápsula recurso (muy claro)
C_RESOURCE_EDG = "#5DADE2"
C_EVENT        = "#FAD4CC"
C_MUELLE       = "#FBF1DA"
C_EDGE         = "#2C2C2A"
C_EVENT_EDG    = "#C0392B"
C_OK           = "#1D9E75"
C_MUELLE_EDG   = "#A8956A"

# ── Helper: nodo de actividad con cápsula de recurso arriba ──────
def actividad_html(recurso, actividad, detalle=None):
    """Genera HTML label con cápsula de recurso arriba y actividad abajo."""
    detalle_html = ""
    if detalle:
        detalle_html = (
            f'<BR/><FONT POINT-SIZE="10">{detalle}</FONT>'
        )
    return (
        f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="6" CELLPADDING="0">'
        # Celda superior: recurso
        f'<TR><TD>'
        f'<TABLE BORDER="1" CELLPADDING="5" CELLSPACING="0" '
        f'BGCOLOR="{C_RESOURCE}" COLOR="{C_RESOURCE_EDG}">'
        f'<TR><TD>'
        f'<FONT POINT-SIZE="9" COLOR="{C_RESOURCE_EDG}">'
        f'<I>{recurso}</I></FONT>'
        f'</TD></TR>'
        f'</TABLE>'
        f'</TD></TR>'
        # Celda inferior: actividad
        f'<TR><TD>'
        f'<TABLE BORDER="2" CELLPADDING="10" CELLSPACING="0" '
        f'BGCOLOR="{C_PROCESS}" COLOR="{C_PROCESS_EDG}">'
        f'<TR><TD>'
        f'<FONT POINT-SIZE="13"><B>{actividad}</B></FONT>'
        f'{detalle_html}'
        f'</TD></TR>'
        f'</TABLE>'
        f'</TD></TR>'
        f'</TABLE>>'
    )


def main():
    OUT_DIR = Path("informe/assets")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_NAME = "diagrama_proceso"

    # ── Grafo ─────────────────────────────────────────────────────────
    dot = Digraph("terminal_baires_proceso", format="png")
    dot.attr(rankdir="LR", bgcolor=C_BG, dpi="180", pad="0.5",
             nodesep="0.5", ranksep="0.8")
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
             "Antepuerto (cola FCFS)\nBarco informa datos\n(nº y ubic. de cont.)",
             shape="box", style="rounded,filled",
             fillcolor=C_QUEUE, color=C_QUEUE_EDG, penwidth="1.6",
             fontcolor=C_QUEUE_EDG)

    dot.node("dec_muelle", "¿Muelle\nlibre?",
             shape="diamond", style="filled", fillcolor=C_DECISION)
    dot.node("dec_clima", "¿Clima\napto?",
             shape="diamond", style="filled", fillcolor=C_DECISION)

    # ── Cluster del muelle con actividades como HTML ─────────────────
    with dot.subgraph(name="cluster_muelle") as c:
        c.attr(label="Recurso: Muelle (ocupado durante todo este tramo)",
               labelloc="t", labeljust="l",
               style="rounded,filled", fillcolor=C_MUELLE,
               color=C_MUELLE_EDG, fontname="Helvetica-Bold",
               fontsize="10", fontcolor="#5F4F2F", penwidth="1.5")

        c.node("amarre",
               actividad_html("Recurso: Práctico", "Amarre"),
               shape="plaintext")
        c.node("descarga",
               actividad_html("Recurso: Grúa", "Descarga",
                              "5–10 contenedores<BR/>(20% medios)"),
               shape="plaintext")
        c.node("carga",
               actividad_html("Recurso: Grúa", "Carga",
                              "10–15 contenedores<BR/>(20% medios)"),
               shape="plaintext")
        c.node("desamarre",
               actividad_html("Recurso: Práctico", "Desamarre"),
               shape="plaintext")

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

    # ── Eventos estocásticos (Falla de grúa primero) ─────────────────
    with dot.subgraph(name="cluster_eventos") as e:
        e.attr(label="Eventos estocásticos globales",
               style="dashed,rounded", color="#888888",
               fontname="Helvetica-Italic", fontsize="10",
               fontcolor="#555555")

        e.node("falla_evento",
               "Falla de grúa\n(≈15% del tiempo operativo)",
               shape="box", style="rounded,filled,dashed",
               fillcolor=C_EVENT, color=C_EVENT_EDG, fontsize="9")

        e.node("clima_evento",
               "Clima adverso\n(el puerto no opera)",
               shape="box", style="rounded,filled,dashed",
               fillcolor=C_EVENT, color=C_EVENT_EDG, fontsize="9")

    # Influencias (dashed, sin afectar layout)
    dot.edge("falla_evento", "descarga", style="dashed",
             color=C_EVENT_EDG, arrowhead="vee", arrowsize="0.6",
             label="interrumpe", fontcolor=C_EVENT_EDG,
             constraint="false")
    dot.edge("falla_evento", "carga", style="dashed",
             color=C_EVENT_EDG, arrowhead="vee", arrowsize="0.6",
             constraint="false")
    dot.edge("clima_evento", "dec_clima", style="dashed",
             color=C_EVENT_EDG, arrowhead="vee", arrowsize="0.6",
             label="condiciona", fontcolor=C_EVENT_EDG,
             constraint="false")

    # ── Render ────────────────────────────────────────────────────────
    out_path = dot.render(filename=OUT_NAME, directory=str(OUT_DIR),
                          cleanup=True)
    print(f"Diagrama guardado: {out_path}")


if __name__ == "__main__":
    main()
