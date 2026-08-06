# Sesión 10 — Cierre: Puerta de Calidad de Release

> **Duración:** 2 horas · Bloque A 40 → ☕ 10 → B 40 → ☕ 10 → C 20
> **Objetivo:** al terminar vas a poder **recorrer las 9 etapas** del gate, correr el **juez único** (`release-gate`) con métricas JSON, explicar por qué un release se **bloquea**, ubicar los **retos** del curso y cerrar con una retrospectiva corta.

**Blanco de hoy:** `proyecto-integrador/release-gate/` — un CLI que lee métricas y decide exit 0 / 1 (incluye visual de la S9).

**Frase del día:** **el verde no es una opinión: es un conjunto de umbrales que alguien acordó.**

**Cómo trabajamos:** demo sincronizada. Sin Docker. Solo `uv` + Python.

---

## Antes de empezar

```bash
cd proyecto-integrador/release-gate
uv sync --group dev
uv run pytest -v
uv run python run_gate.py metrics/healthy.json      # exit 0
uv run python run_gate.py metrics/blocked_mutation.json  # exit 1
```

**Atajos:** `task test:gate` · `task test:gate:healthy` · `task test:gate:blocked`.

**Retos (fuera de clase o al final):** carpeta [`retos/`](../../retos/) — teóricos + práctico Release Gate (sin el check visual; el lab de hoy sí lo incluye).

---

## Anatomía del lab (opcional — core del ejemplo)

| Pieza | Rol |
|---|---|
| `pyproject.toml` | Solo pytest; `pythonpath = ["src"]` |
| `src/release_gate/__init__.py` | `THRESHOLDS` + función `evaluate()` |
| `run_gate.py` | CLI que funciona con `uv run` sin instalar paquete |
| `metrics/*.json` | Entradas de demo (simulan artefactos de jobs de CI) |
| `tests/test_release_gate.py` | El juez se prueba a sí mismo |

---

## Agenda (2 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 40 min | Recorrido Etapas 1–9 · qué es un release gate · umbrales |
| ☕ | 10 min | — |
| **B** | 40 min | Lab: juez JSON sano / mutación / visual · workflow plantilla |
| ☕ | 10 min | — |
| **C** | 20 min | Retos · evaluación rápida · retrospectiva · cierre |

---

## Bloque A — El mapa completo (40 min)

### Etapas del proyecto (recordatorio)

| # | Etapa | Lab / evidencia |
|---|---|---|
| 1 | Diseño + trazabilidad | `design-lab` |
| 2–3 | API + contrato | Postman / `api-lab` |
| 4 | UI | `ui-lab` |
| 5 | CI | `ci-lab` + GHA |
| 6 | Performance | K6 thresholds |
| 7 | Seguridad + a11y | ZAP + Axe |
| 8 | Calidad de la suite | cosmic-ray |
| 9 | Móvil + visual | `mobile-visual-lab` |
| **10** | **Juez único** | **`release-gate`** |

Un release **pasa** solo si **todos** los checks del JSON están en verde.

---

## Bloque B — Lab del juez (40 min)

```bash
cd proyecto-integrador/release-gate
uv run pytest -v
uv run python run_gate.py metrics/healthy.json
uv run python run_gate.py metrics/blocked_mutation.json
uv run python run_gate.py metrics/blocked_visual.json
```

Leé el JSON de salida: `checks`, `failed`, `passed`. El exit code es el gate.

Plantilla CI: `workflows/qa-release-gate.yml`.

---

## Bloque C — Retos, evaluación, cierre (20 min)

- Retos: `retos/RETOS_COMPLETOS.md` + práctico en GitHub.
- Evaluación: 5 preguntas orales del instructor (cobertura ≠ calidad, score≠gate, FAIL vs WARN, baseline visual, por qué Appium quedó en mapa).
- Retrospectiva: qué se llevan / qué costó más / qué usarían mañana en el trabajo.
- Cierre del curso: la puerta existe; mantenerla es el trabajo del equipo.

---

## Checklist de salida

- [ ] Recorro Etapas 1–9 en una frase cada una
- [ ] Corrí el juez con JSON sano (exit 0) y bloqueado (exit 1)
- [ ] Explico por qué mutation 0.80 o visual enorme bloquean
- [ ] Sé dónde están los retos
- [ ] Tengo una frase de retrospectiva
