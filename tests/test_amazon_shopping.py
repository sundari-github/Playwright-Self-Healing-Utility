
from playwright.sync_api import expect
from tests.ui_element_action_wrapper import smart_click
import logging

logger = logging.getLogger(__name__)


def test_run(setup) -> None:

    page = setup

    # Getting past Continue button
    continue_btn = page.get_by_role("button", name="Continue shopping")
    search_btn = page.get_by_role("searchbox", name="Search Amazon.in")
    continue_btn.or_(search_btn).wait_for()
    if continue_btn.is_visible():
        expect(page.get_by_role("heading", name="Click the button below to")).to_be_visible()
        continue_btn.click()
        expect(page.get_by_role("navigation", name="Primary")).to_be_visible()

    # Home Page Navigation & Search
    search_btn.click()
    page.get_by_role("searchbox", name="Search Amazon.in").fill("computer mouse")
    page.get_by_role("button", name="Go", exact=True).click()
    expect(page.get_by_role("navigation", name="Primary")).to_be_visible()

    # Apply Filters
    # smart_click(page, ".broken-selector", "Get It Today")
    smart_click(page, 'role=link[name="Apply the filter Get It Today to narrow results"]', "Get It Today")
    # page.get_by_role("link", name="Apply the filter Get It Today").click()
    logger.info("Get It Today button successfully clicked")
    price_link = page.get_by_role("link", name="Up to ₹", exact=False)
    full_link_name = price_link.inner_text()
    logger.info(f"Interacting with price filter: '{full_link_name}'")
    price_link.click()
    # page.get_by_role("link", name="Up to ₹", exact=False).click()
    logger.info("Up to lowest price button successfully clicked")

    # Search Result Page
    with page.expect_popup() as page1_info:
        page.locator(".a-link-normal.s-no-outline").first.click()
    page1 = page1_info.value
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()

    # Select Quantity
    page1.get_by_text("Quantity:1").click()
    expect(page1.get_by_role("option", name="1", exact=True)).to_be_visible()
    page1.get_by_role("option", name="2", exact=True).click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("Quantity 2 chosen")

    # Add to Cart
    page1.get_by_role("button", name="Add to cart", exact=True).click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("Add to cart button clicked")

    # View Cart
    page1.locator("#sw-gtc").get_by_role("link", name="Go to Cart").click()
    expect(page1.get_by_role("navigation", name="Primary")).to_be_visible()
    logger.info("View cart button successfully clicked")

    # Decrease Quantity
    page1.get_by_role("button", name="Decrease quantity by one").click()
    expect(page1.get_by_role("group", name="Quantity is")).to_be_visible()
    logger.info("Quantity decreased by 1")

    # Delete Button Click
    page1.get_by_text("Delete").click()
    expect(page1.get_by_role("link", name="items in cart")).to_be_visible()
    logger.info("Delete button clicked")

    # Go back to home page
    page1.get_by_role("link", name="Amazon.in").click()
    logger.info("Back to home page")

    '''
    context.close()
    browser.close()
    
with sync_playwright() as playwright:
    run(playwright)
'''