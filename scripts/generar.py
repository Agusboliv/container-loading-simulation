"""Genera los diagramas conceptuales del informe en informe/assets/.

Uso (desde la raíz del proyecto o desde cualquier lado):
    python scripts/generar.py

El proyecto en sí es la simulación del notebook
(notebooks/Terminal_Baires_Simulacion.ipynb); estos scripts solo producen
las figuras conceptuales que acompañan al informe.
"""
from diagrama_proceso import main as diagrama_proceso
from diagrama_vdvr import main as diagrama_vdvr
from matriz_impacto import main as matriz_impacto

if __name__ == "__main__":
    diagrama_proceso()
    diagrama_vdvr()
    matriz_impacto()
