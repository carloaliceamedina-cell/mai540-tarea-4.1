# MAI 540 — Tarea 4.1: Skill de Auditoría de Modelos

Carlo E. Alicea Medina · Atlantis University · Prof. Kevin A. Garcia Gallardo

## Contenido

| Ruta | Qué es |
|---|---|
| `.claude/skills/auditoria-modelos/SKILL.md` | La Skill (propósito, entradas, reglas, pasos, criterios V0-V6, salida) |
| `.claude/skills/auditoria-modelos/README.md` | Qué audita, cómo se invoca, cómo leer el informe, limitaciones |
| `.claude/skills/auditoria-modelos/scripts/extraer_evidencia.py` | Inventario de evidencia de solo lectura (citas estables) |
| `App_Diagnostico_Biopsias_Mama.ipynb` | Tarea 3.1 corregida + **6d**: matriz de confusión, precisión/exhaustividad/F1 de maligno y justificación de la métrica |
| `App_Comparacion_Clasificadores_Iris.ipynb` | Tarea 3.2 + **4b**: KNN (escalado en `Pipeline`, k por CV anidada) y Random Forest; tabla con cinco clasificadores |
| `auditorias/a_biopsias_original/AUDIT_REPORT_biopsias_original.md` | Informe (a): app de biopsias original con defectos |
| `auditorias/b_iris/AUDIT_REPORT_iris.md` | Informe (b): notebook de Iris con cinco clasificadores |
| `auditorias/c_tercer_proyecto/AUDIT_REPORT_tercer_proyecto.md` | Informe (c): tercer proyecto |
| `auditorias/d_biopsias_corregido/` | Ejecución final sobre un proyecto que no es ninguno de los tres |
| `auditorias/e_defecto_inyectado/` | Copia de Iris con un defecto introducido a propósito |
| `auditorias/historial_v1/` | Informes de la versión inicial de la Skill (para comparar) |
| `auditorias/ESTABILIDAD_Y_REFINAMIENTO.md` | Prueba de dos ejecuciones, fallos de la Skill y cómo se corrigieron |
| `tools/run_nb.py` | Ejecutor mínimo usado para regenerar las salidas de los notebooks |

## Notas de procedencia (importante)

- **(a) Biopsias original:** las copias subidas del notebook eran todas la versión ya corregida. El original se **reconstruyó** a partir de esa versión, que documenta ambos defectos (división sin protección en `construir_caracteristicas()` y `sesiones_tratamiento_programadas` en `COLUMNAS_PREDICTORAS`), y se le quitaron las secciones agregadas en la Tarea 3.1. Conviene reemplazarlo por el descargado del enlace de la Tarea 3.1 y volver a ejecutar la Skill.
- **(c) Tercer proyecto:** el proyecto del aula virtual no estaba disponible al hacer la tarea. Se usó un **sustituto de práctica** (Adult Income con datos sintéticos y semilla fija, la misma estructura del problema de las Tareas 1.2-2.2). Cuando esté disponible el proyecto oficial, se audita con la misma Skill y se agrega su informe.

## Reproducir

```bash
python tools/run_nb.py App_Diagnostico_Biopsias_Mama.ipynb
python tools/run_nb.py App_Comparacion_Clasificadores_Iris.ipynb
python .claude/skills/auditoria-modelos/scripts/extraer_evidencia.py auditorias/c_tercer_proyecto/App_Prediccion_Ingresos_Adult.ipynb
python auditorias/c_tercer_proyecto/evidencia/verificacion_disparidad.py
```

Los notebooks también corren en Google Colab (`scikit-learn`, `pandas`, `seaborn`, `joblib`).
