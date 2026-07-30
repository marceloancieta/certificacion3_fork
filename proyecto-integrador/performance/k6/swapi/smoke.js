import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Smoke de performance — pocos VUs, contra la API pública de SWAPI (Star Wars).
 * Checks = asserts por request. Thresholds = criterio de gate (exit code).
 * BASE_URL por defecto: https://swapi.info/api (API real vía internet, sin Docker).
 */
export const options = {
  vus: 2,
  duration: "15s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<1000"],
    checks: ["rate>0.99"],
  },
};

const BASE_URL = __ENV.BASE_URL || "https://swapi.info/api";

export default function () {
  const root = http.get(`${BASE_URL}`);
  check(root, {
    "root status 200": (r) => r.status === 200,
    "root lists films": (r) => String(r.body).includes("films"),
  });

  const film = http.get(`${BASE_URL}/films/1`);
  check(film, {
    "film status 200": (r) => r.status === 200,
    "film has episode_id": (r) => String(r.body).includes("episode_id"),
  });

  sleep(0.5);
}
