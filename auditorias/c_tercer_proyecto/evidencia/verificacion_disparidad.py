"""Verificación reproducida (Skill auditoria-modelos, paso 5). Solo lectura: ejecuta
las celdas 1-4 del notebook auditado en memoria, sin modificarlo, y calcula la
exhaustividad de la clase positiva (income_gt_50k = 1) por subgrupo de `sex` sobre la
partición de prueba de la regresión logística (celda 4, l. 1)."""
import json, pathlib
import numpy as np, pandas as pd
from sklearn.metrics import recall_score, precision_score, confusion_matrix

nb = json.loads(pathlib.Path(__file__).parents[1].joinpath("App_Prediccion_Ingresos_Adult.ipynb").read_text(encoding="utf-8"))
ns = {}
for c in [c for c in nb["cells"] if c["cell_type"] == "code"][:4]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    exec(src.replace("df.head()", ""), ns)

y_test, X_test, logreg, df = ns["y_test"], ns["X_test"], ns["logreg"], ns["df"]
pred = logreg.predict(X_test)
sexo = df.loc[y_test.index, "sex"]
print("Matriz global [0,1]:", confusion_matrix(y_test, pred, labels=[0, 1]).tolist())
glob = recall_score(y_test, pred)
print(f"Global: n={len(y_test)}  positivos={int(y_test.sum())}  exhaustividad={glob:.3f}  precisión={precision_score(y_test, pred):.3f}")
filas = {}
for g in ["Male", "Female"]:
    m = (sexo == g).to_numpy()
    r = recall_score(y_test[m], pred[m])
    filas[g] = r
    print(f"{g:6}: n={m.sum()}  positivos={int(y_test[m].sum())}  exhaustividad={r:.3f}  diferencia vs global={r - glob:+.3f}")
print(f"Cociente peor/mejor subgrupo: {min(filas.values()) / max(filas.values()):.3f}")
