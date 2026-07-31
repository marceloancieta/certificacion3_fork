# Reto teórico — Día 2: Testing de ML, datos, RPA y madurez

> **Formato:** 13 preguntas de selección única (una correcta, tres incorrectas).
> **Tiempo sugerido:** 25–30 minutos · **Aprobación sugerida:** 10 de 13 (~77%).
> Las respuestas están en `respuestas/dia2_respuestas.md` (solo instructor).

---

**1.** Un modelo de crédito tiene accuracy global de 78%, pero aprueba al 80% de solicitantes del norte y solo al 55% del sur. ¿Cuál es el problema principal?

- a) La accuracy es demasiado baja para producción
- b) Hay sesgo geográfico que la accuracy global no revela
- c) El modelo necesita más datos de entrenamiento del norte
- d) No hay problema: 78% de accuracy es aceptable

**2.** ¿Cuál es la fórmula de **precisión** (precision)?

- a) Verdaderos positivos / (verdaderos positivos + falsos negativos)
- b) (Verdaderos positivos + verdaderos negativos) / total de casos
- c) Verdaderos positivos / (verdaderos positivos + falsos positivos)
- d) Falsos positivos / (falsos positivos + verdaderos negativos)

**3.** Según la regla de los 4/5 (*disparate impact*), ¿cuándo hay señal de problema de fairness?

- a) Cuando el ratio entre tasas de selección de dos grupos es menor a 0.8
- b) Cuando la accuracy de un grupo supera 0.8
- c) Cuando el modelo aprueba a más del 80% de los solicitantes
- d) Cuando el ratio entre tasas de selección es mayor a 0.8

**4.** Un sistema de recomendaciones entrenado pre-pandemia sigue sugiriendo viajes internacionales a clientes que hoy solo compran local. ¿Qué fenómeno describe esto?

- a) Sampling bias en el set de test
- b) Overfitting del modelo a los datos de entrenamiento
- c) Un problema de fairness entre grupos de clientes
- d) Drift: los datos actuales ya no se parecen a los del entrenamiento

**5.** ¿Qué tipo de drift ocurre cuando la relación entrada→resultado cambió (lo que antes predecía "buen pagador" ya no aplica)?

- a) Data drift (covariate shift)
- b) Concept drift
- c) Label drift
- d) Sampling drift

**6.** Se mide el PSI de la variable `income` entre referencia y datos actuales y da **0.18**. ¿Qué interpretación corresponde?

- a) Sin cambio significativo, continuar normal
- b) Drift confirmado, reentrenar de inmediato
- c) Zona de investigación: posible drift (entre 0.10 y 0.25)
- d) El valor es inválido: el PSI solo puede estar entre 0 y 0.10

**7.** Un ETL deja pasar 5% de nulos en `income` y el modelo de crédito entrena con esos datos. ¿Cuál es el riesgo principal?

- a) El pipeline de CI se cae con un error de sintaxis
- b) El modelo hereda el error y nadie lo nota porque la accuracy "se ve bien" en promedio
- c) MLflow no puede registrar los experimentos con datos nulos
- d) Great Expectations borra automáticamente los registros nulos

**8.** Encuentras registros con `customer_id` repetido en el dataset. ¿Qué categoría de chequeo de calidad de datos lo detecta?

- a) Completitud
- b) Frescura
- c) Validez de formato
- d) Unicidad

**9.** En el lab, Great Expectations se usa con un contexto **ephemeral**. ¿Qué significa?

- a) Las expectativas se validan una sola vez y luego se borran del código
- b) El contexto vive en memoria: sin carpeta `gx/` ni estado persistente, ideal para CI
- c) Solo funciona con datasets de menos de 1000 registros
- d) Las validaciones expiran después de 24 horas

**10.** ¿Cuál es el rol de **MLflow** en el pipeline del lab?

- a) Validar la calidad de los datos de entrada (nulos, duplicados, rangos)
- b) Calcular el PSI entre distribución de referencia y actual
- c) Registrar parámetros y métricas de los experimentos (tracking)
- d) Detectar y corregir el sesgo del modelo automáticamente

**11.** Un proceso de negocio cruza SAP + Excel + email + un portal web sin API unificada. ¿Qué approach de validación conviene?

- a) Unit tests sobre las reglas de negocio de cada sistema
- b) API testing integrando los cuatro sistemas
- c) RPA: un bot que replica el flujo de punta a punta y captura evidencia
- d) Tests de carga con K6 sobre el portal web

**12.** En la progresión de simulación de usuarios, ¿qué aporta el nivel de **Reinforcement Learning** frente al script fijo?

- a) Ejecuta el mismo happy path pero más rápido
- b) Reduce el costo de licencias de las herramientas de grabación
- c) Garantiza 100% de cobertura de código en la UI
- d) Un agente aprende qué secuencias de acciones maximizan bugs encontrados, incluyendo casos que nadie imaginaría probar

**13.** Un equipo tiene dashboards centralizados con flake, leakage y cobertura, y toma decisiones basadas en esos datos, pero aún no tiene mejora continua ni prevención automatizada de defectos. ¿En qué nivel TMMi está?

- a) Nivel 2 — Gestionado
- b) Nivel 3 — Definido
- c) Nivel 4 — Medido
- d) Nivel 5 — Optimizado
