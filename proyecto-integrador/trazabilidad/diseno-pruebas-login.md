# Diseño de pruebas — Login de [SauceDemo](https://www.saucedemo.com/)

**SUT:** https://www.saucedemo.com/
**Matriz de trazabilidad:** [`matriz-trazabilidad.csv`](matriz-trazabilidad.csv) (filas `REQ-LOG-*`)
**Archivo de pruebas destino:** pendiente de implementación; estado `PENDIENTE` en la matriz

## 1. Datos de prueba

Password única para todos los usuarios: `secret_sauce`.

| Usuario | Comportamiento esperado en el login |
|---|---|
| `standard_user` | Accede al inventario |
| `locked_out_user` | Rechazado: "Sorry, this user has been locked out." |
| `problem_user` | Accede (sus defectos son post-login) |
| `performance_glitch_user` | Accede, pero con lentitud → se verifica timeout |
| `error_user` | Accede (sus defectos son post-login) |
| `visual_user` | Accede (sus defectos son visuales, post-login) |

### 2 Pairwise (pruebas combinatorias)

**Parámetros:** usuario (5 valores válidos — `locked_out_user` se excluye porque no puede completar el login) × navegador (`chromium`, `firefox`, `webkit`) × viewport (`desktop`, `mobile`).

**Producto cartesiano completo:** 5 × 3 × 2 = 30 combinaciones.

**Pares que pairwise exige cubrir:**

| Par de parámetros | Pares |
|---|---|
| usuario × navegador | 5 × 3 = 15 |
| usuario × viewport | 5 × 2 = 10 |
| navegador × viewport | 3 × 2 = 6 |
| **Total** | **31** |

Cada fila de la matriz cubre exactamente un par usuario×navegador, y existen 15 pares distintos, por lo que ninguna matriz pairwise puede tener menos de 15 filas (la cota inferior es el producto de las dos cardinalidades mayores: 5 × 3). Los 16 pares restantes caben dentro de esas mismas filas.


| # | Usuario | Navegador | Viewport |
|---|---|---|---|
| 1 | standard_user | chromium | desktop |
| 2 | problem_user | firefox | desktop |
| 3 | performance_glitch_user | webkit | desktop |
| 4 | error_user | webkit | mobile |
| 5 | visual_user | firefox | mobile |
| 6 | visual_user | chromium | desktop |
| 7 | error_user | chromium | desktop |
| 8 | performance_glitch_user | chromium | mobile |
| 9 | problem_user | chromium | mobile |
| 10 | standard_user | webkit | mobile |
| 11 | standard_user | firefox | mobile |
| 12 | problem_user | webkit | mobile |
| 13 | performance_glitch_user | firefox | mobile |
| 14 | error_user | firefox | mobile |
| 15 | visual_user | webkit | mobile |

las 15 combinaciones se representan con **2 filas TC** (no 15).

- **TC-LOG-PW-001** — aserción de cobertura: la matriz generada cubre los 31 pares exigibles 
- **TC-LOG-PW-002** — combinación representativa de mayor riesgo: `performance_glitch_user × firefox × mobile` con verificación de timeout

Las 15 ejecuciones son el mínimo matemático y no se reducen; lo que se compacta es su representación documental.
