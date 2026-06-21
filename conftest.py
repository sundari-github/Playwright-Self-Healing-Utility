"""
Conftest module for Playwright automation testing configuration.

This module configures pytest fixtures for browser initialization and teardown,
including window maximization, viewport settings, and logging setup. It serves as
the central configuration hub for all test sessions.
"""

import pytest
import logging


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Configure browser launch arguments.
    
    Maximizes the browser window at startup instead of using a default viewport size.
    This ensures tests run in a maximized browser window for better UI interaction.
    
    Args:
        browser_type_launch_args: Default Playwright browser launch arguments
        
    Returns:
        dict: Updated launch arguments with --start-maximized flag
    """
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context arguments.
    
    Disables viewport constraints so Playwright doesn't force a 1280x720 window.
    This allows the test to work with the actual maximized window dimensions.
    
    Args:
        browser_context_args: Default Playwright browser context arguments
        
    Returns:
        dict: Updated context arguments with no_viewport set to True
    """


@pytest.fixture
def setup(page):
    """
    Setup fixture for each test.
    
    Initializes the browser to the Amazon India homepage and configures default
    timeouts. This fixture is executed once per test and yields the page object
    for test use.
    
    Args:
        page: Playwright page object (provided by pytest-playwright)
        
    Yields:
        page: Configured Playwright page object ready for testing
    """
    # Log the browser type being used for debugging
    browser_type = page.context.browser.browser_type.name.upper()
    print(f'\nBrowser Type: {browser_type}')
    
    # Navigate to Amazon India homepage
    page.goto("https://www.amazon.in/")
    
    # Set default timeout for all locator operations (10 seconds)
    page.set_default_timeout(10000)
    yield page


def pytest_configure(config):
    """
    Configure logging for the test session.
    
    Sets up logging to both file and console output. All log messages are written
    to 'automation_flow.log' file and displayed in the console with timestamp,
    logger name, level, and message.
    
    Args:
        config: Pytest configuration object
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler("automation_flow.log", mode="w"),
            logging.StreamHandler()
        ]
    )
