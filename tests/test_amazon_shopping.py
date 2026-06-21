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

The test uses self-healing selectors via smart_click() which leverage AI
to fix broken selectors when UI changes occur.
"""

from playwright.sync_api import expect
from tests.ui_element_action_wrapper import smart_click
import logging

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
    continue_btn = page.get_by_role("button", name="Continue shopping")
    search_btn = page.get_by_role("searchbox", name="Search Amazon.in")
    continue_btn.or_(search_btn).wait_for()
    if continue_btn.is_visible():
        expect(page.get_by_role("heading", name="Click the button below to")).to_be_visible()
        continue_btn.click()
        expect(page.get_by_role("navigation", name="Primary")).to_be_visible()

    # Click search box and enter search query
    search_btn.click()
    page.get_by_role("searchbox", name="Search Amazon.in").fill("computer mouse")
    page.get_by_role("button", name="Go", exact=True).click()
    expect(page.get_by_role("navigation", name="Primary")).to_be_visible()

    # === STEP 2: Search for product ===
    # (Search implementation moved above)

    # === STEP 3: Apply filters to search results ===
    # Apply "Get It Today" filter using self-healing selector
    smart_click(page, 'role=link[name="Apply the filter Get It Today to narrow results"]', "Get It Today")
    logger.info("Get It Today button successfully clicked")
    price_link = page.get_by_role("link", name="Up to ₹", exact=False)
    full_link_name = price_link.inner_text()
    logger.info(f"Interacting with price filter: '{full_link_name}'")
    price_link.click()
    logger.info("Up to lowest price button successfully clicked")

    # === STEP 4: Select and open a product from search results ===
    # Click first product in search results (opens in new tab/popup)
    with page.expect_popup() as page1_info:
        page.locator(".a-link-normal.s-no-outline").first.click()
    page1 = page1_info.value
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()

    # === STEP 5: Modify product quantity ===
    # Click quantity dropdown and change from 1 to 2
    page1.get_by_text("Quantity:1").click()
    expect(page1.get_by_role("option", name="1", exact=True)).to_be_visible()
    page1.get_by_role("option", name="2", exact=True).click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("Quantity 2 chosen")

    # === STEP 6: Add product to shopping cart ===
    # Click Add to cart button
    page1.get_by_role("button", name="Add to cart", exact=True).click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("Add to cart button clicked")

    # === STEP 7: Navigate to shopping cart ===
    # Click "Go to Cart" button
    page1.locator("#sw-gtc").get_by_role("link", name="Go to Cart").click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("View cart button successfully clicked")

    # === STEP 8: Modify cart - decrease quantity ===
    # Click button to decrease quantity from 2 to 1
    page1.get_by_role("button", name="Decrease quantity by one").click()
    expect(page1.get_by_role("group", name="Quantity is")).to_be_visible()
    logger.info("Quantity decreased by 1")

    # === STEP 9: Remove item from cart ===
    # Click Delete button to remove item from cart
    page1.get_by_text("Delete").click()
    expect(page1.get_by_role("link", name="items in cart")).to_be_visible()
    logger.info("Delete button clicked")

    # === STEP 10: Return to home page ===
    # Click Amazon.in logo to return to home page
    page1.get_by_role("link", name="Amazon.in").click()
    logger.info("Back to home page")
    
    # Test complete - all assertions passed