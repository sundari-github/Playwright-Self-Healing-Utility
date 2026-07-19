"""
Search Results Page Object for Amazon.in.

Encapsulates filter application (Get It Today, price) and selecting a
product from the results grid, which opens the product in a new tab.
"""

import logging
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)


class SearchResultsPage(BasePage):
    """Represents the Amazon.in search results listing page."""

    def apply_get_it_today_filter(self):
        """Apply the "Get It Today" delivery filter using the self-healing click wrapper."""
        self.smart_click(
            'role=link[name="Apply the filter Get It Today to narrow results"]',
            "Get It Today",
        )
        logger.info("Get It Today button successfully clicked")

    def apply_price_filter(self):
        """Apply the lowest "Up to <price>" filter link found in the price facet."""
        price_link = self.page.get_by_role("link", name="Up to ₹", exact=False)
        full_link_name = price_link.inner_text()
        logger.info(f"Interacting with price filter: '{full_link_name}'")
        price_link.click()
        logger.info("Up to lowest price button successfully clicked")

    def open_first_product(self):
        """
        Click the first product in the results grid, which opens in a new tab.

        Returns:
            ProductPage: Page object for the newly opened product detail tab.
        """
        with self.page.expect_popup() as popup_info:
            self.page.locator(".a-link-normal.s-no-outline").first.click()
        product_page = popup_info.value
        expect(product_page.get_by_role("navigation", name="Primary")).to_be_visible()
        return ProductPage(product_page)
