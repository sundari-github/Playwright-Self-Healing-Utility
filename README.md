# Playwright Self-Healing Utility

## Project Description
This project provides a self-healing utility for Playwright-based UI automation tests. It aims to enhance the robustness of your automation suites by automatically adapting to minor UI changes, reducing test maintenance effort, and improving test reliability. The utility leverages AI principles to identify and locate elements even when their locators have slightly changed.

## Features
- **Self-Healing Locators**: Automatically attempts to find UI elements using alternative strategies if the primary locator fails.
- **Playwright Integration**: Seamlessly integrates with existing Playwright test suites.
- **Reduced Test Maintenance**: Minimizes the need for frequent test updates due to minor UI modifications.
- **Improved Reliability**: Makes your tests more resilient to changes in the application's UI.
- **AI-Powered Element Identification**: Uses intelligent algorithms to enhance element discovery.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Playwright-Self-Healing-Utility.git
    cd Playwright-Self-Healing-Utility
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    There is no `requirements.txt` in this repo yet, so install the packages directly:
    ```bash
    pip install pytest pytest-playwright ollama
    playwright install
    ```
    *Note: `ollama` is the Python client used by `tests/ai_utils.py` to call a locally running Ollama server for selector healing. You also need the [Ollama app](https://ollama.com) installed and the `qwen2.5-coder:7b` model pulled (`ollama pull qwen2.5-coder:7b`) for self-healing to work.*

## Usage

To use the self-healing utility in your Playwright tests, call the `smart_click()` function from `tests/ui_element_action_wrapper.py` in place of a plain `locator().click()`. It tries the given selector first and, if that times out, asks the local Ollama model to suggest a corrected selector from the surrounding HTML and retries with that.

### Example (tests/test_amazon_shopping.py):

```python
from tests.ui_element_action_wrapper import smart_click

def test_amazon_search(page):
    page.goto("https://www.amazon.in/")
    smart_click(page, 'role=link[name="Apply the filter Get It Today to narrow results"]', "Get It Today")
    # Falls back to an AI-healed selector automatically if the one above stops matching
```

Run the suite with:
```bash
pytest
```

### Page Object Model (`pages/`)

UI interactions are organized as page objects rather than being written inline in the tests. `pages/base_page.py` defines a `BasePage` with the shared `smart_click()` helper and a `expect_primary_nav_visible()` check used across pages; the other classes subclass it and represent one screen each. Methods that navigate return the next page object, so a test reads as a chain, e.g. `home_page.search(...)` → `SearchResultsPage` → `open_first_product()` → `ProductPage` → `go_to_cart()` → `CartPage`.

## Project Structure

```
.gitignore
conftest.py
pages/
    __init__.py
    base_page.py
    home_page.py
    search_results_page.py
    product_page.py
    cart_page.py
tests/
    __init__.py
    ai_utils.py
    test_amazon_shopping.py
    ui_element_action_wrapper.py
```

-   `conftest.py`: pytest configuration and fixtures (browser launch/context args, `setup` fixture, logging).
-   `pages/base_page.py`: Shared base class for all page objects (`smart_click` helper, nav-visibility check).
-   `pages/home_page.py`: Homepage — popup dismissal, search.
-   `pages/search_results_page.py`: Search results — filters, opening a product.
-   `pages/product_page.py`: Product detail page — quantity, add to cart, go to cart.
-   `pages/cart_page.py`: Cart page — quantity adjustment, delete item, return home.
-   `tests/ai_utils.py`: Contains AI-related logic (Ollama calls) for self-healing.
-   `tests/ui_element_action_wrapper.py`: Wraps Playwright clicks with self-healing capabilities (`smart_click`).
-   `tests/test_amazon_shopping.py`: End-to-end Amazon.in shopping test built on the `pages/` POM classes.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.