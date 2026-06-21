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
    ```bash
    pip install -r requirements.txt
    # (You might need to create a requirements.txt file with playwright and any other dependencies)
    ```
    *Note: If `requirements.txt` does not exist, you will need to install Playwright and other necessary packages manually.*
    ```bash
    pip install playwright
    playwright install
    ```

## Usage

To use the self-healing utility in your Playwright tests, you will typically import the `UIElementActionWrapper` and use its methods to interact with UI elements.

### Example (tests/test_amazon_shopping.py):

```python
# ...existing code...
from tests.ui_element_action_wrapper import UIElementActionWrapper

def test_amazon_search(page):
    wrapper = UIElementActionWrapper(page)
    wrapper.goto("https://www.amazon.com")
    wrapper.fill("#twotabsearchtextbox", "Playwright book")
    wrapper.press("#twotabsearchtextbox", "Enter")
    # Further assertions or actions using the wrapper
# ...existing code...
```

## Project Structure

```
.gitignore
conftest.py
tests/
    __init__.py
    ai_utils.py
    test_amazon_shopping.py
    ui_element_action_wrapper.py
```

-   `conftest.py`: pytest configuration and fixtures.
-   `tests/ai_utils.py`: Contains AI-related logic for self-healing.
-   `tests/ui_element_action_wrapper.py`: Wraps Playwright actions with self-healing capabilities.
-   `tests/test_amazon_shopping.py`: Example Playwright test demonstrating the utility.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.