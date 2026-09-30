# AUDIT_REPORT — biopsias_corregido (proyecto fuera de los tres, prueba final)
- **Archivo:** `App_Diagnostico_Biopsias_Mama.ipynb` (raíz del repositorio: versión corregida en la Tarea 3.1 con la sección 6d de esta tarea) · **Fecha:** 2026-09-29 · **Skill:** auditoria-modelos v2.1 (commit `fe73cdc`)
- **Objetivo:** `diagnostico` (positiva = maligno, 0) · **Subgrupos:** `num_biopsias_previas` (0 vs. ≥ 1)

## Resumen
PASA: 14 · FALLA: 3 · NSPD: 1. Las correcciones de la Tarea 3.1 se confirman (sin fuga ni división entre cero, con validación conectada), pero quedan tres defectos que nadie había visto: partición sin estratificar, `cargar_datos()` que genera datos distintos en cada llamada y ninguna métrica por subgrupo en el notebook.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores en salidas |
| V1.1 | Métricas en [0, 1] | PASA | celda 14 (id 3862a5f4), salida: todas las métricas entre 0.6296 y 0.7963 |
| V1.2 | Coherencia con matriz | PASA | celda 14, salida (balanced): VP = 43, FN = 11, FP = 25; 43/68 = 0.6324 = precisión; 43/54 = 0.7963 = exhaustividad; además hay `assert` en celda 14, l. 16 |
| V1.3 | Desbalance | PASA | Desbalance (0.373 < 0.40, celda 3), pero se reportan métricas por clase (celda 13, celda 14) |
| V1.4 | Costo del error | PASA | texto 19: el falso negativo es el error más costoso → exhaustividad de maligno como métrica prioritaria |
| V2.1 | Orden | PASA | Sin transformadores; `train_test_split` en celda 8 (id 881f59c8), l. 25, antes de `fit` |
| V2.2 | Semilla | PASA | celda 8, l. 26: `random_state=RANDOM_STATE` |
| V2.3 | Estratificación | FALLA | celda 8 (id 881f59c8), l. 25-27 y celda 13 (id 25f61993), l. 3: `train_test_split` sin `stratify` |
| V2.4 | Misma partición | PASA | Todas las comparaciones pasan por `entrenar_modelo()` (celda 8); celda 13, l. 3 replica la partición con los mismos parámetros |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | No se presenta ningún hiperparámetro como elegido |
| V3.1 | Transformaciones | PASA | Las métricas de prueba salen de modelos ajustados solo con `X_train` (celda 8) |
| V3.2 | Columnas del futuro | PASA | celda 8, l. 5-9: `COLUMNAS_PREDICTORAS` no contiene `sesiones_tratamiento_programadas` (l. 3 la declara `COLUMNA_FUGA`). La señal `derivada_de_otra_columna` (celda 2, l. 9) y su uso en celda 12 corresponden a la **demostración rotulada "Con fuga"** (texto 14), no al modelo que se reporta y se guarda (celda 16) |
| V4.1 | Métrica por subgrupo | FALLA | El notebook no calcula métricas por `num_biopsias_previas` |
| V4.2 | Brecha | PASA | `evidencia/salida_verificacion_disparidad.txt`: global 0.796; ≥ 1 previas (n = 114) 0.791 (−0.006). El subgrupo "0 previas" tiene n = 29 < 30 y se excluye (0.818) |
| V5.1 | Dependencias | PASA | `load_breast_cancer` |
| V5.2 | Estado aleatorio | FALLA | celda 2 (id bbb980c2), l. 8-11 usa el `rng` global; `cargar_datos()` se llama en celda 2, l. 17 y en celda 11 (id 93d6fc8f), l. 1: la exploración (celdas 3-4) describe un `df` distinto del que se entrena |
| V6.1 | Divisiones seguras | PASA | celda 6 (id b397da6d), l. 9: `.clip(lower=1)` |
| V6.2 | Validación antes de entrenar | PASA | celda 8, l. 20: `validar_datos(df, columnas)` se llama antes del `fit` |

## Acciones recomendadas
1. (V2.3) `stratify=y` en `entrenar_modelo()` y en celda 13.
2. (V5.2) Crear el generador dentro de `cargar_datos()` o cargar los datos una sola vez.
3. (V4.1) Incorporar al notebook la exhaustividad por subgrupo; con n = 29, el grupo "0 previas" necesita más datos o validación cruzada para decidir.

## Limitaciones de esta auditoría
La primera pasada sobre este notebook generó una duda que no resolvía el SKILL.md: ¿cuenta como fuga la celda 12, que usa la columna de fuga a propósito para mostrar el antes y el después? Hubo que decidirlo fuera del archivo. Se resolvió agregando la aclaración al SKILL.md (refinamiento 5).
