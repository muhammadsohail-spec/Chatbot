"""
tests/test_login.py
===================
Test suite for the Login module of the GuidelineBuddy application.

Covers:
    - Data-driven valid / invalid / empty-credential login scenarios
    - Logout functionality
    - Forgot password recovery flow (skipped until environment is ready)

Tech Stack:
    Python | Pytest | Selenium | Page Object Model | Allure Reporting
"""

import pytest
import allure

from pages.login_page import LoginPage
from config.config import (
    URL,
    USERNAME,
    PASSWORD,
    NEW_PASSWORD,
    WRONG_USERNAME,
    WRONG_PASSWORD,
    TEST_OTP,
)
from utils.logger import get_logger

logger = get_logger("TestLogin")


# ---------------------------------------------------------------------------
# Parametrize dataset
# ---------------------------------------------------------------------------
LOGIN_SCENARIOS = [
    pytest.param(USERNAME,      PASSWORD,       "success",     id="valid_credentials"),
    pytest.param(WRONG_USERNAME, PASSWORD,      "error",       id="wrong_username"),
    pytest.param(USERNAME,      WRONG_PASSWORD, "error",       id="wrong_password"),
    pytest.param(WRONG_USERNAME, WRONG_PASSWORD, "error",      id="wrong_username_and_password"),
    pytest.param("",            PASSWORD,       "empty_creds", id="empty_username"),
    pytest.param(USERNAME,      "",             "empty_creds", id="empty_password"),
    pytest.param("",            "",             "empty_creds", id="both_empty"),
]


@allure.feature("Login Module")
class TestLogin:
    """
    End-to-end test suite for the Login module.

    Fixture dependency (injected via conftest.py):
        driver    – class-scoped Selenium WebDriver instance.
        loginbeta – pre-authenticated session fixture (not used here but
                    kept available for other tests that extend this class).
    """

    # ------------------------------------------------------------------
    # Fixtures
    # ------------------------------------------------------------------

    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginbeta):
        """Bind shared fixtures to instance attributes for test access."""
        self.driver = driver
        self.loginbeta = loginbeta

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _open_login_page(self) -> "LoginPage":
        """Navigate to the application URL and return a fresh LoginPage."""
        self.driver.get(URL)
        return LoginPage(self.driver)

    def _perform_login(self, login_page: "LoginPage", username: str, password: str) -> None:
        """
        Enter credentials and submit the login form.

        Args:
            login_page: Active LoginPage instance.
            username:   Email / username string.
            password:   Password string.
        """
        login_page.enter_email(username)
        login_page.enter_password(password)
        login_page.click_login()

    def _complete_otp_and_assert_chat(self, login_page: "LoginPage") -> None:
        """
        Submit OTP and assert that the browser has landed on the chat/dashboard page.

        Args:
            login_page: Active LoginPage instance.
        """
        login_page.enter_otp(TEST_OTP)
        login_page.wait_for_url_contains("chat")
        current_url = self.driver.current_url
        assert "chat" in current_url or "dashboard" in current_url, (
            f"Expected 'chat' or 'dashboard' in URL after login, got: {current_url}"
        )

    # ------------------------------------------------------------------
    # Test Cases
    # ------------------------------------------------------------------

    @allure.story("Data-Driven Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login - {expected_type} scenario ({username})")
    @pytest.mark.parametrize("username, password, expected_type", LOGIN_SCENARIOS)
    def test_login_scenarios(self, username: str, password: str, expected_type: str) -> None:
        """
        Data-driven test covering valid, invalid, and empty-credential login flows.

        Args:
            username:      Input email / username.
            password:      Input password.
            expected_type: One of ``"success"``, ``"error"``, or ``"empty_creds"``.
        """
        logger.info(
            "Scenario '%s' — username: '%s' | password: '%s'",
            expected_type, username, password,
        )

        login_page = self._open_login_page()

        # ── Step 1: Enter only the non-empty credentials ──────────────
        if username:
            login_page.enter_email(username)
        if password:
            login_page.enter_password(password)

        # ── Step 2: Empty-field guard — button must stay disabled ──────
        if expected_type == "empty_creds":
            with allure.step("Verify login button is disabled for empty credentials"):
                assert not login_page.is_login_button_enabled(), (
                    "Login button should be disabled when credentials are empty."
                )
            logger.info("Empty-credentials guard passed — login button is disabled.")
            return

        # ── Step 3: Submit the form ────────────────────────────────────
        with allure.step("Click login button"):
            login_page.click_login()

        # ── Step 4: Post-submission assertions ────────────────────────
        if expected_type == "success":
            with allure.step("Complete OTP verification and validate redirect"):
                self._complete_otp_and_assert_chat(login_page)
            logger.info("Valid-login scenario passed — redirected to chat/dashboard.")

        elif expected_type == "error":
            with allure.step("Validate error message is displayed"):
                error_msg = login_page.get_error_message()
                assert error_msg, "Expected an error message for invalid credentials, but none was displayed."
            logger.info("Invalid-credentials scenario passed — error message: '%s'", error_msg)

    # ------------------------------------------------------------------

    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Logout - User is redirected to login page")
    def test_logout_successfully(self) -> None:
        """
        Verify that an authenticated user can log out and is redirected
        back to the login page.

        Steps:
            1. Navigate to URL and log in with valid credentials.
            2. Complete OTP verification.
            3. Open profile menu and click Logout.
            4. Assert the browser is on the login page.
        """
        logger.info("Starting logout test.")

        login_page = self._open_login_page()

        with allure.step("Log in with valid credentials"):
            self._perform_login(login_page, USERNAME, PASSWORD)

        with allure.step("Complete OTP and confirm authenticated state"):
            self._complete_otp_and_assert_chat(login_page)

        with allure.step("Open profile menu and click Logout"):
            login_page.click_profile()
            login_page.click_logout()

        with allure.step("Verify redirect to login page"):
            login_page.wait_for_url_contains("login")
            current_url = self.driver.current_url
            assert "login" in current_url, (
                f"Expected 'login' in URL after logout, got: {current_url}"
            )

        logger.info("Logout test passed — user redirected to: %s", self.driver.current_url)

    # ------------------------------------------------------------------

    @allure.story("Forgot Password")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Forgot Password - Full recovery flow")
    @pytest.mark.skip(reason="Requires live OTP — enable when environment is ready.")
    def test_forgot_password(self) -> None:
        """
        End-to-end test for the forgot password recovery flow.

        Steps:
            1. Enter registered email on login page.
            2. Click 'Forgot Password?' link.
            3. Re-enter email and request OTP.
            4. Enter OTP and set a new password.
            5. Log in with the new password and assert successful redirect.

        Note:
            Skipped by default because it requires a live OTP delivered to
            the registered email. Remove the ``@pytest.mark.skip`` decorator
            when running against a controlled test environment.
        """
        logger.info("Starting forgot-password recovery flow test.")

        login_page = self._open_login_page()

        with allure.step("Enter registered email"):
            login_page.enter_email(USERNAME)

        with allure.step("Click Forgot Password link"):
            login_page.click_forgot_password_link()

        with allure.step("Re-enter email and request OTP"):
            login_page.enter_email(USERNAME)
            login_page.click_send_otp()

        with allure.step("Enter OTP and set new password"):
            login_page.enter_otp(TEST_OTP)
            login_page.enter_new_password(NEW_PASSWORD)
            login_page.click_resend_password()

        with allure.step("Log in with new password"):
            login_page.enter_email(USERNAME)
            login_page.enter_password(NEW_PASSWORD)
            login_page.click_login()

        with allure.step("Complete OTP and assert redirect"):
            self._complete_otp_and_assert_chat(login_page)

        logger.info("Forgot-password recovery flow passed.")