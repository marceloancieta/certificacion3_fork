# Certificación 6 — Día 2 · Contenido de diapositivas
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> 4 horas · Bloques de 45 min + descansos de 15 min
> Slides 1–52 · Proyecto: `proyectos/ml-data-quality-lab`

---

## Día 2 — IA, datos, RPA y madurez

### Slide 1 — Portada Día 2 (2 min)
**Título:** Validación continua · IA · datos · madurez TMMi
- Certificación 6 · Día 2 autónomo · 4 horas
- Reto 2 + estrategia organizacional (no requiere Docker del Día 1)

### Slide 2 — Agenda del Día 2 (2 min)
- Bloque 1: Testing IA/ML + pipelines de datos
- Bloque 2: Reto 2 práctico
- Bloque 3: RPA · simulación de usuarios · gamificación
- Bloque 4: TMMi + cierre y Q&A

---

## BLOQUE 1 (45 min) — Testing IA/ML y datos

### Slide 3 — Por qué testing de IA es distinto (4 min)
- No hay "assert igual a 200" suficiente
- Modelos: precisión, sesgo, fairness, drift
- Datos malos → modelo "correcto" que decide mal
- **Ejemplo:** modelo de crédito con accuracy 78% pero aprueba 80% del norte y 55% del sur = sesgo

### Slide 4 — Ejemplo concreto: accuracy engañosa (4 min)
- Sistema de recomendaciones pre-pandemia
- Accuracy histórica: alta. Relevancia actual: cero (drift)
- `assert accuracy > 0.75` pasaría verde mientras discrimina
- **Lección:** un solo número no cuenta la historia completa

### Slide 5 — Los tres ejes de validación (5 min)
| Eje | Pregunta | Analogía QA |
|---|---|---|
| Precisión | ¿Acertamos lo que importa? | % tests que detectan bugs reales |
| Sesgo / fairness | ¿El error castiga a un grupo? | Suite que solo cubre happy path de un perfil |
| Drift | ¿Datos de hoy ≠ entrenamiento? | Tests contra versión vieja del schema |

### Slide 6 — Sesgo y fairness: conceptos (5 min)
| Concepto | Definición | Ejemplo |
|---|---|---|
| Demographic parity | Grupos reciben decisión positiva con igual frecuencia | Aprobación ~igual entre regiones |
| Equal opportunity | Misma tasa de verdaderos positivos entre grupos | Si sos buen pagador, te aprueban sin importar región |
| Disparate impact | Ratio < 0.8 entre tasas (regla 4/5) | 55%/80% = 0.69 → señal de problema |
- En el lab: max region gap ≤ 0.25

### Slide 7 — Drift: tu modelo se vence (5 min)
| Tipo | Qué cambió | Ejemplo |
|---|---|---|
| Data drift | Distribución de entrada | Ingresos +15% por inflación |
| Concept drift | Relación entrada→resultado | Lo que predecía "buen pagador" ya no aplica |
| Label drift | Distribución de la etiqueta | Antes 30% aprobados, ahora 60% |
- Métrica del lab: PSI (Population Stability Index)
- PSI < 0.10 = ok · 0.10–0.25 = investigar · > 0.25 = reentrenar

### Slide 8 — Herramientas ML: mapa comparativo (5 min)
| Herramienta | Qué hace | Costo |
|---|---|---|
| DeepChecks | Suites validación ML (tabular/NLP/visión) | Open source + enterprise |
| MLflow | Tracking experimentos, registro de modelos | Open source |
| DVC | Versiona datasets y modelos pesados | Open source |
| SageMaker Model Monitor | Drift en producción (cloud AWS) | AWS pricing |
| Evidently AI | Reports HTML de drift y calidad | Open source |
| Whylogs | Profiling estadístico ligero | Open source |
- En el lab: MLflow + checks custom

### Slide 9 — Testing de pipelines ETL/ELT (5 min)
| Categoría | Chequeo | Ejemplo de fallo |
|---|---|---|
| Completitud | Nulos | email vacío en 5% |
| Unicidad | Duplicados | customer_id repetido → doble cobro |
| Consistencia | Rangos | age = -3 |
| Validez | Formato | email sin @ |
| Integridad ref. | FK válidas | region = "unknown_zone" |
| Frescura | Datos actualizados | Última carga hace 72h |
- Garbage in, garbage out — si ETL ensucia, modelo hereda

### Slide 10 — Herramientas de validación de datos (4 min)
| Herramienta | Approach | Mejor para |
|---|---|---|
| Great Expectations | Expectativas declarativas | Pipelines Spark/Pandas, CI |
| Deequ | Constraints sobre Spark | Ecosistema AWS/Spark |
| Soda Core | Checks en YAML | DBA/analytics |
| DBT tests | Assertions en pipeline | Si ya usan DBT |
- En el lab: GE (API real) + suite custom

### Slide 11 — Plan de testing del Reto 2 (4 min)
```
1. Validar datos (ETL) → 2. Entrenar modelo → 3. Precisión
→ 4. Fairness → 5. Drift PSI → 6. CI + MLflow
```
- Regla: si paso 1 falla, NO pasar al 2
- Datos rotos + modelo = decisiones basura con confianza alta

### Slide 12 — Integración CI/CD para datos (3 min)
- El plan vive en el pipeline, no en una laptop
- Rojo en CI = no merge del cambio de datos/modelo
- Científico cambia threshold sin querer → CI lo atrapa
- "Si no corre en CI, no es gobernanza — es hobby"

### Slide 13 — Preview del Reto 2 (3 min)
Carpeta: `proyectos/ml-data-quality-lab`
```bash
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```
- 5 tests en verde · reporte JSON · MLflow local

### Slide 14 — Cierre Bloque 1 (2 min)
- Datos + modelo + CI = trinomio del Reto 2
- Descanso y manos a la obra

---
**DESCANSO 15 MIN**
---

### Slide 15 — Volvemos · Bloque 2 Reto 2 (1 min)
**Título:** Reto 2 — Plan de testing ML + datos

---

## BLOQUE 2 (45 min) — Reto 2 práctico

### Slide 16 — Enunciado del Reto 2 (3 min)
Diseñar y ejecutar un plan que valide:
- precisión
- sesgo
- drift de datos
- integridad del pipeline ETL
Integrar resultados en pipeline CI/CD (workflow de ejemplo incluido)

### Slide 17 — Estructura del lab (3 min)
| Ruta | Para qué |
|---|---|
| `src/generate_data.py` | Datasets sintéticos |
| `src/data_quality.py` | Suite ETL (patrón GE) |
| `src/model_checks.py` | Precisión + fairness + drift |
| `src/run_pipeline.py` | Orquestador end-to-end |
| `tests/` | Tests automatizados |
| `.github/workflows/quality.yml` | CI de ejemplo |

### Slide 18 — Paso 1: entorno (7 min)
```bash
cd proyectos/ml-data-quality-lab
uv sync
```
- macOS: `brew install uv` o instalador Astral
- Windows: instalador PowerShell de uv
- Python 3.11+

### Slide 19 — Paso 2: suite ETL (8 min)
```bash
uv run pytest tests/test_data_quality.py -v
```
- Limpio pasa · sucio falla (nulos/duplicados)
- Expectativas: not_null, unique, in_set, between, regex
- Dataset sucio: 5 nulos email, 3 nulos age, 2 duplicados, 1 región inválida, 1 ingreso negativo

### Slide 20 — Paso 3: Great Expectations (7 min)
```bash
uv run pytest tests/test_gx_integration.py -v
```
- Suite ephemeral (sin carpeta `gx/`, en memoria)
- Contrato de datos ejecutable con API real de GE
- Expectativas: NotBeNull, BeUnique, BeBetween, BeInSet

### Slide 21 — Paso 4: modelo + MLflow (8 min)
```bash
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline
```
- Precisión · gap por región · PSI de income
- Tracking en SQLite local (`mlruns/mlflow.db`)
- Reporte: `data/pipeline_report.json`

### Slide 22 — Umbrales del lab (3 min)
| Chequeo | Umbral | Si falla |
|---|---|---|
| Precisión | ≥ 0.70 | No deployar modelo |
| Gap fairness | ≤ 0.25 | Investigar features |
| PSI drift | ≤ 0.25 | Reentrenar con datos frescos |

### Slide 23 — Paso 5: CI (5 min)
- Abrir `.github/workflows/quality.yml`
- Mismos comandos que en local
- Push/PR → uv sync → pytest → run_pipeline → artifact
- "Si no corre en CI, no es gobernanza"

### Slide 24 — Debrief Reto 2 (5 min)
- ¿Qué fallaría primero en su empresa: datos o modelo?
- ¿Quién es dueño del umbral de drift?
- Si solo un gate en CI: ¿ETL o modelo?
- Puente al Bloque 3: procesos de negocio y RPA

---
**DESCANSO 15 MIN**
---

### Slide 25 — Volvemos · Bloque 3 (1 min)
**Título:** RPA · simulación de usuarios · gamificación

---

## BLOQUE 3 (45 min) — RPA, simulación y formación

### Slide 26 — RPA: qué es y qué no es (4 min)
- Robotic Process Automation: bots que interactúan con UIs como un humano
- Para testing: complementa donde el proceso completo es el SUT
- NO reemplaza API/UI testing cuando hay endpoints disponibles
- Es para cuando el sistema bajo prueba cruza 3-4 aplicaciones sin API unificada

### Slide 27 — ¿Cuándo RPA para testing? (5 min)
| Escenario | Por qué RPA | Por qué NO API testing |
|---|---|---|
| Proceso cruza SAP + Excel + email + portal | No hay API unificada | 4 APIs distintas (si existen) |
| Backoffice legacy solo con UI | Solo UI disponible | No expone API |
| Flujo contable mensual | Proceso humano → bot replica | No hay endpoint "cerrar mes" |
| Smoke de ERP post-deploy | Validación visual | API no cubre validaciones de UI |

### Slide 28 — ¿Cuándo NO usar RPA? (3 min)
- Cuando existe una API testeable → usá API testing
- UI cambia frecuentemente sin valor → tests frágiles
- Solo validar regla de negocio → unit test
- Criterio: ¿el valor está en el proceso E2E o en un endpoint?

### Slide 29 — Ecosistema RPA (5 min)
| Plataforma | Fortaleza | Debilidad | Ideal para |
|---|---|---|---|
| UiPath | Community gratis, buen recorder | Pesado, licencias enterprise caras | Procesos multi-sistema complejos |
| Power Automate | Integrado con M365, bajo costo | Menos flexible fuera de Microsoft | Orgs 100% Microsoft |
| Automation Anywhere | Cloud-native, escalable | Menos intuitivo | Muchos bots en paralelo |
| Robot Framework | Open source, extensible | Requiere programación | Equipos técnicos con control |
- Criterio: stack IT + licencias + observabilidad + skills del equipo

### Slide 30 — Caso 1: alta de cliente (banco) (4 min)
1. Bot abre portal de onboarding
2. Llena formulario con datos de prueba
3. Sube documentos mock
4. Verifica estado → "Pendiente de revisión"
5. Evidencia: screenshot + ID transacción + timestamp
- Clave: si el bot "pasa" sin evidencia, no hay auditoría

### Slide 31 — Caso 2: conciliación de pagos (4 min)
1. Bot descarga CSV del banco
2. Compara contra ERP
3. Identifica discrepancias (montos, fechas, IDs)
4. Genera reporte de diferencias
5. Diferencia > umbral → alerta automática
- Clave: la validación es en los datos, el bot es el vehículo

### Slide 32 — Caso 3: smoke post-deploy nocturno (3 min)
1. Deploy a prod 2:00 AM
2. Bot ejecuta 5 flujos críticos 2:15 AM
3. Falla → rollback + alerta | Pasa → deploy "verified"
- Sin personas de madrugada, sin riesgo de "nadie lo probó"

### Slide 33 — Simulación de usuarios con IA (5 min)
Evolución:
```
Script fijo → Caminos probables → Política aprendida (RL)
```
| Nivel | Técnica | Qué encuentra |
|---|---|---|
| 1 | Script fijo | Bugs en happy path |
| 2 | Exploración guiada + datos random | Bugs de boundary |
| 3 | Model-based (máquina de estados) | Bugs de flujo/estado |
| 4 | Reinforcement Learning | Bugs que nadie imaginaría probar |

### Slide 34 — RL aplicado a testing (4 min)
- Estado = pantalla actual + DOM
- Acción = click, fill, scroll, navigate
- Recompensa = encontrar crash / error 500 / estado inconsistente
- Política = agente aprende qué secuencias maximizan bugs
- Requisito: telemetría ética + anonimización
- Emergente: LLMs que generan escenarios a partir de specs

### Slide 35 — Gamificación: por qué funciona (4 min)
| Tradicional | Gamificado |
|---|---|
| PDF de 40 páginas | Reto con score automático |
| "Lean este estándar" | "Bajen flake bajo 0.08 en 20 min" |
| Examen múltiple opción | Lab ejecutable con pytest |
| Feedback en 2 semanas | Feedback en 2 segundos |
- Los Retos 1 y 2 ya son gamificación seria

### Slide 36 — Plataformas de referencia (3 min)
| Plataforma | Qué ofrece | Gratis |
|---|---|---|
| Test Automation University | Selenium, API, visual AI | Sí |
| Codecademy | Python, SQL interactivo | Freemium |
| Ministry of Testing | Comunidad + cursos QA | Membresía |
| Killercoda | Labs en browser, entornos reales | Algunos gratis |
- 5 reglas de un buen reto: objetivo medible, score auto, feedback inmediato, dificultad progresiva, contexto realista

### Slide 37 — Mini-caso integrado (5 min)
```
RPA (carga) → GE (ETL) → ML (decisión) → Dashboard (alerta)
```
Proceso de crédito: 4 capas, 4 tipos de testing
- **Pregunta:** ¿dónde pondrían el primer control si solo pueden elegir uno?
- Variantes: ¿y si el bot ingresa datos mal? ¿Si GE aprueba pero hay drift?

### Slide 38 — Cierre Bloque 3 (2 min)
- Personas + procesos + datos + modelos
- RPA: complemento donde el proceso E2E es el SUT
- RL/simulación: el futuro del testing exploratorio
- Falta TMMi: el marco que ordena la evolución

---
**DESCANSO 15 MIN**
---

### Slide 39 — Volvemos · Bloque 4 (1 min)
**Título:** TMMi · madurez · cierre

---

## BLOQUE 4 (45 min) — TMMi y estrategia

### Slide 40 — ¿Qué es TMMi? (4 min)
- Test Management Maturity Model Integration
- No es herramienta: es mapa de madurez organizacional
- Analogía: CMMI para desarrollo, TMMi para testing
- Para: dejar de opinar y empezar a medir nivel

### Slide 41 — Los 5 niveles (6 min)
| Nivel | Nombre | Señales típicas |
|---|---|---|
| 1 | Inicial | "Lo pruebo yo antes de subir" |
| 2 | Gestionado | Test plan existe, no siempre se sigue |
| 3 | Definido | Todos usan mismo framework y proceso |
| 4 | Medido | Dashboards con flake/leakage/coverage |
| 5 | Optimizado | CI gates + feedback loops automáticos |
- Día 1 → nivel 4 · Retos CI → nivel 5

### Slide 42 — Prácticas por nivel (5 min)
| Nivel | Áreas de proceso | Implementación |
|---|---|---|
| 2 | Política, planificación | Documento + plan por release |
| 3 | Organización, formación, ciclo | Roles, onboarding, testing integrado |
| 4 | Medición, evaluación | Métricas con umbral, evaluación cuantitativa |
| 5 | Prevención, optimización | Root cause analysis, feedback auto |

### Slide 43 — Auto-evaluación rápida (5 min)
5 preguntas: política escrita, métricas con umbral, CI integrado, decisiones basadas en datos, feedback loop
- Mayoría 1-2: priorizar política + herramientas
- Mayoría 3: priorizar métricas + observabilidad
- Mayoría 4-5: priorizar prevención + optimización

### Slide 44 — Marcos complementarios (3 min)
| Marco | Enfoque | Relación con TMMi |
|---|---|---|
| CMMI | Desarrollo | TMMi es el complemento testing |
| ISO 29119 | Estándar de testing | Define procesos; TMMi mide madurez |
| ISTQB | Certificación individual | Personas; TMMi evalúa organización |
| SAFe | Agilidad escalada | Testing embebido; TMMi audita calidad |

### Slide 45 — Dashboards como herramienta de madurez (4 min)
```
Nivel 1-2: sin métricas compartidas
Nivel 3:   métricas en silos
Nivel 4:   dashboard centralizado (Prometheus + Grafana)
Nivel 5:   dashboard + alertas + acciones automáticas
```
- Lo que construimos en Día 1 = nivel 4 observable

### Slide 46 — Estrategia sostenible (cadena completa) (4 min)
| # | Componente | Día | Nivel |
|---|---|---|---|
| 1 | Políticas | 1 | 2-3 |
| 2 | Métricas con umbral | 1 | 4 |
| 3 | Observabilidad | 1 | 4 |
| 4 | Datos + ML validados | 2 | 4-5 |
| 5 | RPA + gamificación | 2 | 3-5 |
| 6 | Madurez TMMi | 2 | meta |

### Slide 47 — Tablero de decisión (5 min)
| Si duele… | Empezá por… | Herramienta |
|---|---|---|
| CI rojo por flake | Bajar flake rate | Dashboard + quarantine |
| Bugs en prod | Leakage + riesgo | Cobertura + alertas |
| Modelo injusto | Fairness + datos | GE + fairness checks |
| Proceso manual frágil | RPA | UiPath / Power Automate |
| Nadie sabe el estado | Dashboard | Prometheus + Grafana |
| Datos sucios al modelo | Gate ETL en CI | GE + pipeline gate |
| Equipo no mejora | Gamificación + TMMi | Retos + auto-evaluación |

### Slide 48 — Consolidación Reto 1 + Reto 2 (3 min)
- Reto 1: calidad del sistema de pruebas (observable)
- Reto 2: calidad de datos y modelo (validada en CI)
- Juntos: gobernanza de punta a punta

### Slide 49 — Casos y dudas (8 min)
- Discutir situaciones reales del grupo
- Regla: toda respuesta anclada a métrica, política o evidencia
- Casos provocadores si la sala está callada:
  - "90% cobertura = estamos bien" → ¿qué responderían?
  - "Nadie revisa fairness post-deploy" → ¿qué control mínimo?
  - "Queremos implementar todo a la vez" → ¿por dónde según TMMi?

### Slide 50 — Checklist final (3 min)
- [ ] Sé explicar flake, leakage y effectiveness
- [ ] Levanté el dashboard QA
- [ ] Corrí el lab de datos/ML
- [ ] Ubico RPA, simulación y gamificación en la estrategia
- [ ] Relaciono todo con un nivel TMMi

### Slide 51 — Cierre y siguientes pasos (3 min)
- Lleven un umbral y un dueño a su trabajo el lunes
- Publiquen al menos una métrica donde todo el equipo la vea
- Madurez no es un certificado: es un hábito medible

### Slide 52 — Gracias
**Título:** Certificación 6 — cierre
- Materiales en `curso6/dia2/`
- Proyecto en `proyectos/ml-data-quality-lab`
- Gobiernen con evidencia
