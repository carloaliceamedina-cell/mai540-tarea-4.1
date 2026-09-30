# AUDIT_REPORT — tercer_proyecto
- **Archivo:** `auditorias/c_tercer_proyecto/App_Prediccion_Ingresos_Adult.ipynb` · **Fecha:** 2026-09-29 · **Skill:** auditoria-modelos v2 (commit `ae67998`)
- **Objetivo:** `income_gt_50k` (positiva = 1, > 50K) · **Subgrupos:** `sex`
- **Supuestos:** proyecto sustituto con datos sintéticos (el del aula virtual no estaba disponible); la métrica prioritaria es la exhaustividad de la clase 1, porque el modelo preselecciona solicitudes (texto 5) y un falso negativo excluye a alguien elegible.

## Resumen
PASA: 6 · FALLA: 9 · NSPD: 3. Lo más grave: el escalador se ajusta con todas las filas antes de dividir (V2.1/V3.1), cada modelo se evalúa con una partición distinta y sin semilla (V2.2/V2.4), y la exhaustividad en `Female` (0.302) queda 0.184 por debajo de la global.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores; las celdas 1 y 3 no producen salida por diseño (importaciones, asignaciones) |
| V1.1 | Métricas en [0, 1] | PASA | celda 4 (id 18260dae), salida: 0.809 y 0.796 |
| V1.2 | Coherencia con matriz | NO SE PUEDE DETERMINAR | No hay matriz ni métricas derivadas |
| V1.3 | Desbalance | FALLA | celda 2 (id f6e89e42), salida: clase 1 = 0.251 < 0.40; celda 4, l. 3 y 7: solo `accuracy_score` |
| V1.4 | Costo del error | FALLA | texto 5: "superan el 75 % de accuracy… apto para la preselección"; 75 % equivale a predecir siempre la clase 0 (tasa 0.749, celda 2); el dominio (crédito/preselección) tiene costos asimétricos |
| V2.1 | Orden | FALLA | celda 3 (id ed9c3c92), l. 6: `scaler.fit_transform(X)` sobre todo `X`, antes del `train_test_split` de celda 4 (id 18260dae), l. 1 |
| V2.2 | Semilla | FALLA | celda 4, l. 5: `train_test_split` sin `random_state`; l. 6: `RandomForestClassifier` sin `random_state`. Evidencia: el accuracy del bosque fue 0.796 en el notebook y 0.807 en la verificación reproducida |
| V2.3 | Estratificación | FALLA | celda 4, l. 1 y 5: sin `stratify` |
| V2.4 | Misma partición | FALLA | celda 4, l. 1 (`random_state=1`) frente a l. 5 (sin semilla): los modelos comparados se evalúan con particiones distintas |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | No se presenta ningún hiperparámetro como elegido |
| V3.1 | Transformaciones sin datos de prueba | FALLA | El `StandardScaler` (celda 3, l. 6) usó la media y la desviación de las filas que luego forman `X_test`, y `acc_logreg`/`acc_rf` (celda 4, l. 3 y 7) se calculan sobre ellas |
| V3.2 | Columnas del futuro | PASA | celda 2 (id f6e89e42), l. 3-8: los cinco predictores se generan antes del objetivo (l. 11) y `capital_gain` entra como causa en el `logit` (l. 9-10); ninguno se deriva del objetivo (inventario: 0 `derivada_de_otra_columna`) |
| V4.1 | Métrica por subgrupo | FALLA | No hay métricas por `sex` en el notebook |
| V4.2 | Brecha | FALLA | `evidencia/salida_verificacion_disparidad.txt`: exhaustividad global 0.485; Female (n = 266, positivos 63) 0.302 (−0.184); Male (n = 534) 0.568; cociente 0.531 < 0.80 |
| V5.1 | Dependencias | PASA | Datos generados en celda 2 |
| V5.2 | Estado aleatorio | PASA | El `rng` (celda 1, l. 8) se consume a nivel superior una sola vez (celda 2); no hay función de carga que se llame dos veces |
| V6.1 | Divisiones seguras | PASA | Inventario: 0 `division_por_columna` |
| V6.2 | Validación antes de entrenar | NO SE PUEDE DETERMINAR | No existe función de validación |

## Acciones recomendadas
1. (V2.1, V3.1) Poner el `StandardScaler` dentro de un `Pipeline` y ajustarlo solo con `X_train` (o dentro de la CV).
2. (V2.2, V2.3, V2.4) Una sola partición `train_test_split(..., stratify=y, random_state=RANDOM_STATE)` para ambos modelos, y `random_state` en el bosque.
3. (V1.3, V1.4) Reportar matriz de confusión y precisión, exhaustividad y F1 de la clase 1; comparar contra la línea base de la clase mayoritaria (0.749) y justificar la métrica prioritaria.
4. (V4.1, V4.2) Reportar la exhaustividad por `sex` y analizar la brecha (0.302 frente a 0.568) antes de usar el modelo para preseleccionar; evaluar `class_weight="balanced"`, ajuste de umbral o variables que no actúen como sustituto del sexo.
5. (V6.2, NSPD) Validar nulos e infinitos antes de entrenar.

## Limitaciones de esta auditoría
Los datos son sintéticos: la brecha por `sex` refleja cómo se generaron (el sexo entra en el `logit`) y sirve para probar que la Skill la detecta, no para concluir sobre personas reales.
