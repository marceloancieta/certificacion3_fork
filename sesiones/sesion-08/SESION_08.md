# Sesión 8 — Mantenimiento de suites

> **Duración:** 3 horas · Bloque A 45 → ☕ 15 → B 45 → ☕ 15 → C 45
> **Objetivo:** al terminar vas a poder explicar por qué **cobertura ≠ calidad**, correr **mutation testing** con cosmic-ray y leer el **mutation score**, escribir asserts que **matan mutantes**, diagnosticar un test **flaky** y curarlo de verdad (no con reintentos), y escribir **selectores robustos** que sobreviven un rediseño.

**Blanco de hoy:** `discount.py`, la misma regla de descuento de la Sesión 1 — código puro, sin base de datos ni navegador. Sobre él corre la mutación.

**Herramientas (y por qué estas):**
- **cosmic-ray** para mutation testing. El temario menciona **mutmut**, pero mutmut 3.x necesita `fork` y **no corre en Windows nativo** (exige WSL). cosmic-ray está mantenido en 2026, corre nativo en los tres sistemas y da reporte HTML.
- **Selectores robustos + reparación con IA** para auto-healing. El temario menciona **Healenium**, pero es solo Selenium y pide ~5 contenedores; el curso es Playwright-first. Healenium y **Alumnium** quedan en el mapa.

**Frase del día:** la cobertura te dice qué código **ejecutaste**; la mutación te dice si tus asserts **sirven**.

**Cómo trabajamos hoy:** lab **sincronizado** — seguís al instructor en simultáneo. Hoy **no usamos Docker**: todo con `uv` + Playwright.

---

## Antes de empezar

```bash
cd proyecto-integrador/maintenance-lab
uv sync --group dev
uv run playwright install chromium
uv run pytest -v          # 7 tests en verde (por ahora)
```

**Atajos (Taskfile):** `task test:maint` · `task test:maint:mutation` · `task test:maint:flaky` · `task test:maint:healing`.

> Nota: `task test:maint:healing` sale **exit 1** a propósito (1 failed + 1 passed). El selector frágil no se tapa con `xfail`.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido (alineado al PPT) |
|---|---|---|
| **A** | 45 min | Por qué se pudren las suites · cobertura ≠ calidad · qué es mutation testing · flaky · anotaciones condicionales |
| ☕ | 15 min | — |
| **B** | 45 min | Lab sincronizado: suite débil → cosmic-ray → leer score → matar mutantes → gate (Etapa 8) |
| ☕ | 15 min | — |
| **C** | 45 min | Demo flaky + cura · selectores frágil vs robusto · mapa de auto-healing + reparación con IA |

Las diapositivas están en `PPT_CONTENIDO.md` / `sesion-08.pptx` (misma numeración).

---

## Bloque A — Por qué se pudren las suites (45 min) · Slides 1–9

### 1. La suite en la que nadie confía (Slide 3)

Imaginate una suite de 300 tests que tarda 40 minutos, está verde… y el bug llegó igual a producción. Peor: hay un test que falla 1 de cada 5 corridas sin que nadie tocara el código. ¿Qué hace el equipo? Le da **re-run** hasta que pasa. Con el tiempo, “re-run hasta que pase” se vuelve cultura, y ahí empiezan a ignorarse fallos **reales**.

Ese es el tema de hoy: mantener una suite para que **envejezca bien**. Atacamos tres males:

- **Tests que no prueban** — asserts débiles: verdes, pero no atrapan bugs.
- **Tests flaky** — inestables: a veces pasan, a veces no.
- **Tests frágiles** — selectores rígidos que se rompen con cualquier cambio de UI.

### 2. Cobertura ≠ calidad (Slide 5)

La cobertura mide qué líneas se **ejecutaron**, no qué se **verificó**. Un test sin `assert` (o con un assert flojo como `assert resultado >= 0`) suma cobertura y no prueba nada.

Mirá la suite de hoy (`tests/test_discount.py`): ejecuta todas las ramas de `discount.py` (cobertura alta), pero casi ningún test verifica el **valor exacto**:

```python
def test_premium_con_volumen_y_cupon_no_excede_tope():
    resultado = calculate_discount("premium", 5000.0, True)
    assert 0.0 <= resultado <= 15.0   # ← no dice CUÁNTO debe ser
```

Necesitamos un juez que mida la calidad de los asserts. Ese juez es el **mutation testing**.

### 3. Qué es mutation testing (Slide 6)

La herramienta mete **bugs pequeños a propósito** en tu código (un “mutante” por cambio): `>=` → `>`, `+` → `-`, `10.0` → `11.0`. Después corre tu suite contra cada mutante:

- Si **algún test falla** → mutante **muerto** ✅ (tu suite lo atrapó).
- Si **ningún test falla** → mutante **sobrevive** ❌ (falta un assert).

El **mutation score** = mutantes muertos / total. Más alto, suite más exigente.

### 4. Flaky y anotaciones condicionales (Slide 8)

Un test flaky no es “mala suerte”: tiene una **causa**. Las cuatro clásicas: aleatoriedad sin semilla, esperas de tiempo (`sleep` fijos), orden de tests y estado compartido entre tests.

Reintentar (`pytest-rerunfailures`) **enmascara** el problema; no lo cura. Y las anotaciones condicionales de pytest — `@pytest.mark.skipif(...)`, `@pytest.mark.xfail(...)` — sirven para **documentar** una condición conocida, no para esconder un flaky bajo la alfombra.

### 5. Tour del lab + anticipo (Slide 9)

```bash
cd proyecto-integrador/maintenance-lab
uv run pytest -v
```

`discount.py` es el blanco. La suite está verde. Spoiler pedagógico: cosmic-ray genera **50** mutantes; con esta suite débil **25 sobreviven** (score 50%). En el Bloque B lo vas a medir vos.

---

## Bloque B — Mutation testing → Etapa 8 (45 min) · Slides 10–17

> Lab sincronizado: un comando a la vez.

### Paso 1 — La suite “verde mentirosa” (Slide 11)

```bash
uv run pytest -v
```

7 tests verdes. Ejecutan todo `discount.py`. Pero mirá los asserts: `>= 0`, `isinstance(...)`, `premium > standard`. Cobertura alta, verificación pobre.

### Paso 2–4 — Mutation run completo (Slides 12–14)

Camino recomendado (multiplataforma, idempotente — el mismo que usa la task):

```bash
python scripts/run_mutation.py
```

Ese script hace, en orden: baseline → init `--force` → exec → HTML en `reports/mutation.html` → resumen → reporta el gate **sin tumbar** el exit code (así podés repetir el lab sin pelearte con el rojo).

Resultado con la suite débil: **50 mutantes · 25 sobreviven · score 50%**. Abrí `reports/mutation.html`: por cada mutante sobreviviente vas a ver el **diff** (qué cambió). Leélo como leíste el reporte de ZAP: no es novela; buscás el patrón del assert que falta.

**Score ≠ gate** (Slide 14): ver sobrevivientes no es “pipeline rojo” automático. El umbral decide:

```bash
python scripts/run_mutation.py --enforce-gate   # exit 1 si score < 90%
```

Con la suite débil, `--enforce-gate` **bloquea** (ese es el punto). Mismo patrón mental de S6 (thresholds de K6) y S7 (`rules.tsv` de ZAP).

### Paso 5 — Matar mutantes (Slide 15)

Creá `tests/test_mutantes.py` y escribí asserts **exactos** guiado por los sobrevivientes del reporte:

```python
from maintenance_lab.discount import calculate_discount

def test_base_premium_es_exactamente_10():
    assert calculate_discount("premium", 100.0, False) == 10.0

def test_limite_volumen_999_99_no_recibe_bono():
    assert calculate_discount("standard", 999.99, False) == 0.0

def test_limite_volumen_1000_exacto_si_recibe_bono():
    assert calculate_discount("standard", 1000.0, False) == 5.0
```

Cada assert exacto mata una familia de mutantes. Fijate que son los mismos **valores límite (BVA)** de la Sesión 1: la mutación verifica que de verdad los probaste. (La referencia completa está en `soluciones/test_mutantes.py`.)

### Paso 6 — El score sube + mutantes equivalentes (Slide 16)

Volvé a correr el mismo runner:

```bash
python scripts/run_mutation.py
```

El score sube a **~96%** y quedan **2 mutantes equivalentes**: cambios que **no alteran el comportamiento** (por ejemplo, comparar strings con `<=` cuando el dominio ya está validado). No se pueden matar, y está bien. La meta no es 100%; es no dejar sobrevivientes que **importen**.

### Paso 7 — Etapa 8 del gate (Slide 17)

`workflows/qa-mutation.yml` corre el **mismo** `python scripts/run_mutation.py --enforce-gate` en GitHub Actions y sube el HTML como artefacto. Con la suite débil el job **falla** (score 50% < 90%); cuando el equipo sube el score, pasa. Esa es la **Etapa 8** del proyecto: calidad del conjunto de pruebas.

---

## Bloque C — Flaky y selectores robustos (45 min) · Slides 18–24

### 1. Un test flaky en vivo (Slides 19–20)

Verificación determinista (siempre igual — es lo que corre `task test:maint:flaky`):

```bash
uv run pytest flaky/test_flaky_consistent.py -v
```

Demo **en vivo** (corré 2–3 veces a mano; el resultado cambia ~50%):

```bash
uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v
```

La causa está en `flaky/retry_service.py`: `elegir_worker` usa `random.choice(...)` **sin semilla**. El parche que engaña es reintentar (`@pytest.mark.flaky(reruns=5)`). La **cura** es inyectar la aleatoriedad con semilla fija (está en el mismo `test_flaky_consistent.py`).

### 2. Selector frágil vs robusto (Slide 21)

```bash
uv run pytest healing/test_selectores.py -v
```

Los tests corren contra `healing/app_v2.html`, la página **ya rediseñada**: el equipo de front cambió ids y clases, pero el botón sigue diciendo “Ingresar”.

- `page.locator("#login-btn")` → **FAILED** (el id ya no existe; el test falla de verdad).
- `page.get_by_role("button", name="Ingresar")` → **PASSED**.

Resultado de la corrida: **1 failed, 1 passed**. El frágil no se tapa con `xfail`: si el selector está roto, la suite tiene que quedar en rojo.

Regla 2026: seleccioná por **rol + texto visible** primero. El DOM cambia; la intención del usuario, no.

### 3. Auto-healing y reparación con IA (Slide 22)

**Auto-healing** = reemplazar en runtime un selector roto por el más parecido. Mapa de herramientas: **Healenium** (Selenium, stack Docker) y **Alumnium** (open source, IA-nativo para Playwright/Selenium/Appium).

En clase el instructor demuestra la reparación con IA (error de Playwright + `app_v2.html` → propuesta → revisión humana). Si querés repetirlo en local: mismo criterio — la IA propone, vos decidís (evitar “verde falso” automático).

---

## Checklist de salida

- [ ] Puedo explicar por qué cobertura ≠ calidad
- [ ] Corrí cosmic-ray y leí el mutation score
- [ ] Escribí un assert exacto que mató mutantes
- [ ] Sé qué es un mutante equivalente
- [ ] Diagnostiqué un flaky y sé por qué reintentar no cura
- [ ] Sé escribir un selector robusto (rol + texto)
- [ ] Ubico Healenium / Alumnium / IA en el mapa de healing

**Puente a la Sesión 9:** móviles y escritorio (Appium/Maestro) + regresión visual.
