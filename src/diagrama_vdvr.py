"""
TERMINAL BAIRES — Diagrama de Variables de Decisión y de Referencia.

Muestra la arquitectura de análisis del sistema:
    Sistema  →  Variables de Decisión (VD)  →  Variables de Referencia (VR)

Cada VD tiene un color identificatorio. Las flechas punteadas indican qué
VR se ven afectadas por cada VD (la matriz de impacto vive en otro script).

Uso:
    python src/diagrama_vdvr.py

Genera: informe/assets/diagrama_vdvr.png
Dependencia: pip install matplotlib
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── Paleta ────────────────────────────────────────────────────────
C_GRAY_FILL = "#D3D1C7"
C_GRAY_TXT  = "#2C2C2A"

C_VD_HDR    = "#F0997B"
C_VD_FILL   = "#F5C4B3"
C_VD_EDGE   = "#D85A30"
C_VD_TXT    = "#4A1B0C"

C_VR_HDR    = "#5DCAA5"
C_VR_LIGHT  = "#9FE1CB"
C_VR_MID    = "#5DCAA5"
C_VR_DARK   = "#1D9E75"
C_VR_EDGE   = "#0F6E56"
C_VR_TXT    = "#04342C"
C_VR_DTXT   = "#E1F5EE"

# Color identificador de cada VD (rojo / azul / violeta)
VD_COLORS = ["#C0392B", "#1A6B8A", "#6B4C9A"]

# ── Datos del modelo ──────────────────────────────────────────────
VD_DATA = [
    ("VD1 — Cantidad de grúas",     "1 grúa actual  vs.  2 grúas simultáneas"),
    ("VD2 — Tarifa diferencial",    "Cargo extra por medio-contenedor"),
    ("VD3 — Mantenimiento de grúa", "Reducir fallas del 15% con prev."),
]

VR_DATA = [
    # (etiqueta, sublabel, color de fondo, color de texto)
    ("VR1 — Espera en antepuerto",    "Tiempo hasta acceso al muelle",   C_VR_LIGHT, C_VR_TXT),
    ("VR2 — Estadía total del barco", "Desde llegada hasta partida",     C_VR_LIGHT, C_VR_TXT),
    ("VR3 — Utilización de la grúa",  "% tiempo operativa vs. total",    C_VR_MID,   C_VR_TXT),
    ("VR4 — Throughput del puerto",   "Barcos y contenedores por mes",   C_VR_MID,   C_VR_TXT),
    ("VR5 — Barcos en cola",          "Promedio y máximo en antepuerto", C_VR_MID,   C_VR_TXT),
    ("VR6 — Tiempo perdido/fallas",   "Impacto del 15% de paradas",      C_VR_DARK,  C_VR_DTXT),
]

# Relaciones VD → VR: (índice VD, índice VR, curvatura de la flecha)
RELS = [
    (0, 0,  0.00), (0, 1,  0.04), (0, 2, -0.04),
    (0, 3,  0.06), (0, 4,  0.09),
    (1, 5,  0.00),
    (2, 0, -0.09), (2, 2,  0.00), (2, 5,  0.06),
]

# ── Helpers de dibujo ─────────────────────────────────────────────
def box(ax, x, y, w, h, label, sublabel=None,
        fc="#fff", ec="#999", tc="#000", tc2="#555",
        r=0.15, fs=9.5, fs2=8):
    """Dibuja una caja redondeada con etiqueta principal y opcional sublabel."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={r}",
                       fc=fc, ec=ec, lw=1.3, zorder=3)
    ax.add_patch(p)
    if sublabel:
        ax.text(x, y + 0.14, label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=tc, zorder=4)
        ax.text(x, y - 0.19, sublabel, ha="center", va="center",
                fontsize=fs2, color=tc2, zorder=4)
    else:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=tc, zorder=4)


def arrow(ax, x1, y1, x2, y2, color="#888", lw=1.1, ls="--", rad=0.0):
    """Dibuja una flecha entre dos puntos, opcionalmente curvada."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=2)


def main():
    OUT_DIR = Path("informe/assets")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH = OUT_DIR / "diagrama_vdvr.png"

    # ── Figura ────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 13)
    ax.axis("off")

    # Coordenadas del layout
    X_SYS, X_VD, X_VR = 2.2, 7.2, 16.5
    BW_SYS, BH_SYS = 3.4, 1.0
    BW_HDR, BH_HDR = 4.4, 0.8
    BW_VD,  BH_VD  = 4.4, 0.8
    BW_VR,  BH_VR  = 4.8, 0.8

    Y_SYS = 6.5
    Y_VD_HDR = 11.5
    Y_VR_HDR = 11.5
    Y_VDs = [9.2, 6.5, 3.8]
    Y_VRs = [9.8, 8.5, 7.2, 5.9, 4.6, 3.3]

    # ── Sistema central ──────────────────────────────────────────────
    box(ax, X_SYS, Y_SYS, BW_SYS, BH_SYS,
        "TERMINAL BAIRES", "Puerto de contenedores, La Plata",
        fc=C_GRAY_FILL, ec="#888780", tc=C_GRAY_TXT, tc2="#5F5E5A")

    # ── Headers VD y VR ──────────────────────────────────────────────
    box(ax, X_VD, Y_VD_HDR, BW_HDR, BH_HDR,
        "VARIABLES DE DECISIÓN", "¿Qué puede cambiar el administrador?",
        fc=C_VD_HDR, ec=C_VD_EDGE, tc=C_VD_TXT, tc2=C_VD_TXT)

    box(ax, X_VR, Y_VR_HDR, BW_HDR, BH_HDR,
        "VARIABLES DE REFERENCIA", "¿Cómo medir el desempeño?",
        fc=C_VR_HDR, ec=C_VR_EDGE, tc=C_VR_TXT, tc2=C_VR_TXT)

    # ── Cajas de cada VD ─────────────────────────────────────────────
    for i, ((lbl, sub), y) in enumerate(zip(VD_DATA, Y_VDs)):
        box(ax, X_VD, y, BW_VD, BH_VD, lbl, sub,
            fc=C_VD_FILL, ec=VD_COLORS[i], tc=C_VD_TXT, tc2="#7B3010")
        # Punto de color con número (1/2/3) a la izquierda de la caja
        dot_patch = FancyBboxPatch((X_VD - BW_VD / 2 + 0.08, y - 0.14), 0.28, 0.28,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             fc=VD_COLORS[i], ec="none", zorder=5)
        ax.add_patch(dot_patch)
        ax.text(X_VD - BW_VD / 2 + 0.22, y, str(i + 1),
                ha="center", va="center", fontsize=7, fontweight="bold",
                color="white", zorder=6)

    # ── Cajas de cada VR ─────────────────────────────────────────────
    for (lbl, sub, fc, tc), y in zip(VR_DATA, Y_VRs):
        box(ax, X_VR, y, BW_VR, BH_VR, lbl, sub,
            fc=fc, ec=C_VR_EDGE, tc=tc, tc2=tc)

    # ── Flechas de estructura: Sistema → Headers ─────────────────────
    arrow(ax, X_SYS + BW_SYS / 2, Y_SYS + 0.25, X_VD - BW_HDR / 2, Y_VD_HDR,
          color=C_VD_EDGE, lw=1.6, ls="-")
    arrow(ax, X_SYS + BW_SYS / 2, Y_SYS - 0.25, X_VR - BW_VR / 2, Y_VR_HDR,
          color=C_VR_EDGE, lw=1.6, ls="-")

    # ── Flechas Sistema → cada VD (línea sólida, "control") ─────────
    for y in Y_VDs:
        arrow(ax, X_SYS + BW_SYS / 2, Y_SYS, X_VD - BW_VD / 2, y,
              color=C_VD_EDGE, lw=1.0, ls="-")

    # ── Flechas VD → VR (línea punteada, "impacto") ─────────────────
    for vd_i, vr_i, rad in RELS:
        arrow(ax, X_VD + BW_VD / 2, Y_VDs[vd_i],
                  X_VR - BW_VR / 2, Y_VRs[vr_i],
              color=VD_COLORS[vd_i], lw=1.2, ls="--", rad=rad)

    # ── Leyenda inferior: colores de flechas ─────────────────────────
    lx, ly = 10.5, 1.2
    ax.text(lx, ly + 0.5, "Color de flechas:", fontsize=8,
            color="#2C2C2A", fontweight="bold", va="center")
    for i, (col, (lbl, _)) in enumerate(zip(VD_COLORS, VD_DATA)):
        xi = lx + i * 3.6
        ax.annotate("", xy=(xi + 0.7, ly), xytext=(xi, ly),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5,
                                    linestyle="--"))
        ax.text(xi + 0.8, ly, lbl.split("—")[1].strip(),
                fontsize=7.5, color=col, va="center", fontweight="bold")

    # ── Leyenda inferior izquierda: tipo de caja (VD / VR) ──────────
    for i, (fc, ec, lbl) in enumerate([
        (C_VD_FILL, C_VD_EDGE, "Variable de Decisión (VD)"),
        (C_VR_MID,  C_VR_EDGE, "Variable de Referencia (VR)"),
    ]):
        lx2, ly2 = 0.3, 0.85 - i * 0.38
        ax.add_patch(FancyBboxPatch((lx2, ly2), 0.38, 0.24,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=fc, ec=ec, lw=1.0))
        ax.text(lx2 + 0.50, ly2 + 0.12, lbl, fontsize=8, va="center",
                color="#2C2C2A")

    # ── Línea separadora y título ────────────────────────────────────
    ax.axhline(1.05, xmin=0.01, xmax=0.99, color="#D3D1C7", lw=0.8)
    ax.text(11, 12.6, "TERMINAL BAIRES — Variables de Referencia y Decisión",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color="#2C2C2A")

    # ── Render ───────────────────────────────────────────────────────
    plt.savefig(OUT_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Diagrama guardado: {OUT_PATH}")


if __name__ == "__main__":
    main()
