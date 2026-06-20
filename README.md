# TP2 — Simulación Terminal Baires

Integrantes:
- Bolivar, Agustin
- Martinez Folica, Nazareno

## Cómo correr

- **El proyecto = la simulación:** `notebooks/Terminal_Baires_Simulacion.ipynb` (SimPy, reproducible de punta a punta).
- **Regenerar los diagramas del informe (auxiliar):** `python scripts/generar.py` → escribe los `.png` en `informe/assets/`.

Dependencias: `pip install -r requirements.txt`

## Estructura

```
TP2/
├── requirements.txt
├── notebooks/              # ← el proyecto: simulación completa (SimPy)
│   └── Terminal_Baires_Simulacion.ipynb
├── data/                   # datos crudos (tb_*.csv)
├── informe/                # informe .docx, consigna y assets (diagramas .png)
├── scripts/                # auxiliar: generan los diagramas conceptuales del informe
│   ├── generar.py          # corre los tres scripts de abajo
│   ├── diagrama_proceso.py
│   ├── diagrama_vdvr.py
│   └── matriz_impacto.py
└── docs/                   # sitio de GitHub Pages
    ├── index.html
    ├── assets/             # figuras del sitio (fig_*.png)
    └── sim_web/            # simulador interactivo en HTML
```

## GitHub Pages

El sitio se sirve desde la carpeta `docs/`. En GitHub: **Settings → Pages → Source → Deploy from a branch → carpeta `/docs`**.
