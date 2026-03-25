import random
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="function")
def driver(request):
    chrome_options = Options()

    # Default to headless in CI/sandboxed environments unless overridden.
    run_headless = request.config.getoption("--headless")
    if run_headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    browser = webdriver.Chrome(options=chrome_options)
    if not run_headless:
        browser.maximize_window()

    yield browser

    browser.quit()


def generate_username(base="User"):
    """Generate a unique username."""
    return f"{base}_{random.randint(1000, 9999)}"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed and "driver" in item.funcargs:
        screenshot_dir = Path("failed_testcases_screenshoot")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        try:
            item.funcargs["driver"].save_screenshot(str(screenshot_dir / f"{item.name}.png"))
        except WebDriverException:
            # If the browser crashed or session already closed, avoid failing pytest internals.
            pass