# AUDIT_REPORT — costos_medicos (versión final, después de las correcciones)
- Archivo: `Herramienta_Regresion_Costos_Medicos.ipynb` · Fecha: 2026-09-29 · Skill: auditoria-modelos v3 (modo regresión)
- Objetivo: `costo_medico_anual` (regresión, error en USD) · Subgrupos: `fumador`, `region` · Supuestos: el mejor modelo es el de menor RMSE de prueba (regresión lineal con interacciones).

## Resumen
PASA: 15 · FALLA: 1 · NSPD: 3 — Se corrigieron la fuga de la primera corrección (V3.1) y la falta de error por subgrupo (V4.1). **Persiste la disparidad V4.2**: el RMSE de los fumadores es 1.33× el global (antes 1.94× en la lineal y 1.35× en el mejor modelo) y el de la región *northwest* es 1.30×.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores; las celdas 1 y 4 solo definen |
| V1R.1 | Rango y coherencia | PASA | celda 5 (id 3b6ed2cb), salida: MSE lineal 12,936,021 → √ = 3,597 = RMSE; R² ≤ 1; con `y_test` |
| V1R.2 | Referencia trivial | PASA | celda 5, l. 8: `DummyRegressor(strategy='mean')`; RMSE 10,933; mejora 67 % (lineal) y 65 % (RF) |
| V1R.3 | Más de una métrica | PASA | MSE, RMSE (USD) y R² en la misma tabla |
| V1R.4 | Sobreajuste | PASA | Lineal 0.8790 frente a 0.8907; RF 0.9205 frente a 0.8775 (0.043); texto 6 lo interpreta |
| V1R.5 | Residuos | PASA | celda 6 (id 76be27c2): dispersión + histograma; texto 8 describe heterocedasticidad y cola derecha |
| V2.1 | Orden | PASA | celda 3 (id 17171e38), l. 10: división antes de todo `fit`; imputación, escalado y codificación en `Pipeline` (celda 5, l. 2-4, 15) |
| V2.2 | Semilla | PASA | `random_state=RANDOM_STATE` en división y bosque |
| V2.3 | Estratificación | NO SE PUEDE DETERMINAR | Regresión: no aplica |
| V2.4 | Misma partición | PASA | celda 5, l. 13-16: los tres modelos usan la partición de celda 3; celda 8 compara antes/después con la misma semilla |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | `n_estimators=300`, `min_samples_leaf=5` fijados y no presentados como elegidos |
| V3.1 | Transformaciones | PASA | celda 4 (id 7da08a7a), l. 8: la interacción ya no imputa (`es_fumador * X['imc']`); el NaN lo imputa el `SimpleImputer` ajustado con entrenamiento. `agregar_interacciones` solo usa valores de la propia fila |
| V3.2 | Columnas del futuro | PASA | celda 3, l. 2 y 6: `monto_reembolsado_aseguradora` excluida con `assert` |
| V4.1 | RMSE por subgrupo | PASA | celda 7 (id 73da956d): `rmse_por_subgrupo` por `fumador` y `region`, con error relativo |
| V4.2 | Brecha (RMSE ≥ 1.25× global, n ≥ 30) | FALLA | celda 7, salida: lineal fumador=yes (n = 49) 4,777 = **1.33×**; region=northwest (n = 71) 4,689 = **1.30×**. Error relativo en fumadores: 12.7 % (4,777/37,688), frente a 23.5 % en no fumadores (3,317/14,142) |
| V5.1 | Dependencias | PASA | Datos generados en celda 2 |
| V5.2 | Estado aleatorio | PASA | `RandomState` local en `generar_datos` |
| V6.1 | Divisiones seguras | PASA | Inventario: 0 `division_por_columna` |
| V6.2 | Validación antes de entrenar | NO SE PUEDE DETERMINAR | No existe función de validación explícita |

## Acciones recomendadas
1. (V4.2) La brecha absoluta de los fumadores se redujo, pero sigue sobre el umbral. Como su error **relativo** es la mitad del de los no fumadores, la brecha se debe sobre todo a la escala de su costo. Aun así, se declara en Limitaciones y se prohíbe el uso individual. Para la región *northwest* no hay una variable que la explique; hace falta más datos.
2. (V2.5, NSPD) Elegir los hiperparámetros del bosque con validación cruzada interna.
3. (V6.2, NSPD) Validar rangos (edad 18-64, IMC 16-53) antes de predecir.

## Limitaciones de esta auditoría
Datos sintéticos; n = 49 fumadores en prueba.
