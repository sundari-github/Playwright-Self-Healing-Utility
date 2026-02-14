import pytest
import logging


# 1. This tells the browser to start physically maximized
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
    }


# 2. This tells Playwright NOT to force a 1280x720 window inside that browser
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True
    }


@pytest.fixture
def setup(page):
    browser_type = page.context.browser.browser_type.name.upper()
    print(f'\nBrowser Type: {browser_type}')
    page.goto("https://www.amazon.in/")
    page.set_default_timeout(10000)
    yield page


def pytest_configure(config):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler("automation_flow.log", mode="w"),
            logging.StreamHandler()
        ]
    )
