# AUDIT_REPORT — tercer_proyecto (Skill v1, ejecución 2)

- **Archivo:** `auditorias/c_tercer_proyecto/App_Prediccion_Ingresos_Adult.ipynb`
- **Fecha:** 2026-09-29 · **Versión de la Skill:** v1
- **Columna objetivo:** `income_gt_50k` · **Subgrupos:** `sex`

| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V1.1 | Métricas en [0, 1] | PASA | celda 4 (salida): 0.809 y 0.796 |
| V1.2 | Consistencia con la matriz | PASA | No hay matriz que contradiga |
| V1.3 | No solo accuracy con desbalance | FALLA | celda 2 (salida): clase 1 = 0.251; celda 4 solo accuracy |
| V1.4 | Métrica justificada | FALLA | Celda de conclusión: "superan el 75 % de accuracy"; 75 % es la tasa de la clase mayoritaria |
| V2.1 | División antes de preprocesamiento | FALLA | celda 3, l. 6: `scaler.fit_transform(X)` antes del `train_test_split` de celda 4, l. 1 |
| V2.2 | Semilla fija | FALLA | celda 4, l. 5: segundo `train_test_split` sin `random_state`; l. 6 `RandomForestClassifier` sin `random_state` |
| V2.3 | Estratificación | FALLA | celda 4, l. 1 y 5: sin `stratify` |
| V2.4 | Misma partición | FALLA | celda 4, l. 1 (`random_state=1`) vs. l. 5 (sin semilla): dos particiones distintas |
| V3.1 | Transformadores sin datos de prueba | FALLA | celda 3, l. 6: el `StandardScaler` se ajusta con las filas que luego serán de prueba |
| V3.2 | Sin columnas posteriores al resultado | PASA | celda 2, l. 7-9: `capital_gain` se genera **antes** que `income_gt_50k` y es una de sus causas en el `logit`; no se deriva del objetivo |
| V4.1 | Métrica por subgrupo | FALLA | Ninguna celda calcula métricas por `sex` |
| V4.2 | Diferencia ≤ 0.10 | NO SE PUEDE DETERMINAR | Sin métricas por subgrupo |
| V5.1 | Dependencias | PASA | Datos generados en la celda 2 |

## Acciones recomendadas
1. Mover el escalado dentro de un `Pipeline` después de la división.
2. Fijar semillas, estratificar y usar la misma partición para ambos modelos.
3. (sin acción sobre `capital_gain`)
4. Reportar precisión/exhaustividad/F1 de la clase 1 y calcularlas por `sex`.
