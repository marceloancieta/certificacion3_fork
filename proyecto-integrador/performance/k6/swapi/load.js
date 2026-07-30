import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Load moderno (k6 1.x): scenarios + ramping-vus + thresholds.
 * Misma "historia" que el smoke, contra la API pública SWAPI (Star Wars), con más VUs.
 * Si p95 / error rate / checks se rompen, K6 sale con código ≠ 0 (gate CI).
 */
export const options = {
  scenarios: {
    average_load: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 5 },
        { duration: "20s", target: 10 },
        { duration: "10s", target: 0 },
      ],
      gracefulRampDown: "10s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<1500"],
    checks: ["rate>0.99"],
  },
};

const BASE_URL = __ENV.BASE_URL || "https://swapi.info/api";

export default function () {
  const root = http.get(`${BASE_URL}`, {
    tags: { endpoint: "root" },
  });
  check(root, {
    "root status 200": (r) => r.status === 200,
    "root lists films": (r) => String(r.body).includes("films"),
  });

  const film = http.get(`${BASE_URL}/films/1`, {
    tags: { endpoint: "film_detail" },
  });
  check(film, {
    "film status 200": (r) => r.status === 200,
    "film has episode_id": (r) => String(r.body).includes("episode_id"),
  });

  // Think time: un usuario real no dispara requests en bucle sin pausa.
  sleep(0.3);
}
