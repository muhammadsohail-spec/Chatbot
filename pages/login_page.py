"""
pages/login_page.py
===================
Page Object Model for the Login / Authentication screens.

Responsibilities:
    - Locate all interactive elements on the Login, OTP, and
      Forgot Password screens.
    - Expose a clean, intent-revealing API to test methods.
    - Centralise exception handling through the ``_safe_action`` helper
      so individual methods stay concise and easy to read.
"""

from typing import Callable

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage(BasePage):
    """
    Encapsulates all UI interactions for Login, OTP verification,
    Logout, and Forgot Password flows.
    """

    # ------------------------------------------------------------------
    # Locators — kept as class-level constants so they are easy to update
    # when the application UI changes.
    # ------------------------------------------------------------------

    # Login form
    EMAIL_INPUT    = (By.ID,    "email")
    PASSWORD_INPUT = (By.ID,    "password")
    LOGIN_BTN      = (By.XPATH, "//button[normalize-space()='Login']")

    # OTP screen
    OTP_INPUT  = (By.ID,    "otp")
    VERIFY_BTN = (By.XPATH, "//button[contains(text(),'Verify OTP')]")

    # Forgot password flow
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    SEND_OTP_BTN         = (By.XPATH,     "//button[@type='submit']")
    NEW_PASSWORD_INPUT   = (By.ID,        "new-password")
    RESET_BTN            = (By.XPATH,     "//button[normalize-space()='Reset Password']")

    # Authenticated state
    PROFILE_AVATAR = (By.XPATH, "//span[@class='bg-muted flex size-full items-center justify-center rounded-full']")
    LOGOUT_OPTION  = (By.XPATH, "//div[normalize-space()='Logout']")

    # Validation
    ERROR_MESSAGE = (By.XPATH, "//*[@data-slot='alert-description']")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _safe_action(self, action: Callable, error_msg: str) -> None:
        """
        Execute ``action`` and convert Selenium timeout / not-found errors
        into a logged error followed by a re-raise.

        This helper eliminates the 12 identical try/except blocks that
        previously existed in every public method.

        Args:
            action:    Zero-argument callable wrapping the Selenium call.
            error_msg: Human-readable prefix for the log message on failure.

        Raises:
            TimeoutException | NoSuchElementException: Propagated after logging.
        """
        try:
            action()
        except (TimeoutException, NoSuchElementException) as exc:
            logger.error("%s: %s", error_msg, exc)
            raise

    # ------------------------------------------------------------------
    # Login form interactions
    # ------------------------------------------------------------------

    def enter_email(self, email: str) -> None:
        """Type ``email`` into the email input field."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.EMAIL_INPUT),
                     self.enter_text(self.EMAIL_INPUT, email)),
            "Email field not found or not interactable",
        )

    def enter_password(self, password: str) -> None:
        """Type ``password`` into the password input field."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.PASSWORD_INPUT),
                     self.enter_text(self.PASSWORD_INPUT, password)),
            "Password field not found or not interactable",
        )

    def click_login(self) -> None:
        """Click the Login submit button."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.LOGIN_BTN),
                     self.click(self.LOGIN_BTN)),
            "Login button not clickable",
        )

    def is_login_button_enabled(self) -> bool:
        """
        Return ``True`` if the Login button is present and enabled,
        ``False`` if it is disabled or not found.
        """
        try:
            btn = self.wait_for_visibility(self.LOGIN_BTN)
            return btn.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    # ------------------------------------------------------------------
    # OTP screen interactions
    # ------------------------------------------------------------------

    def enter_otp(self, otp: str) -> None:
        """Type the one-time password into the OTP input field."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.OTP_INPUT),
                     self.enter_text(self.OTP_INPUT, otp)),
            "OTP field not found or not interactable",
        )

    def click_verify(self) -> None:
        """Click the 'Verify OTP' button."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.VERIFY_BTN),
                     self.click(self.VERIFY_BTN)),
            "Verify OTP button not clickable",
        )

    # ------------------------------------------------------------------
    # Logout interactions
    # ------------------------------------------------------------------

    def click_profile(self) -> None:
        """Click the profile / avatar button to open the user menu."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.PROFILE_AVATAR),
                     self.click(self.PROFILE_AVATAR)),
            "Profile/avatar button not clickable",
        )

    def click_logout(self) -> None:
        """Click the Logout option inside the user menu."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.LOGOUT_OPTION),
                     self.click(self.LOGOUT_OPTION)),
            "Logout option not clickable",
        )

    # ------------------------------------------------------------------
    # Forgot password flow interactions
    # ------------------------------------------------------------------

    def click_forgot_password_link(self) -> None:
        """Click the 'Forgot Password?' link on the login page."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.FORGOT_PASSWORD_LINK),
                     self.click(self.FORGOT_PASSWORD_LINK)),
            "Forgot Password link not clickable",
        )

    def click_send_otp(self) -> None:
        """Click the submit / Send OTP button on the forgot password screen."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.SEND_OTP_BTN),
                     self.click(self.SEND_OTP_BTN)),
            "Send OTP button not clickable",
        )

    def enter_new_password(self, new_password: str) -> None:
        """Type ``new_password`` into the new-password field."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.NEW_PASSWORD_INPUT),
                     self.enter_text(self.NEW_PASSWORD_INPUT, new_password)),
            "New password field not found or not interactable",
        )

    def click_resend_password(self) -> None:
        """Click the 'Reset Password' button to finalise the password change."""
        self._safe_action(
            lambda: (self.wait_for_visibility(self.RESET_BTN),
                     self.click(self.RESET_BTN)),
            "Reset Password button not clickable",
        )

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def get_error_message(self) -> str:
        """Return the visible error message text, or an empty string if absent."""
        return self.get_text(self.ERROR_MESSAGE)
