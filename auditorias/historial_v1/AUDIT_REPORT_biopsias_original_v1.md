# AUDIT_REPORT — biopsias_original (Skill v1, ejecución 1)

- **Archivo:** `auditorias/a_biopsias_original/App_Diagnostico_Biopsias_Mama_original.ipynb`
- **Fecha:** 2026-09-29 · **Versión de la Skill:** v1 (commit inicial)
- **Columna objetivo:** `diagnostico` (0 = maligno, 1 = benigno) · **Subgrupos:** `num_biopsias_previas` (0 vs. ≥ 1)

| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V1.1 | Métricas en [0, 1] | PASA | celda 8, l. 23-24: `accuracy_score(...)` devuelve valores en [0, 1] |
| V1.2 | Métricas consistentes con la matriz | PASA | No hay matriz de confusión que contradiga las métricas |
| V1.3 | No solo accuracy con desbalance | FALLA | celda 3 (salida): maligno = 0.373 < 0.40; celda 8, l. 23-24 y celda 9 reportan solo accuracy |
| V1.4 | Métrica justificada por costo del error | FALLA | Ninguna celda de texto justifica la métrica; solo se usa accuracy |
| V2.1 | División antes de preprocesamiento que aprende | PASA | celda 8, l. 12 (`train_test_split`) ocurre antes de `fit` (l. 21); no hay escalado ni imputación |
| V2.2 | Semilla fija | PASA | celda 1, l. 11 `RANDOM_STATE = 42`; celda 8, l. 13 |
| V2.3 | Estratificación | FALLA | celda 8, l. 12-14: `train_test_split` sin `stratify=y` |
| V2.4 | Misma partición entre modelos | PASA | todas las variantes pasan por `entrenar_modelo()` (celda 8) con el mismo `random_state` |
| V3.1 | Transformadores sin datos de prueba | PASA | No hay transformadores ajustables |
| V3.2 | Sin columnas posteriores al resultado | FALLA | celda 2, l. 9-13: `sesiones_tratamiento_programadas = np.where(diagnostico == 0, ...)`, se construye a partir del objetivo; celda 8, l. 4 la incluye en `COLUMNAS_PREDICTORAS` |
| V4.1 | Métrica por subgrupo | FALLA | Ninguna celda calcula métricas por `num_biopsias_previas` |
| V4.2 | Diferencia con el global ≤ 0.10 | NO SE PUEDE DETERMINAR | No hay métricas por subgrupo que comparar |
| V5.1 | Dependencias externas disponibles | PASA | celda 2, l. 3: `load_breast_cancer` (incluido en scikit-learn) |

## Acciones recomendadas
1. (V3.2) Quitar `sesiones_tratamiento_programadas` de `COLUMNAS_PREDICTORAS`: se programa después del diagnóstico maligno.
2. (V2.3) Agregar `stratify=y` al `train_test_split`.
3. (V1.3, V1.4) Reportar precisión, exhaustividad y F1 de la clase maligno y justificar la métrica prioritaria.
4. (V4.1) Calcular la exhaustividad de maligno por subgrupo de `num_biopsias_previas`.
