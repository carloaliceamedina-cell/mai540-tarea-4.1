"""Verificación reproducida (Skill auditoria-modelos, paso 5). Solo lectura: ejecuta en memoria
las celdas de código del notebook indicado (sin modificarlo) y calcula el RMSE por subgrupo del
modelo con menor RMSE de prueba. Uso: python verificacion_rmse_subgrupo.py <notebook.ipynb>"""
import json, sys, io, contextlib
import matplotlib; matplotlib.use("Agg")
import numpy as np
from sklearn.metrics import mean_squared_error
nb = json.load(open(sys.argv[1], encoding="utf-8"))
ns = {"display": lambda *a: None}
for c in [c for c in nb["cells"] if c["cell_type"] == "code"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "rmse_por_subgrupo" in src or "antes = pd.DataFrame" in src:
        continue
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src.replace("plt.show()", "plt.close('all')"), ns)
X_test, y_test = ns["X_test"], ns["y_test"]
for nombre in ["Regresión lineal", "Random Forest"]:
    pred = ns["ajustados"][nombre].predict(X_test)
    glob = np.sqrt(mean_squared_error(y_test, pred))
    print(f"{nombre}: RMSE global = {glob:,.0f} USD (n = {len(y_test)})")
    for col in ["fumador", "region"]:
        for g in sorted(X_test[col].unique()):
            m = (X_test[col] == g).to_numpy()
            r = np.sqrt(mean_squared_error(y_test[m], pred[m]))
            print(f"   {col}={g:<10} n={m.sum():>3}  RMSE={r:>7,.0f}  RMSE/global={r/glob:.2f}  costo medio={y_test[m].mean():>7,.0f}")
