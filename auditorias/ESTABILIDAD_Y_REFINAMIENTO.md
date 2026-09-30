# Estabilidad y refinamiento de la Skill `auditoria-modelos`

## 1. Prueba de estabilidad: dos ejecuciones sobre el mismo proyecto (tercer proyecto)

| ID | v1 · ejecución 1 | v1 · ejecución 2 | v2 · ejecución 1 | v2 · ejecución 2 |
|---|---|---|---|---|
| V1.1 | PASA | PASA | PASA | PASA |
| V1.2 | PASA ⚠ | PASA ⚠ | NSPD | NSPD |
| V1.3 | FALLA | FALLA | FALLA | FALLA |
| V1.4 | FALLA | FALLA | FALLA | FALLA |
| V2.1-V2.4 | FALLA ×4 | FALLA ×4 | FALLA ×4 | FALLA ×4 |
| **V3.1** | FALLA | FALLA | FALLA | FALLA |
| **V3.2** (`capital_gain`) | **FALLA** | **PASA** | PASA | PASA |
| V4.1 | FALLA | FALLA | FALLA | FALLA |
| V4.2 | NSPD | NSPD | FALLA (0.302 vs. 0.485) | FALLA (0.302 vs. 0.485) |
| V0.1, V2.5, V5.2, V6.1, V6.2 | *(no existían)* | — | PASA, NSPD, PASA, PASA, NSPD | ídem |

- **Veredicto inestable en v1:** V3.2 cambió de FALLA a PASA entre ejecuciones. El criterio v1 ("ninguna columna predictora describe algo que solo se conocería después de la predicción") no dice qué evidencia decide. La ejecución 1 razonó por dominio y por la Tarea 2.1 (donde `capital-gain` se había prohibido); la ejecución 2 razonó por el código que genera los datos. Las dos lecturas cumplen el texto v1.
- **Corrección (refinamiento 2, commit `c42e67d`):** V3.2 pasó a ser una tabla de decisión con un criterio temporal. FALLA solo si la columna se deriva del objetivo en el código o la descripción dice que se registra después del resultado; la sospecha sin evidencia es NSPD. Además, el script de inventario detecta `derivada_de_otra_columna`.
- **Evidencia de mejora:** con la v2, las dos ejecuciones producen los mismos 18 veredictos. El inventario de evidencia es determinista: dos ejecuciones dan el mismo SHA-256 (`efaf6180…6dc6d`). Así, las citas `celda N (id X), l. L` coinciden entre ejecuciones; en la v1 la numeración de celdas quedaba a criterio del auditor.
- **Aviso honesto:** las cuatro ejecuciones las hizo Claude en la misma sesión de trabajo, no instancias independientes. La inestabilidad de la v1 demuestra que el texto admitía dos veredictos válidos, no que un modelo "cambió de opinión" al azar. Una prueba más fuerte sería ejecutar la Skill en sesiones nuevas de Claude Code y comparar (pendiente para la Tarea 4.2).

## 2. Registro de fallos de la Skill y refinamientos

| # | Proyecto | Tipo de fallo (v1) | Qué pasó | Cambio en SKILL.md | Commit | Evidencia de mejora |
|---|---|---|---|---|---|---|
| 1 | biopsias_original | Veredicto sin evidencia (falso PASA) | V1.1 y V1.2 = PASA aunque la celda 9 terminó en `ValueError` y no se imprimió ninguna métrica | Regla "sin evidencia no hay PASA", V0.1 (ejecución) que fuerza NSPD, formato de cita estable, script de inventario | `16f083b` | v2: V0.1 FALLA, V1.1/V1.2 NSPD |
| 2 | iris | Falso positivo | V1.3 FALLA: 3 clases de 0.333 < umbral fijo 0.40 | Desbalance relativo a K: p_min < 0.8/K | `c42e67d` | v2: V1.3 PASA con evidencia [50, 50, 50] |
| 3 | iris | Falso positivo | V3.1 FALLA por `fit(X, y)` en celdas 4-6 y 13, que son modelo final y accuracy de entrenamiento rotulada | Aclaración de V3.1: solo cuentan las métricas de generalización | `c42e67d` | v2: V3.1 PASA citando celda 9 (clonado idéntico) |
| 4 | tercer_proyecto | Veredicto que varía | V3.2 FALLA/PASA entre ejecuciones | Criterio temporal y NSPD para la sospecha | `c42e67d` | v2: PASA en ambas ejecuciones |
| 5 | biopsias_original | Omisión | No detectó la división entre cero, la validación definida y nunca llamada ni el `rng` global | V6.1, V6.2, V5.2 | `978520f` | v2: V6.1, V6.2 y V5.2 = FALLA |
| 6 | todos | Umbral sin justificar | V4.2 con 0.10 sin tamaño mínimo | 0.05 o cociente < 0.80, n ≥ 30, verificación reproducida | `978520f` | v2 detecta la brecha en `Female` (−0.184) |
| 7 | iris con defecto inyectado | Omisión | Detectó el escalado global, pero no el k fijado a mano rotulado "por CV" | V2.5 | `ae67998` | v2 + V2.5: FALLA con evidencia |
| 8 | biopsias_corregido (proyecto extra) | Ambigüedad | ¿Es FALLA en V3.2 la demo "con fuga" rotulada? Hubo que decidirlo fuera del SKILL.md | Alcance de V3.2 (modelo reportado/desplegado) | `fe73cdc` | La regla ahora está en el archivo |
