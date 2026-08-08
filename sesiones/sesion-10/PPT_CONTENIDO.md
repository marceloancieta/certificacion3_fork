# Sesión 10 — Contenido de diapositivas (para alumnos)
## Cierre · Puerta de Calidad de Release

> **22 slides** · 2 horas · A 1–7 con 4b y 6b (40) · B 8–9b–14 (40) · C 15–18 con 16b (20)
> Guion en `GUIA_INSTRUCTOR.md`. Lab sincronizado — mismos comandos en tu máquina.

---

### Slide 1 — Portada (2 min)
**Título:** La puerta que construyeron
- Sesión 10 de 10 · Certificación 3 · **2 horas**
- Hoy: integrar el juez · correr escenarios JSON · desbloquear un release · cierre
- Frase del día: **el verde no es una opinión: es un conjunto de umbrales acordados**

### Slide 2 — Agenda de 2 horas (2 min)
**Título:** Tres bloques cortos
- A (40): mapa Etapas 1–9
- B (40): lab `release-gate` (sano / bloqueado / many)
- C (20): un check rojo a la vez · desbloquear · forzar fallos · arco completo
- Dos pausas de 10 minutos

### Slide 3 — De S1 a S9 en un minuto (6 min)
**Título:** Nueve preguntas al pipeline
- 1 Diseño · 2–3 API/contrato · 4 UI · 5 CI
- 6 Performance · 7 Seguridad/a11y · 8 Mutación · 9 Visual/móvil
- Cada una dejó un **umbral** o una **evidencia**
- Hoy el juez las mira juntas

### Slide 4 — Qué es un Release Gate (5 min)
**Título:** Un solo veredicto
- Entrada: métricas (JSON)
- Proceso: comparar contra THRESHOLDS
- Salida: `passed` + lista `failed` + **exit code**
- Si un check falla → el release **no** mergea
- Gate ≠ dashboard: el dashboard informa, el gate **decide**

### Slide 4b — El contrato JSON (6 min)
**Título:** Entrada y salida del juez
- Entrada: 6 campos, ninguno opcional
- `pass_rate` (ratio) · `p95_ms` (ms) · `zap_fail_new` (conteo)
- `mutation_score` (ratio) · `a11y_critical` (conteo) · `visual_diff_pixels` (px)
- Salida: `checks` + `failed` + `passed` + eco de `thresholds`
- stdout = JSON para máquinas · stderr = veredicto humano · exit code = CI

### Slide 5 — Umbrales del curso (6 min)
**Título:** Los números que ya conocen
- pass_rate ≥ 0.95 · p95 ≤ 500 ms
- ZAP fail_new ≤ 0 (WARN no bloquea)
- mutation ≥ 0.90 · a11y critical ≤ 0
- visual_diff ≤ 120 px (S9)
- En el umbral exacto: **pasa**

### Slide 6 — Score ≠ gate (otra vez) (5 min)
**Título:** Medir no es bloquear
- Ver sobrevivientes / WARN / diff ≠ rojo automático
- El umbral decide (S6 K6 · S7 rules.tsv · S8 --enforce-gate · S9 gate/)
- Hoy: un CLI que aplica todos los umbrales
- Cultura: acordar umbrales en equipo, no en silencio

### Slide 6b — El gate en un CI real (4 min)
**Título:** Dónde vive el juez
- Último job del pipeline: `needs:` todos los anteriores
- Las métricas viajan como **artefactos** entre jobs
- Required status check: sin verde no hay botón de merge
- Saltarse el gate con permisos de admin = incidente, no atajo

### Slide 7 — Café (1 min)
**Título:** Pausá 10
- Cuando volvamos: corremos el juez con JSON sano y rojo

### Slide 8 — Arranque Bloque B (1 min)
**Título:** Lab del juez
- Carpeta: `proyecto-integrador/release-gate`
- Mismos comandos en tu máquina y en pantalla del instructor
- Objetivo: ver exit 0 y exit 1 y leer el JSON

### Slide 9 — Setup + tests del juez (5 min)
**Título:** Primero la suite del lab
- `uv sync --group dev`
- `uv run pytest -v` → **16 passed**
- Escenarios de `metrics/` + contrato de `demos/` (incompleto/inválido)
- El juez tiene tests propios (no es magia)
- Task: `task test:gate`

### Slide 9b — Anatomía del repo (4 min)
**Título:** Core del juez (config, no magia)
- `pyproject.toml` — solo pytest; `pythonpath = ["src"]`
- `src/release_gate/__init__.py` — `THRESHOLDS` + `evaluate()`
- `run_gate.py` — atajo: mete `src/` en el path (Windows-friendly)
- `metrics/*.json` — escenarios de demo (simulan artefactos de CI)
- `scripts/run_all_demos.py` — arco completo en un comando

### Slide 10 — Release sano (7 min)
**Título:** metrics/healthy.json → exit 0
- Comando: `uv run python run_gate.py metrics/healthy.json`
- Los 6 checks en `true` · `failed: []` · `passed: true`
- Stderr: `RELEASE: PASA`
- Ese es el merge feliz

### Slide 11 — Bloqueo por mutación (7 min)
**Título:** mutation 0.80 < 0.90
- Comando: `uv run python run_gate.py metrics/blocked_mutation.json`
- Solo `mutation: false` · exit **1**
- El resto puede estar verde: igual se bloquea

### Slide 12 — Bloqueo por visual (7 min)
**Título:** Etapa 9 dentro del juez
- Comando: `uv run python run_gate.py metrics/blocked_visual.json`
- `visual_diff_pixels` enorme (banner broken de S9)
- `failed: ["visual"]` · exit **1**

### Slide 13 — Varios fallos a la vez (5 min)
**Título:** metrics/blocked_many.json
- Varios checks en rojo · lista `failed` completa
- En un PR real: priorizá por riesgo (seguridad / a11y / perf)
- El juez no prioriza: solo reporta

### Slide 14 — Plantilla CI + café (3 min)
**Título:** qa-release-gate.yml
- Workflow de ejemplo en `workflows/`
- Corre pytest del juez + demo sano + demo bloqueado
- Pausá 10 · Bloque C: un check a la vez

### Slide 15 — Un check rojo a la vez (6 min)
**Título:** Cada JSON = una sesión
- `blocked_pass_rate.json` → S4/S5 · `blocked_p95.json` → S6
- `blocked_zap.json` / `blocked_a11y.json` → S7
- `blocked_mutation.json` → S8 · `blocked_visual.json` → S9
- Corré uno por uno y leé `failed: ["…"]`

### Slide 16 — Desbloquear en vivo (5 min)
**Título:** Arreglar la métrica, no el umbral
- Abrí `metrics/blocked_mutation.json`
- Cambiá `0.80` → `0.96` · guardá · volvé a correr el gate
- **exit 0** — el release pasa sin tocar `THRESHOLDS`
- Al final: `git checkout -- metrics/blocked_mutation.json` (lab limpio)
- Misma lógica que arreglar tests, perf o visual en un PR real

### Slide 16b — Forzar el rojo (5 min)
**Título:** Tres fallos distintos (no es lo mismo)
- `demos/incomplete.json` → CLI: `JSON incompleto` (no evalúa)
- `demos/invalid.json` → CLI: `JSON invalido` (sintaxis)
- Fixture que miente → pytest **AssertionError** en rojo
- Comando: `uv run python scripts/demo_force_fail.py`
- `blocked_*.json` = métrica bajo umbral (negocio) ≠ basura de entrada

### Slide 17 — Arco completo (4 min)
**Título:** Un comando, todos los escenarios
- `uv run python scripts/run_all_demos.py`
- pytest + healthy + cada bloqueo + many
- Task: `task test:gate:demos`
- Si algo falla, el script te dice cuál escenario

### Slide 18 — Cierre del curso (3 min)
**Título:** Gracias
- Construyeron una puerta de 9 etapas + un juez
- Mantenerla es trabajo continuo (umbrales, baselines, flaky)
- Frase final: el verde no es una opinión
- Certificación 3 — contenido cerrado
