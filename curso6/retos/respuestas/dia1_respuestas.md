# Respuestas — Reto teórico Día 1 (solo instructor)

| # | Correcta | Justificación breve |
|---|----------|---------------------|
| 1 | **c** | Gobernanza = políticas + cobertura por riesgo + dueños de la deuda + trazabilidad auditable. No es cantidad de tests ni un % mágico. |
| 2 | **b** | Se prioriza regresión crítica, contratos de dinero/auth/datos sensibles y smoke de release. Exploratorio puro y UI volátil sin valor son mala inversión. |
| 3 | **d** | `sleep`/waits fijos y tests intermitentes (flaky) son señales clásicas de deuda técnica en la suite. Las otras opciones son señales de salud. |
| 4 | **c** | 18/200 = **0.09**. El umbral es "> 0.10", así que la alerta NO se dispara. |
| 5 | **b** | 4/25 = **0.16** > 0.12 → la alerta se dispara. |
| 6 | **c** | Effectiveness = defectos hallados en testing / defectos totales. Mide qué tanto atrapa la red antes de producción. |
| 7 | **b** | El exporter publica las métricas en `/metrics` (texto plano) para que Prometheus las lea. No pinta dashboards ni guarda histórico. |
| 8 | **d** | Prometheus hace **scrape** periódico (~10 s en el lab): entra a la URL del exporter, guarda histórico y evalúa reglas de alerta. No hay push. |
| 9 | **a** | Grafana solo **pinta** lo que Prometheus ya tiene. No almacena series ni genera métricas. |
| 10 | **c** | Kibana/Loki se mencionan para correlacionar métricas con logs (ej.: el flake subió justo después de un deploy). |
| 11 | **b** | La cadena completa del curso: **métrica + umbral + dueño + acción**. Sin dueño y acción, el dashboard es decoración. |
| 12 | **a** | "La herramienta no reemplaza la política. Sin reglas, solo tienes un cementerio más ordenado." |

**Aprobación sugerida:** 9 de 12 (75%).
