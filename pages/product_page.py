"""
Product Page Object for Amazon.in.

Encapsulates actions on a product detail page (opened in its own tab):
changing quantity, adding to cart and navigating to the cart.
"""

import logging
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Represents an Amazon.in product detail page."""

    def set_quantity(self, current_quantity, new_quantity):
        """
        Change the product quantity via the quantity dropdown.

        Args:
            current_quantity (int): Quantity shown before opening the dropdown; used
                to confirm the dropdown opened with the expected current selection.
            new_quantity (int): Desired new quantity to select.
        """
        self.page.get_by_text(f"Quantity:{current_quantity}").click()
        expect(self.page.get_by_role("option", name=str(current_quantity), exact=True)).to_be_visible()
        self.page.get_by_role("option", name=str(new_quantity), exact=True).click()
        self.expect_primary_nav_visible()
        logger.info(f"Quantity {new_quantity} chosen")

    def add_to_cart(self):
        """Click the "Add to cart" button."""
        self.page.get_by_role("button", name="Add to cart", exact=True).click()
        self.expect_primary_nav_visible()
        logger.info("Add to cart button clicked")

    def go_to_cart(self):
        """
        Navigate to the cart via the "Go to Cart" confirmation link.

        Returns:
            CartPage: Page object for the shopping cart.
        """
        self.page.locator("#sw-gtc").get_by_role("link", name="Go to Cart").click()
        self.expect_primary_nav_visible()
        logger.info("View cart button successfully clicked")
        return CartPage(self.page)
