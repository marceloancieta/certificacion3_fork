# Reto teórico — Día 1: Gobernanza, métricas y dashboards

> **Formato:** 12 preguntas de selección única (una correcta, tres incorrectas).
> **Tiempo sugerido:** 20–25 minutos · **Aprobación sugerida:** 9 de 12 (75%).
> Las respuestas están en `respuestas/dia1_respuestas.md` (solo instructor).

---

**1.** ¿Cuál de estas opciones describe mejor la gobernanza de pruebas?

- a) Tener la mayor cantidad posible de tests automatizados
- b) Alcanzar un porcentaje de cobertura de código superior al 90%
- c) Políticas de qué se automatiza, criterios ligados a riesgo, dueños de la deuda y trazabilidad auditable
- d) Delegar las decisiones de calidad en la herramienta de gestión de casos

**2.** Según el criterio de cobertura por riesgo, ¿qué deberías automatizar con prioridad?

- a) Pruebas exploratorias puras
- b) Regresión crítica, contratos de dinero/auth/datos sensibles y smoke de release
- c) Toda la UI, incluida la que cambia cada semana sin valor de negocio
- d) Los casos manuales completos, sin filtrar por riesgo

**3.** ¿Cuál de estas señales indica deuda técnica en la suite de pruebas?

- a) La suite corre en cada pull request
- b) Los locators están centralizados en un solo lugar
- c) La suite completa termina en menos de 10 minutos
- d) Hay `sleep` / esperas fijas y tests que a veces pasan y a veces fallan

**4.** Un servicio ejecutó 200 tests y 18 resultaron flaky. Con umbral de alerta "flake rate > 0.10", ¿qué ocurre?

- a) Flake rate = 0.18 y la alerta se dispara
- b) Flake rate = 0.09 y la alerta se dispara
- c) Flake rate = 0.09 y la alerta NO se dispara
- d) Flake rate = 0.11 y la alerta se dispara

**5.** En un release hubo 25 defectos totales y 4 se encontraron en producción. Con umbral "leakage > 0.12":

- a) Leakage = 0.04 → no dispara alerta
- b) Leakage = 0.16 → dispara alerta
- c) Leakage = 0.84 → dispara alerta
- d) Leakage = 0.16 → no dispara alerta

**6.** ¿Qué mide el *test effectiveness ratio*?

- a) El porcentaje de código cubierto por la suite
- b) La velocidad promedio de ejecución de la suite
- c) La proporción de defectos encontrados en testing sobre el total de defectos
- d) La proporción de tests automatizados sobre tests manuales

**7.** En el stack del laboratorio, ¿cuál es el rol del **exporter**?

- a) Pintar los dashboards con gráficos e histórico
- b) Publicar las métricas de QA en una URL (`/metrics`) para que otro sistema las lea
- c) Guardar el histórico de series de tiempo y evaluar reglas
- d) Ejecutar rollbacks automáticos cuando una métrica se rompe

**8.** ¿Cómo obtiene Prometheus las métricas del exporter?

- a) El exporter le hace *push* a Prometheus cada vez que cambia un valor
- b) Grafana copia los valores del exporter hacia Prometheus
- c) Prometheus las lee una única vez al arrancar
- d) Prometheus hace *scrape* periódico a la URL del exporter, guarda histórico y evalúa alertas

**9.** ¿Cuál es el rol de **Grafana** en el stack?

- a) Visualizar lo que Prometheus ya tiene almacenado
- b) Almacenar las series de tiempo con su histórico
- c) Generar las métricas de QA de cada servicio
- d) Reemplazar a Prometheus cuando hay muchas alertas

**10.** ¿Para qué se mencionan **Kibana / Loki** en la arquitectura (a nivel de concepto)?

- a) Para sustituir a Grafana en la capa de visualización
- b) Para calcular el flake rate de cada servicio
- c) Para correlacionar métricas con logs (por ejemplo: el flake subió después de un deploy)
- d) Para gestionar los casos de prueba y sus ciclos

**11.** Una métrica publicada en un dashboard solo genera mejora real cuando se completa la cadena:

- a) métrica + gráfico + refresco automático
- b) métrica + umbral + dueño + acción
- c) métrica + herramienta + licencia enterprise
- d) métrica + auditoría anual + reporte PDF

**12.** Un equipo compra TestRail, Zephyr o Allure TestOps pero no define políticas de automatización. ¿Qué es lo más probable?

- a) La herramienta ordena los casos, pero sin políticas no hay gobernanza
- b) La herramienta define las políticas automáticamente
- c) El test effectiveness sube por usar una herramienta reconocida
- d) La deuda técnica de pruebas desaparece al migrar los casos
