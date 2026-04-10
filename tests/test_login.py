import time

import allure
import pytest
from pages.login_page import LoginPage
from config.config import URL, USERNAME, PASSWORD,NEW_PASSWORD
import logging
from utils.logger import get_logger
import logging
from pages.base_page import BasePage

from utils.helpers import generate_unique_email


@allure.title("Login with valid credentials")
@allure.description("Test login functionality using valid username and password")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke

class TestLogin:



    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, login):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver



    @pytest.mark.regression
    def test_login_valid_credentials(self,driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        # Enter login detail
        logging.info("Entering username")
        login_page.enter_email(USERNAME)
        login_page.enter_password(PASSWORD)
        login_page.click_login()
        login_page.enter_otp("712312")
        login_page.wait_for_url_contains("chat")
        # assert "chat" in driver.current_url
        assert "chat" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"
        # get_logger.info("Positive test passed: valid login successful")

    def test_invalid_password(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        login_page.enter_email(USERNAME)
        login_page.enter_password("Wrong password")
        login_page.click_login()
        error = login_page.get_error_message()

        assert "invalid password" in error.lower(), f"Expected 'invalid password' error but got: {error}"


    def test_invalid_username(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        login_page.enter_email("wrongemail@gmail.com")
        login_page.enter_password(PASSWORD)
        login_page.click_login()

        error = login_page.get_error_message()
        assert "user not found" in error.lower(), f"Expected 'user not found1' error but got: {error}"


    def test_invalid_username_password(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        login_page.enter_email("invalidmail@gmail.com")
        login_page.enter_password("invalidpassword")
        login_page.click_login()

        error = login_page.get_error_message()
        assert "user not found" in error.lower(), f"Expected 'user not found' error but got: {error}"

    def test_logout_successfully(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        # Enter login detail
        logging.info("Entering username")
        login_page.enter_email(USERNAME)
        login_page.enter_password(PASSWORD)
        login_page.click_login()
        login_page.enter_otp("712312")
        login_page.click_profile()
        login_page.click_logout()

        login_page.wait_for_url_contains("login")
        assert "login" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"

    def test_empty_username(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        # Enter login detail
        logging.info("Entering Password")
        login_page.enter_password(PASSWORD)
        assert not login_page.is_login_button_enabled(), "Login button should be disabled for empty Username"

    def test_empty_password(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        # Enter login detail
        logging.info("Entering username")
        login_page.enter_email(USERNAME)
        assert not login_page.is_login_button_enabled(), "Login button should be disabled for empty Password"

    def test_empty_credentials(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        assert not login_page.is_login_button_enabled(), "Login button should be disabled for empty credentials"
    @pytest.mark.skip
    def test_forgot_password(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
        login_page.enter_email(USERNAME)
        login_page.click_forgot_password_link()
        time.sleep(2)
        login_page.enter_email(USERNAME)
        login_page.click_send_otp()
        time.sleep(3)
        login_page.enter_otp("712312")
        login_page.enter_new_password(NEW_PASSWORD)
        time.sleep(3)
        login_page.click_resend_password()
        time.sleep(5)
        # Enter login detail
        logging.info("Entering username")
        login_page.enter_email(USERNAME)
        login_page.enter_password(NEW_PASSWORD)
        login_page.click_login()
        login_page.enter_otp("712312")
        login_page.wait_for_url_contains("chat")
        # assert "chat" in driver.current_url
        assert "chat" in driver.current_url, f"Expected 'chat1' in URL but got {driver.current_url}"







