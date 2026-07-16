# Sesión 3 — Contenido de diapositivas
## APIs y servicios web I: Postman + Newman

> 20 slides · Bloque A: slides 1-8 (45 min) · Bloque B: slides 9-14 (45 min) · Bloque C: slides 15-20 (45 min)

---

### Slide 1 — Portada (2 min)
**Título:** APIs y servicios web I — Postman + Newman
- Sesión 3 de 10 · Curso QA Automation
- Hoy: de "apretar Send" a una suite automatizada corriendo en terminal
- SUT del día: JSONPlaceholder (API pública, sin registro)

### Slide 2 — ¿Dónde estamos? (3 min)
- S1 ✅ Diseñamos casos con técnica (EP, BVA, decisión)
- S2 ✅ Automatizamos la UI (*User Interface*) con POM y Screenplay
- S3 → Hoy bajamos una capa: probamos **directo la API**, sin navegador
- **Por qué importa:** los tests de API son ~10× más rápidos y estables que los de UI

### Slide 3 — ¿Qué es una API REST? (5 min)
- **API** = *Application Programming Interface* — el "mesero" entre apps
- **REST** = *Representational State Transfer* — todo es un recurso con URL
- Pides con **verbos HTTP**, recibes **JSON** (*JavaScript Object Notation*)

```
GET https://jsonplaceholder.typicode.com/posts/1
→ { "userId": 1, "id": 1, "title": "...", "body": "..." }
```

### Slide 4 — Los 5 verbos = CRUD (5 min)
| Verbo | CRUD | Ejemplo |
|---|---|---|
| POST | **C**reate | `POST /posts` |
| GET | **R**ead | `GET /posts/1` |
| PUT / PATCH | **U**pdate | `PUT /posts/1` |
| DELETE | **D**elete | `DELETE /posts/1` |
- PUT reemplaza **todo** el recurso; PATCH solo lo que envías

### Slide 5 — Status codes: el idioma de la API (5 min)
- `2xx` → todo bien (200 OK, 201 Created, 204 No Content)
- `4xx` → **tú** te equivocaste (400, 401, 403, 404)
- `5xx` → **el servidor** se equivocó (500, 503)
- **Regla de oro:** 4xx = revisa tu request · 5xx = repórtalo al backend

### Slide 6 — Headers y demo del primer request (7 min)
- `Content-Type: application/json` → qué formato viaja
- `Authorization: Bearer <token>` → credenciales
- **DEMO en vivo:** Postman → `GET {{base_url}}/posts/1` → leer status, tiempo, tamaño, body

### Slide 7 — Variables: una URL, un solo lugar (6 min)
- Environment: `base_url = https://jsonplaceholder.typicode.com`
- En el request: `{{base_url}}/posts/1`
- Cambia el dominio mañana → tocas **una línea**, no 50 requests
- **DEMO:** importar colección + environment del repo

### Slide 8 — Scripts: tests y pre-request (12 min)
```javascript
pm.test('Status es 200 OK', () => pm.response.to.have.status(200));
```
- **Post-response (Tests):** validan DESPUÉS de la respuesta
- **Pre-request:** preparan datos ANTES (`Date.now()` → título único)
- **DEMO:** correr la colección completa con el Collection Runner

---
**☕ DESCANSO 15 MIN**
---

### Slide 9 — El problema de la interfaz gráfica (4 min)
- Postman es genial para **diseñar**… pero alguien tiene que apretar botones
- La automatización real vive en la **terminal**
- CI/CD (*Continuous Integration/Delivery*) solo entiende comandos

### Slide 10 — Newman: Postman sin ventanas (5 min)
- Ejecutor oficial de colecciones por CLI (*Command Line Interface*)
- Open source, sin cuenta, corre donde haya Node.js
- **Nota 2026:** Postman CLI es el sucesor oficial, pero pide cuenta — Newman sigue siendo el estándar sin fricción

### Slide 11 — Exportar: la colección es código (6 min)
- Colección → clic derecho → Export → **v2.1** → `.json`
- Environment → ⚙️ → Export
- Los `.json` van a Git → se versionan, se revisan en PR, se ejecutan en CI
- **DEMO:** mostrar los archivos en `proyecto-integrador/api-tests/postman/`

### Slide 12 — DEMO: Newman en acción (12 min)
```bash
npx --yes newman run postman/s3_crud_jsonplaceholder.postman_collection.json \
  --environment postman/jsonplaceholder.postman_environment.json
```
- Leer juntos la salida: requests → tests → tabla final
- **Resultado esperado:** `17 assertions | 0 failed`
- Atajo del curso: `task test:api:postman`

### Slide 13 — Opciones útiles de Newman (8 min)
```bash
--iteration-count 3   # repetir (estabilidad)
--bail                # parar al primer fallo
-r cli,htmlextra      # reporte HTML
```
- **MINI-LAB:** cada quien corre la colección con `--iteration-count 2`

### Slide 14 — Conexión con CI/CD (10 min)
- Mismo comando → GitHub Actions lo corre en cada push (Sesión 5)
- Exit code ≠ 0 → pipeline rojo → el release **no sale**
```bash
- npx --yes newman run <colección> -e <env> ; echo "exit code: $LASTEXITCODE"
```
- Eso es una **puerta de calidad** (*quality gate*) — el corazón del proyecto integrador

---
**☕ DESCANSO 15 MIN**
---

### Slide 15 — El test que pasa… y la app rota (4 min)
- Backend renombra `title` → `postTitle`
- Tu test de "status 200" sigue verde 😱
- Las apps que consumen la API explotan
- **Moraleja:** validar el status no basta — hay que validar la **estructura**

### Slide 16 — JSON Schema: el contrato (8 min)
```javascript
const postSchema = {
    type: 'object',
    required: ['userId', 'id', 'title', 'body'],
    properties: { userId: { type: 'integer' }, title: { type: 'string' } }
};
pm.response.to.have.jsonSchema(postSchema);
```
- `required` → si falta un campo, falla
- `type` → si cambia el tipo, falla
- Postman valida con **Ajv** (*Another JSON Schema Validator*)

### Slide 17 — DEMO: romper el contrato a propósito (6 min)
- Cambiar `title: string` → `title: integer` → Send → leer el error de Ajv
- Regresarlo → verde otra vez
- Schema de **arrays**: `items: { … }` valida los 100 posts de un tiro

### Slide 18 — El reto: suite CRUD de `/users` (20 min)
- Colección `RETO_S3_<tu-nombre>` · recurso `/users` · **mínimo 5 requests**
- GET lista (10 usuarios) · GET detalle (**con schema**) · POST (pre-request dinámico) · PUT · DELETE
- Bonus: caso negativo 404 + correrla con Newman
- **Entrega:** el `.json` exportado — se aprueba si Newman dice `0 failed`

### Slide 19 — Errores comunes (4 min)
- `{{base_url}}` literal → falta seleccionar environment
- `ENOTFOUND` → internet o URL mal escrita
- `newman: command not found` → usa `npx --yes newman`
- Pre-request en la pestaña equivocada → el título dinámico no se genera

### Slide 20 — Cierre y próxima sesión (3 min)
- Hoy: REST + Postman + Newman + JSON Schema = suite de API versionada
- La colección ya es parte del proyecto integrador (Etapa 2a)
- **S4:** los mismos tests… en **Python puro** (`httpx` + `pytest`) 🐍
