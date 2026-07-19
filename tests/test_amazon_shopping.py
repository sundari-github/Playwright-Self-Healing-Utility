"""
Amazon shopping end-to-end test using Playwright.

This test automates a complete shopping workflow on Amazon.in, including:
- Dismissing initial popups/modals
- Searching for products
- Applying filters (Get It Today, Price)
- Selecting products
- Adding items to cart
- Modifying cart (quantity, deletion)
- Returning to homepage

The test uses self-healing selectors via smart_click() (see BasePage) which
leverage AI to fix broken selectors when UI changes occur. Page interactions
are encapsulated in the pages/ Page Object Model classes.
"""

import logging
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger(__name__)


def test_run(setup) -> None:
    """
    Execute the complete Amazon shopping workflow test.

    This test simulates a user performing a full shopping journey:
    1. Closes any popups blocking access to main navigation
    2. Searches for "computer mouse"
    3. Applies filters to refine search results
    4. Selects a product and opens it in a new tab
    5. Changes quantity to 2 and adds to cart
    6. Views the cart
    7. Decreases quantity back to 1
    8. Deletes the item from cart
    9. Returns to home page

    Args:
        setup: Pytest fixture that provides a configured Playwright page object

    Returns:
        None
    """
    page = setup

    # === STEP 1: Handle initial popup/modal blocking navigation ===
    home_page = HomePage(page)
    home_page.dismiss_popup_if_present()

    # === STEP 2: Search for product ===
    home_page.search("computer mouse")
    search_results_page = SearchResultsPage(page)

    # === STEP 3: Apply filters to search results ===
    search_results_page.apply_get_it_today_filter()
    search_results_page.apply_price_filter()

    # === STEP 4: Select and open a product from search results ===
    # Opens in a new tab/popup; ProductPage wraps that new tab's page object
    product_page = search_results_page.open_first_product()

    # === STEP 5: Modify product quantity ===
    product_page.set_quantity(current_quantity=1, new_quantity=2)

    # === STEP 6: Add product to shopping cart ===
    product_page.add_to_cart()

    # === STEP 7: Navigate to shopping cart ===
    cart_page = product_page.go_to_cart()

    # === STEP 8: Modify cart - decrease quantity ===
    cart_page.decrease_quantity()

    # === STEP 9: Remove item from cart ===
    cart_page.delete_item()

    # === STEP 10: Return to home page ===
    cart_page.go_home()

    # Test complete - all assertions passed
