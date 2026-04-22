import pytest
import allure
from pages.login_page import LoginPage
from config.config import URL, USERNAME, PASSWORD, NEW_PASSWORD, WRONG_USERNAME, WRONG_PASSWORD, TEST_OTP
from utils.logger import get_logger

logger = get_logger("TestLogin")


@pytest.mark.smoke
class TestLogin:
    """
    Test suite for Login module covering:
    - Valid / Invalid login scenarios
    - Empty credential validation
    - Logout functionality
    - Forgot password flow
    """

    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginbeta):
        """
        Autouse fixture to initialize WebDriver instance for all test methods.
        Ensures driver is available as self.driver in every test.
        """
        self.driver = driver

    @allure.feature("Login Module")
    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Authentication and Login Tests")
    @pytest.mark.parametrize("username, password, expected_type", [
        # Success scenario — uses config constants (no hardcoded credentials)
        (USERNAME, PASSWORD, "success"),
        # Invalid credentials scenarios
        (WRONG_USERNAME, PASSWORD, "error"),
        (USERNAME, WRONG_PASSWORD, "error"),
        (WRONG_USERNAME, WRONG_PASSWORD, "error"),
        # Empty credential scenarios
        ("", PASSWORD, "empty_creds"),
        (USERNAME, "", "empty_creds"),
        ("", "", "empty_creds"),
    ])
    def test_login_scenarios(self, username, password, expected_type):
        """
        Data-driven test for login functionality covering:
        - Valid login
        - Invalid credentials
        - Empty input validation
        """
        logger.info(f"Testing login with Username: '{username}' | Password: '{password}'")

        # Navigate to application URL
        self.driver.get(URL)
        login_page = LoginPage(self.driver)

        # -------------------------------
        # Step 1: Enter credentials
        # -------------------------------
        if username:
            login_page.enter_email(username)
        if password:
            login_page.enter_password(password)

        # -------------------------------
        # Step 2: Validate empty fields scenario
        # -------------------------------
        if expected_type == "empty_creds":
            assert not login_page.is_login_button_enabled(), \
                "Login button should be disabled when credentials are empty."
            return

        # -------------------------------
        # Step 3: Perform login action
        # -------------------------------
        login_page.click_login()

        # -------------------------------
        # Step 4: Assertions based on scenario
        # -------------------------------
        if expected_type == "success":
            # Handle OTP verification for successful login
            login_page.enter_otp(TEST_OTP)

            # Wait until user is redirected to dashboard/chat page
            login_page.wait_for_url_contains("chat")

            # Validate successful navigation
            assert "chat" in self.driver.current_url or "dashboard" in self.driver.current_url, \
                "Expected 'chat' or 'dashboard' in URL after successful login."

            logger.info("Successful login validated.")

        elif expected_type == "error":
            # Validate error message for invalid login attempts
            error_msg = login_page.get_error_message()
            assert error_msg, "Expected error message but none was displayed."

            logger.info(f"Error validation successful: {error_msg}")


    # -------------------------------
    # Logout Test Case
    # -------------------------------
    @allure.feature("Login Module")
    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Logout Functionality")
    def test_logout_successfully(self):
        """
        Validate user logout functionality:
        - Open profile menu
        - Click logout
        - Verify user redirected to login page
        """
        login_page = LoginPage(self.driver)

        # Perform logout steps
        login_page.click_profile()
        login_page.click_logout()

        # Wait for redirection to login page
        login_page.wait_for_url_contains("login")

        # Verify logout success
        assert "login" in self.driver.current_url, \
            "User was not redirected back to login page after logout."

        logger.info("Logout validated successfully.")


    # -------------------------------
    # Forgot Password Flow Test Case
    # -------------------------------
    @allure.feature("Login Module")
    @allure.story("Forgot Password")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Forgot Password Recovery Flow")
    def test_forgot_password(self):
        """
        Validate forgot password workflow:
        - Request OTP
        - Reset password
        - Login with new password
        """
        logger.info("Testing forgotten password recovery flow.")

        self.driver.get(URL)
        login_page = LoginPage(self.driver)

        # Step 1: Enter registered email
        login_page.enter_email(USERNAME)

        # Step 2: Trigger forgot password flow
        login_page.click_forgot_password_link()

        # Step 3: Request OTP
        login_page.enter_email(USERNAME)
        login_page.click_send_otp()

        # Step 4: Reset password using OTP
        login_page.enter_otp(TEST_OTP)
        login_page.enter_new_password(NEW_PASSWORD)
        login_page.click_resend_password()

        # Step 5: Verify login with new password
        login_page.enter_email(USERNAME)
        login_page.enter_password(NEW_PASSWORD)
        login_page.click_login()

        # OTP verification after password reset
        login_page.enter_otp(TEST_OTP)

        # Validate successful login
        login_page.wait_for_url_contains("chat")
        assert "chat" in self.driver.current_url, \
            "Expected 'chat' in URL after login with new password."

        logger.info("Forgot password flow validated successfully.")