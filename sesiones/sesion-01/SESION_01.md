# GUÍA DEL INSTRUCTOR — Sesión 1: Diseño Técnico de Pruebas

> **Duración:** 3 horas (Bloque A 55min + Bloque B 55min + Bloque C 60min + 2 descansos de 5min)
> **Objetivo:** Que el estudiante convierta requerimientos en casos de prueba usando EP, BVA, tablas de decisión y pairwise.
> **Entregable:** Suite de tests corriendo en verde + matriz de trazabilidad actualizada.
> **Prerequisitos:** Python 3.12+, `uv` instalado, terminal funcional.

---

## ANTES DE CLASE — Checklist del instructor

Haz esto **antes** de llegar al salón. No lo dejes para el momento de la clase.

- [ ] Ejecuta `cd proyecto-integrador/design-lab && uv sync && uv run pytest -v` en tu máquina. Todo debe pasar.
- [ ] Abre SauceDemo (https://www.saucedemo.com) y verifica que funciona.
- [ ] Ten proyectado en pantalla: este documento, un navegador abierto con SauceDemo, y una terminal.
- [ ] Verifica que los estudiantes tienen `uv` instalado (puedes enviar instrucciones por correo/chat antes de clase).

---

## 🗺️ MAPA DE LA SESIÓN (proyéctalo al inicio)

```
Bloque A (55 min) — Yo explico, tú observas
  0-10   Problema real: por qué 300 tests no encontraron el bug
  10-25  Las 4 técnicas explicadas con ejemplos simples
  25-35  Trazabilidad: qué es y por qué importa
  35-50  Demo en vivo: de requerimiento a test
  50-55  Resumen + preguntas

  ☕ Descanso 5 min

Bloque B (55 min) — Tú codificas, yo te guío
  0-10   Arrancar el laboratorio
  10-30  Leer y ejecutar EP + BVA
  30-45  Leer y ejecutar tabla de decisión
  45-55  Leer y ejecutar pairwise

  ☕ Descanso 5 min

Bloque C (60 min) — Tú trabajas solo, yo superviso
  0-25   Ejercicio: diseñar casos para login de SauceDemo
  25-45  Mini reto: pairwise para matriz web
  45-60  Errores comunes + cierre
```

---

## [POWERPOINT] Contenido exacto de cada diapositiva

> Cada diapositiva tiene: título, texto exacto que va en la slide, y nota de diseño.
> El guion del instructor (qué decir en voz alta) NO va en la slide — está en el cuerpo de esta guía.

---

### SLIDE 1 — Portada

**Título (grande, centrado):**
```
Sesión 1: Diseño Técnico de Pruebas Automatizadas
```

**Subtítulo:**
```
Certificación 3 — Ingeniería de Automatización: APIs, Performance y Seguridad
```

**Pie de página:**
```
Tu nombre · Institución · Fecha
```

**Diseño:** Logo de la institución en la esquina superior derecha. Fondo limpio, sin imágenes.

---

### SLIDE 2 — Objetivo de hoy

**Título:**
```
¿Qué vas a aprender hoy?
```

**Texto (una sola frase, grande):**
```
Convertir requerimientos en casos de prueba
antes de escribir una sola línea de código.
```

**Debajo, las 4 técnicas en una línea:**
```
EP · BVA · Tabla de Decisión · Pairwise
```

**Diseño:** Sin bullets, sin explicaciones. Solo la frase y los 4 nombres. El instructor los explica en voz alta.

---

### SLIDE 3 — El problema

**Título:**
```
El problema
```

**Texto (grande, centrado, 3 líneas):**
```
300 tests automatizados.
Todo pasa en verde.
Producción se rompe con un pedido de $1,000.
```

**Pregunta debajo (en otro color):**
```
¿Por qué?
```

**Diseño:** Fondo oscuro, texto blanco grande. La pregunta en amarillo o naranja. Pausa dramática — dejar que los estudiantes respondan antes de cambiar de slide.

---

### SLIDE 4 — La respuesta

**Título:**
```
Cantidad de tests ≠ Cobertura de diseño
```

**Texto (3 preguntas, una por línea):**
```
Antes de codificar, responde:

1. ¿QUÉ probar?    → Las técnicas de diseño
2. ¿CUÁNTO probar?  → Cobertura mínima suficiente
3. ¿CÓMO demostrarlo? → La matriz de trazabilidad
```

**Diseño:** Las 3 preguntas numeradas. Las respuestas a la derecha en color distinto. Sin diagramas — el instructor explica cada una en voz alta.

---

### SLIDE 5 — EP: Partición de Equivalencias

**Título:**
```
EP — Partición de Equivalencias
```

**Texto:**
```
Si todos los valores dentro de un rango producen el mismo resultado,
basta probar UNO por grupo.
```

**Diagrama (dibujar en la slide):**
```
Campo "edad": acepta de 18 a 65

 ❌ Inválido        ✅ Válido          ❌ Inválido
┌───────────┐    ┌────────────┐    ┌───────────┐
│  < 18     │    │  18 a 65   │    │  > 65     │
│  ej: 10   │    │  ej: 30    │    │  ej: 70   │
│  → error  │    │  → ok      │    │  → error  │
└───────────┘    └────────────┘    └───────────┘
     ↑                 ↑                 ↑
  probar 1          probar 1          probar 1
```

**Nota al pie (en rojo):**
```
⚠️ Siempre incluir las particiones INVÁLIDAS.
   Ahí viven los errores más frecuentes.
```

---

### SLIDE 6 — BVA: Análisis de Valores Límite

**Título:**
```
BVA — Análisis de Valores Límite
```

**Texto:**
```
Los errores viven en las fronteras.
El bug típico: un < que debería ser <=
```

**Diagrama:**
```
Rango: 18 a 65

       probar   probar                   probar   probar
         ↓        ↓                        ↓        ↓
   ──────17──────18──────────────────────65──────66──────
         ↑        ↑                        ↑        ↑
      inválido  válido                  válido   inválido
```

**Ejemplo del laboratorio:**
```
Umbral de volumen: $1,000

Probar: $999.99 → sin bono   (justo antes del límite)
Probar: $1,000.00 → con bono (exactamente en el límite)

Si el programador escribió > en vez de >=,
el test de $1,000.00 lo detecta.
```

---

### SLIDE 7 — Tabla de Decisión

**Título:**
```
Tabla de Decisión
```

**Texto:**
```
3 condiciones (sí/no) = 2³ = 8 reglas
Sin la tabla completa, las combinaciones peligrosas se escapan.
```

**Tabla (dibujar en la slide):**

| # | ¿Premium? | ¿≥ $1,000? | ¿Cupón? | Descuento |
|---|-----------|-----------|---------|-----------|
| R1 | No | No | No | 0% |
| R2 | No | No | Sí | 5% |
| R3 | No | Sí | No | 5% |
| R4 | No | Sí | Sí | 10% |
| R5 | Sí | No | No | 10% |
| R6 | Sí | No | Sí | 15% |
| R7 | Sí | Sí | No | 15% |
| **R8** | **Sí** | **Sí** | **Sí** | **15% ← tope** |

**Nota al pie (en rojo, debajo de la tabla):**
```
⭐ R8 es la regla más valiosa:
   Premium(10%) + Volumen(5%) + Cupón(5%) = 20%
   Pero el tope de 15% la recorta.
   Sin la tabla, NADIE piensa en probar este caso.
```

---

### SLIDE 8 — Pairwise Testing

**Título:**
```
Pairwise Testing: de 54 a ~10
```

**Texto (lado izquierdo — el problema):**
```
Problema:
  3 navegadores
  × 3 sistemas
  × 2 idiomas
  × 3 roles
  = 54 combinaciones
```

**Texto (lado derecho — la solución):**
```
Pairwise garantiza que cada PAR
de valores aparece junto
al menos una vez.

54 combinaciones → ~10 filas
~80% menos tests
~misma detección de defectos
```

**¿Por qué funciona? (debajo, centrado):**
```
La mayoría de defectos son causados por
la interacción de máximo 2 parámetros.
```

**Nota de advertencia (en amarillo, al final):**
```
⚠️  La herramienta puede dejar pares sin cubrir.
    En el laboratorio van a descubrir el bug y escribir
    un test que lo detecte.
```

---

### SLIDE 9 — Trazabilidad

**Título:**
```
Trazabilidad: REQ → TC → DEF
```

**Diagrama (centro de la slide):**
```
 REQUERIMIENTO         CASO DE PRUEBA           DEFECTO
┌──────────────┐ 1..N ┌─────────────────┐ 0..N ┌──────────┐
│ REQ-DSC-002  │─────►│ TC-DSC-BVA-004  │─────►│ DEF-017  │
│ "≥1000 → +5%"│      │ límite $1,000   │      │ off-by-1 │
└──────────────┘      └─────────────────┘      └──────────┘
```

**Debajo, las 2 preguntas que responde la matriz:**
```
¿Qué REQ no tiene TC?  → hueco de cobertura
¿Qué TC no tiene REQ?  → test zombie (borrar)
```

**Nota al pie:**
```
La matriz vive en el repo (CSV), no en Excel.
Se revisa en cada Pull Request junto al código.
```

**Diseño:** Los 3 recuadros en colores distintos (azul, verde, rojo). Flechas gruesas. Las 2 preguntas en amarillo.

---

### SLIDE 10 — Demo: la función del laboratorio

**Título:**
```
Demo: calculate_discount
```

**Contenido:** Screenshot o fragmento de código de `discount.py`:
```python
def calculate_discount(customer_type, order_total, has_coupon):
    """
    REQ-DSC-001: premium → +10%; standard → +0%
    REQ-DSC-002: order_total >= 1000 → +5% (volumen)
    REQ-DSC-003: has_coupon → +5%
    REQ-DSC-004: descuento total nunca excede 15%
    REQ-DSC-005: 0 < order_total <= 10000; si no, ValueError
    """
```

**Nota al pie:**
```
5 requerimientos. 5 reglas trazables.
Cada test que escribamos tendrá el ID del REQ que prueba.
```

**Diseño:** Fondo oscuro tipo IDE. Código en fuente monoespaciada. Los REQ-DSC-* en color destacado.

---

### SLIDE 11 — Estructura del laboratorio

**Título:**
```
Estructura del proyecto
```

**Contenido (árbol de archivos):**
```
proyecto-integrador/
├── trazabilidad/
│   └── matriz-trazabilidad.csv     ← REQ ↔ TC ↔ DEF
└── design-lab/                     ← laboratorio de hoy
    ├── pyproject.toml              ← dependencias
    ├── data/
    │   └── decision_table.yaml     ← 8 reglas (datos)
    ├── design_lab/
    │   ├── discount.py             ← función a probar
    │   └── pairwise_matrix.py      ← generador pairwise
    └── tests/
        ├── test_equivalence_boundary.py   ← EP + BVA
        ├── test_decision_table.py         ← tabla de decisión
        └── test_pairwise.py               ← pairwise
```

**Nota al pie:**
```
Cada archivo tiene una sola responsabilidad.
Los datos están separados de la lógica.
```

---

### SLIDE 12 — Comandos

**Título:**
```
Comandos del laboratorio
```

**Contenido (2 columnas):**

| Con `task` (atajo) | Sin `task` (comando completo) |
|---|---|
| `task setup` | `cd proyecto-integrador/design-lab && uv sync` |
| `task test:design` | `cd proyecto-integrador/design-lab && uv run pytest -v` |

**Output esperado (debajo, en fuente monoespaciada):**
```
============================= 25 passed in 0.33s ==============================
```

**Nota:**
```
Si ves "25 passed" — tu entorno está listo.
```

---

### SLIDE 13 — Ejercicio: Login de SauceDemo

**Título:**
```
Ejercicio: Diseñar casos para el login
```

**Screenshot:** Captura de https://www.saucedemo.com mostrando la pantalla de login.

**Usuarios de prueba (tabla):**

| Usuario | Contraseña | Comportamiento |
|---------|-----------|----------------|
| `standard_user` | `secret_sauce` | Login exitoso |
| `locked_out_user` | `secret_sauce` | Error: usuario bloqueado |
| `problem_user` | `secret_sauce` | Login con glitches |
| `performance_glitch_user` | `secret_sauce` | Login lento |

**Tu tarea:**
```
Editar matriz-trazabilidad.csv:
  - Completar REQ-LOG-001, 002, 003
  - Derivar particiones de equivalencia
  - Construir tabla de decisión (3 condiciones)
  - Asignar tc_id a cada caso
```

---

### SLIDE 14 — Mini reto: Pairwise

**Título:**
```
Mini reto: Pairwise para matriz web
```

**Parámetros (tabla):**

| Parámetro | Valores |
|-----------|--------|
| Navegador | chromium, firefox, webkit |
| Pantalla | mobile, tablet, desktop |
| Tema | light, dark |
| Rol | admin, user |

**Restricción:**
```
admin NO se prueba en mobile
```

**Total sin pairwise:** 3 × 3 × 2 × 2 = **36 combinaciones**

**Tu test debe verificar:**
```
✅ a) El total es menor que 36
✅ b) La restricción se respeta (ninguna fila tiene admin + mobile)
✅ c) Todos los pares (pantalla, tema) están cubiertos
```

---

### SLIDE 15 — Errores comunes

**Título:**
```
Errores comunes vs Prácticas correctas
```

**Tabla (7 filas):**

| ❌ Error común | ✅ Práctica correcta |
|---|---|
| Probar solo el camino feliz | Cada valor viene de una técnica y traza a un REQ |
| Test gigante con 15 asserts | Parametrizado: agregar caso = agregar 1 línea |
| Datos incrustados en el test | Datos en YAML o CSV versionados en `data/` |
| Matriz en Excel que nadie actualiza | CSV en el repo, revisado en el Pull Request |
| "Más tests = más calidad" | Cobertura mínima suficiente: EP + BVA + tabla + pairwise |
| Ignorar particiones inválidas | `pytest.raises` como caso de primera clase |
| Copiar y pegar tests | `@parametrize`: el código no se duplica |

**Diseño:** Columna izquierda en rojo suave, columna derecha en verde suave.

---

### SLIDE 16 — Checklist de salida

**Título:**
```
Antes de irte, verifica:
```

**Checklist (4 items con checkbox):**
```
☐ uv run pytest -v → 25 passed (EP, BVA, tabla, pairwise)
☐ matriz-trazabilidad.csv → REQ-LOG-* completados con técnica
☐ Mini reto pairwise → implementado y pasando
☐ Puedes explicar en 1 min por qué DT-R8 no existiría sin tabla
```

**Diseño:** Texto grande, un item por línea. Los checkboxes vacíos para que mentalmente marquen.

---

### SLIDE 17 — Próxima sesión

**Título:**
```
Sesión 2: De diseño a código
```

**Texto:**
```
Lo que diseñaste hoy se convierte en
pruebas automatizadas de la UI de SauceDemo.

Patrones: Page Object Model · Screenplay · DRY
Datos: JSON · YAML · CSV · Fixtures

La matriz crece: TC-LOG-* pasan de DISEÑO → PASS
```

**Diseño:** Simple, sin diagramas. Solo las 3 líneas de texto. El instructor cierra con entusiasmo.

---

# BLOQUE A (55 min) — Yo explico, tú observas

---

## A.1 El problema real (minutos 0-10)

### [SLIDE 3] QUÉ DECIR (guion sugerido):

> "Imaginen esto: un equipo de QA tiene 300 tests automatizados. La suite tarda 40 minutos.
> Todo pasa en verde. Y aun así, producción se rompe cuando un cliente hace un pedido de
> exactamente $1,000. ¿Cómo es posible?"

**Pausa.** Deja que respondan. Alguien va a decir "porque no probaron ese valor". Exacto.

### [SLIDE 4] QUÉ DECIR:

> "Cantidad de tests NO es lo mismo que cobertura de diseño. Antes de escribir una sola
> línea de código, necesitamos responder 3 preguntas:"

1. **¿Qué probar?** → Las técnicas de diseño responden esto.
2. **¿Cuánto probar?** → Cobertura mínima suficiente, no exhaustiva.
3. **¿Cómo demostrar que está probado?** → La matriz de trazabilidad.

### QUÉ MOSTRAR:
- Nada de código todavía. Solo las 3 preguntas en la slide.
- Si preguntan "¿qué son las técnicas?", responde: "eso viene en los siguientes 15 minutos".

---

## A.2 Las 4 técnicas (minutos 10-25)

### [SLIDE 5] EP — Partición de Equivalencias (5 min)

**QUÉ DECIR:**
> "Si un campo acepta edades de 18 a 65, no necesitas probar los 47 valores.
> Todos los valores DENTRO del rango producen el mismo resultado. Basta con probar UNO."

**QUÉ MOSTRAR (dibuja en pizarra o slide):**
```
Campo "edad": 18 a 65

  Partición inválida     Partición válida     Partición inválida
  ┌──────────────┐      ┌──────────────┐     ┌──────────────┐
  │  edad < 18   │      │  18 ≤ edad   │     │  edad > 65   │
  │  ej: 10      │      │  ≤ 65        │     │  ej: 70      │
  │  → error     │      │  ej: 30      │     │  → error     │
  └──────────────┘      │  → aceptado  │     └──────────────┘
                        └──────────────┘
```

**REGLA CLAVE PARA ESTUDIANTES:**
> "Siempre incluir las particiones INVÁLIDAS. Ahí están los errores más frecuentes."

---

### [SLIDE 6] BVA — Análisis de Valores Límite (5 min)

**QUÉ DECIR:**
> "Los errores se acumulan en las fronteras. El típico bug es un `<` que debería ser `<=`.
> Por eso probamos el valor EXACTO del límite y sus vecinos inmediatos."

**QUÉ MOSTRAR:**
```
Rango: 18 a 65

       inválido   válido                    válido   inválido
          ↓         ↓                         ↓        ↓
    ────17────18─────────────────────65────66────
          ↑         ↑                         ↑        ↑
        probar    probar                    probar   probar
```

**EJEMPLO CONCRETO DEL LABORATORIO:**
> "En nuestro ejercicio de hoy, el umbral de volumen es $1,000. Vamos a probar $999.99
> (sin bono) y $1,000.00 (con bono). Si el programador escribió `>` en vez de `>=`,
> el test de $1,000.00 lo detecta."

---

### [SLIDE 7] Tabla de Decisión (5 min)

**QUÉ DECIR:**
> "Cuando hay condiciones que interactúan, hacemos una tabla con TODAS las combinaciones.
> 3 condiciones sí/no = 2³ = 8 reglas."

**QUÉ MOSTRAR (dibuja la tabla en pizarra):**

| # | ¿Premium? | ¿≥ $1,000? | ¿Cupón? | Descuento |
|---|-----------|-----------|---------|-----------|
| R1 | No | No | No | 0% |
| R2 | No | No | Sí | 5% |
| R3 | No | Sí | No | 5% |
| R4 | No | Sí | Sí | 10% |
| R5 | Sí | No | No | 10% |
| R6 | Sí | No | Sí | 15% |
| R7 | Sí | Sí | No | 15% |
| **R8** | **Sí** | **Sí** | **Sí** | **15%** ← tope |

**ENFATIZAR:**
> "La regla R8 es la más importante. Premium + volumen + cupón suma 20%, pero el tope
> de 15% lo recorta. Si no construyen la tabla completa, NADIE piensa en probar este caso.
> Y es un defecto que llega a producción."

---

### [SLIDE 8] Pairwise Testing (5 min)

**QUÉ DECIR:**
> "Imaginen probar: 3 navegadores × 3 sistemas × 2 idiomas × 3 roles = 54 combinaciones.
> Pairwise reduce a ~10 filas garantizando que cada PAR de valores aparece al menos una vez.
> ¿Por qué funciona? Porque la mayoría de defectos de interacción involucran máximo 2 parámetros."

**ADVERTENCIA (muy importante):**
> "La herramienta que usamos, allpairspy, tiene un bug conocido: cuando hay restricciones,
> puede dejar pares sin cubrir. Hoy van a ver eso en el código y van a aprender a detectarlo
> con un test. Moraleja: nunca confíen ciegamente en la herramienta."

---

## A.3 Trazabilidad (minutos 25-35)

### [SLIDE 9] QUÉ DECIR:

> "Trazabilidad es poder rastrear desde un fallo hasta el requerimiento en segundos.
> Usamos 3 IDs: REQ (requerimiento), TC (test case), DEF (defecto)."

**QUÉ MOSTRAR (dibuja este diagrama):**
```
  REQUERIMIENTO            CASO DE PRUEBA              DEFECTO
 ┌──────────────┐  1..N  ┌─────────────────┐  0..N  ┌──────────┐
 │ REQ-DSC-002  │───────►│ TC-DSC-BVA-004  │───────►│ DEF-017  │
 │ "≥1000 → +5%"│        │ límite 1000.00  │        │ off-by-1 │
 └──────────────┘        └─────────────────┘        └──────────┘
```

**QUÉ AGREGAR:**
> "La matriz vive en un CSV dentro del repo, no en un Excel que nadie actualiza.
> Cuando alguien revisa tu Pull Request, lo primero que mira es: '¿la parametrización
> cubre la tabla completa?' — el código viene después."

---

## A.4 Demo en vivo (minutos 35-50)

### [SLIDE 10] QUÉ HACER — paso a paso:

**PASO 1 (3 min):** Abre `design_lab/discount.py` proyectado en pantalla.

> "Esta función calcula el descuento de un pedido. Tiene 5 requerimientos
> en el docstring: REQ-DSC-001 al 005. Léanlos."

Señala cada constante y explica qué hace:
- `VOLUME_THRESHOLD = 1_000.0` → "umbral de bono por volumen"
- `DISCOUNT_CAP = 15.0` → "tope máximo, sin importar qué sume"

**PASO 2 (5 min):** Deriva casos en voz alta desde los requerimientos.

> "REQ-DSC-005 dice: el pedido debe estar en (0; 10000]. De ahí salen 3 particiones:"

Escribe en pizarra:
- Inválida baja: `≤ 0` (ej: 0, -50)
- Válida: `(0; 10000]` (ej: 500)
- Inválida alta: `> 10000` (ej: 10000.01)

> "BVA sobre el rango: 0.01, 0, 10000, 10000.01 — 4 tests cubren toda la frontera."

**PASO 3 (5 min):** Muestra cómo la tabla de decisión expone DT-R8.

> "3 condiciones: ¿premium? / ¿≥1000? / ¿cupón? → 8 reglas. La regla R8:
> premium + volumen + cupón = 20%, pero el tope recorta a 15%.
> Sin la tabla, este caso NO existe en la suite."

**PASO 4 (2 min):** Abre `matriz-trazabilidad.csv` y muestra cómo los IDs conectan todo.

> "Miren: el TC-DSC-BVA-004 del test es el mismo ID que está en la matriz.
> Si este test falla, sé exactamente qué requerimiento está en riesgo."

---

## A.5 Resumen y preguntas (minutos 50-55)

**QUÉ DECIR:**
> "Resumen: 4 técnicas (EP, BVA, tabla, pairwise) + trazabilidad (REQ→TC→DEF).
> En el Bloque B van a ejecutar todo esto en código real."

**Preguntas de chequeo rápido (hazlas al grupo, que respondan en voz alta):**
1. "¿Cuántos valores de BVA necesito para un rango (0; 10000]?" → **4: los dos límites y sus vecinos**
2. "¿Cuántas reglas tiene una tabla con 3 condiciones booleanas?" → **8 (2³)**
3. "¿Qué pasa si un test no tiene ID de trazabilidad?" → **Es un test zombie: no sabemos qué prueba ni por qué**

> ☕ **Descanso 5 min**

---

# BLOQUE B (55 min) — Tú codificas, yo te guío

---

## B.1 Arrancar el laboratorio (minutos 0-10)

### [SLIDE 11 + 12] QUÉ HACER:

**PASO 1:** Proyecta la estructura de carpetas:
```
proyecto-integrador/
├── trazabilidad/matriz-trazabilidad.csv   ← la matriz REQ↔TC↔DEF
└── design-lab/                            ← laboratorio de hoy
    ├── pyproject.toml                     ← dependencias
    ├── design_lab/
    │   ├── discount.py                    ← función a probar
    │   └── pairwise_matrix.py             ← generador pairwise
    ├── data/decision_table.yaml           ← datos desacoplados
    └── tests/
        ├── test_equivalence_boundary.py   ← EP + BVA
        ├── test_decision_table.py         ← tabla de decisión
        └── test_pairwise.py              ← pairwise
```

**PASO 2:** Di a los estudiantes que ejecuten en su terminal:

```bash
cd proyecto-integrador/design-lab
uv sync
```

**QUÉ VERIFICAR:** Camina por el salón. Todos deben ver algo como:
```
Resolved N packages in Xms
Installed pytest-8.x.x pyyaml-6.x.x allpairspy-2.x.x
```

Si alguien tiene error, las causas más comunes son:
- No tiene `uv` → Instalar: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Está en la carpeta equivocada → Verificar que esté en `design-lab/`

**PASO 3:** Cuando todos tengan `uv sync` listo:

```bash
uv run pytest -v
```

**OUTPUT ESPERADO** (proyéctalo para que vean qué esperar):
```
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-001-standard-base] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-002-premium-base] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-003-standard-cupon] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-004-premium-volumen] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-001-minimo-valido] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-003-justo-bajo-umbral-volumen] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-004-umbral-volumen-exacto] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-005-maximo-valido] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-001-total-cero] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-002-sobre-maximo] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-003-tipo-cliente-desconocido] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-004-total-negativo] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R1] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R2] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R3] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R4] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R5] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R6] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R7] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R8] PASSED
tests/test_decision_table.py::test_decision_table_is_complete PASSED
tests/test_pairwise.py::test_pairwise_reduces_cartesian_product PASSED
tests/test_pairwise.py::test_pairwise_respects_constraints PASSED
tests/test_pairwise.py::test_pairwise_covers_every_achievable_pair PASSED
tests/test_pairwise.py::test_impossible_pairs_are_not_required PASSED

25 passed
```

**QUÉ SEÑALAR:**
> "Cuenten: 25 tests, todos en verde. Miren los IDs: TC-DSC-EP-001, TC-DSC-BVA-004,
> TC-DT-R8... son los mismos que están en la matriz de trazabilidad."

---

## B.2 EP + BVA ejecutables (minutos 10-30)

### QUÉ HACER — paso a paso:

**PASO 1 (5 min):** Di a los estudiantes que abran `tests/test_equivalence_boundary.py`.

> "Antes de ejecutar nada, LEAN los datos. Cada `pytest.param` es un caso de prueba.
> El `id=` es el identificador de trazabilidad."

**HAZ QUE NOTEN:**
- `VALID_PARTITIONS` tiene 4 filas → 4 particiones válidas distintas.
- `BOUNDARIES` tiene 4 filas → los 4 puntos críticos.
- `INVALID_PARTITIONS` tiene 4 filas → las 4 entradas que deben fallar.

**PREGUNTA PARA EL GRUPO:**
> "¿Por qué en BOUNDARIES usamos 'standard' y sin cupón?"

Respuesta: "Para aislar el efecto del monto. Si usáramos premium, no sabríamos si el resultado es por el tipo de cliente o por el monto."

**PASO 2 (10 min):** Haz que cada estudiante lea los comentarios del archivo (ahora documentados). Pide que sigan el flujo:

1. Lee la docstring del archivo → explica qué son EP y BVA.
2. Lee el BLOQUE 1 (VALID_PARTITIONS) → cada fila con su comentario.
3. Lee el BLOQUE 2 (BOUNDARIES) → nota por qué se usa "standard".
4. Lee el BLOQUE 3 (INVALID_PARTITIONS) → nota el `pytest.raises`.

**PASO 3 (5 min):** Ejecuta SOLO los tests de EP/BVA para que vean el output filtrado:

```bash
uv run pytest -v tests/test_equivalence_boundary.py
```

**OUTPUT ESPERADO:** 12 passed.

**QUÉ SEÑALAR:**
> "12 tests cubren todo: 4 particiones válidas, 4 valores límite, 4 particiones inválidas.
> El `pytest.raises(ValueError)` no es manejo de errores — es un requerimiento ejecutable.
> Si el código no lanza la excepción, el test falla."

---

## B.3 Tabla de decisión (minutos 30-45)

### QUÉ HACER:

**PASO 1 (5 min):** Di a los estudiantes que abran PRIMERO los datos:

```
data/decision_table.yaml
```

> "Este archivo tiene las 8 reglas. Léanlas. La más importante es DT-R8 — la última."

**QUÉ PREGUNTAR:**
> "Si el negocio cambia el tope de 15% a 20%, ¿qué archivo tengo que tocar?"

Respuesta: "Solo el YAML — cambio `expected: 15.0` a `expected: 20.0` en DT-R6, DT-R7 y DT-R8. No toco código Python. Eso es desacoplamiento."

**PASO 2 (5 min):** Ahora que abran `tests/test_decision_table.py`.

> "Miren la función `load_rules()`: lee el YAML y lo convierte en `pytest.param`.
> El test no tiene ningún dato hardcodeado — todo viene del YAML."

**SEÑALAR EL TEST GUARDRAIL:**
> "`test_decision_table_is_complete` cuenta las combinaciones. Si alguien borra una
> regla del YAML, este test falla. Protege el diseño, no solo el código."

**PASO 3 (5 min):** Ejecuta solo los tests de tabla:

```bash
uv run pytest -v tests/test_decision_table.py
```

**OUTPUT ESPERADO:** 9 passed (8 reglas + 1 guardrail).

**EJERCICIO RÁPIDO (si hay tiempo):** Pide que borren la regla DT-R8 del YAML y corran de nuevo:

```bash
uv run pytest -v tests/test_decision_table.py::test_decision_table_is_complete
```

**OUTPUT ESPERADO:** FAILED — "Faltan reglas: hay 7 de 8 combinaciones esperadas"

> "Esto es un guardrail de diseño. Si alguien borra una regla, el test lo detecta."

**Después del ejercicio, restaurar el YAML.**

---

## B.4 Pairwise (minutos 45-55)

### QUÉ HACER:

**PASO 1 (3 min):** Pide que abran `tests/test_pairwise.py`.

> "Este archivo prueba la matriz cross-browser: 3 navegadores × 3 sistemas × 2 idiomas × 3 roles = 54 combinaciones.
> Pairwise reduce a ~10 filas."

**SEÑALAR LA RESTRICCIÓN:**
> "webkit solo corre en macOS. Es una restricción real: Safari no existe en Windows ni Linux."

**PASO 2 (3 min):** Ejecuta:

```bash
uv run pytest -v tests/test_pairwise.py
```

**OUTPUT ESPERADO:** 4 passed.

**PASO 3 (4 min):** Explica el gap analysis. Abre `design_lab/pairwise_matrix.py` y señala:

> "El patrón es: generar → auditar → complementar. allpairspy genera la matriz inicial.
> Nuestra función `missing_pairs` revisa si quedaron huecos. Si los hay, agregamos filas extra."

**LA LECCIÓN:**
> "Nunca asuman que la herramienta garantiza algo. Demuéstrenlo con un test.
> El test `test_pairwise_covers_every_achievable_pair` hace exactamente eso:
> audita que no queden pares sin cubrir."

> ☕ **Descanso 5 min**

---

# BLOQUE C (60 min) — Tú trabajas solo, yo superviso

---

## C.1 Ejercicio individual: Diseñar casos para SauceDemo Login (minutos 0-25)

### [SLIDE 13] QUÉ HACER:

**PASO 1 (3 min):** Pide que abran https://www.saucedemo.com en su navegador.

> "Dediquen 3 minutos a explorar la página. Prueben hacer login con diferentes usuarios.
> Anoten lo que observan."

**Los 4 usuarios de prueba (escríbelos en pizarra):**
- `standard_user` / `secret_sauce` → login exitoso
- `locked_out_user` / `secret_sauce` → mensaje de error específico
- `problem_user` / `secret_sauce` → login exitoso (pero con glitches visuales)
- `performance_glitch_user` / `secret_sauce` → login exitoso (pero lento)

**PASO 2 (2 min):** Explica la tarea:

> "Van a editar la matriz de trazabilidad (`matriz-trazabilidad.csv`) y agregar casos
> de prueba para el login. Ya hay 3 filas marcadas como PENDIENTE: REQ-LOG-001, 002, 003."

**QUÉ MOSTRAR** (proyecta una fila de ejemplo de la matriz):

| Columna | Qué escribir |
|---------|-------------|
| `req_id` | Ej: `REQ-LOG-001` |
| `requerimiento` | Lo que observaste, redactado como requerimiento |
| `tc_id` | Ej: `TC-LOG-EP-001` |
| `caso_de_prueba` | Qué entra y qué se espera |
| `tecnica` | `Partición de equivalencias`, `BVA` o `Tabla de decisión` |
| `archivo_prueba` | Dejar vacío (se completa en S2) |
| `estado` | `DISEÑO` |
| `def_id` | Dejar vacío |

**PASO 3 (20 min):** Los estudiantes trabajan solos. Tú caminas por el salón respondiendo dudas.

**GUÍA DE LO QUE DEBEN PRODUCIR** (para ti, no se los digas directamente):

Requerimientos observables:
- `REQ-LOG-001`: Credenciales válidas redirigen a `/inventory.html`
- `REQ-LOG-002`: Usuario bloqueado recibe mensaje específico
- `REQ-LOG-003`: Credenciales inválidas muestran error

Particiones de equivalencia:
- Usuario: válido activo / válido bloqueado / inexistente / vacío
- Contraseña: correcta / incorrecta / vacía

Tabla de decisión (3 condiciones: ¿usuario existe? / ¿contraseña correcta? / ¿usuario bloqueado?)

**CÓMO SABER SI QUEDÓ BIEN** (diles esto a los 15 min):
> "Checklist: cada REQ-LOG tiene al menos un TC, cada TC declara su técnica,
> y hay al menos una partición inválida y una tabla de decisión."

---

## C.2 Mini reto: Pairwise para matriz web (minutos 25-45)

### [SLIDE 14] QUÉ HACER:

**PASO 1 (2 min):** Explica el escenario:

> "La matriz de compatibilidad del proyecto es:
> navegador × tamaño de pantalla × tema × rol = 36 combinaciones.
> Su tarea: generar la matriz pairwise con una restricción."

**Escribe en pizarra:**
```
navegador:   {chromium, firefox, webkit}
pantalla:    {mobile, tablet, desktop}
tema:        {light, dark}
rol:         {admin, user}

Restricción: admin NO se prueba en mobile

Total combinaciones: 3 × 3 × 2 × 2 = 36
```

**PASO 2 (18 min):** Los estudiantes trabajan en `tests/test_pairwise.py`.

Deben:
1. Agregar la constante `PARAMETERS_LOGIN` con los 4 parámetros.
2. Crear la función de restricción (admin no va con mobile).
3. Generar la matriz pairwise.
4. Escribir un test que verifique:
   - (a) El total es menor que 36.
   - (b) La restricción se respeta.
   - (c) Todos los pares `(pantalla, tema)` están cubiertos.

**QUÉ PREGUNTAR AL FINALIZAR** (para la justificación):
> "¿Qué defectos podrían escaparse con pairwise en vez del producto cartesiano?"

Respuesta esperada: "Defectos que requieren 3 o más parámetros interactuando simultáneamente — ej: un bug que solo aparece con chromium + mobile + dark + admin. Pairwise garantiza pares, no tríos ni cuartetos."

---

## C.3 Errores comunes + cierre (minutos 45-60)

### [SLIDE 15] QUÉ HACER (10 min):

Proyecta esta tabla y discútela con el grupo. Pide ejemplos de cada uno:

| ❌ Error común | ✅ Práctica correcta |
|---|---|
| Probar solo el "camino feliz" con valores arbitrarios | Cada valor viene de una técnica y es trazable a un REQ |
| Un test gigante con 15 asserts | Un caso parametrizado; agregar caso = agregar línea |
| Datos incrustados en el código del test | Datos en YAML o CSV versionados en `data/` |
| Matriz de trazabilidad en Excel que nadie actualiza | CSV en el repo, revisado en el PR |
| "Más tests = más calidad" → suites de 40 min con huecos | Cobertura mínima suficiente: EP + BVA + tabla + pairwise |
| Ignorar particiones inválidas ("eso nunca pasa") | `pytest.raises` como caso de primera clase |
| Copiar y pegar tests cambiando solo un número | `@parametrize`: agregar caso = agregar una línea |

### [SLIDE 16] CHECKLIST DE SALIDA (5 min):

Proyecta y pide que cada estudiante verifique en su máquina:

- [ ] `uv run pytest -v` corre en verde: EP, BVA, tablas de decisión y pairwise (25+ tests).
- [ ] `matriz-trazabilidad.csv` tiene los REQ-DSC-* verificados y los REQ-LOG-* completados.
- [ ] Mini reto pairwise implementado y pasando.
- [ ] Pueden explicar en 1 minuto por qué DT-R8 no existiría sin tabla de decisión.

### [SLIDE 17] PRÓXIMA SESIÓN (2 min):

> "En la Sesión 2, estos diseños se convierten en pruebas automatizadas de la UI
> de SauceDemo, usando Page Object Model, Screenplay y DRY. La matriz de trazabilidad
> crece: los TC-LOG-* pasan de DISEÑO a PASS."

---

## NOTAS PARA EL INSTRUCTOR

### Si el grupo es avanzado:
- En B.3, después de mostrar el guardrail, pide que MODIFIQUEN el YAML para agregar una novena regla con un tipo de cliente "vip" y vean qué pasa.
- En C.1, pide que diseñen también casos para el carrito de compras de SauceDemo (agregar/quitar items, cantidades).

### Si el grupo necesita más tiempo:
- Reduce C.2 (mini reto) a 10 min y da el código base del pairwise login como plantilla.
- Salta el ejercicio de borrar DT-R8 en B.3 — solo muéstralo tú en tu pantalla.

### Si algo falla técnicamente:
- `uv sync` falla → verifica conexión a internet. Alternativa: `pip install pytest allpairspy pyyaml`.
- `pytest` no encuentra tests → verifica que están en la carpeta `design-lab/`.
- Tests fallan en rojo → ejecuta `uv run pytest -v --tb=short` para ver el error específico.

### Para evaluar esta sesión:
- Revisa los commits de cada estudiante en la matriz de trazabilidad.
- Verifica que los REQ-LOG-* tienen al menos 3 TC cada uno con técnica declarada.
- El mini reto pairwise debe tener las 3 validaciones (a, b, c).
# Sesión 1 (Horas 1-3) — Diseño Técnico de Pruebas Automatizadas

> **Qué vas a lograr hoy:** convertir requisitos en casos de prueba usando cuatro técnicas concretas — partición de equivalencias (*Equivalence Partitioning*, EP), análisis de valores límite (*Boundary Value Analysis*, BVA), tablas de decisión y pruebas combinatorias por pares (*Pairwise Testing*). Al terminar tendrás un laboratorio corriendo en verde y la primera versión de tu matriz de trazabilidad, que conecta requerimientos, casos y defectos.

## Las herramientas que vamos a usar — y por qué

Antes de arrancar, hay que entender qué tenemos encima de la mesa. No necesitas memorizarlo todo ahora, solo ten claro para qué sirve cada cosa.

### `uv` — el gestor de entornos de Python

Python tiene un problema histórico: si instalas librerías directamente en tu sistema, tarde o temprano chocan entre sí. Un proyecto necesita la versión 1.x de algo, otro la 2.x, y el resultado son horas perdidas en errores que no tienen nada que ver con tu código.

`uv` resuelve eso. Crea una carpeta `.venv` por proyecto con solo las librerías que ese proyecto necesita, en las versiones exactas. Lo que instales ahí no toca nada más de tu máquina.

Por debajo hace tres cosas que importan:
- **Gestiona la versión de Python automáticamente.** Si no tienes la correcta, la descarga por ti.
- **Instala desde binarios pre-compilados.** Nada de compilar desde cero — detecta tu procesador (Intel, M1, M2, Windows) y descarga lo que corresponde.
- **Congela las versiones en `uv.lock`.** Ese archivo es una foto exacta de tus dependencias. Gracias a él, este laboratorio va a funcionar igual en tu máquina, en la de un compañero y en el servidor de integración continua.

### `Taskfile` — atajos para no escribir comandos largos

`Taskfile` no hace nada mágico. Agrupa comandos en alias cortos definidos en un archivo YAML. En lugar de escribir `cd proyecto-integrador/design-lab && uv run pytest -v --tb=short` cada vez, escribes `task test:design`.

A diferencia del clásico `Makefile`, funciona igual en macOS, Linux y Windows. Y como vive en el repo, también es documentación: cualquier persona que clone el proyecto sabe exactamente qué comandos existen y qué hacen.

**No es obligatorio.** Cada ejercicio incluye el comando equivalente por si no lo tienes instalado.

### `pytest` y `allpairspy` — el motor del laboratorio

`pytest` es el estándar de la industria para pruebas en Python. Lo usamos principalmente por la **parametrización**: escribes el código de un test una sola vez y lo ejecutas con decenas de combinaciones de datos. Agregar un caso nuevo es agregar una línea de datos, no duplicar código.

`allpairspy` implementa el algoritmo de pruebas por pares. Su trabajo es tomar una lista de parámetros con muchos valores posibles y calcular el subconjunto mínimo de combinaciones que garantiza que cada par de valores aparece al menos una vez junto.

### Git y Docker — lo que viene después

Hoy no los vas a usar, pero los vas a ver en el proyecto desde el principio:

- **Git** es el control de versiones. Toda la trazabilidad del código — quién cambió qué, cuándo y por qué — vive ahí. La revisión de trabajo mediante Pull Request (*PR*) es parte del flujo real que vamos a practicar.
- **Docker** aparece en sesiones posteriores. Permite levantar navegadores y bases de datos con un solo comando, tanto en tu máquina como en el servidor de automatización. El entorno es idéntico en ambos lados, sin sorpresas.

---

## Antes de empezar — prepara el entorno

Instala `uv` una sola vez (elige tu sistema):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verifica que quedó listo:

```bash
uv --version
```

Si vas a usar `task`, instálalo desde [taskfile.dev](https://taskfile.dev/installation/). Si no, sin problema — cada ejercicio tiene el comando completo.

Para inicializar el laboratorio de hoy:

```bash
cd proyecto-integrador/design-lab
uv sync
```

`uv sync` lee `pyproject.toml`, descarga todo lo necesario y lo deja listo en segundos.

---

# BLOQUE A (55 min) — Del requerimiento al caso de prueba

## A.1 El problema real (10 min)

Imagina este escenario: un equipo tiene 300 tests automatizados, la suite tarda 40 minutos en correr, todo pasa — y aun así producción se rompe con un pedido de exactamente $1,000.

¿Cómo es posible? Simple: **cantidad de tests no es lo mismo que cobertura de diseño**. Si nadie pensó en probar exactamente $1,000 — el límite entre "sin bono" y "con bono de volumen" — ese escenario no existe en la suite, no importa cuántos tests haya.

Los defectos no viven en los valores "cómodos" que uno elige al azar. Viven en los **límites** y en las **combinaciones de reglas** que nadie pensó de forma explícita.

El diseño técnico responde tres preguntas antes de escribir una sola línea de código:
1. **¿Qué probar?** → las técnicas de diseño (EP, BVA, tablas de decisión, pairwise) responden esto.
2. **¿Cuánto probar?** → la cobertura mínima suficiente, no exhaustiva.
3. **¿Cómo demostrar que está probado?** → la matriz de trazabilidad.

## A.2 Las técnicas — qué hace cada una (15 min)

**Partición de equivalencias (EP):** el sistema se comporta igual con todos los valores dentro de la misma clase. Por eso basta probar un valor representativo por clase, no todos. Regla fundamental: **incluir siempre las particiones inválidas** — ahí están los errores más frecuentes.

**Análisis de valores límite (BVA):** los errores se acumulan en las fronteras — en el `<` que debería ser `<=`, en el `>` que debería ser `>=`. Por cada límite se prueban el valor exacto y sus vecinos inmediatos.

**Tablas de decisión:** cuando hay N condiciones booleanas que interactúan, la tabla de 2^N reglas expone combinaciones que nadie habría pensado manualmente. Por ejemplo: ¿qué pasa cuando un cliente premium alcanza el umbral de volumen *y* encima tiene cupón? Sin la tabla, ese caso no existe en la suite.

**Pruebas combinatorias por pares (Pairwise Testing):** la mayoría de los defectos de interacción involucran como máximo 2 parámetros. Cubrir todos los *pares* posibles reduce 54 combinaciones a unas 12 filas sin perder casi nada en detección de defectos.

**Mantenibilidad — por diseño, no por accidente:**
- **Reusabilidad:** el caso parametrizado es la unidad reutilizable. Agregar un caso nuevo es agregar una línea de datos.
- **Desacoplamiento:** los datos viven en archivos YAML (*YAML Ain't Markup Language*) o CSV (*Comma-Separated Values*) fuera del código del test. Un analista puede modificarlos sin tocar Python.
- **Modulación:** un archivo por técnica. La lógica que se prueba vive separada de los tests.

## A.3 Trazabilidad — el contrato del conjunto de pruebas (10 min)

Tres identificadores son todo lo que necesitamos: `REQ` para requerimiento, `TC` para caso de prueba (*Test Case*) y `DEF` para defecto.

```
  REQUERIMIENTO            CASO DE PRUEBA              DEFECTO
 ┌──────────────┐  1..N  ┌─────────────────┐  0..N  ┌──────────┐
 │ REQ-DSC-002  │───────►│ TC-DSC-BVA-004  │───────►│ DEF-017  │
 │ "≥1000 → +5%"│        │ límite 1000.00  │        │ off-by-1 │
 └──────────────┘        └─────────────────┘        └──────────┘
        ▲                        │
        │   La matriz responde:  ▼
        │   "¿Qué REQ queda sin TC?"  → hueco de cobertura
        └── "¿Qué TC no mapea a REQ?" → test zombie (candidato a borrar)
```

La matriz vive en `proyecto-integrador/trazabilidad/matriz-trazabilidad.csv` y los identificadores de parametrización de pytest coinciden con los `tc_id` de esa matriz. La idea es tener **trazabilidad ejecutable** — no un Excel que nadie actualiza.

## A.4 Del ejemplo sencillo al mundo real (10 min)

**Primero, algo simple:** un campo "edad" que acepta valores entre 18 y 65.
- EP: `<18` (inválida), `18-65` (válida), `>65` (inválida), no numérico (inválida).
- BVA: `17, 18, 65, 66` → 4 tests que cubren toda la frontera.

**Ahora en el laboratorio.** Abre el archivo:

```
proyecto-integrador/design-lab/design_lab/discount.py
```

En las primeras líneas vas a encontrar las constantes y la función que usaremos durante toda la sesión:

```python
VOLUME_THRESHOLD = 1_000.0   # umbral de bono por volumen (REQ-DSC-002)
DISCOUNT_CAP     = 15.0      # tope máximo de descuento  (REQ-DSC-004)

def calculate_discount(customer_type: str, order_total: float, has_coupon: bool) -> float:
    """
    REQ-DSC-001: premium → +10 %; standard → +0 %
    REQ-DSC-002: order_total >= 1000 → +5 % (bono por volumen)
    REQ-DSC-003: has_coupon → +5 %
    REQ-DSC-004: el descuento total nunca excede 15 %
    REQ-DSC-005: 0 < order_total <= 10 000; de lo contrario lanza ValueError
    """
```

Los cinco requerimientos están en ese docstring. La implementación debajo es lo que vamos a probar. Los `REQ-DSC-*` son los mismos que aparecen en la matriz de trazabilidad:

```
proyecto-integrador/trazabilidad/matriz-trazabilidad.csv
```

Cuando alguien revisa tu trabajo en un Pull Request (PR), lo primero que valida no es el código del test, sino esto: "¿la parametrización cubre la tabla completa? ¿están los límites del REQ-DSC-002?". El código viene después.

## A.5 Demo — cómo se derivan los casos (10 min)

Vamos a derivar los casos directo desde los requerimientos que acabas de leer:

1. **REQ-DSC-005** dice `0 < order_total <= 10000`. De ahí salen tres particiones:
   - Inválida baja: cualquier valor `≤ 0` (por ejemplo, `0` o `-50`).
   - Válida: cualquier valor en `(0; 10000]` (por ejemplo, `500`).
   - Inválida alta: cualquier valor `> 10000` (por ejemplo, `10000.01`).

2. **BVA sobre ese rango:** los cuatro puntos que hay que probar son `0` (inválido, frontera exclusiva), `0.01` (el primer válido), `10000` (el último válido) y `10000.01` (inválido). Con esos cuatro valores queda cubierta toda la frontera.

3. **REQ-DSC-002** tiene su propio límite interno en `1000`: probar `999.99` (sin bono) y `1000.00` (con bono) captura el típico error de `<` donde debería ir `<=`.

4. **Condiciones que interactúan:** ¿es premium? / ¿total ≥ 1000? / ¿tiene cupón? → 2³ = 8 reglas. La regla R8 es `premium + volumen + cupón = 20 %`, pero el tope del REQ-DSC-004 lo recorta a `15 %`. Ese caso solo aparece cuando construyes la tabla completa — jamás lo encontrarías probando al azar.

5. Cada caso entra en `matriz-trazabilidad.csv` con su `tc_id` (por ejemplo `TC-DSC-BVA-004`) y la técnica usada.

> ☕ **Descanso 5 min**

---

# BLOQUE B (55 min) — Laboratorio guiado

## B.1 Estructura y primer arranque (15 min)

Así está organizado lo que vamos a usar hoy:

```
curso-automatizacion-apis-performance-seguridad/
├── Taskfile.yml                      ← atajos opcionales para ejecutar comandos del curso
├── proyecto-integrador/
│   ├── trazabilidad/matriz-trazabilidad.csv
│   └── design-lab/                   ← laboratorio práctico de hoy en Python
│       ├── pyproject.toml            ← dependencias declaradas del laboratorio
│       ├── design_lab/
│       │   ├── discount.py           ← regla de negocio que vamos a probar
│       │   └── pairwise_matrix.py    ← generación pairwise + análisis de huecos de cobertura
│       ├── data/decision_table.yaml  ← datos desacoplados de la lógica
│       └── tests/
│           ├── test_equivalence_boundary.py
│           ├── test_decision_table.py
│           └── test_pairwise.py
└── sesiones/sesion-01/SESION_01.md   ← este documento
```

Para correr la suite completa:

```bash
cd curso-automatizacion-apis-performance-seguridad
task setup          # instala las dependencias del laboratorio
task test:design    # corre todos los tests de la sesión
```

Sin `task`:

```bash
cd proyecto-integrador/design-lab
uv sync
uv run pytest -v
```

## B.2 EP + BVA ejecutables (15 min)

Abre el archivo:

```
proyecto-integrador/design-lab/tests/test_equivalence_boundary.py
```

Vas a encontrar tres bloques de parametrización. Léelos antes de ejecutar:

**Bloque 1 — particiones válidas** (`VALID_PARTITIONS`): cuatro filas, una por partición. El cuarto argumento es el resultado esperado y el `id` coincide exactamente con el `tc_id` de la matriz:

```python
pytest.param("standard", 500.0, False, 0.0,  id="TC-DSC-EP-001-standard-base"),
pytest.param("premium",  500.0, False, 10.0, id="TC-DSC-EP-002-premium-base"),
```

**Bloque 2 — valores límite** (`BOUNDARIES`): los cuatro puntos críticos del rango y del umbral de volumen. El test usa siempre `"standard"` sin cupón para aislar únicamente el efecto del monto:

```python
pytest.param(   0.01, 0.0, id="TC-DSC-BVA-001-minimo-valido"),
pytest.param( 999.99, 0.0, id="TC-DSC-BVA-003-justo-bajo-umbral-volumen"),
pytest.param(1000.00, 5.0, id="TC-DSC-BVA-004-umbral-volumen-exacto"),   # ← límite REQ-DSC-002
pytest.param(10_000.00, 5.0, id="TC-DSC-BVA-005-maximo-valido"),
```

**Bloque 3 — particiones inválidas** (`INVALID_PARTITIONS`): cuatro entradas que deben lanzar `ValueError`. El `pytest.raises(ValueError)` no es manejo de errores — es un **requerimiento ejecutable** (REQ-DSC-005). Si el código no lanza la excepción, el test falla.

> **Regla de oro:** agregar una partición nueva es agregar una línea de datos. El test no cambia.

## B.3 Tabla de decisión con datos externos (15 min)

Abre primero los datos:

```
proyecto-integrador/design-lab/data/decision_table.yaml
```

Vas a ver las 8 reglas (2³ condiciones: ¿premium? / ¿≥1000? / ¿cupón?). Busca la regla DT-R8:

```yaml
- id: DT-R8
  customer_type: premium
  order_total: 1500.0
  has_coupon: true
  expected: 15.0   # REQ-DSC-004: tope — sin la tabla, este caso nunca aparecería
```

`premium(10) + volumen(5) + cupón(5) = 20 %`, pero el tope del REQ-DSC-004 lo recorta a `15 %`. Este caso no aparece probando al azar. Solo la tabla completa lo expone.

Ahora abre el test:

```
proyecto-integrador/design-lab/tests/test_decision_table.py
```

Fíjate en dos cosas:
1. `load_rules()` lee el YAML y convierte cada fila en un `pytest.param`. Un analista puede editar las reglas **sin tocar Python** — eso es desacoplamiento real.
2. `test_decision_table_is_complete` cuenta las combinaciones únicas de condiciones y falla si hay menos de 8. Si alguien borra una regla por accidente, la suite lo detecta antes de que llegue a revisión.

## B.4 Pairwise + análisis de huecos de cobertura (10 min)

Abre el test:

```
proyecto-integrador/design-lab/tests/test_pairwise.py
```

El escenario: 3 navegadores × 3 sistemas operativos × 2 idiomas × 3 roles = **54 combinaciones**. Pairwise las reduce a ~10 filas cubriendo todos los pares.

Lee la restricción de negocio del archivo (líneas 24-28):

```python
def is_valid_combination(row: list) -> bool:
    """webkit (motor de Safari) solo corre en macOS."""
    if row[0] == "webkit" and row[1] != "macos":
        return False
    return True
```

**Hallazgo real que vas a ver documentado ahí:** con esa restricción, el algoritmo interno de `allpairspy` dejó fuera los pares `(chromium, macos)` y `(firefox, macos)` — huecos reales que no aparecen en la documentación de la herramienta.

Para resolverlo, abre:

```
proyecto-integrador/design-lab/design_lab/pairwise_matrix.py
```

El patrón tiene tres pasos: **generar → auditar los pares exigibles → completar los que faltan**. Un par es "exigible" solo si existe al menos una combinación válida completa que lo contenga. Los pares imposibles por la restricción no se exigen.

El test `test_pairwise_covers_every_achievable_pair` corre ese análisis y falla si quedan huecos. La moraleja: nunca asumas que una herramienta garantiza algo — demuéstralo con un test.

> ☕ **Descanso 5 min**

---

# BLOQUE C (60 min) — Tu turno

## C.1 Ejercicio individual (25 min) — Diseño del login de SauceDemo

Hoy solo diseñamos los casos. La automatización de la pantalla de login llega en la Sesión 2. Abre en el navegador:

```
https://www.saucedemo.com
```

Dedica 3 minutos a explorar la página antes de diseñar. Esto es lo que vas a observar:
- Hay 4 usuarios de prueba: `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`.
- Todos comparten la misma contraseña: `secret_sauce`.
- `locked_out_user` recibe un mensaje de error diferente al de credenciales incorrectas.
- Usuario o contraseña incorrectos muestran un mensaje de error genérico.
- Un login exitoso redirige a `/inventory.html`.

**Tu tarea** — edita el archivo:

```
proyecto-integrador/trazabilidad/matriz-trazabilidad.csv
```

Ya tiene encabezados y tres filas marcadas como `PENDIENTE` para `REQ-LOG-001`, `REQ-LOG-002` y `REQ-LOG-003`. Esto significa cada columna:

| Columna | Qué escribir |
|---|---|
| `req_id` | Identificador del requerimiento (ej. `REQ-LOG-001`) |
| `requerimiento` | Lo que observaste en la página, redactado como requerimiento |
| `tc_id` | Identificador del caso (ej. `TC-LOG-EP-001`) |
| `caso_de_prueba` | Qué entra y qué resultado se espera |
| `tecnica` | `Partición de equivalencias`, `Análisis de valores límite` o `Tabla de decisión` |
| `archivo_prueba` | Dejar vacío — se completa en la Sesión 2 cuando se automatice |
| `estado` | `DISEÑO` — el caso está definido pero aún no automatizado |
| `def_id` | Dejar vacío |

**Una fila ya completada del bloque de descuento, como referencia:**

```
REQ-DSC-002,Pedido >= 1000 suma 5% por volumen,TC-DSC-BVA-004,Límite exacto del umbral: 1000.00 → con bono de volumen,Análisis de valores límite,tests/test_equivalence_boundary.py,PASS,
```

**Cómo completar el ejercicio, paso a paso:**

1. **Escribe los requerimientos observables.** Por ejemplo:
   - `REQ-LOG-001`: "Credenciales válidas redirigen al inventario (`/inventory.html`)"
   - `REQ-LOG-002`: "El usuario bloqueado recibe un mensaje específico, diferente al de credenciales incorrectas"
   - `REQ-LOG-003`: "Campos vacíos o credenciales inválidas muestran un mensaje de error"

2. **Deriva las particiones de equivalencia** para los dos campos:
   - Usuario: válido activo / válido bloqueado / inexistente / vacío
   - Contraseña: correcta / incorrecta / vacía
   - Pregunta clave: ¿qué combinaciones producen el mismo resultado? Las que sí, colapsan en una sola partición.

3. **Construye la tabla de decisión** con tres condiciones: ¿el usuario existe? / ¿la contraseña es correcta? / ¿el usuario está bloqueado? → 2³ = 8 reglas posibles. Elimina las que son imposibles — no puede haber contraseña correcta si el usuario no existe.

4. Asigna un `tc_id` con prefijo `TC-LOG-*` a cada caso. Si identifies más requerimientos, agrega filas.

**¿Cómo saber si quedó bien?** Cada `REQ-LOG-*` tiene al menos un TC, cada TC declara su técnica, y hay al menos una partición inválida (campo vacío) y una regla de decisión con las 3 condiciones.

## C.2 Mini reto (20 min) — Pairwise para una matriz web

La matriz de compatibilidad del proyecto es: navegador `{chromium, firefox, webkit}` × tamaño de pantalla `{mobile, tablet, desktop}` × tema `{light, dark}` × rol `{admin, user}` = **36 combinaciones**.

1. En `tests/test_pairwise.py`, agrega una constante `PARAMETERS_LOGIN` con esos 4 parámetros.
2. Restricción de equipo: el rol `admin` no se prueba en pantalla `mobile`.
3. Genera la matriz pairwise y escribe un test que demuestre: (a) que el total es menor que 36, (b) que la restricción se respeta, y (c) que todos los pares `(tamaño de pantalla, tema)` están cubiertos.
4. **Justifica en 2 líneas** — en un comentario del Pull Request, no en el código: ¿qué tipo de defectos podrían escaparse con pairwise en vez del producto cartesiano y por qué ese intercambio vale la pena?

## C.3 Errores comunes — qué evitar y qué hacer (15 min)

| ❌ Error común | ✅ Práctica correcta |
|---|---|
| Probar solo el "camino feliz" con valores arbitrarios (`total=500`) | Cada valor de test viene de una técnica y es trazable a un REQ |
| Un test gigante con 15 asserts que mezcla particiones | Un caso parametrizado por diseño; el `id` es el `tc_id` de la matriz |
| Datos incrustados en el código del test | Datos en YAML o CSV versionados en `data/`, lógica en `tests/` |
| Matriz de trazabilidad en un Excel que nadie actualiza | CSV en el repo, revisado en el PR junto al código que traza |
| "Más tests = más calidad" → suites de 40 min con huecos de frontera | Cobertura mínima suficiente: EP + BVA + tabla + pairwise |
| Ignorar particiones inválidas ("eso nunca pasa") | `pytest.raises` como caso de primera clase (REQ-DSC-005) |
| Copiar y pegar el mismo test cambiando solo un número | `@parametrize`: agregar un caso = agregar una línea de datos |

**Lo que hiciste hoy en términos de código limpio:** nombres de test que describen comportamiento (`test_invalid_partitions_raise`), constantes de negocio con nombre propio (`VOLUME_THRESHOLD` en lugar del número `1000` suelto en el código), un archivo por técnica, y validaciones preventivas que protegen el diseño (`test_decision_table_is_complete`).

---

## ¿Quedó todo? — Lista de salida

- [ ] `task setup && task test:design` corre en verde: EP, BVA, tablas de decisión y pairwise.
- [ ] `matriz-trazabilidad.csv` con los REQ-DSC-* verificados y los REQ-LOG-* completados por ti.
- [ ] Mini reto pairwise implementado y pasando.
- [ ] Puedes explicar en 1 minuto por qué DT-R8 no existiría sin tabla de decisión.

**Próxima sesión (S2):** estos diseños se convierten en pruebas automatizadas de la interfaz de usuario (*User Interface*, UI) de SauceDemo, usando **Page Object Model**, **Screenplay** y el principio **Don't Repeat Yourself** (DRY), estados de prueba compartidos (*fixtures*) y datos externos en JSON (*JavaScript Object Notation*), YAML y CSV. La matriz de trazabilidad crece con los `TC-LOG-*` ya automatizados.
