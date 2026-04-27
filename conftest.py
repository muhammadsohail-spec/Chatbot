import random
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from config.config import URL, USERNAME, PASSWORD, NEW_PASSWORD, URLBeta, URLFSB, USERNAME_FSB, PASSWORD_FSB

from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="class")
def driver(request):
    chrome_options = Options()

    # Default to headless in CI/sandboxed environments unless overridden.
    run_headless = request.config.getoption("--headless")
    if run_headless:
        chrome_options.add_argument("--headless")

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


@pytest.fixture(scope="class")
def loginbeta(driver):
    driver.get(URLBeta)
    login_page = LoginPage(driver)
    # Enter login detail
    login_page.enter_email(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login()
    login_page.enter_otp("712312")
    login_page.wait_for_url_contains("chat")
    # assert "chat" in driver.current_url
    assert "chat" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"
    # replace credentials


@pytest.fixture(scope="class")
def loginevergreenbeta(driver):
    driver.get(URL)
    login_page = LoginPage(driver)
    # Enter login detail
    login_page.enter_email(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login()
    login_page.enter_otp("712312")
    login_page.wait_for_url_contains("chat")
    # assert "chat" in driver.current_url
    assert "chat" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"


@pytest.fixture(scope="class")
def loginfsbbeta(driver):
    driver.get(URLFSB)
    login_page = LoginPage(driver)
    # Enter login detail
    login_page.enter_email(USERNAME_FSB)
    login_page.enter_password(PASSWORD_FSB)
    login_page.click_login()
    login_page.wait_for_url_contains("chat")
    # assert "chat" in driver.current_url
    assert "chat" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"


import pytest
from utils.helpers import take_screenshot

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Check if test failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            take_screenshot(driver, name=item.name)