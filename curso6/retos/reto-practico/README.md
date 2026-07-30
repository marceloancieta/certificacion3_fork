# Reto práctico — Quality Gate de Certificación 6

> **Modalidad:** individual · **Tiempo sugerido:** 60–90 minutos · **Nivel:** medio.
> **Evidencia de que funcionó:** `uv run pytest -v` → **14 passed** (el score es automático).

## Contexto

Eres QA engineer en un banco. El equipo tiene un dashboard de gobernanza (Día 1) y un pipeline de ML de aprobación de crédito (Día 2). Te piden un **quality gate**: un módulo Python que reciba las métricas del release y decida, con los umbrales del curso, si el release pasa o se bloquea.

El esqueleto ya existe. Tu trabajo es implementar **6 funciones** marcadas con `TODO` en `src/quality_gate.py`. Una suite de pytest valida cada una: cuando todo está bien implementado, los 14 tests pasan.

## Umbrales (los mismos del curso)

| Chequeo | Umbral | Día |
|---------|--------|-----|
| Flake rate | falla si **> 0.10** | 1 |
| Defect leakage | falla si **> 0.12** | 1 |
| Test effectiveness | falla si **< 0.85** | 1 |
| Fairness gap (regiones) | falla si **> 0.25** | 2 |
| PSI (drift) | falla si **> 0.25** | 2 |

## Funciones a implementar

1. `flake_rate(flaky_tests, total_tests)` — tests flaky / tests ejecutados
2. `defect_leakage(prod_defects, total_defects)` — defectos en prod / defectos totales
3. `test_effectiveness(defects_found_in_test, total_defects)` — defectos hallados en testing / totales
4. `fairness_gap(approval_rates)` — tasa de aprobación más alta menos la más baja entre regiones
5. `psi(expected_pct, actual_pct)` — Population Stability Index: `Σ (actual − esperado) × ln(actual / esperado)`
6. `quality_gate(metrics)` — evalúa las 5 métricas contra los umbrales y devuelve el veredicto

Cada función tiene un docstring con los detalles (casos borde incluidos). Léelos antes de programar.

## Cómo correrlo

> **Requisito:** tener `uv` instalado (el mismo del lab del Día 2).
> Windows (PowerShell): `irm https://astral.sh/uv/install.ps1 | iex` · macOS: `brew install uv`

```bash
# Desde esta carpeta (reto-practico/, donde está el pyproject.toml)

# 1) Instala dependencias (solo pytest)
uv sync

# 2) Corre la suite — al inicio va a fallar: es lo esperado
uv run pytest -v

# 3) Implementa función por función y vuelve a correr hasta ver:
#    14 passed
```

Cuando el gate esté implementado, también puedes verlo decidir sobre un release de ejemplo:

```bash
uv run python -m src.quality_gate
```

Salida esperada (release de ejemplo con leakage roto: 28 de 200 bugs llegaron a prod → 0.14 > 0.12):

```json
{
  "checks": {
    "flake_rate": true,
    "defect_leakage": false,
    "test_effectiveness": true,
    "fairness_gap": true,
    "psi": true
  },
  "passed": false
}
```

## Entregable

- [ ] `uv run pytest -v` → **14 passed** (captura de pantalla o salida en texto)
- [ ] `uv run python -m src.quality_gate` → JSON con `"passed": false` y solo `defect_leakage` en `false`
- [ ] Puedes explicar en una frase por qué ese release se bloquea y quién debería ser el dueño de la acción

## Reglas

- No modifiques `tests/test_quality_gate.py` ni los umbrales: el gate se adapta al negocio, no al revés.
- Sin librerías externas: solo `math` y la biblioteca estándar.
- Si un test no te pasa, lee el nombre del test y su assert — es feedback inmediato (gamificación aplicada).
