# GUÍA DEL INSTRUCTOR — Sesión 1: Diseño Técnico de Pruebas

> **Duración:** 3 horas (Bloque A 55min + Bloque B 55min + Bloque C 60min + 2 descansos de 5min)
> **Objetivo:** Que el estudiante convierta requerimientos en casos de prueba usando EP, BVA, tablas de decisión y pairwise.
> **Entregable:** Suite de tests corriendo en verde + matriz de trazabilidad actualizada.
> **Prerequisitos:** Python 3.12+, `uv` instalado, terminal funcional.

---

## ANTES DE CLASE — Checklist del instructor

Haz esto **antes** de conectarte a la videollamada. No lo dejes para el momento de la clase.

- [ ] Ejecuta `cd proyecto-integrador/design-lab && uv sync && uv run pytest -v` en tu máquina. Todo debe pasar.
- [ ] Abre SauceDemo (https://www.saucedemo.com) y verifica que funciona.
- [ ] Ten listo para compartir pantalla: este documento, un navegador abierto con SauceDemo, una terminal, y una pizarra virtual (Miro, Jamboard, o la pizarra integrada de Zoom/Teams).
- [ ] Verifica que los estudiantes tienen `uv` instalado (envía el SETUP_ESTUDIANTES.md por correo/chat al menos 48h antes).
- [ ] **Configuración de la videollamada:** habilita el chat, ten a la mano el link de breakout rooms, y pide que todos tengan cámara encendida si es posible.

---

## 🗺️ MAPA DE LA SESIÓN (comparte pantalla al inicio)

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

**Diseño:** Fondo oscuro, texto blanco grande. La pregunta en amarillo o naranja. Pausa dramática — pide que escriban su respuesta en el chat antes de cambiar de slide.

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

> **Regla de oro del Bloque A:** los estudiantes NO tocan el teclado. Solo observan y escuchan.
> Si alguien empieza a teclear, dile: "Todavía no, en el Bloque B codificamos todos juntos."

---

## A.1 El problema real (minutos 0-10)

### ACCIONES DEL INSTRUCTOR:

1. **[SLIDE 1]** Comparte pantalla con la portada mientras la gente se conecta. No digas nada todavía.
2. **[SLIDE 2]** Cuando estés listo, cambia al objetivo. Léelo en voz alta (30 segundos). No lo expliques — solo léelo.
3. **[SLIDE 3]** Cambia al problema. Lee el escenario en voz alta, despacio:

> **GUION:**
> "Imaginen esto: un equipo de QA tiene 300 tests automatizados.
> La suite tarda 40 minutos en correr. Todo pasa en verde.
> Y aun así, producción se rompe cuando un cliente hace un pedido de exactamente $1,000.
> ¿Cómo es posible?"

4. **PAUSA DE 10 SEGUNDOS.** No hables. Deja que piensen. Alguien va a escribir en el chat o usar la reacción de levantar mano. Lee lo que escriben en voz alta.
5. Si nadie escribe en 15 segundos, di: "¿Nadie? La respuesta es simple: porque nadie pensó en probar exactamente $1,000. El límite."

6. **[SLIDE 4]** Cambia a las 3 preguntas. Lee cada una:

> **GUION:**
> "Cantidad de tests NO es lo mismo que cobertura de diseño.
> Antes de escribir una sola línea de código, necesitamos responder 3 preguntas:
> 1. ¿Qué probar? → Las técnicas de diseño responden esto.
> 2. ¿Cuánto probar? → Cobertura mínima suficiente, no exhaustiva.
> 3. ¿Cómo demostrar que está probado? → La matriz de trazabilidad."

7. Si alguien pregunta "¿qué son las técnicas?", responde: "Eso viene en los siguientes 15 minutos. Solo memoriza las 3 preguntas por ahora."

### CHECKPOINT:
- Los estudiantes deberían tener las 3 preguntas anotadas (en papel o mentalmente).
- Pide que escriban "✅" en el chat si tienen las 3 preguntas claras.

---

## A.2 Las 4 técnicas (minutos 10-25)

> **Transición:** "Ahora vamos a ver las 4 técnicas que responden la primera pregunta: ¿qué probar? Cada una la voy a explicar con un ejemplo simple, y después vamos a ver cómo se aplica en código real."

### TÉCNICA 1 — [SLIDE 5] EP: Partición de Equivalencias (min 10-15)

**ACCIÓN:** Cambia a la slide de EP.

**GUION (lee despacio):**
> "Si un campo acepta edades de 18 a 65, no necesitas probar los 47 valores.
> Todos los valores DENTRO del rango producen el mismo resultado.
> Basta con probar UNO por grupo."

**ACCIÓN:** Usa el cursor/laser pointer de tu herramienta de videollamada para señalar el diagrama (los 3 recuadros).

**GUION:**
> "Dividimos los valores en grupos — llamados particiones.
> Los valores dentro de cada grupo se comportan igual.
> Entonces probamos UN representante de cada grupo."

**ACCIÓN:** Señala con el cursor el texto rojo al pie de la slide.

**GUION (énfasis):**
> "Regla que no se olvida: siempre incluir las particiones INVÁLIDAS.
> Ahí están los errores más frecuentes. Los programadores prueban el camino feliz.
> El tester prueba lo que NO debería pasar."

---

### TÉCNICA 2 — [SLIDE 6] BVA: Análisis de Valores Límite (min 15-20)

**ACCIÓN:** Cambia a la slide de BVA.

**GUION:**
> "Los errores se acumulan en las fronteras. El típico bug: el programador escribe
> menor-que cuando debería ser menor-o-igual. Por eso probamos el valor EXACTO
> del límite y sus vecinos inmediatos."

**ACCIÓN:** Señala con el cursor el diagrama de la línea numérica.

**GUION:**
> "Para un rango de 18 a 65, probamos 4 valores: 17, 18, 65, 66.
> 17 → debería dar error. 18 → debería pasar. 65 → debería pasar. 66 → debería dar error.
> Si alguno de esos 4 falla, encontramos el bug."

**ACCIÓN:** Conecta con el laboratorio.

**GUION:**
> "Hoy en el laboratorio vamos a ver esto con dinero. El umbral de volumen es $1,000.
> Vamos a probar $999.99 — sin bono — y $1,000.00 — con bono.
> Si el programador escribió mayor-que en vez de mayor-o-igual,
> el test de $1,000 lo detecta."

---

### TÉCNICA 3 — [SLIDE 7] Tabla de Decisión (min 20-25)

**ACCIÓN:** Cambia a la slide de tabla de decisión.

**GUION:**
> "Cuando hay condiciones que interactúan — cuando el resultado depende de
> VARIAS cosas a la vez — hacemos una tabla con TODAS las combinaciones.
> 3 condiciones sí/no = 2 al cubo = 8 reglas."

**ACCIÓN:** Señala con el cursor la tabla de 8 filas en la slide.

**GUION (recorre la tabla de arriba a abajo):**
> "R1: no premium, bajo monto, sin cupón → 0%.
> R2: no premium, bajo monto, con cupón → 5%.
> ... y así hasta R8."

**ACCIÓN:** Detente en R8. Señálala con el cursor.

**GUION (énfasis, más despacio):**
> "R8 es la regla más importante de toda la tabla. Miren:
> premium más volumen más cupón. Eso suma 10 + 5 + 5 = 20%.
> Pero hay un tope de 15%. Entonces el resultado es 15%, no 20%.
> Sin construir la tabla completa, NADIE piensa en probar este caso.
> Y si no lo pruebas, es un defecto que llega a producción."

---

### TÉCNICA 4 — [SLIDE 8] Pairwise Testing (min 25-30)

**ACCIÓN:** Cambia a la slide de pairwise.

**GUION:**
> "Imaginen que tienen que probar su app en todas las combinaciones:
> 3 navegadores por 3 sistemas por 2 idiomas por 3 roles.
> 3 por 3 por 2 por 3 = 54 combinaciones.
> Si cada test tarda 30 segundos, son 27 minutos solo para cross-browser."

**ACCIÓN:** Señala con el cursor el lado derecho de la slide.

**GUION:**
> "Pairwise dice: la mayoría de defectos son causados por la interacción
> de máximo 2 parámetros. No necesitas probar todo junto.
> Solo necesitas que cada PAR de valores aparezca junto al menos una vez.
> Con eso, 54 se reduce a 10. 80% menos tests."

**ACCIÓN:** Señala con el cursor la advertencia amarilla al pie de la slide.

**GUION (cambia el tono a serio):**
> "Pero cuidado. La herramienta que usamos hoy tiene un bug conocido.
> Cuando hay restricciones, puede dejar pares sin cubrir.
> En el laboratorio van a descubrir ese bug y van a escribir un test
> que lo detecte. Esa es la lección más importante de toda la sesión:
> nunca confíen ciegamente en la herramienta."

---

## A.3 Trazabilidad (minutos 25-35)

> **Transición:** "Ya sabemos qué probar. Ahora, ¿cómo demostramos que está probado? Con trazabilidad."

### [SLIDE 9]

**ACCIÓN:** Cambia a la slide de trazabilidad.

**GUION:**
> "Trazabilidad es poder rastrear desde un fallo hasta el requerimiento en segundos.
> Usamos 3 identificadores: REQ para requerimiento, TC para test case, DEF para defecto."

**ACCIÓN:** Señala con el cursor el diagrama REQ → TC → DEF.

**GUION:**
> "Un requerimiento tiene uno o muchos test cases.
> Un test case puede encontrar cero o muchos defectos.
> Todo está conectado con IDs."

**ACCIÓN:** Señala con el cursor las 2 preguntas debajo del diagrama.

**GUION:**
> "La matriz responde 2 preguntas:
> ¿Qué REQ no tiene TC? Eso es un hueco — algo que no estamos probando.
> ¿Qué TC no tiene REQ? Eso es un test zombie — no sabemos qué prueba ni por qué existe."

**GUION (cierre):**
> "La matriz vive en un CSV dentro del repo, versionada en Git.
> No en Excel. Cuando alguien revisa tu Pull Request,
> lo primero que mira es: ¿la parametrización cubre la tabla completa?
> El código viene después."

---

## A.4 Demo en vivo (minutos 35-50)

> **Transición:** "Ahora vamos a ver todo esto en código real. Voy a abrir el archivo del laboratorio y les voy a mostrar cómo se derivan los casos directo desde los requerimientos."

### [SLIDE 10]

**PASO 1 — Abrir el código (3 min):**

**ACCIÓN:** Abre `design_lab/discount.py` en tu editor, compartido en pantalla.

**GUION:**
> "Esta función calcula el descuento de un pedido.
> Miren el docstring — tiene 5 requerimientos, del REQ-DSC-001 al 005.
> Tómense 30 segundos para leerlos."

**ACCIÓN:** Espera 30 segundos en silencio.

**ACCIÓN:** Sube el scroll a las constantes. Señala cada una:

**GUION:**
> "Arriba ven las constantes. VOLUME_THRESHOLD es 1,000 — el umbral de bono por volumen.
> DISCOUNT_CAP es 15 — el tope máximo de descuento.
> Están como constantes para que si el negocio cambia, se toca UNA línea."

---

**PASO 2 — Derivar EP en vivo (5 min):**

**ACCIÓN:** Abre la pizarra virtual (Miro, Jamboard, o pizarra de Zoom/Teams). Comparte esa ventana.

**GUION:**
> "Vamos a derivar casos desde los requerimientos. Empiezo con REQ-DSC-005:
> el pedido debe estar entre 0 exclusivo y 10,000 inclusivo.
> De ahí salen 3 particiones:"

**ACCIÓN:** Escribe en la pizarra virtual:
```
EP para order_total (REQ-DSC-005):
  Inválida baja:  ≤ 0        → ej: 0, -50
  Válida:         (0; 10000] → ej: 500
  Inválida alta:  > 10000    → ej: 10000.01
```

**GUION:**
> "3 particiones. Probamos un valor de cada una. Eso es EP."

---

**PASO 3 — Derivar BVA en vivo (3 min):**

**ACCIÓN:** Escribe debajo en la pizarra virtual:
```
BVA para order_total (REQ-DSC-005):
  0       → inválido (frontera exclusiva, NO pasa)
  0.01    → válido (primer valor que sí pasa)
  10000   → válido (último valor que pasa)
  10000.01→ inválido (primer valor que NO pasa)

BVA para umbral volumen (REQ-DSC-002):
  999.99  → sin bono
  1000.00 → con bono  ← el límite exacto
```

**GUION:**
> "4 valores para el rango, 2 para el umbral. Con 6 tests de BVA
> cubrimos TODAS las fronteras. Si hay un error de menor-que versus
> menor-o-igual, uno de estos tests lo detecta."

---

**PASO 4 — Derivar tabla de decisión en vivo (3 min):**

**ACCIÓN:** Escribe en la pizarra virtual:
```
Tabla de decisión (3 condiciones):
  ¿Premium?    Sí / No
  ¿≥ $1,000?   Sí / No
  ¿Cupón?      Sí / No
  → 2³ = 8 reglas

  R8: Sí + Sí + Sí = 10 + 5 + 5 = 20% → TOPE → 15%
```

**GUION:**
> "3 condiciones booleanas = 8 combinaciones. La más peligrosa es R8:
> premium más volumen más cupón suma 20, pero el tope recorta a 15.
> Sin la tabla, nadie piensa en probar este caso."

---

**PASO 5 — Mostrar la matriz (1 min):**

**ACCIÓN:** Abre `matriz-trazabilidad.csv` en pantalla.

**GUION:**
> "Miren la matriz. El TC-DSC-BVA-004 del test es el mismo ID que está aquí.
> Si este test falla, sé exactamente qué requerimiento está en riesgo:
> REQ-DSC-002, el umbral de volumen. En segundos. No en horas."

---

## A.5 Resumen y preguntas (minutos 50-55)

**ACCIÓN:** Sin compartir pantalla. Habla directo a cámara.

**GUION:**
> "Resumen rápido: aprendimos 4 técnicas — EP, BVA, tabla de decisión y pairwise.
> Y aprendimos trazabilidad: REQ, TC, DEF.
> En el Bloque B van a ejecutar todo esto en código real.
> Pero antes, 3 preguntas rápidas."

**ACCIÓN:** Haz las preguntas al grupo. Pide que respondan en el chat.

1. **Pregunta:** "¿Cuántos valores de BVA necesito para un rango de 0 a 10,000?"
   **Respuesta esperada:** "4: los dos límites y sus vecinos."
   **Si nadie responde:** "4. El 0, el 0.01, el 10000 y el 10000.01."

2. **Pregunta:** "¿Cuántas reglas tiene una tabla con 3 condiciones sí/no?"
   **Respuesta esperada:** "8, porque es 2 al cubo."

3. **Pregunta:** "¿Qué pasa si un test no tiene ID de trazabilidad?"
   **Respuesta esperada:** "Es un test zombie."
   **Si nadie responde:** "Es un test zombie: no sabemos qué prueba ni por qué existe. Candidato a borrar."

> ☕ **Descanso 5 min**
>
> **ACCIÓN durante el descanso:** Verifica que SauceDemo (https://www.saucedemo.com) carga bien
> en tu navegador. Lo vas a necesitar en el Bloque C.

---

# BLOQUE B (55 min) — Tú codificas, yo te guío

> **Regla de oro del Bloque B:** los estudiantes siguen tu ritmo. Tú dictas el paso, ellos ejecutan.
> Nunca digas "hagan el ejercicio". Di: "abran X archivo, línea Y, lean Z".
> **Tip virtual:** después de cada comando, pide que escriban "✅" o "❌" en el chat para confirmar que avanzan.

---

## B.1 Arrancar el laboratorio (minutos 0-10)

### ACCIONES DEL INSTRUCTOR:

1. **[SLIDE 11]** Comparte pantalla con la estructura de carpetas. No cambies de slide todavía.

2. **GUION (abriendo la sesión):**
> "Bienvenidos al Bloque B. Ahora sí, manos al teclado.
> Voy a guiarlos paso a paso. Sigan mi ritmo.
> Si algo falla, escriban 'ERROR' en el chat y les abro un breakout room para ayudarlos uno-a-uno."

3. **ACCIÓN:** Cambia a **[SLIDE 12]**. Señala con el cursor cada carpeta del árbol:

> **GUION (señalando cada línea):**
> "Miren la estructura:
> design_lab — ahí está el código fuente: discount.py y pairwise_matrix.py.
> data — ahí están los datos externos: decision_table.yaml.
> tests — ahí están los tests: uno por cada técnica.
> trazabilidad — la matriz CSV que conecta todo.
> No memoricen esto. Solo sepan dónde está cada cosa."

---

4. **ACCIÓN:** Pide que abran terminal. Dicta el comando en voz alta:

> **GUION:**
> "Abran su terminal. Naveguen a la carpeta del repo. Ejecuten exactamente esto:"

**ACCIÓN:** Escribe tú primero en tu terminal (compartida en pantalla), luego espera:
```bash
cd proyecto-integrador/design-lab
uv sync
```

5. **PAUSA:** Monitorea el chat. Pide que escriban "✅" cuando tengan `uv sync` completado.

> **⚠️ TIEMPO:** Esto toma 2-3 minutos. Si a los 4 min no todos confirman en el chat, di:
> "Si aún está descargando, no se preocupen. Escriban 'AYUDA' en el chat y les abro un breakout room."

6. **ACCIÓN:** Cuando ~80% tenga `uv sync` listo, comparte en pantalla el output esperado:
```
Resolved N packages in Xms
Installed pytest-8.x.x pyyaml-6.x.x allpairspy-2.x.x
```

> **GUION:**
> "Deberían ver algo así. 3 paquetes instalados. Si dice 'error', escriban en el chat qué mensaje les aparece.
> Las causas más comunes: no tener uv instalado, o estar en la carpeta equivocada."

7. **ACCIÓN:** Cuando todos estén listos, dicta el siguiente comando:
```bash
uv run pytest -v
```

8. **PAUSA:** Espera 10 segundos mientras corren los tests.

9. **ACCIÓN:** Comparte tu propia terminal con el output completo (25 passed).

> **GUION:**
> "Cuenten conmigo: 25 tests. Todos en verde.
> Miren los IDs entre corchetes: TC-DSC-EP-001, TC-DSC-BVA-004, TC-DT-R8.
> Esos IDs son los mismos que están en la matriz de trazabilidad.
> Así es como se conectan los tests con los requerimientos."

### CHECKPOINT:
- Todos tienen 25 tests en verde (confirman con "✅" en el chat).
- Nadie está atascado en `uv sync`.
- Si alguien sigue con problemas, crea un breakout room con un compañero como "pair" mientras continúas. Si son muchos, dedica 5 minutos extra y comparte pantalla con ellos.

---

## B.2 EP + BVA ejecutables (minutos 10-30)

> **Transición:** "Perfecto. 25 tests verdes. Ahora vamos a entender QUÉ prueba cada uno.
> Abran el archivo de EP y BVA. Vamos a leerlo juntos."

### PARTE 1 — Leer los datos (min 10-18)

1. **ACCIÓN:** Di en voz alta:
> "Abran `tests/test_equivalence_boundary.py`. No ejecuten nada todavía. Solo lean."

2. **ACCIÓN:** Comparte tu editor en pantalla con el archivo abierto. Haz scroll a la docstring.

> **GUION (leyendo la docstring en voz alta):**
> "La docstring dice: este archivo implementa dos técnicas.
> EP — particiones de equivalencias: agrupamos valores que se comportan igual.
> BVA — valores límite: probamos las fronteras donde viven los bugs.
> Eso ya lo sabemos del Bloque A. Ahora veámoslo en código."

3. **ACCIÓN:** Haz scroll al **BLOQUE 1: VALID_PARTITIONS**. Señala con el cursor cada fila:

> **GUION:**
> "Miren VALID_PARTITIONS. 4 filas. Cada fila es un caso de prueba.
> Fíjense en el `id=`: TC-DSC-EP-001, 002, 003, 004.
> Esos son los IDs de trazabilidad. Si un test falla, sé exactamente qué requerimiento probar."

4. **ACCIÓN:** Señala con el cursor los valores de cada fila:

> **GUION:**
> "EP-001: standard, $500, sin cupón → descuento base 0%.
> EP-002: premium, $500, sin cupón → descuento 10%.
> EP-003: standard, $500, con cupón → descuento 5%.
> EP-004: premium, $2000, sin cupón → 10% premium + 5% volumen = 15%.
> Cuatro particiones distintas. Cuatro comportamientos distintos."

---

5. **ACCIÓN:** Haz scroll al **BLOQUE 2: BOUNDARIES**.

> **GUION (pregunta al grupo antes de explicar):**
> "Antes de explicar esto, una pregunta:
> ¿Por qué en BOUNDARIES usamos 'standard' y sin cupón?"

6. **PAUSA:** Espera 10 segundos. Alguien responderá.

> **Si nadie responde, GUION:**
> "Porque queremos aislar el efecto del monto.
> Si usáramos premium, no sabríamos si el resultado es por el tipo de cliente o por el monto.
> En BVA, una sola variable cambia a la vez."

7. **ACCIÓN:** Señala con el cursor cada fila de BOUNDARIES:

> **GUION:**
> "BVA-001: $0.01 — el mínimo válido. Primer valor que pasa.
> BVA-003: $999.99 — justo antes del umbral de volumen. Sin bono.
> BVA-004: $1,000.00 — exactamente en el umbral. Con bono.
> BVA-005: $10,000.00 — el máximo válido. Último valor que pasa.
> Si el programador escribió `>` en vez de `>=`, el test BVA-004 lo detecta."

---

8. **ACCIÓN:** Haz scroll al **BLOQUE 3: INVALID_PARTITIONS**.

> **GUION:**
> "Último bloque. 4 particiones inválidas.
> Miren `pytest.raises(ValueError)`.
> Esto NO es manejo de errores. Es un requerimiento ejecutable.
> El test dice: 'si entro un valor inválido, el código DEBE lanzar ValueError'.
> Si no lo lanza, el test falla. Y eso es un bug."

### CHECKPOINT (min 18):
- Pregunta rápida al grupo (responder en chat): "¿Cuántos tests de EP+BVA tenemos en total?"
- Respuesta: "12. 4 válidas + 4 límites + 4 inválidas."

---

### PARTE 2 — Ejecutar y verificar (min 18-30)

1. **ACCIÓN:** Di a los estudiantes:
> "Ahora sí, ejecuten. Pero solo los tests de EP y BVA, no todos."

**ACCIÓN:** Escribe en tu terminal (compartida en pantalla):
```bash
uv run pytest -v tests/test_equivalence_boundary.py
```

2. **PAUSA:** Espera 5 segundos.

3. **ACCIÓN:** Cuando la mayoría confirme en el chat, comparte el output:
```
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-001-standard-base] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-002-premium-base] PASSED
... (12 passed total)
```

> **GUION:**
> "12 passed. Cuenten: 4 válidas + 4 límite + 4 inválidas = 12.
> Cada test tiene su ID. Cada ID está en la matriz.
> Si mañana alguien borra una partición, la cuenta no da y lo notamos."

4. **ACCIÓN (si hay tiempo — 3 min extra):** Pide que abran `design_lab/discount.py`.

> **GUION:**
> "Miren el código que están probando. La función calculate_discount.
> Vean las constantes: VOLUME_THRESHOLD = 1000. DISCOUNT_CAP = 15.
> Los tests de BVA prueban exactamente esos valores.
> Si alguien cambia VOLUME_THRESHOLD a 2000, los tests BVA-003 y BVA-004 fallan.
> Eso es trazabilidad viva."

### CHECKPOINT:
- Todos tienen 12 passed en EP+BVA.
- Los estudiantes entienden qué prueba cada bloque.

---

## B.3 Tabla de decisión (minutos 30-45)

> **Transición:** "Ya tenemos EP y BVA. Ahora la técnica más poderosa: tabla de decisión.
> Pero primero, vamos a ver dónde están los datos."

### PARTE 1 — Los datos YAML (min 30-37)

1. **ACCIÓN:** Di en voz alta:
> "Abran `data/decision_table.yaml`. No el test — primero los datos."

2. **ACCIÓN:** Comparte tu editor en pantalla con el YAML abierto.

> **GUION:**
> "Este archivo tiene las 8 reglas de la tabla de decisión.
> 3 condiciones × sí/no = 8 combinaciones.
> Léanlas. La más importante es la última: DT-R8."

3. **PAUSA:** 30 segundos para que lean.

4. **ACCIÓN:** Haz scroll hasta DT-R8. Señálala con el cursor.

> **GUION:**
> "DT-R8: premium sí, volumen sí, cupón sí.
> Eso suma 10 + 5 + 5 = 20%.
> Pero el tope es 15%. Entonces expected es 15.0, no 20.0.
> Esta regla NO existiría si no hubiéramos hecho la tabla completa."

5. **ACCIÓN:** Haz la pregunta de desacoplamiento:

> **GUION:**
> "Pregunta: si el negocio cambia el tope de 15% a 20%,
> ¿qué archivo tengo que tocar?"

6. **PAUSA:** Espera respuesta.

> **Respuesta esperada:** "Solo el YAML."
> **Si nadie responde:**
> "Solo el YAML. Cambio `expected: 15.0` a `expected: 20.0` en DT-R6, DT-R7 y DT-R8.
> No toco código Python. Eso es desacoplamiento: los datos viven aparte del código."

---

### PARTE 2 — El test de tabla (min 37-42)

1. **ACCIÓN:** Di a los estudiantes:
> "Ahora abran `tests/test_decision_table.py`."

2. **ACCIÓN:** Comparte tu editor en pantalla. Señala con el cursor la función `load_rules()`.

> **GUION:**
> "Miren `load_rules()`. Esta función lee el YAML y lo convierte en `pytest.param`.
> El test no tiene NINGÚN dato hardcodeado.
> Todo viene del YAML. Si agrego una regla al YAML, automáticamente se prueba."

3. **ACCIÓN:** Haz scroll al test `test_decision_table_is_complete`. Señálalo con el cursor.

> **GUION (énfasis):**
> "Este test es especial. Se llama test guardrail.
> Cuenta cuántas combinaciones hay en el YAML.
> Si alguien borra una regla — por accidente o por flojera — este test falla.
> Protege el DISEÑO, no solo el código."

---

### PARTE 3 — Ejecutar y demo del guardrail (min 42-45)

1. **ACCIÓN:** Dicta el comando:
```bash
uv run pytest -v tests/test_decision_table.py
```

2. **PAUSA:** Espera 5 segundos.

> **GUION:** "9 passed. 8 reglas más 1 guardrail."

3. **ACCIÓN (DEMO EN VIVO):** Di al grupo:
> "Ahora voy a hacer algo. Voy a borrar la regla DT-R8 del YAML. A ver qué pasa."

4. **ACCIÓN:** En tu editor, borra (o comenta) las líneas de DT-R8 en el YAML.

5. **ACCIÓN:** Ejecuta solo el guardrail:
```bash
uv run pytest -v tests/test_decision_table.py::test_decision_table_is_complete
```

6. **ACCIÓN:** Comparte el FAILED en pantalla (asegúrate de que se vea bien en la videollamada).

> **GUION:**
> "Falló. Dice: 'Faltan reglas: hay 7 de 8 combinaciones esperadas'.
> El guardrail detectó que alguien borró una regla.
> Esto es diseño protegido por código."

7. **ACCIÓN:** Restaura el YAML (Ctrl+Z o `git checkout -- data/decision_table.yaml`).

> **GUION:**
> "Siempre restauren después del experimento. O hacen `git checkout` para volver al estado original."

### CHECKPOINT:
- Todos tienen 9 passed en tabla de decisión.
- Entendieron qué es un test guardrail y por qué importa.

---

## B.4 Pairwise (minutos 45-55)

> **Transición:** "Última técnica del bloque: pairwise.
> Vamos a ver la matriz cross-browser y descubrir el bug de la herramienta."

### PARTE 1 — Leer el test (min 45-50)

1. **ACCIÓN:** Di al grupo:
> "Abran `tests/test_pairwise.py`. Lean los primeros 20 segundos."

2. **PAUSA:** 20 segundos de silencio.

3. **ACCIÓN:** Comparte tu editor en pantalla con el archivo.

> **GUION:**
> "Este archivo prueba la matriz cross-browser:
> 3 navegadores por 3 sistemas por 2 idiomas por 3 roles.
> Producto cartesiano: 54 combinaciones.
> Pairwise: aproximadamente 10 filas. 80% menos."

4. **ACCIÓN:** Señala la constante `CONSTRAINTS`.

> **GUION:**
> "Miren la restricción: webkit solo corre en macOS.
> Es real: Safari no existe en Windows ni Linux.
> La herramienta debería respetar esta restricción."

5. **ACCIÓN:** Dicta el comando:
```bash
uv run pytest -v tests/test_pairwise.py
```

6. **PAUSA:** Espera 5 segundos.

> **GUION:** "4 passed. La matriz pairwise funciona."

---

### PARTE 2 — Gap analysis y el bug (min 50-55)

1. **ACCIÓN:** Di al grupo:
> "Ahora abran `design_lab/pairwise_matrix.py`. Vamos a ver cómo se genera la matriz."

2. **ACCIÓN:** Comparte tu editor en pantalla. Señala con el cursor el patrón de 3 pasos:

> **GUION:**
> "El patrón es: generar, auditar, complementar.
> Paso 1: allpairspy genera la matriz inicial.
> Paso 2: nuestra función `missing_pairs` revisa si quedaron huecos.
> Paso 3: si hay huecos, agregamos filas extra manualmente."

3. **ACCIÓN:** Señala con el cursor el test `test_pairwise_covers_every_achievable_pair`.

> **GUION (cambia el tono a serio):**
> "Este test es la lección más importante de toda la sesión.
> Audita que no queden pares sin cubrir.
> La herramienta allpairspy tiene un bug conocido: cuando hay restricciones,
> puede dejar pares sin cubrir sin avisar.
> Nosotros NO confiamos ciegamente. Escribimos un test que lo verifique."

4. **ACCIÓN:** Haz la pregunta de cierre:

> **GUION:**
> "Pregunta para cerrar: ¿por qué escribimos un test que audite la herramienta?"

5. **PAUSA:** Espera respuesta.

> **Respuesta esperada:** "Porque la herramienta puede tener bugs."
> **Si nadie responde:**
> "Porque nunca confiamos ciegamente en una herramienta.
> Si la herramienta dice 'cubrí todos los pares', lo demostramos con un test.
> Esa es la mentalidad del QA engineer: dudar de todo, incluso de las herramientas."

### CHECKPOINT:
- Todos tienen 4 passed en pairwise.
- Entendieron el patrón generar-auditar-complementar.
- La frase "nunca confíen ciegamente en la herramienta" quedó clara.

> ☕ **Descanso 5 min**
>
> **ACCIÓN durante el descanso:**
> 1. Verifica que SauceDemo (https://www.saucedemo.com) carga en tu navegador.
> 2. Abre la matriz `matriz-trazabilidad.csv` y verifica que las filas REQ-LOG-001/002/003
>    tienen estado "PENDIENTE". Lo necesitas para el Bloque C.
> 3. Si algún estudiante sigue atascado del Bloque B, ayúdalo ahora.

---

# BLOQUE C (60 min) — Tú trabajas solo, yo superviso

> **Regla de oro del Bloque C:** los estudiantes trabajan solos. Tú monitorean el chat,
> responden dudas uno-a-uno (por mensaje privado o breakout room), y detectas problemas comunes para discutirlos al final.
> Deja de compartir pantalla durante C.1 y C.2 — ellos producen, tú observas el chat.

---

## C.1 Ejercicio individual: Diseñar casos para SauceDemo Login (minutos 0-25)

### PARTE 1 — Exploración (min 0-5)

1. **[SLIDE 13]**

2. **ACCIÓN:** Comparte pantalla con SauceDemo abierto.

> **GUION:**
> "Bloque C. Ahora ustedes trabajan solos.
> Abran https://www.saucedemo.com en su navegador.
> Tienen 3 minutos para explorar. Prueben hacer login con diferentes usuarios.
> Anoten lo que observan: qué funciona, qué no, qué mensajes aparecen."

3. **ACCIÓN:** Comparte la pizarra virtual y escribe los 4 usuarios (para que los tengan a la vista):
```
standard_user          / secret_sauce  → login exitoso
locked_out_user        / secret_sauce  → mensaje de error
problem_user           / secret_sauce  → login con glitches
performance_glitch_user/ secret_sauce  → login lento
```

4. **PAUSA:** 3 minutos de exploración libre. Monitorea el chat — pueden escribir observaciones en tiempo real.

> **⚠️ SI ALGUIEN PREGUNTA:** "¿Qué es un glitch?" → "Una falla visual. Por ejemplo,
> una imagen que no carga o un texto cortado. Anótalo como observación."

---

### PARTE 2 — Explicar la tarea (min 5-8)

1. **ACCIÓN:** Vuelve a compartir tu pantalla. Comparte la matriz `matriz-trazabilidad.csv` abierta.

> **GUION:**
> "Ya exploraron. Ahora vamos a convertir lo que observaron en casos de prueba trazables.
> Abran `matriz-trazabilidad.csv`.
> Van a ver que ya hay 3 filas marcadas como PENDIENTE: REQ-LOG-001, 002 y 003.
> Su trabajo: completar esas filas con los casos de prueba que diseñen."

2. **ACCIÓN:** Comparte una fila de ejemplo de la matriz. Señala con el cursor cada columna:

> **GUION (columna por columna):**
> "req_id → Ejemplo: REQ-LOG-001. Es el ID del requerimiento.
> requerimiento → Lo que observaron, redactado como requerimiento formal.
> Por ejemplo: 'Credenciales válidas redirigen a /inventory.html'.
> tc_id → Ejemplo: TC-LOG-EP-001. Es el ID del test case. Noten el EP: es la técnica.
> caso_de_prueba → Qué entra y qué se espera. Ejemplo: 'standard_user + secret_sauce → redirect a /inventory.html'.
> tecnica → El nombre completo: 'Partición de equivalencias', 'BVA' o 'Tabla de decisión'.
> archivo_prueba → Déjenlo vacío. Lo completamos en la Sesión 2.
> estado → Escriban 'DISEÑO'. Significa que el caso existe pero aún no está automatizado.
> def_id → Déjenlo vacío. Solo se llena si el test encuentra un bug real."

3. **ACCIÓN:** Da la instrucción de inicio:

> **GUION:**
> "Tienen 20 minutos. Trabajen solos.
> Mínimo esperado: cada REQ-LOG con al menos un TC,
> al menos una partición inválida, y una tabla de decisión.
> Estoy en el chat. Si tienen duda, escriban — o envíenme un mensaje privado para ayuda uno-a-uno.
> Si necesitan que vea su pantalla, pidan un breakout room conmigo."

---

### PARTE 3 — Trabajo individual (min 8-25)

1. **ACCIÓN:** Los estudiantes trabajan. Tú monitorean el chat activamente.

> **⚠️ NO te quedes en silencio.** Revisa el chat cada 2-3 minutos. Si alguien pide ayuda, responde por mensaje privado
> o abre un breakout room rápido (máx 3 min). Si ves la misma pregunta repetida, interrumpe al grupo y aclara en voz alta.

2. **GUÍA INTERNA (para ti, NO se los digas directamente):**

   Esto es lo que los estudiantes deberían producir. Si alguien se atasca en el chat, oriéntalo con preguntas, no con respuestas:

   **Requerimientos observables:**
   - `REQ-LOG-001`: Credenciales válidas redirigen a `/inventory.html`
   - `REQ-LOG-002`: Usuario bloqueado recibe mensaje específico
   - `REQ-LOG-003`: Credenciales inválidas muestran error

   **Particiones de equivalencia (usuario):**
   - Válido activo (`standard_user`) / Válido bloqueado (`locked_out_user`)
   - Inexistente (`fake_user`) / Vacío (campo en blanco)

   **Particiones de equivalencia (contraseña):**
   - Correcta (`secret_sauce`) / Incorrecta (`wrong_password`) / Vacía

   **Tabla de decisión (3 condiciones):**
   - ¿Usuario existe? / ¿Contraseña correcta? / ¿Usuario bloqueado?
   - 2³ = 8 reglas, pero algunas son imposibles (usuario bloqueado + contraseña incorrecta puede no ser distinguible de usuario inexistente)

3. **ACCIÓN (a los 15 minutos):** Interrumpe al grupo (todos deberían estar con micrófono apagado, habla en voz alta):

> **GUION:**
> "Atención. Faltan 10 minutos. Checklist de verificación:
> ¿Cada REQ-LOG tiene al menos un TC?
> ¿Cada TC declara su técnica?
> ¿Hay al menos una partición inválida para usuario y para contraseña?
> ¿Hay una tabla de decisión?
> Si les falta algo, complétenlo ahora."

4. **PAUSA:** 10 minutos más de trabajo.

### CHECKPOINT (min 25):
- Pide que escriban "✅" en el chat los que tienen los 3 REQ-LOG con al menos un TC cada uno.
- Si menos del 50% confirma, da 3 minutos extra y reduce C.2.

---

## C.2 Mini reto: Pairwise para matriz web (minutos 25-45)

> **Transición:** "Buen trabajo. Ahora un reto más difícil.
> Vamos a aplicar pairwise a una matriz de compatibilidad con una restricción real."

### PARTE 1 — Plantear el problema (min 25-28)

1. **[SLIDE 14]**

2. **ACCIÓN:** Comparte la pizarra virtual y escribe (no cambies de slide, usa la pizarra para que lo copien):
```
navegador:   {chromium, firefox, webkit}
pantalla:    {mobile, tablet, desktop}
tema:        {light, dark}
rol:         {admin, user}

Restricción: admin NO se prueba en mobile

Total combinaciones: 3 × 3 × 2 × 2 = 36
```

3. **GUION (explicando el escenario):**
> "Este es un caso real típico. Tenemos una app web que debe funcionar en
> 3 navegadores, 3 tamaños de pantalla, 2 temas y 2 roles.
> Producto cartesiano: 36 combinaciones. Demasiado.
> Pairwise lo reduce a ~10. Pero hay una restricción: admin no se prueba en mobile
> — porque la app no soporta panel de admin en móvil."

4. **ACCIÓN:** Da la instrucción:

> **GUION:**
> "Su tarea, en `tests/test_pairwise.py`:
> 1. Agregar la constante PARAMETERS_LOGIN con los 4 parámetros.
> 2. Crear la función de restricción: si rol es admin y pantalla es mobile, esa combinación no va.
> 3. Generar la matriz pairwise.
> 4. Escribir UN test que verifique 3 cosas:
>    a) El total es menor que 36.
>    b) La restricción se respeta — ninguna fila tiene admin + mobile.
>    c) Todos los pares de (pantalla, tema) están cubiertos.
> Tienen 18 minutos."

---

### PARTE 2 — Trabajo individual (min 28-44)

1. **ACCIÓN:** Los estudiantes trabajan. Tú monitorean el chat.

> **⚠️ ESTE ES EL RETO MÁS DIFÍCIL DE LA SESIÓN.**
> Muchos estudiantes se van a atascar en cómo escribir la restricción.

2. **AYUDA SI SE ATASCAN (preguntas orientadoras, no respuestas):**
   - Si no saben cómo empezar: "Miren cómo está definida la restricción webkit del laboratorio. Es el mismo patrón."
   - Si no saben verificar la restricción en el test: "Piensen: si recorro cada fila de la matriz, ¿cómo verifico que ninguna tenga admin Y mobile juntos?"
   - Si no saben verificar cobertura de pares: "Miren el test `test_pairwise_covers_every_achievable_pair` del laboratorio. Es el mismo patrón."

3. **ACCIÓN (a los 15 minutos, min 43):** Interrumpe al grupo:

> **GUION:**
> "Un minuto para cerrar. Los que no terminaron, anoten dónde se quedaron.
> Vamos a discutir la solución."

---

### PARTE 3 — Discusión de la solución (min 44-45)

1. **ACCIÓN:** Pregunta al grupo:

> **GUION:**
> "Pregunta para cerrar: ¿qué defectos podrían escaparse con pairwise
> en vez del producto cartesiano completo?"

2. **PAUSA:** Espera respuesta.

> **Respuesta esperada:**
> "Defectos que requieren 3 o más parámetros interactuando simultáneamente.
> Por ejemplo: un bug que solo aparece con chromium + mobile + dark + admin.
> Pairwise garantiza pares, no tríos ni cuartetos."
>
> **Si nadie responde:**
> "Imaginen un bug que SOLO aparece cuando se juntan chromium + mobile + dark + admin.
> Pairwise garantiza que cada PAR aparezca junto. Pero no garantiza que los 4 aparezcan juntos.
> Por eso pairwise es 'suficiente para la mayoría de casos' pero no para todos.
> Es un trade-off: menos tests a cambio de un riesgo pequeño."

### CHECKPOINT:
- Al menos la mitad de la clase tiene el test del mini reto pasando.
- Todos entienden la limitación de pairwise (garantiza pares, no tríos).

---

## C.3 Errores comunes + cierre (minutos 45-60)

> **Transición:** "Buen trabajo hoy. Antes de irnos, vamos a ver los 7 errores más comunes
> que cometen los equipos de QA — y cómo evitarlos."

### PARTE 1 — Los 7 errores (min 45-55)

1. **[SLIDE 15]**

2. **ACCIÓN:** Comparte pantalla con la tabla de errores. No la leas completa — ve error por error.

> **⚠️ DINÁMICA VIRTUAL:** Para cada error, lanza una encuesta rápida (poll) de Zoom/Teams:
> "¿Hiciste esto hoy?" — Sí / No. Luego explica la práctica correcta. Los polls son anónimos, así que nadie se siente juzgado.

**Error 1:** "Probar solo el camino feliz con valores arbitrarios."

> **GUION:**
> "Practicar solo el camino feliz es lo más común. El usuario feliz nunca existe en producción.
> Siempre hay alguien que mete un valor raro. La práctica correcta:
> cada valor viene de una técnica y es trazable a un REQ. No inventamos valores al azar."

**Error 2:** "Un test gigante con 15 asserts."

> **GUION:**
> "Un test con 15 asserts es un test que prueba 15 cosas distintas.
> Si falla el assert 8, ¿cuál de los 15 escenarios rompió?
> La práctica: un caso parametrizado. Agregar caso = agregar una línea."

**Error 3:** "Datos incrustados en el código del test."

> **GUION:**
> "Si los datos están en el código, cada vez que cambia un valor, modifico el test.
> La práctica: datos en YAML o CSV, versionados en data/.
> Vimos esto con decision_table.yaml — si el negocio cambia, solo toco el YAML."

**Error 4:** "Matriz de trazabilidad en Excel que nadie actualiza."

> **GUION:**
> "Excel se queda en el correo de alguien. Nadie lo abre. Nadie lo actualiza.
> La práctica: CSV en el repo, versionado en Git, revisado en cada Pull Request."

**Error 5:** "Más tests = más calidad."

> **GUION:**
> "Una suite de 40 minutos con 300 tests que tienen huecos de diseño.
> La práctica: cobertura mínima suficiente. EP + BVA + tabla + pairwise.
> Menos tests, mejor diseñados, más bugs detectados."

**Error 6:** "Ignorar particiones inválidas."

> **GUION:**
> "Eso nunca pasa' — famoso últimas palabras.
> La práctica: pytest.raises como caso de primera clase.
> Las particiones inválidas son tan importantes como las válidas."

**Error 7:** "Copiar y pegar tests cambiando solo un número."

> **GUION:**
> "Si tienes 10 tests idénticos que solo cambia un valor, tienes 10 copias.
> La práctica: @pytest.mark.parametrize. Agregar caso = agregar una línea."

---

### PARTE 2 — Checklist de salida (min 55-58)

1. **[SLIDE 16]**

2. **ACCIÓN:** Comparte pantalla con el checklist. Pide que cada estudiante verifique en su máquina:

> **GUION:**
> "Antes de cerrar, verifiquen esto en su máquina. Si algo no está, escriban en el chat."

**ACCIÓN:** Lee cada punto en voz alta y da 10 segundos para verificar:

- [ ] `uv run pytest -v` corre en verde: 25+ tests (EP, BVA, tablas, pairwise).
- [ ] `matriz-trazabilidad.csv` tiene los REQ-DSC-* verificados y los REQ-LOG-* completados con al menos un TC cada uno.
- [ ] Mini reto pairwise implementado (aunque esté incompleto, anota dónde te quedaste).
- [ ] Puedes explicar en 1 minuto por qué DT-R8 no existiría sin tabla de decisión.

3. **ACCIÓN:** Pregunta final al grupo:

> **GUION:**
> "¿Quién puede explicar por qué DT-R8 no existiría sin la tabla de decisión?
> Escriban en el chat o activen su micrófono."

> **Si alguien activa el micrófono o escribe una respuesta buena, pídele que lo explique en voz alta al grupo.**
> Respuesta esperada: "Porque premium + volumen + cupón suma 20%, pero el tope es 15%.
> Sin la tabla completa, nadie piensa en probar la combinación de los 3 juntos."
>
> **Si nadie responde en el chat ni activa micrófono, dilo tú:**
> "Premium más volumen más cupón suma 20%. Pero el tope es 15%.
> Sin construir la tabla completa con las 8 reglas, nadie piensa en probar ese caso.
> Y ese caso es un bug que llega a producción."

---

### PARTE 3 — Próxima sesión + commit (min 58-60)

1. **[SLIDE 17]**

2. **ACCIÓN:** Comparte pantalla con el preview de la Sesión 2.

> **GUION (cierre energético):**
> "Hoy aprendieron a diseñar tests antes de escribir código.
> En la Sesión 2, estos diseños se convierten en pruebas automatizadas reales
> de la UI de SauceDemo, usando Page Object Model, Screenplay y DRY.
> La matriz de trazabilidad crece: los TC-LOG-* pasan de DISEÑO a PASS.
> Nos vemos en la próxima sesión."

3. **ACCIÓN:** Da la instrucción de commit:

> **GUION:**
> "Antes de irse, hagan commit de su trabajo de hoy:
> ```
> git add .
> git commit -m "S1: completar matriz trazabilidad REQ-LOG + mini reto pairwise"
> git push
> ```
> Yo revisaré sus repos después de clase. No necesitan enviar nada por correo."

4. **ACCIÓN:** Espera a que todos confirmen con "✅" en el chat que hicieron commit y push. Si alguien tiene problemas con git, abre un breakout room rápido para ayudarlo.

### CHECKPOINT FINAL:
- Todos confirmaron commit y push en el chat.
- La matriz tiene los REQ-LOG-* completados.
- Nadie se desconecta con dudas sin resolver (o con plan para resolverlas antes de S2 por chat/correo).

---

## NOTAS PARA EL INSTRUCTOR

### Si el grupo es avanzado:
- En B.3, después de mostrar el guardrail, pide que MODIFIQUEN el YAML para agregar una novena regla con un tipo de cliente "vip" y vean qué pasa.
- En C.1, pide que diseñen también casos para el carrito de compras de SauceDemo (agregar/quitar items, cantidades).
- En C.2, pide que además verifiquen cobertura de todos los pares (navegador, rol) — no solo (pantalla, tema).

### Si el grupo necesita más tiempo:
- Reduce C.2 (mini reto) a 10 min y da el código base del pairwise login como plantilla.
- Salta el ejercicio de borrar DT-R8 en B.3 — solo muéstralo tú en tu pantalla.
- En C.1, reduce el mínimo esperado a 2 REQ-LOG en vez de 3.

### Si algo falla técnicamente:
- `uv sync` falla → verifica conexión a internet. Alternativa: `pip install pytest allpairspy pyyaml`.
- `pytest` no encuentra tests → verifica que están en la carpeta `design-lab/`.
- Tests fallan en rojo → ejecuta `uv run pytest -v --tb=short` para ver el error específico.
- SauceDemo no carga → ten screenshots listos como backup (captúralos antes de clase).

### Para evaluar esta sesión:
- Revisa los commits de cada estudiante en la matriz de trazabilidad.
- Verifica que los REQ-LOG-* tienen al menos 3 TC cada uno con técnica declarada.
- El mini reto pairwise debe tener las 3 validaciones (a, b, c).
- Penalización: si la matriz tiene REQ sin TC o TC sin técnica, pide correcciones antes de S2.
