# Tarea 4.2 — Herramienta de Regresión Auditada: costo médico anual

Carlo E. Alicea Medina · MAI 540: Machine Learning · Atlantis University

Predice el **costo médico anual por asegurado (USD)** con tres modelos (referencia trivial, regresión lineal y Random Forest) sobre la misma partición, analiza los residuos y audita la herramienta con la Skill `auditoria-modelos` de la Tarea 4.1, extendida para regresión.

## Cómo ejecutarla (sin preguntar nada)

**Opción A — Google Colab**
1. Abre https://colab.research.google.com → **Archivo → Subir notebook** → elige `Herramienta_Regresion_Costos_Medicos.ipynb`.
2. **Entorno de ejecución → Ejecutar todas**. No necesita archivos externos: los datos se generan dentro del notebook con semilla 42, y Colab ya trae todas las librerías.

**Opción B — Local**
```bash
pip install numpy pandas scikit-learn matplotlib jupyter
jupyter notebook Herramienta_Regresion_Costos_Medicos.ipynb   # Kernel → Restart & Run All
```
Versión probada: scikit-learn 1.8, pandas 2.x, Python 3.11. Con la semilla fija, los resultados deben coincidir: RMSE lineal 3,597 USD y R² 0.891.

## Archivos

| Archivo | Qué es |
|---|---|
| `Herramienta_Regresion_Costos_Medicos.ipynb` | Herramienta final (corregida) |
| `contexto_proyecto.md` | Archivo de contexto: objetivo, columna prohibida, reglas, criterios |
| `AUDIT_REPORT.md` | Auditoría de la versión final, generada por la Skill sin retoques |
| `auditoria/AUDIT_REPORT_antes.md` | Auditoría antes de la corrección |
| `auditoria/AUDIT_REPORT_correccion1.md` | Auditoría de la primera corrección (detectó una fuga nueva) |
| `auditoria/AUDIT_REPORT_skill_v2.1_sin_regresion.md` | Primer intento con la Skill sin modo regresión |
| `auditoria/*_ANTES.ipynb`, `auditoria/*_CORRECCION1.ipynb` | Notebooks auditados en cada etapa |
| `auditoria/evidencia/` | Script de verificación del RMSE por subgrupo y sus salidas |
| `../claude/skills/auditoria-modelos/` | La Skill (v3, con modo regresión) |
| `docs/` | Informe técnico APA y bitácora (PDF) |

## Resultados (prueba, n = 300)

| Modelo | RMSE (USD) | R² prueba | R² entrenamiento |
|---|---|---|---|
| Referencia (media) | 10,933 | −0.010 | 0.000 |
| Regresión lineal (con interacciones fumador × IMC) | **3,597** | **0.891** | 0.879 |
| Random Forest | 3,807 | 0.878 | 0.921 |

## Datos
Son sintéticos (1,500 filas), con la estructura del dataset público *Medical Cost Personal* (`insurance.csv`), que no se pudo descargar desde el entorno de trabajo. Supuestos: el costo crece con la edad y los hijos; fumar suma unos 11,500 USD y, con IMC ≥ 30, otros 20,000 USD; el 7 % de los asegurados tiene costos extra no observados. Columna de fuga: `monto_reembolsado_aseguradora`. Subgrupos: `fumador` y `region`.

## Limitaciones
Ver la sección 7 del notebook. En resumen: no extrapolar fuera de 18-64 años, IMC 16-53 y 2,809-66,640 USD; el error es mayor en fumadores (1.33×) y en la región *northwest* (1.30×); no usar para primas individuales, cobertura ni decisiones clínicas; reentrenar con datos reales antes de cualquier uso.
