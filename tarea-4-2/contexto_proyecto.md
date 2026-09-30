# Archivo de contexto — Herramienta de regresión de costo médico (Tarea 4.2)

Adaptado del archivo de contexto de la Tarea 2.1 (Adult Income) a un problema de regresión del sector salud.

## Objetivo y alcance
- Predecir `costo_medico_anual` (USD por asegurado y año) para **planificar reservas y priorizar programas preventivos**.
- Fuera de alcance: fijar primas individuales, negar cobertura, decisiones clínicas.
- Modelos: `DummyRegressor` (media) como referencia, `LinearRegression` y `RandomForestRegressor`, todos sobre **la misma partición**.

## Reglas de tratamiento de datos
1. **Columna prohibida (fuga):** `monto_reembolsado_aseguradora`. Se conoce solo después de facturar el costo (es ≈ 70-90 % del objetivo). **Nunca** puede ser predictor, ni directa ni derivada. El notebook lo verifica con `assert`.
2. Dividir 80/20 con `random_state=42` **antes** de cualquier imputación, codificación o escalado.
3. Imputación (mediana), escalado (`StandardScaler`) y codificación (`OneHotEncoder`) solo dentro de un `Pipeline` ajustado con entrenamiento.
4. Las variables derivadas solo pueden usar valores de la misma fila: nada de estadísticas calculadas sobre el lote que se transforma.
5. Los datos son sintéticos y se generan con semilla fija dentro del notebook. No se suben datos reales de asegurados.

## Criterios de evaluación
- MSE, RMSE (USD) y R² en prueba para los tres modelos, más R² de entrenamiento para detectar sobreajuste.
- Mejora relativa del RMSE frente a la referencia trivial.
- Residuos del mejor modelo: residuos vs. predichos e histograma.
- RMSE por subgrupo (`fumador`, `region`), con umbral de disparidad ≥ 1.25× el global (n ≥ 30).

## Restricciones de seguridad
- No instalar paquetes ni descargar datos sin autorización.
- No modificar el notebook durante la auditoría: la Skill solo lee.

## Subgrupos para la auditoría
`fumador` (yes/no) y `region` (northeast, northwest, southeast, southwest).
