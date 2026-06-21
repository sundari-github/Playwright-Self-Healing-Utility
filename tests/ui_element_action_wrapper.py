"""
UI element action wrapper with self-healing capabilities.

This module provides smart interaction methods that handle stale/broken selectors
automatically. When a selector times out, it uses AI (via ai_utils) to generate
a corrected selector based on the element's description and HTML context.

Primary functionality:
- smart_click(): Clicks elements with fallback to AI-generated selectors
- Automatic element ancestor traversal to find clickable elements
- Comprehensive logging for debugging selector healing
"""

from tests.ai_utils import get_healed_selector
from playwright.sync_api import TimeoutError
import logging


logger = logging.getLogger(__name__)


def smart_click(page, selector, desc):
    """
    Click an element with self-healing capability when selector fails.
    
    Attempts to click an element using the provided selector. If the selector
    times out (3 second timeout), triggers AI-powered selector healing:
    1. Extracts HTML context around the target element
    2. Sends context to AI model to generate corrected selector
    3. Attempts click with the healed selector
    4. Handles non-clickable elements by traversing to parent clickable element
    
    Args:
        page (Page): Playwright page object to perform clicks on
        selector (str): CSS/Playwright selector for the element to click
        desc (str): Human-readable description of the element (used for AI context)
        
    Returns:
        bool: True if click succeeded (either original or healed selector),
              False if both initial attempt and healing retry failed
              
    Process flow:
        1. Try original selector (3 second timeout)
        2. If timeout:
           a. Extract HTML snippet containing the element
           b. Call AI to generate new selector
           c. Retry with healed selector
           d. If healed element is not clickable, find clickable parent
        3. Return success/failure status
    """
    try:
        # Attempt initial click with original selector
        logger.info(f"Attempting click on: {desc} (Selector: {selector})")
        page.locator(selector).click(timeout=3000)
        return True
        
    except TimeoutError as e:
        # Original selector failed - prepare for selector healing
        try:
            # Try to find element by text description and extract its HTML
            anchor_element = page.get_by_text(desc, exact=False).first
            logger.info(f"anchor_element\n{anchor_element}")
            focused_html = anchor_element.evaluate("el => el.parentElement.outerHTML")
        except:
            # If text-based lookup fails, use full page content as context
            logger.warning(f"Could not find element by text: {desc}. Falling back to page content.")
            focused_html = page.content()[:20000]

        # Log HTML being sent to AI model and start healing process
        logger.info(f"HTML sent to the model {focused_html}")
        logger.warning(f"TIMEOUT: {desc} failed. Starting self-healing...")
        
        # Generate new selector using AI
        new_selector = get_healed_selector(selector, focused_html, desc)
        logger.info(f"RETRYING: Clicking {desc} with healed selector: {new_selector}")
        
        try:
            # Attempt to use the healed selector
            healed_locator = page.locator(new_selector).first
            logger.info(f"Healed location 1 {healed_locator}")
            
            # Check the HTML tag of the found element
            tag = healed_locator.evaluate("el => el.tagName.toLowerCase()")
            logger.info(f"Tag {tag}")
            
            # If element is not directly clickable, find clickable parent
            # (e.g., if healed selector points to span inside button, traverse to button)
            if tag not in ["a", "button", "input", "label"]:
                healed_locator = healed_locator.locator(
                    "xpath=ancestor::*[self::a or self::button or self::input or self::label or @role='button'][1]"
                )
            logger.info(f"Healed location 2 {healed_locator}")
            
            # Click the healed/adjusted element
            healed_locator.click(timeout=3000)
            return True
            
        except Exception as ex2:
            # Even with healed selector, click failed
            logger.error(f"RETRY FAILED: {desc} with healed selector: {new_selector}")
            return False
