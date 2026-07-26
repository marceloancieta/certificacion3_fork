# K6 contra SWAPI

Scripts (`smoke.js`, `load.js`, `fail_demo.js`) apuntando a la API pública `https://swapi.info/api` en vez del `target` local.

## Por qué se crearon los servicios `k6-swapi-*` en `docker-compose.yml`

Originalmente estos scripts se corrían con `docker run` suelto, montando la carpeta `k6/` a mano en cada comando. Para no repetir el mismo `-v` y `-e BASE_URL` cada vez, se agregaron los servicios `k6-swapi-smoke` / `k6-swapi-load` / `k6-swapi-fail` en `docker-compose.yml` — son solo un atajo sobre el mismo comando, para poder correr:

```bash
docker compose run --rm k6-swapi-smoke
docker compose run --rm k6-swapi-load
docker compose run --rm k6-swapi-fail
```

A diferencia de `k6-smoke` / `k6-load` / `k6-fail`, estos no tienen `depends_on: target` porque no dependen del nginx local — pegan directo a internet.

## Forma alternativa (antes de agregar los servicios de compose)

Corriendo el contenedor de k6 directo, montando `k6/` como volumen:

```powershell
# PowerShell
docker run --rm -v "${PWD}\k6:/scripts:ro" grafana/k6:1.8.0 run /scripts/swapi/smoke.js
docker run --rm -v "${PWD}\k6:/scripts:ro" grafana/k6:1.8.0 run /scripts/swapi/load.js
docker run --rm -v "${PWD}\k6:/scripts:ro" grafana/k6:1.8.0 run /scripts/swapi/fail_demo.js
```

Comandos ejecutados parado en `proyecto-integrador/performance/`.
