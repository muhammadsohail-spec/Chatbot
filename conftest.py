"""
conftest.py
===========
Pytest configuration and shared fixtures for the entire test suite.

Fixtures:
    driver           – class-scoped Chrome WebDriver instance.
    loginbeta        – pre-authenticated session against URLBeta.
    loginevergreenbeta – pre-authenticated session against URL (Evergreen Beta).
    loginfsbbeta     – pre-authenticated session against URLFSB.
    logindsldbeta    – pre-authenticated session against URLDSLD.

Hooks:
    pytest_addoption         – Adds ``--headless`` CLI flag.
    pytest_runtest_makereport – On failure: saves screenshot locally
                                and attaches it to the Allure report.
"""

from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from config.config import (
    URL,
    USERNAME,
    PASSWORD,
    URLBeta,
    URLFSB,
    USERNAME_FSB,
    PASSWORD_FSB,
    URLDSLD,
    USERNAME_DSLD,
    PASSWORD_DSLD,
)
from pages.login_page import LoginPage
from utils.helpers import take_screenshot
from utils.logger import get_logger

logger = get_logger("Conftest")

# Directory where failure screenshots are persisted locally.
SCREENSHOT_DIR = Path("failed_testcases_screenshoot")


# ---------------------------------------------------------------------------
# CLI options
# ---------------------------------------------------------------------------

def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the ``--headless`` command-line flag."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run the browser in headless mode (useful for CI/CD environments).",
    )


# ---------------------------------------------------------------------------
# WebDriver fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="class")
def driver(request: pytest.FixtureRequest):
    """
    Provide a class-scoped Chrome WebDriver instance.

    The browser is launched once per test class, shared across all tests
    in that class, and closed after the last test completes.

    CLI flags:
        --headless  Run Chrome without a visible window.

    Yields:
        selenium.webdriver.Chrome: Active browser session.
    """
    options = Options()
    run_headless: bool = request.config.getoption("--headless")

    if run_headless:
        options.add_argument("--headless=new")  # modern headless flag

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    browser = webdriver.Chrome(options=options)
    if not run_headless:
        browser.maximize_window()

    logger.info("Chrome WebDriver started (headless=%s).", run_headless)
    yield browser

    browser.quit()
    logger.info("Chrome WebDriver closed.")


# ---------------------------------------------------------------------------
# Login helper — shared by all environment fixtures
# ---------------------------------------------------------------------------

def _login(driver, url: str, username: str, password: str, use_otp: bool = False, otp: str = "") -> None:
    """
    Navigate to ``url``, log in with the supplied credentials, and assert
    that the browser lands on the chat page.

    Args:
        driver:   Active Selenium WebDriver.
        url:      Full URL to navigate to before logging in.
        username: Email / username to enter.
        password: Password to enter.
        use_otp:  Whether to complete OTP verification after login.
        otp:      OTP string to submit (required when ``use_otp=True``).

    Raises:
        AssertionError: If the browser is not on the chat page after login.
    """
    driver.get(url)
    login_page = LoginPage(driver)
    login_page.enter_email(username)
    login_page.enter_password(password)
    login_page.click_login()

    if use_otp:
        login_page.enter_otp(otp)

    login_page.wait_for_url_contains("chat")
    assert "chat" in driver.current_url, (
        f"Login fixture failed — expected 'chat' in URL, got: {driver.current_url}"
    )
    logger.info("Login fixture: authenticated at %s", driver.current_url)


# ---------------------------------------------------------------------------
# Environment-specific login fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="class")
def loginbeta(driver) -> None:
    """Pre-authenticate against the Beta environment (URLBeta)."""
    _login(driver, URLBeta, USERNAME, PASSWORD, use_otp=True, otp="712312")


@pytest.fixture(scope="class")
def loginevergreenbeta(driver) -> None:
    """Pre-authenticate against the Evergreen Beta environment (URL)."""
    _login(driver, URL, USERNAME, PASSWORD, use_otp=True, otp="712312")


@pytest.fixture(scope="class")
def loginfsbbeta(driver) -> None:
    """Pre-authenticate against the FSB Beta environment (URLFSB)."""
    _login(driver, URLFSB, USERNAME_FSB, PASSWORD_FSB)


@pytest.fixture(scope="class")
def logindsldbeta(driver) -> None:
    """Pre-authenticate against the DSLD Beta environment (URLDSLD)."""
    _login(driver, URLDSLD, USERNAME_DSLD, PASSWORD_DSLD)


# ---------------------------------------------------------------------------
# Failure screenshot hook
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call) -> None:
    """
    After each test call phase, if the test **failed**:
        1. Save a PNG screenshot to the local ``failed_testcases_screenshoot/`` folder.
        2. Attach the screenshot to the Allure report.

    Both steps are wrapped in individual try/except blocks so that a
    screenshot failure does not mask the original test failure.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    active_driver = item.funcargs.get("driver")
    if not active_driver:
        return

    # 1. Persist screenshot locally
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    local_path = SCREENSHOT_DIR / f"{item.name}.png"
    try:
        active_driver.save_screenshot(str(local_path))
        logger.info("Failure screenshot saved: %s", local_path)
    except WebDriverException as exc:
        logger.warning("Could not save failure screenshot locally: %s", exc)

    # 2. Attach to Allure
    try:
        take_screenshot(active_driver, name=item.name)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not attach screenshot to Allure: %s", exc)