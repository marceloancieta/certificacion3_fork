# Respuestas — Reto teórico Día 2 (solo instructor)

| # | Correcta | Justificación breve |
|---|----------|---------------------|
| 1 | **b** | Accuracy global "se ve bien" mientras discrimina por región. Es el ejemplo del curso: 80% norte vs 55% sur = sesgo geográfico. |
| 2 | **c** | Precision = TP / (TP + FP). La opción a es recall; la b es accuracy. |
| 3 | **a** | Regla de los 4/5: ratio entre tasas de selección < 0.8 es señal de disparate impact (ej.: 55%/80% = 0.69). |
| 4 | **d** | Es drift: la distribución de compras cambió y el modelo quedó entrenado con un mundo que ya no existe. |
| 5 | **b** | Concept drift = cambió la relación entrada→resultado. Data drift es cambio en la distribución de entrada; label drift, en la etiqueta. |
| 6 | **c** | PSI 0.10–0.25 = investigar, posible drift. < 0.10 sin cambio; > 0.25 drift confirmado. |
| 7 | **b** | Garbage in, garbage out: el modelo hereda el error silenciosamente y el promedio de accuracy lo esconde. |
| 8 | **d** | Duplicados de `customer_id` = chequeo de **unicidad** (`expect_column_values_to_be_unique`). |
| 9 | **b** | Ephemeral = Data Context en memoria, sin carpeta `gx/` ni estado persistente. Ideal para CI sin estado entre corridas. |
| 10 | **c** | MLflow es tracking: registra parámetros y métricas (en el lab, SQLite en `mlruns/mlflow.db`). No valida datos ni corrige sesgo. |
| 11 | **c** | Sin API unificada y cruzando 4 sistemas, RPA replica el proceso de punta a punta con evidencia (screenshots, logs, IDs). |
| 12 | **d** | RL: estado = pantalla, acción = click/fill, recompensa = encontrar bugs. Descubre secuencias que ningún script fijo cubriría. |
| 13 | **c** | Nivel 4 (Medido): métricas cuantitativas y decisiones basadas en datos. El nivel 5 exige mejora continua y prevención de defectos. |

**Aprobación sugerida:** 10 de 13 (~77%).
