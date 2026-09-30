"""Verificación reproducida (solo lectura): ejecuta en memoria las celdas del notebook corregido
hasta el pipeline (sin modificarlo) y calcula la exhaustividad de maligno (clase 0) por subgrupo
de num_biopsias_previas (0 vs >= 1) con el modelo class_weight='balanced' de la sección 6d."""
import json, pathlib, io, contextlib
import matplotlib; matplotlib.use("Agg")
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
nb = json.loads(pathlib.Path(__file__).parents[3].joinpath("App_Diagnostico_Biopsias_Mama.ipynb").read_text(encoding="utf-8"))
ns = {"display": lambda *a: None}
for c in [c for c in nb["cells"] if c["cell_type"] == "code"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src.replace("plt.show()", "plt.close('all')"), ns)
    if "modelo, acc_train, acc_test = entrenar_modelo(df)" in src:
        break
df, P, RS = ns["df"], ns["COLUMNAS_PREDICTORAS"], ns["RANDOM_STATE"]
m, _, _ = ns["entrenar_modelo"](df, usar_class_weight=True)
X_tr, X_te, y_tr, y_te = train_test_split(df[P], df["diagnostico"], test_size=0.25, random_state=RS)
pred = m.predict(X_te); y = y_te.to_numpy()
g = np.where(X_te["num_biopsias_previas"].to_numpy() == 0, "0 previas", ">=1 previas")
glob = recall_score(y, pred, pos_label=0)
print(f"Global: n={len(y)} malignos={(y==0).sum()} exhaustividad maligno={glob:.3f}")
r = {}
for k in ["0 previas", ">=1 previas"]:
    s = g == k; r[k] = recall_score(y[s], pred[s], pos_label=0)
    print(f"{k:12}: n={s.sum()} malignos={(y[s]==0).sum()} exhaustividad={r[k]:.3f} diferencia={r[k]-glob:+.3f}")
print(f"Cociente peor/mejor: {min(r.values())/max(r.values()):.3f}")
