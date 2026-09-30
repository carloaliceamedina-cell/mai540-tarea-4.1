# AUDIT_REPORT — iris
- **Archivo:** `App_Comparacion_Clasificadores_Iris.ipynb` (raíz del repositorio, con los cinco clasificadores) · **Fecha:** 2026-09-29 · **Skill:** auditoria-modelos v2 (commit `ae67998`)
- **Objetivo:** `target` (3 especies; multiclase, sin clase positiva) · **Subgrupos:** no indicados (Iris no tiene una variable de grupo con sentido)
- **Supuestos:** la métrica prioritaria es accuracy (clases balanceadas y sin costos asimétricos, ver V1.4).

## Resumen
PASA: 14 · FALLA: 0 · NSPD: 4. No se encontraron defectos de partición ni de fuga. Los NSPD se deben a que no hay matriz de confusión, no se definieron subgrupos y no existe una función de validación de datos.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores en salidas; las celdas sin salida (4-7) solo definen funciones |
| V1.1 | Métricas en [0, 1] | PASA | celda 16 (id cadcbbdd), salida: accuracy entre 0.9400 y 0.9667, mínimos ≥ 0.8667 |
| V1.2 | Coherencia con matriz | NO SE PUEDE DETERMINAR | No hay matriz de confusión ni métricas por clase |
| V1.3 | Desbalance | PASA | `evidencia/salida_verificacion_distribucion.txt`: conteo [50, 50, 50], p_min = 0.333 ≥ 0.8/3 = 0.267; no hay desbalance |
| V1.4 | Costo del error | PASA | texto 1: vivero que clasifica especies, sin mención de errores más costosos; con clases balanceadas, accuracy es adecuada |
| V2.1 | Orden | PASA | celda 10 (id 3cecb4e8), l. 9-10: `StandardScaler` dentro de `Pipeline`, evaluado con `evaluar_con_cv` (l. 20) |
| V2.2 | Semilla | PASA | celda 7 (id a37aa1ce), l. 3: `StratifiedKFold(..., shuffle=True, random_state=RANDOM_STATE)`; celda 5, l. 3 y celda 10, l. 18: árbol y bosque con `random_state` (inventario: 0 `estimador_sin_semilla`) |
| V2.3 | Estratificación | PASA | celda 7 (id a37aa1ce), l. 3: `StratifiedKFold`; celda 10, l. 13: CV interna también estratificada |
| V2.4 | Misma partición | PASA | celdas 8 y 10: los cinco modelos pasan por `evaluar_con_cv` con las mismas `X`, `y`; celda 11 (id 69b99402), salida: "Mismas particiones que evaluar_con_cv -> True" |
| V2.5 | Hiperparámetros | PASA | k de KNN: `GridSearchCV` con CV interna (celda 10, l. 13-15) anidada en la CV externa; celda 11, salida: k por partición [19, 11, 13, 11, 13, 3, 7, 11, 15, 15]. `max_depth=3` del árbol viene dado por el enunciado (texto 5) y se explora en celda 13 |
| V3.1 | Transformaciones sin datos de prueba | PASA | Las métricas de generalización salen de `cross_val_score` (celda 7, l. 4), que clona el estimador; celda 9, salida: resultados idénticos con el modelo ya entrenado (`True` ×3). Los `fit(X, y)` de celdas 4-6 y 13 (l. 8) solo producen modelos finales o accuracy **de entrenamiento** rotulada como tal (celda 13, l. 20) |
| V3.2 | Columnas del futuro | PASA | celda 2 (id 4abcd0e9), l. 5: `X = iris.data`, cuatro medidas morfológicas que se toman antes de clasificar |
| V4.1 | Métrica por subgrupo | NO SE PUEDE DETERMINAR | No se indicó columna de subgrupo |
| V4.2 | Brecha | NO SE PUEDE DETERMINAR | Ídem |
| V5.1 | Dependencias | PASA | celda 2, l. 1: `load_iris` |
| V5.2 | Estado aleatorio | PASA | Inventario: 0 `rng_global` |
| V6.1 | Divisiones seguras | PASA | Inventario: 0 `division_por_columna` |
| V6.2 | Validación antes de entrenar | NO SE PUEDE DETERMINAR | No existe función de validación (dataset de librería, sin nulos conocidos) |

## Acciones recomendadas
1. (V1.2, NSPD) Agregar una matriz de confusión multiclase del modelo recomendado (por ejemplo con `cross_val_predict`) para ver qué especies se confunden: versicolor y virginica, según las fronteras de la sección 5.
2. (V6.2, NSPD) Opcional: afirmar que `X` no tiene nulos antes de entrenar.

## Limitaciones de esta auditoría
Con 150 muestras, las diferencias entre modelos (≤ 4 muestras) son menores que una desviación estándar. La auditoría verifica que la comparación sea justa, no que el orden entre modelos sea significativo.
