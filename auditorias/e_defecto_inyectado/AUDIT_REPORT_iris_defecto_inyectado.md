# AUDIT_REPORT — iris_defecto_inyectado
- **Archivo:** `auditorias/e_defecto_inyectado/App_Comparacion_Clasificadores_Iris_defecto.ipynb` (copia de Iris con un defecto introducido a propósito) · **Fecha:** 2026-09-29
- **Defecto introducido:** en celda 10 (id 3cecb4e8), l. 21-22, se reemplazó el `Pipeline` + `GridSearchCV` por `X_escalado = StandardScaler().fit_transform(X)` y `KNeighborsClassifier(n_neighbors=5)` evaluado sobre `X_escalado`, **sin cambiar la etiqueta** "KNN (escalado + k por CV)".
- **Objetivo:** `target` · **Subgrupos:** no indicados

## Resultado por versión de la Skill (solo las filas que cambian respecto de `AUDIT_REPORT_iris.md`)

| ID | Skill v2 sin V2.5 (commit `978520f`) | Skill v2 con V2.5 (commit `ae67998`) | Evidencia |
|---|---|---|---|
| V2.1 Orden | FALLA | FALLA | celda 10 (id 3cecb4e8), l. 21: `StandardScaler().fit_transform(X)` sobre todo `X` antes de `evaluar_con_cv` (l. 22) |
| V2.5 Hiperparámetros | *(no existía)* → omisión | FALLA | celda 10, l. 22: `n_neighbors=5` fijado a mano, con la etiqueta "k por CV"; texto 8 afirma que "k se elige por validación". celda 11 (id 69b99402), salida: "Mismas particiones que evaluar_con_cv -> False" (los puntajes impresos no coinciden con la búsqueda de k) |
| V3.1 Transformaciones | FALLA | FALLA | Los puntajes de CV de KNN (celda 16, 0.9533) provienen de un escalador que vio las filas de cada partición de prueba |
| Resto (15 filas) | igual que `AUDIT_REPORT_iris.md` | igual | — |

## Conclusión de la prueba
La v2 detecta la fuga por escalado global aunque el impacto en la métrica sea pequeño (KNN 0.9600 → 0.9533): la Skill decide por la estructura del código, no porque el número suba o baje. La prueba reveló una **omisión**: nada verificaba que el hiperparámetro rotulado "por validación" lo estuviera de verdad. Se agregó V2.5 (refinamiento 4) y, al volver a ejecutar, la omisión queda detectada.
