"""Tests del flujo de checkout usando el patrón Screenplay.

Qué demuestra este archivo
--------------------------
1. Composición de Tasks: Login + AddToCart + CompleteCheckout en una
   sola secuencia legible de attempts_to().
2. Reutilización: CompleteCheckout orquesta los Page Objects existentes
   (CartPage, CheckoutPage) sin duplicar locators.
"""

from screenplay.actor import Actor
from screenplay.abilities.browse_web import BrowseTheWeb
from screenplay.tasks.login import Login
from screenplay.tasks.add_to_cart import AddToCart
from screenplay.tasks.complete_checkout import CompleteCheckout
from pages.checkout_page import CheckoutPage


def test_actor_completa_el_checkout(page):
    """Un Actor puede completar los datos de envío y llegar al resumen."""
    maria = Actor("María").can(BrowseTheWeb.using(page))

    maria.attempts_to(
        Login.as_user("standard_user", "secret_sauce"),
        AddToCart.the_item("Sauce Labs Backpack"),
        CompleteCheckout.with_info("María", "Quispe", "15001"),
    )

    assert "checkout-step-two" in page.url, (
        "María debería estar en el resumen de la orden tras el checkout."
    )


def test_actor_no_avanza_sin_datos_de_envio(page):
    """Sin datos de envío, el checkout muestra un error y no avanza."""
    pedro = Actor("Pedro").can(BrowseTheWeb.using(page))

    pedro.attempts_to(
        Login.as_user("standard_user", "secret_sauce"),
        AddToCart.the_item("Sauce Labs Bike Light"),
        CompleteCheckout.with_info("", "", ""),
    )

    assert CheckoutPage(page).has_error(), (
        "Pedro debería ver un error al continuar sin datos de envío."
    )
