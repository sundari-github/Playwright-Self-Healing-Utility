from tests.ai_utils import get_healed_selector
from playwright.sync_api import TimeoutError
import logging


logger = logging.getLogger(__name__)


def smart_click(page, selector, desc):
    try:
        logger.info(f"Attempting click on: {desc} (Selector: {selector})")
        page.locator(selector).click(timeout=3000)
        return True
    except TimeoutError as e:
        try:
            anchor_element = page.get_by_text(desc, exact=False).first
            logger.info(f"anchor_element\n{anchor_element}")
            focused_html = anchor_element.evaluate("el => el.parentElement.outerHTML")
        except:
            logger.warning(f"Could not find element by text: {desc}. Falling back to page content.")
            focused_html = page.content()[:20000]

        logger.info(f"HTML sent to the model {focused_html}")
        logger.warning(f"TIMEOUT: {desc} failed. Starting self-healing...")
        new_selector = get_healed_selector(selector, focused_html, desc)
        logger.info(f"RETRYING: Clicking {desc} with healed selector: {new_selector}")
        try:
            healed_locator = page.locator(new_selector).first
            logger.info(f"Healed location 1 {healed_locator}")
            tag = healed_locator.evaluate("el => el.tagName.toLowerCase()")
            logger.info(f"Tag {tag}")
            if tag not in ["a", "button", "input", "label"]:
                healed_locator = healed_locator.locator(
                    "xpath=ancestor::*[self::a or self::button or self::input or self::label or @role='button'][1]"
                )
            logger.info(f"Healed location 2 {healed_locator}")
            healed_locator.click(timeout=3000)
            return True
        except Exception as ex2:
            logger.error(f"RETRY FAILED: {desc} with healed selector: {new_selector}")
            return False
