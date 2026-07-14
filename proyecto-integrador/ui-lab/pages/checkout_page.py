"""Page Object de la pantalla de checkout (paso 1) de SauceDemo.

Cubre el formulario de datos de envío que aparece tras hacer clic en
'Checkout' desde el carrito. Igual que el resto de Page Objects del
laboratorio, usa los atributos `data-test` por ser los más estables.
"""

from __future__ import annotations
from playwright.sync_api import Page


class CheckoutPage:
    """Representa https://www.saucedemo.com/checkout-step-one.html."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._first_name   = page.locator('[data-test="firstName"]')
        self._last_name    = page.locator('[data-test="lastName"]')
        self._postal_code  = page.locator('[data-test="postalCode"]')
        self._continue_btn = page.locator('[data-test="continue"]')
        self._error_msg    = page.locator('[data-test="error"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def fill_shipping(self, first: str, last: str, zip_code: str) -> "CheckoutPage":
        """Rellena los tres campos de envío y devuelve self (interfaz fluida)."""
        self._first_name.fill(first)
        self._last_name.fill(last)
        self._postal_code.fill(zip_code)
        return self

    def continue_to_overview(self) -> "CheckoutPage":
        """Hace clic en 'Continue' para avanzar al resumen de la orden."""
        self._continue_btn.click()
        return self

    # ── Consultas ─────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        """True si la URL actual es la del paso 1 del checkout."""
        return self.page.url == self.URL

    def has_error(self) -> bool:
        """True si hay un mensaje de error visible en el formulario."""
        return self._error_msg.is_visible()

    def error_message(self) -> str:
        """Texto del mensaje de error visible tras una validación fallida."""
        return self._error_msg.inner_text()
