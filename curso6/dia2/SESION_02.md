# Día 2 — Testing IA/ML, datos, RPA y madurez TMMi

> **Duración:** 4 horas · **Ritmo:** Bloque A (45) → descanso 15 → B (45) → descanso 15 → C (45) → descanso 15 → D (45)
> **Lo que vas a construir:** un plan de testing ejecutable para datos ETL + modelo ML (Great Expectations, precisión/sesgo/drift, MLflow) integrado a un pipeline CI de ejemplo.
> **Este día es autónomo:** no necesitás tener Docker ni el lab del Día 1 levantados.

---

## Antes de empezar

### Requisitos

| Herramienta | Windows | macOS |
|-------------|---------|-------|
| Python 3.11+ | [python.org](https://www.python.org/downloads/) o Store | `brew install python` |
| **uv** (recomendado) | Ver abajo | Ver abajo |
| Git | Opcional pero útil | Opcional pero útil |
| Editor | VS Code / Cursor | VS Code / Cursor |

### Instalar `uv`

**Windows (PowerShell):**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Cerrá y reabrí la terminal. Verificá:

```powershell
uv --version
```

**macOS:**

```bash
brew install uv
# o:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
uv --version
```

### Arranque del laboratorio

```bash
# Desde la carpeta del Día 2
cd curso6/dia2/proyectos/ml-data-quality-lab

# 1) Instala dependencias en un entorno local del proyecto
uv sync

# 2) Corre la suite
uv run pytest -v
```

**Resultado esperado:** `5 passed`.

Si falla aquí, **paré** y mirá [Errores comunes](#errores-comunes).

---

## Agenda

| Bloque | Duración | Contenido |
|--------|----------|-----------|
| **A** | 45 min | Testing de IA/ML + pipelines de datos (ETL) |
| Descanso | 15 min | ☕ |
| **B** | 45 min | **Reto 2:** plan de testing ML/datos + CI |
| Descanso | 15 min | ☕ |
| **C** | 45 min | RPA · simulación de usuarios · gamificación |
| Descanso | 15 min | ☕ |
| **D** | 45 min | TMMi, estrategia de madurez y cierre |

Material de apoyo:
- Diapositivas: `ppt_contenido.md` / `dia2.pptx`
- Guion del instructor: `instructor_guide.md`

---

## Bloque A — Testing IA/ML y pipelines de datos (45 min)

### 1. Por qué testing de IA es distinto

En APIs un `assert status_code == 200` te salva mucho.
En IA **no alcanza**:

- Un modelo puede "andar" y ser injusto (sesgo / fairness)
- Puede quedar viejo por **drift** (los datos de hoy no se parecen a los de entrenamiento)
- Si el **ETL** ensucia, el modelo hereda el bug con sonrisa de accuracy

**Ejemplo concreto:** un modelo de aprobación de crédito entrenado con datos de 2022 aprueba al 80% de los solicitantes del norte pero solo al 55% del sur. Accuracy global: 78%. ¿Está bien? No — hay sesgo geográfico. Un `assert accuracy > 0.75` pasaría verde mientras discrimina.

**Otro ejemplo:** un sistema de recomendaciones entrenado con datos pre-pandemia. Hoy la distribución de compras cambió (drift), pero el modelo sigue sugiriendo viajes internacionales a clientes que ahora solo compran local. Accuracy histórica: alta. Relevancia actual: cero.

### 2. Validación de modelos — los tres ejes

| Eje | Pregunta que responde | Analogía QA tradicional |
|-----|------------------------|-------------------------|
| **Precisión** | ¿Acertamos lo que importa? | Como medir % de tests que detectan bugs reales |
| **Sesgo / fairness** | ¿El error castiga a un grupo? | Como si tu suite solo cubriera el happy path de un perfil de usuario |
| **Drift** | ¿Hoy ya no nos parecemos al entrenamiento? | Como correr tests contra una versión vieja del API schema |

#### Precisión (y por qué no basta sola)

```
Precision = verdaderos positivos / (verdaderos positivos + falsos positivos)
```

Un modelo puede tener precision 0.95 en datos de test y fallar en producción porque:
- Los datos de test no representan al mundo real (sampling bias)
- La distribución cambió (temporal drift)
- Un grupo minoritario tiene precision 0.60 (fairness issue)

#### Sesgo y fairness — conceptos clave

| Concepto | Definición práctica | Ejemplo |
|----------|---------------------|---------|
| **Demographic parity** | Todos los grupos reciben la decisión positiva con igual frecuencia | Aprobación de crédito ~igual entre regiones |
| **Equal opportunity** | Todos los grupos tienen igual tasa de verdaderos positivos | Si sos buen pagador, te aprueban sin importar región |
| **Disparate impact** | Ratio entre tasas de selección; < 0.8 es señal de problema (regla de los 4/5) | Sur: 55% aprobados / Norte: 80% = ratio 0.69 → señal |

En el lab medimos **max region gap**: la diferencia entre la tasa de aprobación más alta y la más baja entre regiones. Si ese gap supera 0.25, el modelo falla el umbral de fairness.

#### Drift — tu modelo se vence como la leche

| Tipo de drift | Qué cambió | Ejemplo |
|---------------|-----------|---------|
| **Data drift** (covariate shift) | La distribución de entrada cambió | Ingresos subieron 15% por inflación |
| **Concept drift** | La relación entrada→resultado cambió | Lo que antes predecía "buen pagador" ya no aplica |
| **Label drift** | La distribución de la etiqueta cambió | Antes 30% aprobados, ahora 60% |

**Cómo medimos drift en el lab:** PSI (*Population Stability Index*).

```
PSI = Σ (% actual - % referencia) × ln(% actual / % referencia)
```

| PSI | Interpretación |
|-----|----------------|
| < 0.10 | Sin cambio significativo |
| 0.10 – 0.25 | Investigar — posible drift |
| > 0.25 | Drift confirmado — reentrenar o alertar |

### 3. Herramientas del ecosistema (mapa comparativo)

| Herramienta | Qué hace | Cuándo usarla | Costo |
|-------------|----------|---------------|-------|
| **DeepChecks** | Suites de validación ML (tabular + NLP + visión) | Validación pre-deploy y monitoreo | Open source + enterprise |
| **MLflow** | Tracking de experimentos, registro de modelos, serving | Siempre que entrenes modelos — es el "Git de ML" | Open source |
| **DVC** (Data Version Control) | Versiona datasets y modelos pesados fuera de Git | Datasets > 100 MB o modelos binarios | Open source |
| **Amazon SageMaker Model Monitor** | Drift en producción (cloud) | Si ya estás en AWS y tu modelo está en SageMaker | AWS pricing |
| **Evidently AI** | Reports HTML de drift, calidad de datos y performance | Alternativa visual a DeepChecks | Open source |
| **Whylogs** | Profiling estadístico ligero (genera "profiles" sin guardar datos) | Monitoreo en streaming o batch con privacidad | Open source |

**Para el lab usamos:** MLflow (tracking) + chequeos de modelo custom (precisión, fairness, PSI). No instalamos DeepChecks ni SageMaker porque el objetivo es entender el plan de testing, no la herramienta específica.

### 4. Testing de pipelines ETL/ELT

**ETL** = Extract, Transform, Load. **ELT** = Extract, Load, Transform (el orden cambia pero la validación no).

Chequeos típicos de calidad de datos:

| Categoría | Chequeo | Ejemplo de fallo |
|-----------|---------|------------------|
| **Completitud** | Valores nulos | `email` vacío en 5% de registros |
| **Unicidad** | Duplicados | `customer_id` repetido → doble cobro |
| **Consistencia** | Valores en rango | `age = -3` o `age = 250` |
| **Validez** | Formato correcto | `email = "no es un email"` |
| **Integridad referencial** | FK válidas | `region = "unknown_zone"` no está en catálogo |
| **Frescura** | Datos actualizados | Última carga hace 72h cuando debería ser diaria |

**¿Por qué importa tanto?** Garbage in, garbage out. Si el ETL deja pasar un 5% de nulos en `income`, tu modelo de crédito entrena con datos incompletos y las predicciones heredan ese error — pero nadie se entera porque accuracy "se ve bien" en promedio.

### 5. Herramientas de validación de datos (comparativa)

| Herramienta | Approach | Lenguaje | Mejor para |
|-------------|----------|----------|------------|
| **Great Expectations** | "Expectativas" declarativas sobre DataFrames | Python | Pipelines Spark/Pandas, CI/CD |
| **Deequ** | Constraints + análisis sobre Spark | Scala/Java | Equipos en ecosistema AWS/Spark |
| **Soda Core** | Checks en YAML contra cualquier BD | YAML + Python | DBA/analytics que no programan mucho |
| **DBT tests** | Assertions dentro del pipeline de transformación | SQL + YAML | Si ya usan DBT para sus transformaciones |

**En el lab usamos:** Great Expectations (API real) + una suite custom que imita el patrón GE para enseñar el concepto sin overhead de configuración.

### 6. El plan de testing que vamos a ejecutar

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ 1. Validar  │────▶│ 2. Entrenar  │────▶│ 3. Medir    │
│    datos    │     │    modelo    │     │  precisión  │
│   (ETL)     │     │              │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                    ┌──────────────┐     ┌──────▼──────┐
                    │ 5. Medir     │◀────│ 4. Medir    │
                    │   drift PSI  │     │  fairness   │
                    └──────┬───────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │ 6. Publicar │
                    │  CI + MLflow│
                    └─────────────┘
```

**Regla de oro:** si el paso 1 (datos) falla, **no** pasar al paso 2. Datos rotos + modelo = decisiones basura con confianza alta.

### 7. Preview de comandos del lab

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```

### Checklist rápido del Bloque A

- [ ] Sé explicar por qué accuracy sola no alcanza en ML
- [ ] Puedo nombrar los tres ejes: precisión, fairness, drift
- [ ] Entiendo qué mide PSI y sus umbrales (0.10 / 0.25)
- [ ] Distingo ETL vs ELT y nombro al menos 4 chequeos de datos
- [ ] Ubico Great Expectations, DeepChecks y MLflow en el mapa

---

## Bloque B — Reto 2: plan de testing ML + datos (45 min)

### Enunciado

Diseñar y ejecutar un plan que valide:

- precisión
- sesgo
- drift de datos
- integridad del pipeline ETL

…integrando resultados en un pipeline CI/CD (workflow de ejemplo incluido).

Carpeta del lab: `proyectos/ml-data-quality-lab`

### Estructura del lab (orientación)

| Ruta | Para qué |
|------|----------|
| `src/generate_data.py` | Datasets sintéticos: limpio, sucio y referencia |
| `src/data_quality.py` | Suite ETL estilo Great Expectations |
| `src/model_checks.py` | Precisión, fairness proxy, drift + MLflow |
| `src/run_pipeline.py` | Pipeline end-to-end (orquesta todo) |
| `tests/test_data_quality.py` | Tests del ETL (limpio pasa, sucio falla) |
| `tests/test_gx_integration.py` | Suite con la API real de Great Expectations |
| `tests/test_model_checks.py` | Valida umbrales del modelo |
| `.github/workflows/quality.yml` | Ejemplo de CI con GitHub Actions |

### Paso 1 — Entorno

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab
uv sync
```

### Paso 2 — Suite ETL (patrón Great Expectations)

```bash
uv run pytest tests/test_data_quality.py -v
```

**Qué valida:** nulos, `customer_id` único, regiones permitidas, rangos age/income, formato email.

Abrí `src/data_quality.py` y leé los nombres de las expectativas:
- `expect_column_values_to_not_be_null` → ¿hay huecos?
- `expect_column_values_to_be_unique` → ¿hay duplicados?
- `expect_column_values_to_be_in_set` → ¿valores fuera de catálogo?
- `expect_column_values_to_be_between` → ¿rangos rotos?
- `expect_column_values_to_match_regex` → ¿formato válido (email)?

#### Dataset sucio (para ver fallos a propósito):

```bash
uv run pytest tests/test_data_quality.py::test_dirty_current_fails_etl_suite -v
```

El test pasa (verde) porque **espera** que el dataset sucio falle las validaciones. Así confirmamos que nuestra suite detecta problemas reales.

**Qué tiene el dataset sucio:**
- 5 registros con `email` nulo
- 3 registros con `age` nulo
- 2 registros duplicados (mismo `customer_id`)
- 1 región inválida (`unknown_zone`)
- 1 ingreso negativo (`-100`)
- Drift artificial: ingresos inflados un 15%

### Paso 3 — Great Expectations (API real)

```bash
uv run pytest tests/test_gx_integration.py -v
```

Suite ephemeral sobre el dataset limpio. Contrato de datos ejecutable.

**¿Qué es "ephemeral"?** — Great Expectations puede funcionar sin un "Data Context" persistente (sin carpeta `gx/` ni base de datos). Creamos un contexto en memoria, definimos expectativas, validamos y descartamos. Ideal para CI donde no queremos estado entre corridas.

**Expectativas que se validan:**
1. `ExpectColumnValuesToNotBeNull` → customer_id nunca nulo
2. `ExpectColumnValuesToBeUnique` → customer_id nunca repetido
3. `ExpectColumnValuesToBeBetween` → age entre 18 y 100
4. `ExpectColumnValuesToBeInSet` → region solo north/south/east/west

### Paso 4 — Modelo + MLflow

```bash
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline
```

**Resultado esperado del pipeline:** JSON con `"overall_passed": true` y archivo `data/pipeline_report.json`.

#### Umbrales del lab:

| Chequeo | Umbral | Qué pasa si falla |
|---------|--------|-------------------|
| Precisión | ≥ 0.70 | Modelo no clasifica bien → no deployar |
| Gap de fairness por región | ≤ 0.25 | Sesgo geográfico → investigar feature engineering |
| PSI drift (income) | ≤ 0.25 | Datos cambiaron demasiado → reentrenar con datos frescos |

#### ¿Qué hace el pipeline paso a paso?

1. **Genera datos** → reference (400 registros) y current (200 registros)
2. **Valida ETL** → corre la suite de integridad sobre `current`
3. **Entrena modelo** → LogisticRegression con features `[age, income, region]`
4. **Mide precisión** → `precision_score` sobre el test set
5. **Mide fairness** → compara tasa de aprobación por región, calcula max gap
6. **Mide drift** → PSI entre distribución de `income` en referencia vs current
7. **Logea en MLflow** → parámetros + métricas en SQLite local
8. **Genera reporte** → `data/pipeline_report.json`

#### Tracking MLflow

```bash
# Ver el contenido del reporte
# macOS/Linux:
cat data/pipeline_report.json

# Windows PowerShell:
Get-Content data/pipeline_report.json
```

Ejemplo de salida:

```json
{
  "etl_passed": true,
  "model": {
    "precision": 0.82,
    "max_region_gap": 0.18,
    "income_drift_psi": 0.03,
    "passed": true
  },
  "overall_passed": true
}
```

Tracking MLflow: SQLite en `mlruns/mlflow.db` (se crea solo). Los experimentos se guardan con nombre `curso6-ml-quality` y run name `credit-approval-lab`.

### Paso 5 — CI de ejemplo

Abrí `.github/workflows/quality.yml`.

```yaml
# Lo que verás (simplificado):
- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest -v

- name: Run full pipeline
  run: uv run python -m src.run_pipeline
```

Los mismos comandos que corriste en local, ejecutados automáticamente en cada push/PR.

**Frase para llevarte:** si no corre en CI, no es gobernanza — es hobby.

**¿Por qué CI para datos y modelos?** Porque:
- Un científico de datos puede cambiar un threshold sin querer
- Un cambio en el ETL upstream puede introducir nulos
- Una actualización de librería puede cambiar el comportamiento del modelo
- Sin CI, estos errores llegan a producción silenciosamente

### Entregable / checklist del Reto 2

- [ ] `uv run pytest -v` → **5 passed**
- [ ] `uv run python -m src.run_pipeline` → `overall_passed: true`
- [ ] Entendés qué falla en el dataset sucio y por qué
- [ ] Abriste el workflow de CI y reconocés los pasos
- [ ] Podés explicar precisión vs fairness vs drift en una frase cada uno

### Preguntas de cierre (discusión)

1. ¿En tu empresa fallaría primero la calidad de **datos** o la del **modelo**?
2. ¿Quién debería ser dueño del umbral de drift — data engineering, ML engineering, o producto?
3. Si solo pudieras poner **un** gate en CI (ETL o modelo), ¿cuál elegirías?

---

## Bloque C — RPA, simulación de usuarios y gamificación (45 min)

### 1. RPA para validación de procesos

**RPA** = *Robotic Process Automation* — bots de software que interactúan con UIs y sistemas como lo haría un humano.

En testing, **no reemplaza** pruebas de API/UI bien hechas: **complementa** cuando el proceso de negocio completo (de punta a punta, cruzando 3-4 sistemas) es el sistema bajo prueba.

#### ¿Cuándo usar RPA para testing?

| Escenario | Por qué RPA | Por qué NO API testing |
|-----------|-------------|------------------------|
| Proceso cruza SAP + Excel + email + portal web | No hay API unificada | Habría que integrar 4 APIs distintas (si existen) |
| Validar output de backoffice legacy | Solo UI disponible | No expone API ni se puede modificar |
| Regresión de flujo contable mensual | Es un proceso humano → bot lo replica | No hay endpoint para "cerrar mes" |
| Smoke post-deploy de ERP | Solo se valida vía pantalla | API del ERP no cubre validaciones visuales |

#### ¿Cuándo NO usar RPA?

- Cuando existe una API testeable → usá API testing
- Cuando la UI cambia frecuentemente sin valor de negocio → test frágil
- Cuando solo querés verificar una regla de negocio → unit test

### 2. Ecosistema RPA

| Plataforma | Fortaleza | Debilidad | Ideal para |
|------------|-----------|-----------|------------|
| **UiPath** | Community edition gratis, amplia base, buen recorder | Pesado para instalar, licencias enterprise caras | Equipos con procesos complejos multi-sistema |
| **Power Automate** | Integrado con Microsoft 365, bajo costo si ya tienen licencia | Menos flexible para UIs no-Microsoft | Organizaciones 100% Microsoft |
| **Automation Anywhere** | Cloud-native, buena escalabilidad | Menos intuitivo, documentación dispersa | Empresas grandes con muchos bots en paralelo |
| **Robot Framework** | Open source, extensible, gran comunidad QA | Requiere programación, no tiene recorder visual | Equipos técnicos que quieren control total |

**Criterio de selección:** stack IT existente + licencias disponibles + observabilidad de resultados + habilidades del equipo.

### 3. Casos de uso reales de RPA en validación

**Caso 1 — Alta de cliente (banco):**
1. Bot abre portal de onboarding
2. Llena formulario con datos de prueba
3. Sube documentos de identidad (mock)
4. Verifica que el estado pase a "Pendiente de revisión"
5. Captura evidencia: screenshot + ID de transacción + timestamp

**Caso 2 — Conciliación de pagos:**
1. Bot descarga reporte de pagos del día (CSV del banco)
2. Lo compara contra registros en el ERP
3. Identifica discrepancias (montos, fechas, IDs)
4. Genera reporte de diferencias
5. Si diferencia > umbral → alerta automática

**Caso 3 — Smoke de backoffice post-deploy:**
1. Deploy sale a producción a las 2 AM
2. Bot ejecuta 5 flujos críticos a las 2:15 AM
3. Si alguno falla → rollback automático + alerta al equipo
4. Si pasa → marca deploy como "verified"

**Evidencia mínima en todos los casos:** capturas de pantalla, logs estructurados, ID de transacción, timestamp inicio/fin, resultado (pass/fail con razón).

### 4. Simulación de usuarios reales con IA

El testing tradicional sigue scripts lineales: login → acción → assert. Pero los usuarios reales no siguen scripts.

**Evolución del approach:**

```
Script fijo          →  Caminos probables      →  Política aprendida
(lo que hacemos hoy)    (model-based testing)      (RL / IA generativa)
```

| Nivel | Técnica | Qué encuentra |
|-------|---------|---------------|
| 1. Script fijo | "Clic aquí, luego allá" | Bugs en el happy path |
| 2. Exploración guiada | Datos aleatorios + heurísticas | Bugs de boundary |
| 3. Model-based | Máquina de estados + transiciones | Bugs de flujo / estado |
| 4. RL (Reinforcement Learning) | Agente aprende a navegar buscando recompensa (bugs) | Bugs que nadie imaginaría probar |

**Reinforcement Learning aplicado a testing:**
- **Estado** = pantalla actual + datos del DOM
- **Acción** = click, fill, scroll, navigate
- **Recompensa** = encontrar un crash, un error 500, un estado inconsistente
- **Política** = el agente aprende qué secuencias de acciones maximizan bugs encontrados

**Herramientas emergentes:**
- Curiosity-driven exploration (agentes que prefieren estados no visitados)
- LLM-based test generation (GPT/Claude que generan escenarios a partir de specs)
- Monkey testing inteligente (no solo random: prioriza paths con más riesgo)

**Requisitos éticos:**
- Telemetría de uso real solo con consentimiento
- No entrenar con datos personales identificables
- Anonimización de sesiones de usuario
- Transparencia: ¿qué datos se usan para simular?

### 5. Formación, simulación y gamificación

**¿Por qué gamificar la formación en testing?**

| Approach tradicional | Approach gamificado |
|---------------------|---------------------|
| PDF de 40 páginas | Reto con score automático |
| "Lean este estándar" | "Bajen el flake bajo 0.08 en 20 min" |
| Examen de múltiple opción | Lab ejecutable con tests que validan |
| Feedback en 2 semanas | Feedback en 2 segundos (pytest) |

**Plataformas de referencia:**

| Plataforma | Qué ofrece | Gratis |
|------------|-----------|--------|
| **Test Automation University** (Applitools) | Cursos de Selenium, API, mobile, visual AI | Sí |
| **Codecademy** | Cursos interactivos de Python, SQL, etc. | Freemium |
| **HackerRank / LeetCode** | Challenges de código con scoring | Freemium |
| **Ministry of Testing** | Comunidad + cursos + desafíos QA | Membresía |
| **Katacoda / Killercoda** | Labs en browser con entornos reales | Algunos gratis |

**Diseño de un reto gamificado efectivo (lo que hicimos en Reto 1 y 2):**

1. **Objetivo medible** — no "aprender Grafana" sino "identificar el servicio más crítico"
2. **Score automático** — tests verdes, métricas en umbral, checklist con checkboxes
3. **Feedback inmediato** — `pytest` te dice en 3 segundos si pasaste
4. **Dificultad progresiva** — datos limpios → datos sucios → tuning de umbrales
5. **Contexto realista** — no "sumar 2+2" sino "aprobar créditos con sesgo"

Los Retos 1 y 2 de este curso **son** gamificación seria: objetivo claro, score automático (tests/métricas), feedback inmediato, contexto de negocio real.

### 6. Mini-caso integrado (ejercicio de discusión)

**Proceso de crédito de un banco:**

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌───────────┐
│ 1. RPA  │───▶│ 2. ETL   │───▶│ 3. ML   │───▶│ 4. Dash   │
│ carga   │    │ valida   │    │ decide  │    │ alerta    │
│ backoff │    │ datos    │    │ crédito │    │ leakage   │
└─────────┘    └──────────┘    └─────────┘    └───────────┘
```

1. **RPA** valida carga en backoffice (el operador ingresó bien los datos)
2. **Great Expectations** valida dataset ETL (nulos, duplicados, formatos)
3. **Modelo ML** decide aprobación/rechazo
4. **Dashboard QA** (Día 1) alerta si leakage sube

**Pregunta:** si solo pudieras poner **un** control hoy, ¿dónde lo pondrías y por qué?

**Variantes para discutir:**
- ¿Qué pasa si el bot de RPA "pasa" pero el dato que ingresó está mal?
- ¿Qué pasa si GE aprueba datos limpios pero con drift severo?
- ¿Quién es responsable si el modelo discrimina: data engineer, ML engineer, o producto?

### Checklist rápido del Bloque C

- [ ] Sé cuándo usar RPA y cuándo es mala idea
- [ ] Puedo nombrar 3 plataformas RPA y sus fortalezas
- [ ] Entiendo la progresión script → model-based → RL
- [ ] Sé diseñar un reto gamificado con las 5 reglas

---

## Bloque D — TMMi y estrategia de madurez (45 min)

### 1. ¿Qué es TMMi?

**Test Management Maturity Model Integration**

No es una herramienta que se instala: es un **mapa de madurez** de la organización de testing (niveles + prácticas recomendadas).

**Analogía:** CMMI es para desarrollo de software lo que TMMi es para testing. Si CMMI pregunta "¿qué tan maduro es tu proceso de desarrollo?", TMMi pregunta "¿qué tan maduro es tu proceso de pruebas?".

**¿Para qué sirve?**
- Dejar de pelear "somos senior" y preguntar "¿en qué nivel medible estamos?"
- Tener un roadmap de mejora con prácticas concretas por nivel
- Hablar con liderazgo en un idioma que entienden (niveles, certificación, benchmarks)
- Compararse con la industria (benchmarking)

### 2. Los cinco niveles (visión práctica)

| Nivel | Nombre | Qué lo define | Señales típicas |
|-------|--------|---------------|-----------------|
| **1** | Inicial | Testing ad-hoc, depende de héroes | "Lo pruebo yo antes de subir" |
| **2** | Gestionado | Política existe, hay planes de prueba | Hay un test plan pero no siempre se sigue |
| **3** | Definido | Proceso estándar, integrado al ciclo | Todos usan el mismo framework y proceso |
| **4** | Medido | Métricas cuantitativas, decisiones basadas en datos | Dashboards con flake/leakage/coverage (¡Día 1!) |
| **5** | Optimizado | Mejora continua, prevención de defectos | CI/CD con gates automáticos + feedback loops |

**Donde nos ubicamos con este curso:**
- Día 1 (métricas + dashboards) empuja hacia **nivel 4 (Medido)**
- Retos con CI empujan hacia **nivel 5 (Optimizado)**

### 3. Prácticas recomendadas por nivel

| Nivel | Áreas de proceso | Lo que implementás |
|-------|-----------------|-------------------|
| 2 | Política de pruebas, planificación | Documento de política, plan por release |
| 3 | Organización, formación, ciclo de vida | Roles claros, onboarding de QA, testing integrado |
| 4 | Medición, evaluación de calidad | Métricas con umbral, evaluación cuantitativa |
| 5 | Prevención, optimización, control de calidad | Root cause analysis, feedback automatizado |

### 4. Auto-evaluación rápida (ejercicio)

Respondé honestamente (1 a 5):

| Pregunta | Tu equipo |
|----------|-----------|
| ¿Hay política escrita de qué se automatiza? | ___ |
| ¿Hay métricas de flake/leakage con umbral? | ___ |
| ¿El testing está integrado al pipeline (CI)? | ___ |
| ¿Las decisiones de calidad se basan en datos? | ___ |
| ¿Hay feedback loop que prevenga defectos recurrentes? | ___ |

**Interpretación:**
- Mayoría 1-2: nivel Inicial/Gestionado → priorizar política + herramientas básicas
- Mayoría 3: nivel Definido → priorizar métricas + observabilidad
- Mayoría 4-5: nivel Medido/Optimizado → priorizar prevención + optimización

### 5. Marcos complementarios a TMMi

| Marco | Enfoque | Relación con TMMi |
|-------|---------|-------------------|
| **CMMI** | Desarrollo completo | TMMi es el complemento de testing |
| **ISO 29119** | Estándar internacional de testing | Define procesos; TMMi mide madurez |
| **ISTQB** | Certificación individual | Personas; TMMi evalúa la organización |
| **SAFe** | Agilidad escalada | Testing embebido; TMMi audita calidad del proceso |

### 6. Dashboards centralizados como herramienta de madurez

```
Nivel 1-2: no hay métricas compartidas
Nivel 3:   métricas existen pero en silos
Nivel 4:   dashboard centralizado (Prometheus + Grafana)
Nivel 5:   dashboard + alertas + acciones automáticas
```

La gestión centralizada de calidad con dashboards de **cobertura, defectos y flakiness** es exactamente lo que construimos en el Día 1. Prometheus, Grafana, y Kibana/Loki para logs = la capa observable que distingue nivel 4 de nivel 3.

**Visualización de métricas (stack completo del temario):**

| Herramienta | Capa | Qué aporta |
|-------------|------|------------|
| **Prometheus** | Almacenamiento + alertas | Guarda series de tiempo, evalúa reglas |
| **Grafana** | Visualización | Dashboards legibles, compartibles |
| **Kibana** | Exploración de logs | Buscar eventos, correlacionar con métricas |
| **Loki** | Logs ligeros | Integración directa con Grafana, query por labels |

### 7. Estrategia sostenible (la cadena completa)

Todo lo que vimos en dos días forma una cadena:

| # | Componente | Día | Nivel TMMi |
|---|-----------|-----|-----------|
| 1 | Políticas (gobernanza) | Día 1 | 2-3 |
| 2 | Métricas con umbral | Día 1 | 4 |
| 3 | Observabilidad (Prometheus / Grafana / Kibana-Loki) | Día 1 | 4 |
| 4 | Datos + ML validados | Día 2 | 4-5 |
| 5 | Procesos RPA + aprendizaje gamificado | Día 2 | 3-5 |
| 6 | Madurez TMMi | Día 2 | meta |

### 8. Tablero de decisión (chuleta de salida)

| Si duele… | Empezá por… | Herramienta/concepto |
|-----------|-------------|---------------------|
| CI rojo por flake | Bajar flake rate | Dashboard + política de quarantine |
| Bugs en prod | Leakage + alcance por riesgo | Cobertura por riesgo + alertas |
| Modelo injusto | Fairness + datos | Great Expectations + fairness checks |
| Proceso manual frágil | RPA de validación | UiPath / Power Automate + evidencia |
| Nadie sabe el estado | Dashboard de gobernanza | Prometheus + Grafana |
| Datos sucios llegan al modelo | Gate de calidad ETL en CI | GE + pipeline gate |
| El equipo no mejora | Gamificación + TMMi roadmap | Retos con score + auto-evaluación |

### 9. Consolidación Reto 1 + Reto 2

| Reto | Qué validamos | Stack |
|------|---------------|-------|
| **Reto 1** (Día 1) | Calidad del sistema de pruebas (observable) | Prometheus + Grafana + alertas |
| **Reto 2** (Día 2) | Calidad de datos y modelo (validada en CI) | GE + MLflow + GitHub Actions |

**Juntos:** gobernanza de punta a punta — desde la métrica de flake hasta la precisión del modelo, todo observable y automatizado.

### 10. Casos y dudas (discusión abierta)

Regla: toda respuesta tiene que anclarse a una **métrica**, una **política** o una **evidencia**. Si solo hay opinión, la convertimos en hipótesis medible.

**Casos para provocar discusión si la sala está callada:**

1. "Mi jefe dice que tenemos 90% de cobertura así que estamos bien." ¿Qué le responderías con lo que aprendiste?
2. "Implementamos ML pero nadie revisa si el modelo sigue siendo justo después del primer deploy." ¿Qué control mínimo pondrías?
3. "Nuestro equipo de QA quiere implementar todo a la vez: dashboards, ML testing, RPA, gamificación." ¿Por dónde empezarían según TMMi?

### Checklist final del curso (Certificación 6)

- [ ] Sé explicar flake, leakage y effectiveness con umbral
- [ ] Levanté / usé el dashboard QA (Día 1) **o** entiendo el flujo
- [ ] Corrí el lab de datos/ML (Día 2)
- [ ] Ubico RPA, simulación y gamificación en la estrategia
- [ ] Relaciono todo con un nivel TMMi

### Dos pedidos para el lunes

1. Elegí **un umbral** y **un dueño**
2. Publicá **al menos una métrica** donde todo el equipo la vea

Madurez no es un certificado en la pared: es un hábito medible.

---

## Errores comunes

| Error / síntoma | Causa probable | Solución |
|-----------------|----------------|----------|
| `uv: command not found` | uv no instalado o PATH viejo | Reinstalá uv y **reabrí** la terminal |
| `python: command not found` | Python no en PATH | Windows: instalá Python marcando "Add to PATH"; Mac: `python3` |
| Falla `uv sync` por red/proxy | Restricción corporativa | Reintentá; si persiste, pedí al instructor el plan B (wheelhouse / mirror) |
| `ModuleNotFoundError: src` | Corrés fuera de la carpeta del lab | `cd` a `ml-data-quality-lab` y usá `uv run` |
| Test de GE falla con API distinta | Versión de Great Expectations | `uv sync` de nuevo (lockfile del repo) |
| MLflow error de file store | Backend viejo | El lab usa SQLite (`mlruns/mlflow.db`); no fuerces `./mlruns` a mano |
| pytest 4 passed / 1 failed | Modelo o datos drift | Corré `uv run python -m src.generate_data` vía pipeline; no edites umbrales sin entenderlos |
| Workflow CI no corre en GitHub | El YAML vive dentro del proyecto | Es un **ejemplo**; GitHub solo lee `.github/workflows` en la raíz del repo. Podés copiarlo allí si versionás el monorepo |

---

## Comandos útiles (atajo)

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab

uv sync
uv run pytest -v
uv run pytest tests/test_data_quality.py -v
uv run pytest tests/test_gx_integration.py -v
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline

# Ver reporte
# macOS/Linux:  cat data/pipeline_report.json
# Windows:      Get-Content data/pipeline_report.json
```

Script opcional (macOS/Linux/Git Bash):

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

---

## Para llevar

Después del Día 2 tenés:

- Plan de testing para datos + modelo (ejecutable)
- Experiencia con Great Expectations + MLflow
- Criterios para ubicar RPA y simulación de usuarios
- Marco TMMi para hablar de madurez sin humo
- Tablero de decisión: "si duele X, empezá por Y"

Junto con el Día 1: **gobernanza de punta a punta** (sistema de pruebas observable + datos/modelos validados en CI).
