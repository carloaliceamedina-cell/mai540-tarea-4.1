# AUDIT_REPORT — costos_medicos (antes de la corrección)
- Archivo: `auditoria/Herramienta_Regresion_Costos_Medicos_ANTES.ipynb` · Fecha: 2026-09-29 · Skill: auditoria-modelos v3 (modo regresión)
- Objetivo: `costo_medico_anual` (regresión, error en USD) · Subgrupos: `fumador`, `region` · Supuestos: el mejor modelo es el de menor RMSE de prueba (Random Forest).

## Resumen
PASA: 14 · FALLA: 2 · NSPD: 3 — Lo más grave: la herramienta no calcula el error por subgrupo, y al reproducirlo el RMSE de los **fumadores** es 1.35× el global en el mejor modelo y **1.94×** en la regresión lineal.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores; la celda 1 solo importa |
| V1R.1 | Rango y coherencia | PASA | celda 4 (id 115ff2ea), salida: MSE ≥ 0; RMSE = √MSE (√15,148,202 = 3,892); R² ≤ 1; calculados con `y_test` (l. 19-21) |
| V1R.2 | Referencia trivial | PASA | celda 4, l. 8: `DummyRegressor(strategy='mean')`, misma partición; salida: RMSE 10,933, columna "Mejora RMSE vs. referencia" |
| V1R.3 | Más de una métrica | PASA | celda 4, salida: MSE, RMSE (USD) y R² |
| V1R.4 | Sobreajuste | PASA | celda 4, salida: RF 0.9214 (entrenamiento) vs. 0.8720 (prueba), diferencia 0.049 ≤ 0.10; texto 5 lo interpreta |
| V1R.5 | Residuos | PASA | celda 5 (id 387721e8), l. 5-10: dispersión e histograma; texto 7 interpreta el patrón |
| V2.1 | Orden | PASA | celda 3 (id ffa43eaa), l. 10: división antes del `fit` (celda 4, l. 16); imputación, escalado y codificación en `Pipeline` (celda 4, l. 2-4, 15) |
| V2.2 | Semilla | PASA | celda 3, l. 10 y celda 4, l. 10: `random_state=RANDOM_STATE` |
| V2.3 | Estratificación | NO SE PUEDE DETERMINAR | Regresión: no aplica |
| V2.4 | Misma partición | PASA | celda 4, l. 13-16: los tres modelos usan `X_train`/`X_test` de la celda 3 |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | `n_estimators=300`, `min_samples_leaf=5` fijados y no presentados como elegidos por validación |
| V3.1 | Transformaciones | PASA | Ningún transformador se ajusta fuera del `Pipeline`; inventario: 0 `fit_transform` |
| V3.2 | Columnas del futuro | PASA | celda 2 (id 56dfb191), l. 19: `monto_reembolsado_aseguradora` se deriva del objetivo, pero celda 3, l. 2 y 6 la excluyen de `PREDICTORES` con `assert` |
| V4.1 | RMSE por subgrupo | FALLA | Ninguna celda calcula métricas por `fumador` o `region` |
| V4.2 | Brecha (RMSE ≥ 1.25× global, n ≥ 30) | FALLA | `evidencia/salida_antes.txt`: RF global 3,892; fumador=yes (n = 49) 5,262 = **1.35×**. Lineal: fumador=yes 10,393 = **1.94×**. Error relativo lineal: 28 % del costo medio de fumadores (10,393/37,688) frente a 26 % en no fumadores (3,641/14,142) |
| V5.1 | Dependencias | PASA | Datos generados en celda 2 |
| V5.2 | Estado aleatorio | PASA | celda 2, l. 4: `RandomState(semilla)` local |
| V6.1 | Divisiones seguras | PASA | Inventario: 0 `division_por_columna` |
| V6.2 | Validación antes de entrenar | NO SE PUEDE DETERMINAR | No hay función de validación; los faltantes se imputan en el `Pipeline` |

## Acciones recomendadas
1. (V4.1) Calcular el RMSE por `fumador` y `region` en el notebook.
2. (V4.2) Investigar la brecha de los fumadores. Los residuos (texto 7) sugieren una interacción fumador × IMC que el modelo lineal no representa.
3. (V2.5, NSPD) Declarar que los hiperparámetros del bosque no se ajustaron, o elegirlos con validación cruzada interna.

## Limitaciones de esta auditoría
Con n = 49 fumadores en prueba, su RMSE tiene incertidumbre alta; el umbral de n ≥ 30 se cumple por poco.
