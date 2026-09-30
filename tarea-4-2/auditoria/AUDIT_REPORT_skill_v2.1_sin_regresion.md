# AUDIT_REPORT — costos_medicos (primer intento, Skill v2.1 sin modo regresión)
- Archivo: `auditoria/Herramienta_Regresion_Costos_Medicos_ANTES.ipynb` · Fecha: 2026-09-29 · Skill: auditoria-modelos v2.1 (commit `fe73cdc`, Tarea 4.1)
- Objetivo: `costo_medico_anual` (continuo, USD) · Subgrupos: `fumador`, `region` · Supuestos: la Skill v2.1 pide "clase positiva"; no existe en regresión.

## Resumen
PASA: 9 · FALLA: 1 · NSPD: 8 — La Skill **no sabe auditar regresión**: 6 de sus 18 verificaciones dependen de conceptos de clasificación (matriz de confusión, clase minoritaria, exhaustividad) y quedan NSPD o se aplican mal.

## Verificaciones
| ID | Verificación | Resultado | Evidencia |
|---|---|---|---|
| V0.1 | Ejecución sin errores | PASA | Inventario: 0 errores |
| V1.1 | Métricas en [0, 1] | FALLA | celda 4 (id 115ff2ea), salida: MSE = 28,732,964 y R² de referencia = −0.0102, fuera de [0, 1]. *El criterio v2.1 supone métricas de clasificación: es un falso positivo.* |
| V1.2 | Coherencia con matriz | NO SE PUEDE DETERMINAR | No hay matriz de confusión (no aplica a regresión) |
| V1.3 | Desbalance | NO SE PUEDE DETERMINAR | No hay clases; p_min no está definido |
| V1.4 | Costo del error | NO SE PUEDE DETERMINAR | La tabla v2.1 pide justificar la métrica por clase |
| V2.1 | Orden | PASA | celda 3 (id ffa43eaa), l. 10: `train_test_split` antes del `fit` de celda 4, l. 16; transformadores dentro de `Pipeline` (celda 4, l. 3-4, 15) |
| V2.2 | Semilla | PASA | celda 3, l. 10: `random_state=RANDOM_STATE`; celda 4, l. 10: bosque con `random_state` |
| V2.3 | Estratificación | NO SE PUEDE DETERMINAR | Regresión: no aplica |
| V2.4 | Misma partición | PASA | celda 4, l. 13-16: los tres modelos se ajustan con el mismo `X_train` |
| V2.5 | Hiperparámetros | NO SE PUEDE DETERMINAR | Ninguno se presenta como elegido por validación |
| V3.1 | Transformaciones | PASA | Imputación, escalado y codificación dentro del `Pipeline` ajustado con `X_train` (celda 4, l. 16) |
| V3.2 | Columnas del futuro | PASA | celda 3 (id ffa43eaa), l. 2 y 6: `COLUMNA_FUGA` excluida y verificada con `assert` |
| V4.1 | Métrica por subgrupo | NO SE PUEDE DETERMINAR | La variante v2.1 exige "exhaustividad de la clase positiva", que no existe; no se puede aplicar |
| V4.2 | Brecha | NO SE PUEDE DETERMINAR | Ídem |
| V5.1 | Dependencias | PASA | Datos generados en celda 2 |
| V5.2 | Estado aleatorio | PASA | `generar_datos()` crea su propio `RandomState` (celda 2, l. 4) |
| V6.1 | Divisiones seguras | PASA | Inventario: 0 `division_por_columna` |
| V6.2 | Validación antes de entrenar | NO SE PUEDE DETERMINAR | No existe función de validación |

## Acciones recomendadas
1. **(Skill)** Agregar un modo de regresión: métricas MSE/RMSE/R² coherentes, referencia trivial, residuos y disparidad del RMSE por subgrupo. → Se hizo en el commit de extensión de la Skill (v3).

## Limitaciones de esta auditoría
Este informe se conserva para documentar qué tan reutilizable era la Skill: servía para partición y fuga, pero no para métricas ni disparidad en regresión.
