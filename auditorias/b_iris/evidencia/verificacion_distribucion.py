"""Verificación reproducida (solo lectura): distribución de clases de Iris para V1.3."""
import numpy as np
from sklearn.datasets import load_iris
y = load_iris().target
c = np.bincount(y); print("Conteo por clase:", c.tolist(), "| p_min =", round(c.min() / c.sum(), 3), "| umbral 0.8/K =", round(0.8 / len(c), 3))
