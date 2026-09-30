# AUDIT_REPORT — costos_medicos (primera corrección)
- Archivo: `auditoria/Herramienta_Regresion_Costos_Medicos_CORRECCION1.ipynb` · Fecha: 2026-09-29 · Skill: auditoria-modelos v3
- Objetivo: `costo_medico_anual` · Subgrupos: `fumador`, `region`

## Resumen
PASA: 14 · FALLA: 2 · NSPD: 3 — La corrección redujo la brecha de los fumadores (lineal: 1.94× → 1.38×), pero **introdujo una fuga nueva**: la variable de interacción imputa el IMC con la mediana del lote que se transforma, que en predicción es el conjunto de prueba.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores |
| V1R.1 | Rango y coherencia | PASA | celda 5 (id 4a7637d4), salida: RMSE lineal 3,646 = √13,289,938; R² ≤ 1 |
| V1R.2 | Referencia trivial | PASA | celda 5: `DummyRegressor`, misma partición |
| V1R.3 | Más de una métrica | PASA | MSE, RMSE y R² |
| V1R.4 | Sobreajuste | PASA | Lineal 0.8767 frente a 0.8877; RF 0.9214 frente a 0.8722 (0.049) |
| V1R.5 | Residuos | PASA | celda 6 (id 114f5828) con gráficas; texto de lectura |
| V2.1 | Orden | PASA | celda 3 (id b295f19c), l. 10: división antes del `fit` |
| V2.2 | Semilla | PASA | `random_state` en división y bosque |
| V2.3 | Estratificación | NO SE PUEDE DETERMINAR | Regresión: no aplica |
| V2.4 | Misma partición | PASA | Los tres modelos usan la partición de celda 3 |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | Fijados, no elegidos |
| V3.1 | Transformaciones | **FALLA** | celda 4 (id 49709650), l. 8: `X['imc'].fillna(X['imc'].median() ...)` dentro de un `FunctionTransformer` (celda 5, l. 15). Un `FunctionTransformer` no aprende en `fit`: en `predict` calcula la mediana **del lote de prueba**, así que las predicciones de prueba usan estadísticas de prueba |
| V3.2 | Columnas del futuro | PASA | `COLUMNA_FUGA` excluida (celda 3, l. 2 y 6) |
| V4.1 | RMSE por subgrupo | PASA | celda 7 (id a44bc93e): tabla de RMSE por `fumador` y `region` |
| V4.2 | Brecha | FALLA | celda 7, salida: lineal fumador=yes 5,015 = 1.38× (n = 49); region=northwest 4,919 = 1.35× (n = 71). Error relativo en fumadores: 13 % frente a 23 % en no fumadores |
| V5.1 | Dependencias | PASA | celda 2 |
| V5.2 | Estado aleatorio | PASA | `RandomState` local |
| V6.1 | Divisiones seguras | PASA | 0 divisiones por columna |
| V6.2 | Validación | NO SE PUEDE DETERMINAR | No existe |

## Acciones recomendadas
1. (V3.1) No imputar dentro de la función de interacción: dejar el NaN y que lo impute el `SimpleImputer`, que aprende la mediana solo de entrenamiento.
2. (V4.2) La brecha absoluta persiste, pero el error relativo de los fumadores es menor que el de los no fumadores. Declararlo como limitación y no usar el modelo para decisiones individuales sobre fumadores.
