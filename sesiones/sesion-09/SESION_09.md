# Sesión 9 — Móviles, escritorio y regresión visual

> **Duración:** 3 horas · Bloque A 45 → ☕ 15 → B 45 → ☕ 15 → C 45
> **Objetivo:** al terminar vas a poder ubicar Appium/Maestro/nativos/escritorio en el mapa, explicar emulador vs dispositivo real, correr un **smoke móvil** con Playwright (viewport), generar y comparar **baselines visuales**, y activar un **gate** que falla en rojo si la UI regresa.

**Blanco de hoy:** `app/index.html` — mini tienda responsive con modo claro/oscuro. Sobre ella corren smoke + visual.

**Herramientas (y por qué estas):**
- **Playwright** (viewport móvil + capturas PNG) para el lab. El temario menciona **Appium** + emulador; el setup de SDK/drivers no es multiplataforma “sin trucos” en 45 min. Appium, Maestro, Espresso, XCUITest quedan en el mapa.
- **Baselines PNG + umbral de píxeles** para regresión visual. El temario menciona Applitools/Percy; Playwright nativo ya sustituye Recheck en el PLAN_MAESTRO. Applitools/Percy quedan en el mapa (IA comercial).
- **FlaUI / Pywinauto** — mapa de escritorio (Windows-only; el curso es cross-OS).

**Frase del día:** **mismo flujo, distinta pantalla** — si no medís el layout (o el píxel), el verde del desktop miente.

**Cómo trabajamos hoy:** lab sincronizado. Sin Docker. Todo con `uv` + Playwright.

---

## Antes de empezar

```bash
cd proyecto-integrador/mobile-visual-lab
uv sync --group dev
uv run playwright install chromium
uv run python scripts/capture_baselines.py
uv run pytest tests -v          # 5 passed
```

**Atajos:** `task setup:mobile` · `task test:mobile` · `task test:mobile:gate` (este último **exit 1** a propósito).

---

## Anatomía del lab (opcional — core del ejemplo)

No es curso de front. Esto es lo que suele interesar cuando preguntan “¿cómo está armado?”:

| Archivo / carpeta | Para qué sirve en QA |
|---|---|
| `pyproject.toml` | Deps (`playwright`, `pillow`) y `testpaths = ["tests"]` |
| `tests/conftest.py` | Viewports 390×844 / 1280×720 y URLs `file://` |
| `tests/visual_utils.py` | Diff de píxeles (Pillow) + umbral |
| `tests/baselines/*.png` | Contrato visual versionado en git |
| `gate/` | Suite roja fuera de `testpaths` (patrón S8 `healing/`) |
| `reports/` | Capturas actuales (gitignored) |
| `app/index.html` | Solo importan `?broken=1`, `?theme=dark` y roles ARIA |

---

## Agenda (3 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 45 min | Mapa móvil/escritorio · híbrido vs nativo · emulador vs real · por qué Playwright hoy |
| ☕ | 15 min | — |
| **B** | 45 min | Lab: smoke móvil → baselines → regresión visual → gate rojo |
| ☕ | 15 min | — |
| **C** | 45 min | Dark mode + breakpoints · Applitools/Percy en mapa · Etapa 9 CI · puente a S10 |

Diapositivas: `PPT_CONTENIDO.md` / `sesion-09.pptx`.

---

## Bloque A — Mapa de plataformas (45 min) · Slides 1–9

### 1. El verde del desktop no basta (Slide 3)

Una suite desktop pasa: login, carrito, checkout. En el teléfono el botón “Ingresar” queda fuera de pantalla o el precio se superpone. Nadie midió el layout. Hoy cerramos esa brecha.

### 2. Tres mundos de UI (Slide 4–5)

- **Web móvil / responsive** — misma app, viewport distinto (lo que practicamos hoy).
- **Híbrido** — WebView dentro de un shell nativo (a menudo Appium).
- **Nativo** — UIKit / Jetpack Compose / etc. (Espresso, XCUITest, Appium, Maestro).

**Escritorio nativo:** FlaUI (Windows/.NET), Pywinauto (Windows). Útiles en empresas Windows; no son el lab multiplataforma de hoy.

### 3. Appium vs Maestro vs nativos (Slide 6)

| Herramienta | Rol |
|---|---|
| **Appium** | Estándar multiplataforma (iOS/Android/móvil web); server + drivers |
| **Maestro** | Flujos YAML, rápido de escribir; emergente 2026 |
| **Espresso** | Android nativo, en-proceso, muy estable |
| **XCUITest** | iOS nativo (Apple) |

### 4. Emulador vs dispositivo real (Slide 7)

Emulador: barato, reproducible, no idéntico al hardware. Dispositivo real: gestos, red, batería — más caro de mantener.

### 5. Regresión visual y Playwright (Slides 8–9)

Línea base (PNG) + captura actual + umbral de píxeles. Si el diff supera el umbral, el gate falla — igual que K6, ZAP y mutación. Applitools/Percy agregan IA y baselines en la nube; el concepto es el mismo. Hands-on: Playwright (viewport + PNG) porque Appium no cabe en 45 min.

---

## Bloque B — Lab sincronizado (45 min) · Slides 10–17

```bash
cd proyecto-integrador/mobile-visual-lab
uv run pytest tests/test_mobile_smoke.py -v
```

Smoke en viewport 390×844: login y producto usables.

```bash
uv run python scripts/capture_baselines.py   # si aún no lo corriste
uv run pytest tests/test_visual_regression.py -v
```

Tres baselines: desktop light/dark + mobile light. Diff ≤ 120 píxeles → pasa.

```bash
uv run pytest gate -v
```

`?broken=1` mete banner rojo → **FAILED** (exit 1). Gate real: si hay regresión, no queda verde.

Plantilla CI: `workflows/qa-visual.yml` — mismo smoke + gate.

---

## Bloque C — Dark, mapa IA visual, Etapa 9 (45 min) · Slides 18–24

- Dark mode: `?theme=dark` y baseline `home-desktop-dark.png`.
- Responsive: media query ≥768px cambia a dos columnas (mirá el HTML).
- Mapa: Applitools / Percy / Chromatic — cuándo pagar IA vs PNG local.
- Etapa 9 del proyecto: evidencia visual en el PR.
- Puente a **S10:** ensamblar la puerta de release completa.

---

## Checklist de salida

- [ ] Distingo web móvil, híbrido y nativo
- [ ] Ubico Appium, Maestro, Espresso, XCUITest, FlaUI/Pywinauto
- [ ] Corrí smoke en viewport móvil
- [ ] Generé / comparé baselines visuales
- [ ] Vi el gate fallar con UI rota
- [ ] Sé qué aportan Applitools/Percy frente a PNG local
