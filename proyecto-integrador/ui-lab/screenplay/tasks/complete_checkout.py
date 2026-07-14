"""Task: CompleteCheckout — completa el paso 1 del checkout de SauceDemo.

Orquesta el flujo completo desde la perspectiva del Actor:
navega al carrito, inicia el checkout, rellena los datos de envío
y continúa al resumen. Reutiliza los Page Objects existentes,
igual que las demás Tasks del laboratorio.
"""

from __future__ import annotations
from screenplay.abilities.browse_web import BrowseTheWeb
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class CompleteCheckout:
    """Tarea de alto nivel: completar los datos de envío del checkout."""

    def __init__(self, first: str, last: str, zip_code: str) -> None:
        self._first = first
        self._last = last
        self._zip_code = zip_code

    @classmethod
    def with_info(cls, first: str, last: str, zip_code: str) -> "CompleteCheckout":
        """Constructor expresivo: CompleteCheckout.with_info('Ana', 'Pérez', '15001')."""
        return cls(first, last, zip_code)

    def perform_as(self, actor) -> None:
        """Ejecuta la tarea usando las Abilities del Actor.

        1. Navega al carrito.
        2. Hace clic en Checkout.
        3. Rellena los datos de envío.
        4. Hace clic en continuar.
        """
        page = actor.ability_to(BrowseTheWeb).page
        page.goto(CartPage.URL)
        CartPage(page).proceed_to_checkout()
        CheckoutPage(page).fill_shipping(
            self._first, self._last, self._zip_code
        ).continue_to_overview()
