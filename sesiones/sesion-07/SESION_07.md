# Sesión 7 — Seguridad y otras no funcionales

> **Duración:** 3 horas · Bloque A 45 → ☕ 15 → B 45 → ☕ 15 → C 45  
> **Objetivo:** al terminar esta sesión vas a poder explicar qué es un escaneo **DAST** baseline, correr **OWASP ZAP** contra **Juice Shop** en Docker, leer un reporte de alertas, entender el rol de `rules.tsv` como “threshold” de seguridad, y seguir una demo de **Axe** (WCAG) en tu máquina.

**SUT de seguridad:** [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) en Docker (`localhost:3000`) — aplicación **vulnerable a propósito** para aprender.  
**No escaneamos SauceDemo** (es un sitio público de terceros): usamos un target local controlado.

**Frase del día:** un test funcional en verde **no** garantiza que la app sea segura ni usable para todas las personas.

**Cómo trabajamos hoy:** en los labs vas a **seguir al instructor en simultáneo** (mismos comandos, mismos archivos). No hay “reto para la casa” separado: la práctica es la clase.

---

## Antes de empezar

```bash
# 1. Docker Desktop Running
docker version

# 2. Entrá al lab
cd proyecto-integrador/security

# 3. (Primera vez) dejá bajando imágenes mientras arranca la teoría
docker compose pull
```

**Puertos:** `3000` libre (Juice Shop).  
**Atajos** (cuando existan en Taskfile): `task test:security:zap` · `task test:security:axe`.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido (alineado al PPT) |
|---|---|---|
| **A** | 45 min | Por qué seguridad en QA · Top 10 · SAST/DAST · ZAP vs Burp · baseline vs full · mapa del lab |
| ☕ | 15 min | — |
| **B** | 45 min | Lab sincronizado: Juice Shop → ZAP baseline → leer HTML → `rules.tsv` → plantilla CI |
| ☕ | 15 min | — |
| **C** | 45 min | WCAG · demo Axe (seguí en local) · Lighthouse · clouds de compatibilidad · checklist |

Las diapositivas están en `PPT_CONTENIDO.md` / `sesion-07.pptx` (misma numeración).

---

## Bloque A — Seguridad sin magia (45 min) · Slides 1–9

### 1. El problema que el assert no ve (Slide 3)

Imaginate este escenario:

1. El login automatizado está **verde**: status 200, redirige al inventario.  
2. En producción alguien roba la sesión porque la cookie **no** traía `HttpOnly` / `Secure`.  
3. O un campo de búsqueda refleja HTML sin escapar → **XSS**.

Tu suite de API/UI seguía pasando. El negocio igual tiene un incidente.

**Idea:** la puerta de calidad (S5) ya pregunta “¿pasa el test?” y “¿es rápido?” (S6). Hoy pregunta: **¿es obviamente inseguro?** y más tarde **¿es accesible?**

### 2. Tu rol (Slide 4)

No venís a reemplazar a un pentester. Venís a:

- meter un **escaneo base** en el mismo ritual que CI;  
- **leer** un reporte y abrir un bug entendible;  
- acordar con el equipo qué hallazgo es **FAIL** (bloquea) y cuál es ruido.

### 3. OWASP Top 10 — mapa (Slide 5)

OWASP publica un “top” de riesgos web. No lo memorices de pe a pa hoy. Sí ubicá que existen categorías como *Injection*, *Broken Access Control*, *Security Misconfiguration*, etc. En el lab vas a ver sobre todo cosas que ZAP detecta en modo **pasivo** (headers, cookies, configuraciones).

### 4. SAST vs DAST vs SCA (Slide 6)

| Tipo | ¿Qué inspecciona? | Ejemplo |
|---|---|---|
| **SAST** | Código fuente | Sonar, CodeQL |
| **DAST** | La app **corriendo** | **OWASP ZAP** (hoy), Burp |
| **SCA** | Librerías / dependencias | npm audit, pip-audit |

Hoy hacemos **DAST**: levantamos Juice Shop y ZAP le pega como un cliente más.

### 5. ZAP vs Burp (Slide 7)

| Herramienta | Cuándo la vas a ver |
|---|---|
| **OWASP ZAP** | Open source, scripts Docker, Actions — **hands-on de hoy** |
| **Burp Suite** | Proxy manual, pentest exploratorio (Community/Pro) |

El patrón es parecido (interceptar, reptar el sitio, listar alertas). Cambia el encaje: **ZAP entra fácil al pipeline**.

### 6. Baseline vs Full (Slide 8)

| Scan | Comportamiento | Uso sano |
|---|---|---|
| **Baseline** | Spider corto + reglas **pasivas** | PR / cada cambio — **lo de hoy** |
| **Full** | Ataque **activo** (payloads) | Staging dedicado / job nocturno — **no** contra prod “porque sí” |

Pensalo como el smoke vs load de K6: el baseline es barato y seguro para repetir.

### 7. El laboratorio (Slide 9)

```
proyecto-integrador/security/
  docker-compose.yml     ← juiceshop + zap-baseline
  zap/rules.tsv          ← política WARN/FAIL/IGNORE
  reports/               ← HTML + JSON del escaneo
  a11y/                  ← demo Axe (Bloque C)
  scripts/run_baseline.py ← atajo multiplataforma (Windows/Mac/Linux)
  workflows/qa-security.yml  ← plantilla CI (lectura)
```

**Comandos que vas a usar en el Bloque B:**

```bash
cd proyecto-integrador/security
# Importante: copiá la política al workdir (el script run_baseline.py ya lo hace)
cp zap/rules.tsv reports/rules.tsv
docker compose up -d --wait juiceshop
docker compose run --rm zap-baseline
```

O usá el atajo (mismo en cualquier SO):

```bash
python scripts/run_baseline.py
```

---

## ☕ Descanso (15 min)

Dejá Docker Desktop abierto. Si podés, empezá el `docker compose pull` si no lo corriste.

---

## Bloque B — Lab sincronizado con el instructor (45 min) · Slides 10–17

> **Regla:** el instructor dicta el paso; vos lo ejecutás en tu máquina. Si te atrasás, no improvises: reenganchá en el siguiente comando de la pantalla.

### Paso 1 — Juice Shop arriba (Slide 11)

```bash
cd proyecto-integrador/security
docker compose up -d --wait juiceshop
```

Abrí el navegador en `http://localhost:3000`. Deberías ver la tienda Juice Shop.

Si el puerto 3000 está ocupado, avisá: hay que liberarlo o cambiar el mapeo en `docker-compose.yml`.

### Paso 2 — Baseline (Slide 12)

```bash
cd proyecto-integrador/security
python scripts/run_baseline.py
```

Equivale a levantar Juice Shop + correr `docker compose run --rm zap-baseline` (y copia `rules.tsv`).

Esto puede tardar **2–3 minutos**. Mientras corre, anotá el exit code final.

### Paso 3 — Leer el reporte (Slide 13)

Abrí `reports/zap-report.html` en el navegador.

Como en K6 (solo 4 cosas), acá mirá:

1. **Risk**  
2. **Name**  
3. **Description**  
4. **Solution**

Elegí **una** alerta y escribí en el chat / cuaderno:  
*“Esta alerta dice que ___ y el riesgo es ___.”*

También existe `reports/zap-report.json` (útil para CI o scripts).

### Paso 4 — El “threshold” de seguridad: `rules.tsv` (Slides 14–15)

Abrí `zap/rules.tsv`. Vas a ver líneas como:

```tsv
10038	WARN	Content Security Policy (CSP) Header Not Set
10096	IGNORE	Timestamp Disclosure - Unix (a menudo ruido)
```

| Acción | Efecto práctico |
|---|---|
| `IGNORE` | No ensucia el gate |
| `WARN` | Avisa |
| `FAIL` | Puede poner el job en **rojo** (bloquea merge si así lo configurás) |

**Puente con S5/S6:** pytest falla → rojo. K6 threshold roto → exit 99. ZAP con regla en FAIL → el pipeline también puede decir **no**.

Los IDs de regla salen del reporte. En un equipo real, AppSec y QA acuerdan el archivo juntos.

### Paso 5 — Plantilla CI (Slide 16)

Abrí `workflows/qa-security.yml` (plantilla didáctica). La idea es la misma:

```yaml
docker compose up -d --wait juiceshop
docker compose run --rm zap-baseline
```

Hoy no hace falta que el workflow esté activo en GitHub: el criterio ya lo viste en local (comando + reporte + política).

### Logro del Bloque B (Slide 17)

Si llegaste hasta acá, ya hiciste la **Etapa 6** del proyecto integrador en la práctica: escaneo base automatizable.

---

## ☕ Descanso (15 min)

Sin tarea pesada. Si el baseline no terminó, pedile al instructor el HTML de ejemplo y seguí en el Bloque C con la lectura.

---

## Bloque C — Accesibilidad y mapa no funcional (45 min) · Slides 18–24

### 1. WCAG en una frase (Slide 19)

**WCAG** = pautas de accesibilidad web. Los 4 principios (**POUR**):

- **Perceptible** — ¿se puede percibir la info?  
- **Operable** — ¿se puede usar (teclado, etc.)?  
- **Comprensible** — ¿se entiende?  
- **Robusto** — ¿funciona con tecnologías de asistencia?

Automatizar ayuda; **no reemplaza** pruebas con teclado / lector de pantalla.

### 2. Demo Axe — seguí al instructor (Slide 20)

El instructor corre esto en vivo. **Vos podés (y deberías) repetirlo en local:**

```bash
cd proyecto-integrador/security/a11y
uv sync --group dev
uv run playwright install chromium
uv run pytest -v
```

La página `bad_page.html` tiene problemas **a propósito** (imagen sin `alt`, contraste malo, controles sin nombre accesible, etc.).

**Resultado esperado:** Axe encuentra violaciones (p. ej. **7**) y pytest sale **FAILED** (`assert total == 0`). Eso es el gate: si hay fallos de a11y, la suite **no** queda verde. Los reportes HTML/JSON se escriben *antes* del assert para poder leerlos en clase.

> Ojo: un `assert len(violations) >= 1` dejaría la suite verde cuando la página está rota. Eso no es un gate; es una demo engañosa. Acá el assert exige **cero** violaciones.

Así queda plantada la **Etapa 7** (accesibilidad) del gate: un chequeo automatizable en CI, igual que ZAP.

### 3. Lighthouse (Slide 21)

Lighthouse (Chrome DevTools) mezcla performance, a11y, SEO y buenas prácticas. Hoy es **mapa**: sabé que existe; Axe es más enfocado a reglas WCAG en automatización.

### 4. Compatibilidad entre navegadores (Slide 22)

| Plataforma | Para qué sirve |
|---|---|
| BrowserStack | Matriz real browser × OS en la nube |
| Sauce Labs | Igual, muy visto con Selenium/Appium |
| LambdaTest | Alternativa vigente (reemplazo práctico de CrossBrowserTesting) |

No hace falta cuenta hoy. La idea: **“en mi Chrome pasa” no es estrategia**.

### Checklist (Slide 23)

- [ ] Explico DAST en una frase  
- [ ] Distingo baseline vs full scan  
- [ ] Corrí (o seguí) ZAP baseline y abrí el HTML  
- [ ] Sé para qué sirve `rules.tsv`  
- [ ] Vi Axe marcar problemas en `bad_page.html`  
- [ ] Ubico Burp, Lighthouse y las clouds de compatibilidad  

### Frase de cierre (Slide 24)

Completá: *"Un hallazgo de ZAP sirve para ___."*

### Para llevar

Sumaste al proyecto integrador:

- **Etapa 6:** seguridad base con ZAP  
- **Etapa 7:** accesibilidad con Axe (lab listo para repetir)

**Próxima (S8):** mantenimiento de suites, auto-healing y pruebas de mutación.

---

## Errores comunes

| Síntoma | Qué hacer |
|---|---|
| Puerto 3000 ocupado | Liberá el puerto o cambiá `"3001:3000"` en compose |
| Juice Shop no abre | `docker compose logs juiceshop` · esperá el healthcheck |
| ZAP no resuelve `juiceshop` | Usá `docker compose run` (misma red), no `localhost` desde el contenedor ZAP |
| Primera corrida muy lenta | Estás bajando imágenes; pre-pull: `docker compose pull` |
| `reports/` vacío | El volumen necesita permisos de escritura; revisá que la carpeta exista |
| Axe / Playwright falla | `uv sync --group dev` + `uv run playwright install chromium` |

---

## Resumen de comandos

```bash
cd proyecto-integrador/security
python scripts/run_baseline.py
# Abrí reports/zap-report.html

docker compose down

# Axe
cd proyecto-integrador/security/a11y
uv sync --group dev
uv run playwright install chromium
uv run pytest -v
```
