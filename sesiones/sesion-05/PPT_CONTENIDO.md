# Sesión 5 — Contenido de diapositivas
## CI/CD: control de calidad automático

> 20 slides · Bloque A: 1–7 (45 min) · Bloque B: 8–14 (45 min) · Bloque C: 15–20 (45 min)  
> Misma densidad que S4/S6: **idea + ejemplo concreto** (YAML/código), no solo bullets.

---

### Slide 1 — Portada (2 min)
**Título:** CI/CD — control de calidad automático
- Sesión 5 de 10 · Curso QA Automation
- Hoy: la suite de la S4 corre **sola**, en un entorno común
- Frase: si un test solo pasa en tu máquina, no es un test de equipo

### Slide 2 — ¿Dónde estamos? (3 min)
- S3/S4 ✅ Tests de API (Postman + pytest) que **vos** corrés a mano
- S5 → Hoy el **juez** pasa a ser un entorno controlado (Docker / GitHub Actions)
- S6 → Mañana: el gate también mira **velocidad** (K6)
- Al salir: CI en una frase · YAML leído · suite verde en Docker

### Slide 3 — “En mi máquina sí pasa” (5 min)
**Título:** El problema que CI resuelve todos los días

1. Ana corre tests → **verde**
2. Sube el código
3. En la máquina de Luis / el servidor → **rojo**

- Nadie mintió: entornos distintos (Python, deps, OS, archivo no commiteado)
- Falta un lugar **neutral y común**
- Chat 10 s: ¿les ha pasado?

### Slide 4 — CI y CD en una frase (4 min)
| Sigla | En una frase |
|---|---|
| **CI** | Cada cambio se **verifica solo** en un entorno controlado |
| **CD** | Además se **prepara o despliega** de forma automatizada |

- Hoy = solo la **puerta de calidad** (verificación)
- Desplegar es otro capítulo — mismo patrón de automatización

### Slide 5 — Mapa de herramientas (4 min)
**Título:** Todas hacen lo mismo: evento → pasos → verde/rojo

| Herramienta | Hoy |
|---|---|
| **GitHub Actions** | Hands-on — YAML en el repo |
| Jenkins / GitLab CI / Azure Pipelines | Mapa — mismo patrón, otro archivo |

- El patrón importa; la sintaxis se aprende en una semana
- Elegimos Actions porque vive en el mismo repo y no instalás nada extra

### Slide 6 — Anatomía del YAML (10 min)
**Título:** No memorices — aprendé qué pregunta responde cada clave

Abrí: `ci-lab/workflows/qa-api.yml`

| Clave | Pregunta |
|---|---|
| `on:` / `paths:` | ¿Cuándo? ¿Ante qué cambios? |
| `permissions:` | ¿Con qué privilegios? (`contents: read`) |
| `concurrency:` | ¿Cancela runs viejos del mismo PR? |
| `jobs:` / `runs-on:` | ¿Qué trabajos? ¿En qué máquina? |
| `steps:` / `run:` | ¿Qué comandos, en orden? |

```yaml
- run: uv sync --group dev
- run: uv run pytest -v
- run: uv run pytest -v -k smoke
```

- Esos `run:` son **los mismos comandos** que corrés a mano en api-lab
- Pausa 20 s: sin mirar — ¿qué hace `on:`?

### Slide 7 — Regla de oro + patrones 2026 (5 min)
**Título:** Mismo comando local ≈ CI

> El comando en el que confiás localmente debe ser el mismo que corre en CI.

- Docker = puente entre tu laptop y el runner Ubuntu
- En el YAML real también: `permissions` · `concurrency` · caché `uv`
- Café → lo vemos **verde** en contenedor

---
**☕ DESCANSO 15 MIN**
---

### Slide 8 — Arranque B (1 min)
**Título:** Lab — el juez en tu máquina
- Misma suite api-lab (S4) · lab principal = Docker

### Slide 9 — Predicción (3 min)
- Antes de Enter: ¿verde o rojo? ¿por qué?
- Escribí 5 s en el chat (predict → observe → explain)

### Slide 10 — Lab Docker (12 min)
```bash
cd proyecto-integrador/ci-lab
docker compose build test
docker compose run --rm --no-deps test
```

- Esperado: **17 passed** (los mismos de la S4)
- `build` la 1.ª vez tarda; después usa caché
- Local con `uv` = opcional (Plan B si JSONPlaceholder cae: Docker + YAML)

### Slide 11 — Qué hay dentro del contenedor (5 min)
**Título:** No es magia — es una imagen con la suite empaquetada

```dockerfile
FROM python:3.12-slim
# uv + COPY de api-lab (client, tests, data…)
RUN uv sync --group dev --frozen
CMD ["uv", "run", "pytest", "-v"]
```

- Deps fijas · Python fijo · menos “en mi máquina…”
- Espejo razonable del runner de GitHub Actions

### Slide 12 — Disparadores (5 min)
| Evento | Cuándo |
|---|---|
| `push` / `pull_request` | Cambios (filtrados por `paths`) |
| `workflow_dispatch` | Botón manual en Actions |
| `schedule` | Cron nocturno — concepto (S6 lo retoma) |

- `paths` = no gastar minutos si cambió un README de otra carpeta
- Smoke barato en PR · load pesado después (idea S6)

### Slide 13 — Workflow real del repo (5 min)
**Título:** `.github/workflows/qa-api.yml`

- Señalá: `permissions` · `concurrency` · `working-directory` · step smoke
- Pregunta: ¿quién ve el `working-directory`? → `proyecto-integrador/api-lab`
- Caché `enable-cache: true` en setup-uv → 2.ª corrida más rápida

### Slide 14 — Logro del bloque (2 min)
- Verde en un entorno que **no** es “tu laptop a ojo”
- Café → mini-reto smoke + ticket de salida

---
**☕ DESCANSO 15 MIN**
---

### Slide 15 — Arranque C (1 min)
**Título:** Mini-reto y cierre

### Slide 16 — Mini-reto: `-k smoke` (10 min)
```bash
cd proyecto-integrador/api-lab
uv run pytest -v -k smoke
```

- Smoke = “¿lo básico funciona?” en segundos
- En un PR de 40 archivos: ¿por qué un job smoke primero ahorra tiempo?
- Sin `uv`: el mismo step ya está en el YAML — leelo y explicalo

### Slide 17 — Checklist (5 min)
- [ ] Explico CI en **una** frase
- [ ] Señalo `on` / `jobs` / `steps` (y sé para qué son `permissions` / `concurrency`)
- [ ] Corrí la suite en Docker (`ci-lab`) → 17 passed
- [ ] Regla: mismo comando local ≈ CI

### Slide 18 — Errores comunes (4 min)
| Síntoma | Qué hacer |
|---|---|
| Docker daemon | Desktop → **Running** |
| 1.ª build lenta | Normal; la 2.ª es rápida |
| API pública caída | Plan B: Docker + YAML |
| Sin `uv` | El lab Docker no lo necesita |

### Slide 19 — Ticket de salida + puente S6 (5 min)
- Completá: *"CI es ___ porque ___."*
- Pedí 2 lecturas en voz alta
- Mañana: ¿la API es lo bastante **rápida**? (K6 + thresholds)

### Slide 20 — Gracias
- Material: `sesiones/sesion-05/` + `proyecto-integrador/ci-lab/`
- Próxima: Performance con K6 — el gate también se pone rojo si es lento
