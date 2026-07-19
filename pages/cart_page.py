"""
Cart Page Object for Amazon.in.

Encapsulates cart modification actions: decreasing item quantity, deleting
an item and returning to the homepage.
"""

import logging
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.home_page import HomePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Represents the Amazon.in shopping cart page."""

    def decrease_quantity(self):
        """Click the "Decrease quantity by one" stepper button."""
        self.page.get_by_role("button", name="Decrease quantity by one").click()
        expect(self.page.get_by_role("group", name="Quantity is")).to_be_visible()
        logger.info("Quantity decreased by 1")

    def delete_item(self):
        """Delete the item from the cart."""
        self.page.get_by_text("Delete").click()
        expect(self.page.get_by_role("link", name="items in cart")).to_be_visible()
        logger.info("Delete button clicked")

    def go_home(self):
        """
        Return to the Amazon.in homepage via the logo link.

        Returns:
            HomePage: Page object for the homepage.
        """
        self.page.get_by_role("link", name="Amazon.in").click()
        logger.info("Back to home page")
        return HomePage(self.page)
