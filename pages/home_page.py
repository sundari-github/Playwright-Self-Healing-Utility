"""
Home Page Object for Amazon.in.

Encapsulates the landing page behavior: dismissing the initial interstitial
(if present) and performing a search.
"""

from playwright.sync_api import expect
from pages.base_page import BasePage


class HomePage(BasePage):
    """Represents the Amazon.in homepage / landing state."""

    def dismiss_popup_if_present(self):
        """
        Dismiss the "Continue shopping" interstitial if Amazon shows it.

        Amazon.in intermittently shows a bot-check style interstitial before
        the real homepage loads. This waits for either that interstitial's
        button or the real search box, and only clicks through if the
        interstitial actually appeared.
        """
        continue_btn = self.page.get_by_role("button", name="Continue shopping")
        search_btn = self.page.get_by_role("searchbox", name="Search Amazon.in")
        continue_btn.or_(search_btn).wait_for()

        if continue_btn.is_visible():
            expect(self.page.get_by_role("heading", name="Click the button below to")).to_be_visible()
            continue_btn.click()
            self.expect_primary_nav_visible()

    def search(self, query):
        """
        Search for a product from the homepage.

        Args:
            query (str): Search term to enter into the Amazon search box.
        """
        search_btn = self.page.get_by_role("searchbox", name="Search Amazon.in")
        search_btn.click()
        search_btn.fill(query)
        self.page.get_by_role("button", name="Go", exact=True).click()
        self.expect_primary_nav_visible()
