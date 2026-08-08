# Sesión 10 — Cierre: Puerta de Calidad de Release

> **Duración:** 2 horas · Bloque A 40 → ☕ 10 → B 40 → ☕ 10 → C 20
> **Objetivo:** al terminar vas a poder **recorrer las 9 etapas** del gate, correr el **juez único** (`release-gate`) con métricas JSON, ver **un check rojo a la vez**, **desbloquear** un release editando métricas y cerrar el mapa del curso.

**Blanco de hoy:** `proyecto-integrador/release-gate/` — un CLI que lee métricas y decide exit 0 / 1 (incluye visual de la S9).

**Frase del día:** **el verde no es una opinión: es un conjunto de umbrales que alguien acordó.**

**Cómo trabajamos:** lab sincronizado. Mismos comandos en tu máquina y en la del instructor. Sin Docker. Solo `uv` + Python.

---

## Antes de empezar

```bash
cd proyecto-integrador/release-gate
uv sync --group dev
uv run pytest -v                                         # 16 passed
uv run python run_gate.py metrics/healthy.json           # exit 0
uv run python run_gate.py metrics/blocked_mutation.json  # exit 1
```

**Atajos:** `task test:gate` · `task test:gate:healthy` · `task test:gate:demos`.

---

## Anatomía del lab (core del ejemplo)

| Pieza | Rol |
|---|---|
| `pyproject.toml` | Solo pytest; `pythonpath = ["src"]` |
| `src/release_gate/__init__.py` | `THRESHOLDS` + función `evaluate()` |
| `run_gate.py` | CLI que funciona con `uv run` sin instalar paquete |
| `metrics/*.json` | Escenarios de demo (simulan artefactos de CI) |
| `demos/` | JSON rotos a propósito (incompleto / inválido) |
| `scripts/run_all_demos.py` | Arco completo en un solo comando |
| `scripts/demo_force_fail.py` | Tres fallos forzados (CLI + assert en rojo) |
| `tests/test_release_gate.py` | El juez se prueba a sí mismo |

---

## Agenda (2 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 40 min | Recorrido Etapas 1–9 · qué es un release gate · umbrales |
| ☕ | 10 min | — |
| **B** | 40 min | Lab: pytest del juez · JSON sano / mutación / visual / many |
| ☕ | 10 min | — |
| **C** | 20 min | Un check rojo a la vez · desbloquear · forzar fallos · arco completo · cierre |

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
uv sync --group dev
uv run pytest -v
uv run python run_gate.py metrics/healthy.json
uv run python run_gate.py metrics/blocked_mutation.json
uv run python run_gate.py metrics/blocked_visual.json
uv run python run_gate.py metrics/blocked_many.json
```

Leé el JSON de salida: `checks`, `failed`, `passed`. El exit code es el gate.

Plantilla CI: `workflows/qa-release-gate.yml`.

---

## Bloque C — Un check a la vez y cierre (20 min)

### Un solo check rojo (cada JSON = una sesión)

```bash
uv run python run_gate.py metrics/blocked_pass_rate.json  # S4/S5
uv run python run_gate.py metrics/blocked_p95.json        # S6
uv run python run_gate.py metrics/blocked_zap.json        # S7
uv run python run_gate.py metrics/blocked_a11y.json       # S7
uv run python run_gate.py metrics/blocked_mutation.json   # S8
uv run python run_gate.py metrics/blocked_visual.json     # S9
```

### Desbloquear en vivo

1. Abrí `metrics/blocked_mutation.json`.
2. Cambiá `"mutation_score": 0.80` → `0.96`.
3. Corré de nuevo: `uv run python run_gate.py metrics/blocked_mutation.json` → **exit 0**.
4. Revertí para dejar el lab limpio: `git checkout -- metrics/blocked_mutation.json` (si no, pytest falla: cada JSON tiene test).

### Forzar fallos (tres clases de rojo)

No es lo mismo un release bloqueado que un artefacto podrido:

```bash
# 1) Contrato incompleto — faltan claves; el juez NO evalúa
uv run python run_gate.py demos/incomplete.json
# → JSON incompleto; faltan: ['mutation_score', 'visual_diff_pixels']

# 2) JSON inválido — trailing comma; falla el parseo
uv run python run_gate.py demos/invalid.json
# → JSON invalido en invalid.json: ...

# 3) Assert de pytest en rojo — fixture que miente (envenena, falla, restaura)
uv run python scripts/demo_force_fail.py
```

| Rojo | Causa | Mensaje típico |
|---|---|---|
| Gate bloqueado | Métrica bajo umbral (`blocked_*.json`) | `RELEASE: BLOQUEADO - fallo: mutation` |
| JSON incompleto | Falta un campo del contrato | `JSON incompleto; faltan: [...]` |
| JSON inválido | Sintaxis rota | `JSON invalido ...` |
| Assert pytest | El JSON de demo no cumple lo que el test espera | `AssertionError` en `test_escenarios_metrics_json` |

### Arco completo

```bash
uv run python scripts/run_all_demos.py
```

---

## Checklist de salida

- [ ] Recorro Etapas 1–9 en una frase cada una
- [ ] Corrí el juez con JSON sano (exit 0) y bloqueado (exit 1)
- [ ] Vi un JSON con **un solo** check en rojo y sé qué sesión lo originó
- [ ] Desbloqueé un release editando una métrica
- [ ] Vi tres rojos distintos: incompleto · inválido · AssertionError (`demo_force_fail.py`)
- [ ] Corrí `scripts/run_all_demos.py` (o el equivalente comando por comando)
