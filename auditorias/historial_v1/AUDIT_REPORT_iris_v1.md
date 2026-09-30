# AUDIT_REPORT — iris (Skill v1, ejecución 1)

- **Archivo:** `App_Comparacion_Clasificadores_Iris.ipynb` (con los cinco clasificadores)
- **Fecha:** 2026-09-29 · **Versión de la Skill:** v1
- **Columna objetivo:** `target` (3 especies) · **Subgrupos:** no indicados

| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V1.1 | Métricas en [0, 1] | PASA | celda 16 (salida): accuracy entre 0.9400 y 0.9667 |
| V1.2 | Consistencia con la matriz | PASA | No hay matriz de confusión que contradiga |
| V1.3 | No solo accuracy con desbalance | FALLA | La clase minoritaria es 50/150 = 0.333 < 0.40 y solo se reporta accuracy (celda 7, l. 4; celda 16) |
| V1.4 | Métrica justificada por costo | FALLA | No hay justificación escrita de por qué accuracy |
| V2.1 | División antes de preprocesamiento | PASA | celda 10, l. 9-10: `StandardScaler` dentro de `Pipeline` |
| V2.2 | Semilla fija | PASA | celda 7, l. 3 `random_state=RANDOM_STATE` |
| V2.3 | Estratificación | PASA | celda 7, l. 3 `StratifiedKFold` |
| V2.4 | Misma partición | PASA | celdas 8 y 10: los cinco pasan por `evaluar_con_cv` con las mismas `X`, `y` |
| V3.1 | Transformadores sin datos de prueba | FALLA | celdas 4-6, l. 4 y celda 13, l. 8: `modelo.fit(X, y)` con **todo** el dataset, incluidos los datos que después se usan para evaluar; celda 13, l. 9 reporta `modelo.score(X, y)` |
| V3.2 | Sin columnas posteriores al resultado | PASA | Predictores = 4 medidas morfológicas (celda 2, l. 5) |
| V4.1 | Métrica por subgrupo | NO SE PUEDE DETERMINAR | No se indicó columna de subgrupos |
| V4.2 | Diferencia ≤ 0.10 | NO SE PUEDE DETERMINAR | Ídem |
| V5.1 | Dependencias | PASA | `load_iris` (celda 2) |

## Acciones recomendadas
1. (V1.3) Reportar F1 macro además de accuracy.
2. (V1.4) Justificar la métrica.
3. (V3.1) No entrenar sobre el dataset completo antes de evaluar.
