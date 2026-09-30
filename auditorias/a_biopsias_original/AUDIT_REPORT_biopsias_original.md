# AUDIT_REPORT — biopsias_original
- **Archivo:** `auditorias/a_biopsias_original/App_Diagnostico_Biopsias_Mama_original.ipynb` · **Fecha:** 2026-09-29 · **Skill:** auditoria-modelos v2 (commit `ae67998`)
- **Objetivo:** `diagnostico` (positiva = maligno, valor 0) · **Subgrupos:** `num_biopsias_previas` (0 vs. ≥ 1)
- **Supuestos:** el archivo es la versión original con defectos de la Tarea 3.1, reconstruida desde el notebook corregido porque la copia descargada no estaba disponible (ver README del repositorio).

## Resumen
PASA: 4 · FALLA: 9 · NSPD: 5. Lo más grave: `sesiones_tratamiento_programadas` se construye a partir del objetivo y se usa como predictor (fuga de información). Además, el pipeline no llega a entrenar porque una división entre cero genera `inf`.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | FALLA | celda 9 (id 93d6fc8f): `ValueError: Input X contains infinity…`; celdas 10-12: `NameError: name 'modelo' is not defined` |
| V1.1 | Métricas en [0, 1] | NO SE PUEDE DETERMINAR | La única celda que imprime métricas, la celda 9 (id 93d6fc8f), terminó en error. No hay valores observados |
| V1.2 | Coherencia con matriz | NO SE PUEDE DETERMINAR | No hay matriz de confusión ni métricas derivadas |
| V1.3 | Desbalance | FALLA | celda 3 (id cba9b56a), salida: maligno = 0.373 < 0.40; celda 8 (id 881f59c8), l. 23-24: solo `accuracy_score` |
| V1.4 | Costo del error | FALLA | texto 1: dominio clínico ("priorizar qué casos revisa primero un especialista"); no hay justificación de la métrica; solo accuracy |
| V2.1 | Orden división/preprocesamiento | PASA | No hay transformadores (inventario: 0 `transformador`); `train_test_split` en celda 8 (id 881f59c8), l. 12, antes de `fit` en l. 21 |
| V2.2 | Semilla | PASA | celda 1 (id b7d1693a), l. 11 `RANDOM_STATE = 42`; celda 8, l. 13 `random_state=RANDOM_STATE`; `LogisticRegression` es determinista |
| V2.3 | Estratificación | FALLA | celda 8 (id 881f59c8), l. 12-14: `train_test_split` sin `stratify` |
| V2.4 | Misma partición | NO SE PUEDE DETERMINAR | Solo se entrena un modelo (celda 9); no hay comparación |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | No se presenta ningún hiperparámetro como elegido |
| V3.1 | Transformaciones sin datos de prueba | PASA | `acc_test` (celda 8, l. 24) proviene de un modelo ajustado solo con `X_train` (l. 21); no hay transformadores |
| V3.2 | Columnas del futuro | FALLA | celda 2 (id bbb980c2), l. 9: `df['sesiones_tratamiento_programadas'] = np.where(df['diagnostico'] == ...)`, es decir, derivada del objetivo; texto 3: "sesiones de tratamiento que tiene ya programadas"; celda 8, l. 4: está en `COLUMNAS_PREDICTORAS` |
| V4.1 | Métrica por subgrupo | FALLA | Ninguna celda calcula métricas por `num_biopsias_previas` (inventario: señales `metrica` solo en celda 8) |
| V4.2 | Brecha | NO SE PUEDE DETERMINAR | V0.1 = FALLA: no hay modelo entrenado con el cual reproducir los números |
| V5.1 | Dependencias | PASA | celda 2, l. 3: `load_breast_cancer` (incluido en scikit-learn) |
| V5.2 | Estado aleatorio | FALLA | celda 2 (id bbb980c2), l. 8 y 11 usan el `rng` global (celda 1, l. 12); `cargar_datos()` se llama en celda 2, l. 17 y en celda 9, l. 1, así que el `df` explorado y el entrenado tienen columnas aleatorias distintas |
| V6.1 | Divisiones seguras | FALLA | celda 6 (id b397da6d), l. 4: `/ df['num_biopsias_previas']` sin protección; celda 2, l. 8: `rng.randint(0, 4)` incluye el 0 |
| V6.2 | Validación antes de entrenar | FALLA | `validar_datos` se define en celda 5 (id fbef5102) y no se llama en ninguna celda |

## Acciones recomendadas
1. (V3.2) Retirar `sesiones_tratamiento_programadas` de `COLUMNAS_PREDICTORAS`: solo existe después de un diagnóstico maligno.
2. (V0.1, V6.1) Proteger el denominador (`num_biopsias_previas.clip(lower=1)` u otra regla justificada) y volver a ejecutar de principio a fin.
3. (V6.2) Llamar `validar_datos()` antes del `fit`.
4. (V2.3) Agregar `stratify=y` al `train_test_split`.
5. (V1.3, V1.4) Reportar matriz de confusión y precisión, exhaustividad y F1 de maligno, y justificar la métrica prioritaria según el costo de un falso negativo.
6. (V4.1) Calcular la exhaustividad de maligno por subgrupo de `num_biopsias_previas`.
7. (V5.2) Crear el generador dentro de `cargar_datos()` (`np.random.RandomState(RANDOM_STATE)`) o cargar una sola vez.

## Limitaciones de esta auditoría
El notebook no llega a entrenar, así que V1.1, V1.2 y V4.2 no se pueden observar. Con la fuga presente, el notebook corregido documenta un accuracy de prueba de 1.0000 (Tarea 3.1), pero esta auditoría no lo usa como evidencia porque proviene de otro archivo.
