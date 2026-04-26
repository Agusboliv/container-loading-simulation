"""
TERMINAL BAIRES — Matriz de impacto VD → VR.

Cada celda indica qué tipo de efecto produce una Variable de Decisión
sobre una Variable de Referencia: reduce, aumenta, justifica un costo,
o no tiene impacto directo.

Uso:
    python src/matriz_impacto.py

Genera: informe/assets/matriz_impacto.png
Dependencia: pip install matplotlib
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── Paleta ────────────────────────────────────────────────────────
C_VD_FILL = "#F5C4B3"
C_VD_TXT  = "#4A1B0C"
C_VR_MID  = "#5DCAA5"
C_VR_EDGE = "#0F6E56"
C_VR_TXT  = "#04342C"

# Color identificador de cada VD (rojo / azul / violeta)
VD_COLORS = ["#C0392B", "#1A6B8A", "#6B4C9A"]

# ── Datos ─────────────────────────────────────────────────────────
VD_LABELS = [
    "VD1\nCantidad de grúas",
    "VD2\nTarifa diferencial",
    "VD3\nMantenimiento\nde grúa",
]

VR_LABELS = [
    "VR1\nEspera\nantepuerto",
    "VR2\nEstadía\ntotal",
    "VR3\nUtilización\ngrúa",
    "VR4\nThroughput\npuerto",
    "VR5\nBarcos\nen cola",
    "VR6\nTiempo\nperdido",
]

# Tipos de impacto: (texto, color de fondo, color de texto)
NONE    = ("—",            "#F1EFE8", "#B4B2A9")
REDUCE  = ("↓ reduce",     "#FAEEDA", "#633806")
AUMENTA = ("↑ aumenta",    "#EAF3DE", "#173404")
MEJORA  = ("↑ mejora",     "#EAF3DE", "#173404")
COSTO   = ("$ justifica",  "#E6F1FB", "#042C53")

# Matriz: filas = VD, columnas = VR
IMPACTOS = [
    [REDUCE,  REDUCE, AUMENTA, AUMENTA, REDUCE, NONE  ],   # VD1 — Grúas
    [NONE,    NONE,   NONE,    NONE,    NONE,   COSTO ],   # VD2 — Tarifa
    [REDUCE,  NONE,   MEJORA,  NONE,    NONE,   REDUCE],   # VD3 — Mantenimiento
]


def main():
    OUT_DIR = Path("informe/assets")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH = OUT_DIR / "matriz_impacto.png"

    # ── Figura ────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 6), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Título y subtítulo
    ax.text(9, 7.5, "Matriz de impacto — VD → VR",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="#2C2C2A")
    ax.text(9, 7.0,
            "Cada celda indica qué efecto produce una Variable de Decisión "
            "sobre una Variable de Referencia",
            ha="center", va="center", fontsize=8.5, color="#5F5E5A")

    # Geometría de la grilla
    col_w, row_h = 2.3, 1.5
    x0, y0       = 2.8, 5.8
    header_h     = 0.9
    header_w     = 2.2

    # ── Headers superiores (VR) ──────────────────────────────────────
    for j, lbl in enumerate(VR_LABELS):
        xc = x0 + j * col_w + col_w / 2
        ax.add_patch(FancyBboxPatch(
            (x0 + j * col_w + 0.06, y0 - header_h + 0.06),
            col_w - 0.12, header_h - 0.08,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            fc=C_VR_MID, ec=C_VR_EDGE, lw=1.0, zorder=3))
        ax.text(xc, y0 - header_h / 2 + 0.03, lbl,
                ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=C_VR_TXT, zorder=4)

    # ── Filas: header VD + celdas de impacto ─────────────────────────
    for i, (vd_lbl, row) in enumerate(zip(VD_LABELS, IMPACTOS)):
        yc = y0 - header_h - i * row_h - row_h / 2

        # Header de fila (VD)
        ax.add_patch(FancyBboxPatch(
            (0.06, yc - row_h / 2 + 0.06),
            header_w - 0.12, row_h - 0.10,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            fc=C_VD_FILL, ec=VD_COLORS[i], lw=1.3, zorder=3))
        ax.text(header_w / 2, yc, vd_lbl,
                ha="center", va="center",
                fontsize=8, fontweight="bold", color=C_VD_TXT, zorder=4)

        # Punto identificador de color en la esquina del header
        ax.add_patch(FancyBboxPatch(
            (0.10, yc + row_h / 2 - 0.35), 0.22, 0.22,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            fc=VD_COLORS[i], ec="none", zorder=5))

        # Celdas de impacto
        for j, (txt, fc, tc) in enumerate(row):
            xc = x0 + j * col_w + col_w / 2
            ax.add_patch(FancyBboxPatch(
                (x0 + j * col_w + 0.06, yc - row_h / 2 + 0.06),
                col_w - 0.12, row_h - 0.10,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                fc=fc, ec="#D3D1C7", lw=0.8, zorder=3))
            ax.text(xc, yc, txt, ha="center", va="center",
                    fontsize=9, fontweight="bold", color=tc, zorder=4)

    # ── Render ───────────────────────────────────────────────────────
    plt.savefig(OUT_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Matriz guardada: {OUT_PATH}")


if __name__ == "__main__":
    main()
