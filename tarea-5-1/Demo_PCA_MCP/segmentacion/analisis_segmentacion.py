"""Tarea 5.2 — Justificación de k y visualización PCA de la segmentación de 'wine'.
Usa las mismas funciones que exponen las tools del servidor (kmeans_utils, pca_utils).
Uso (desde la carpeta del proyecto): python segmentacion/analisis_segmentacion.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import kmeans_utils, pca_utils  # noqa: E402

DATASET, K = "wine", 3
SALIDA = RAIZ / "segmentacion"

# 1) Elección de k: método del codo + silueta
tabla = kmeans_utils.evaluar_k(DATASET, 2, 8)
tabla["caida_inercia"] = (-tabla["inercia"].diff()).round(2)
tabla.to_csv(SALIDA / "eleccion_k.csv", index=False)
print(tabla.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(tabla["k"], tabla["inercia"], "o-", color="#1f4e79", label="Inercia (codo)")
ax1.set_xlabel("k (número de grupos)"); ax1.set_ylabel("Inercia", color="#1f4e79")
ax2 = ax1.twinx()
ax2.plot(tabla["k"], tabla["silueta"], "s--", color="#c55a11", label="Silueta")
ax2.set_ylabel("Coeficiente de silueta", color="#c55a11")
ax1.axvline(K, color="gray", ls=":", lw=1)
ax1.set_title(f"Elección de k para '{DATASET}': codo en k={K} y silueta máxima en k={K}")
fig.tight_layout(); fig.savefig(SALIDA / "eleccion_k.png", dpi=150); plt.close(fig)

# 2) Segmentación con el k elegido
seg = kmeans_utils.ejecutar_kmeans(DATASET, K)
etiquetas = np.array(seg["etiquetas"])

# 3) Proyección 2D con el PCA de la Tarea 5.1 (pca_utils.ejecutar_pca da varianza y cargas)
pca = pca_utils.ejecutar_pca(DATASET, 2)
_, X, numericas = kmeans_utils.cargar_y_escalar(DATASET)
cargas = np.array([[pca["cargas"]["PC1"][v], pca["cargas"]["PC2"][v]] for v in numericas])
Z = X @ cargas                                  # coordenadas = datos estandarizados × cargas
var1, var2 = pca["varianza_explicada_por_componente"]
nombres = {0: "Grupo 0: ligeros y suaves", 1: "Grupo 1: intensos y ácidos", 2: "Grupo 2: robustos y premium"}
colores = {0: "#2e75b6", 1: "#c00000", 2: "#548235"}
fig, ax = plt.subplots(figsize=(7, 5))
for g in range(K):
    m = etiquetas == g
    ax.scatter(Z[m, 0], Z[m, 1], s=22, alpha=0.75, color=colores[g], label=f"{nombres[g]} (n={m.sum()})")
ax.set_xlabel(f"PC1 ({var1:.1%} de la varianza)"); ax.set_ylabel(f"PC2 ({var2:.1%} de la varianza)")
ax.set_title(f"K-Means (k={K}) sobre 2 componentes PCA: {pca['varianza_acumulada']:.1%} de la varianza")
ax.legend(fontsize=8); ax.axhline(0, color="#ccc", lw=0.6); ax.axvline(0, color="#ccc", lw=0.6)
fig.tight_layout(); fig.savefig(SALIDA / "pca_kmeans_2d.png", dpi=150); plt.close(fig)

# 4) Perfil de cada grupo en z-scores (para interpretar sin depender de las unidades)
zperfil = pd.DataFrame(X, columns=numericas).groupby(etiquetas).mean().round(2).T
zperfil.columns = [nombres[g] for g in zperfil.columns]
zperfil.to_csv(SALIDA / "perfil_grupos_zscore.csv")
print(f"\nSilueta k={K}: {seg['silueta']} | tamaños: {seg['tamano_por_grupo']}")
print(f"Varianza conservada por PC1+PC2: {pca['varianza_acumulada']} ({var1} + {var2})")
print("\nPerfil (z-score) por grupo:\n", zperfil.to_string())
