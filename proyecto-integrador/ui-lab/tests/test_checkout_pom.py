"""Tests del flujo de checkout usando el patrón Page Object Model (POM).

Qué demuestra este archivo
--------------------------
1. Composición de Page Objects: Inventory → Cart → Checkout en un solo flujo.
2. Validación negativa: el formulario exige los datos de envío.
3. Caso feliz: con datos válidos se avanza al resumen de la orden.
"""

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_checkout_sin_nombre_muestra_error(authenticated_page):
    """Enviar el formulario de envío vacío debe mostrar un error de validación."""
    InventoryPage(authenticated_page).add_to_cart("Sauce Labs Backpack").go_to_cart()
    CartPage(authenticated_page).proceed_to_checkout()
    checkout = CheckoutPage(authenticated_page)
    checkout.fill_shipping("", "", "").continue_to_overview()
    assert checkout.has_error(), "Se esperaba un error al enviar el formulario vacío."


def test_checkout_con_datos_validos_avanza_al_resumen(authenticated_page):
    """Con datos de envío completos se debe llegar al paso 2 (overview)."""
    InventoryPage(authenticated_page).add_to_cart("Sauce Labs Backpack").go_to_cart()
    CartPage(authenticated_page).proceed_to_checkout()

    checkout = CheckoutPage(authenticated_page)
    assert checkout.is_loaded(), "Se esperaba estar en el paso 1 del checkout."

    checkout.fill_shipping("Ana", "Pérez", "15001").continue_to_overview()

    assert "checkout-step-two" in authenticated_page.url, (
        "Se esperaba avanzar al resumen de la orden (checkout-step-two)."
    )
    assert not checkout.has_error(), "No debería haber errores con datos válidos."
