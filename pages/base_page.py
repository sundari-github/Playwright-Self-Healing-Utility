"""
Base Page Object for Amazon shopping automation.

Provides behavior shared by every page object in the flow: access to the
underlying Playwright page, the self-healing click wrapper, and the
"Primary" navigation visibility check that repeats after most actions.
"""

from playwright.sync_api import expect
from tests.ui_element_action_wrapper import smart_click


class BasePage:
    """Base class that all page objects inherit from."""

    def __init__(self, page):
        """
        Args:
            page: Playwright page object this page object operates on.
        """
        self.page = page

    def smart_click(self, selector, desc):
        """Click an element via the self-healing wrapper (see ui_element_action_wrapper)."""
        return smart_click(self.page, selector, desc)

    def expect_primary_nav_visible(self):
        """Assert the primary navigation bar is visible (used as a post-action stability check)."""
        expect(self.page.get_by_role("navigation", name="Primary")).to_be_visible()
