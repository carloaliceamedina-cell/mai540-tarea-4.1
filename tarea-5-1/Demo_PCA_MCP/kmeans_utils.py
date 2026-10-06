"""
Lógica de negocio de la segmentación con K-Means (Tarea 5.2). Igual que pca_utils.py,
este archivo no sabe que existe MCP: mcp_server.py solo lo envuelve con un decorador.

Reutiliza la validación de nombres de pca_utils (solo CSV dentro de datasets/), así la
nueva tool hereda el mismo permiso mínimo que se corrigió en la Tarea 5.1.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

import pca_utils

SEMILLA = 42


def cargar_y_escalar(nombre: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    """Carga el dataset (solo desde datasets/) y estandariza sus columnas numéricas."""
    df = pca_utils.cargar_dataset(nombre)          # valida el nombre contra la lista blanca
    numericas = df.select_dtypes(include="number").columns.tolist()
    if not numericas:
        raise ValueError(f"'{nombre}' no tiene columnas numéricas para segmentar.")
    df = df.dropna(subset=numericas).reset_index(drop=True)
    X = StandardScaler().fit_transform(df[numericas])
    return df, X, numericas


def ejecutar_kmeans(nombre: str, k: int) -> dict:
    """K-Means con k grupos: etiquetas, tamaños, inercia, silueta y perfil medio por grupo."""
    df, X, numericas = cargar_y_escalar(nombre)
    if k < 2 or k >= len(df):
        raise ValueError(f"k debe estar entre 2 y {len(df) - 1} (filas de '{nombre}').")
    modelo = KMeans(n_clusters=k, n_init=10, random_state=SEMILLA).fit(X)
    etiquetas = modelo.labels_
    perfil = df[numericas].groupby(etiquetas).mean().round(3)
    return {
        "dataset": nombre,
        "k": k,
        "filas_usadas": len(df),
        "etiquetas": [int(e) for e in etiquetas],
        "tamano_por_grupo": {f"grupo_{g}": int(n) for g, n in zip(*np.unique(etiquetas, return_counts=True))},
        "inercia": round(float(modelo.inertia_), 3),
        "silueta": round(float(silhouette_score(X, etiquetas)), 4),
        "perfil_medio_por_grupo": {f"grupo_{g}": perfil.loc[g].to_dict() for g in perfil.index},
    }


def evaluar_k(nombre: str, k_min: int = 2, k_max: int = 8) -> pd.DataFrame:
    """Inercia (método del codo) y silueta para cada k en [k_min, k_max]."""
    _, X, _ = cargar_y_escalar(nombre)
    filas = []
    for k in range(k_min, k_max + 1):
        m = KMeans(n_clusters=k, n_init=10, random_state=SEMILLA).fit(X)
        filas.append({"k": k, "inercia": round(float(m.inertia_), 2),
                      "silueta": round(float(silhouette_score(X, m.labels_)), 4)})
    return pd.DataFrame(filas)
