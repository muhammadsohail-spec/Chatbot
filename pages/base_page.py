"""
pages/base_page.py
==================
Foundation class for all Page Object Models.

All page classes inherit from ``BasePage``, which wraps common Selenium
patterns (waiting, clicking, text input) into a single, reusable layer.
This avoids duplicating ``WebDriverWait`` calls throughout the codebase.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from utils.logger import get_logger

logger = get_logger("BasePage")

# Default explicit wait timeout (seconds).
DEFAULT_TIMEOUT = 10


class BasePage:
    """
    Provides reusable Selenium helper methods for all Page Object classes.

    Args:
        driver:  Active Selenium WebDriver instance.
        timeout: Default explicit wait duration in seconds.
    """

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Interaction helpers
    # ------------------------------------------------------------------

    def click(self, locator: tuple) -> None:
        """
        Click the element identified by ``locator``.

        Falls back to a JavaScript click if the element is intercepted
        by an overlay (e.g. modal, cookie banner).

        Args:
            locator: Selenium (By, value) locator tuple.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator: tuple, text: str) -> None:
        """
        Clear the field identified by ``locator`` and type ``text``.

        Args:
            locator: Selenium (By, value) locator tuple.
            text:    String to be typed into the element.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """
        Return the visible text of the element identified by ``locator``.

        Args:
            locator: Selenium (By, value) locator tuple.

        Returns:
            Visible text string of the matched element.
        """
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    # ------------------------------------------------------------------
    # Wait helpers
    # ------------------------------------------------------------------

    def wait_for_visibility(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Wait until the element is visible and return it.

        Args:
            locator: Selenium (By, value) locator tuple.
            timeout: Override the default wait timeout.

        Returns:
            The visible ``WebElement``.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_invisibility(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """
        Wait until the element is no longer visible.

        Args:
            locator: Selenium (By, value) locator tuple.
            timeout: Override the default wait timeout.

        Returns:
            ``True`` once the element is invisible.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, keyword: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Block until the current URL contains ``keyword``.

        Args:
            keyword: Substring to look for in ``driver.current_url``.
            timeout: Override the default wait timeout.
        """
        WebDriverWait(self.driver, timeout).until(EC.url_contains(keyword))