# pages/login_page.py

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from utils.helpers import generate_unique_email
from utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage(BasePage):

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    NEW_PASSWORD_INPUT = (By.ID, "new-password")
    LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Login']")
    OTP_INPUT = (By.ID, "otp")
    SEND_OTP = (By.XPATH, "//button[@type='submit']")
    VERIFY_BTN = (By.XPATH, "//button[contains(text(),'Verify OTP')]")
    REMEMBER_ME = (By.ID, "remember-me")
    NAVIGATE_LOGOUT_BUTTON = (By.XPATH, "//span[@class='bg-muted flex size-full items-center justify-center rounded-full']")
    LOGOUT = (By.XPATH, "//div[normalize-space()='Logout']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space()='Reset Password']")
    ERROR_MESSAGE = (By.XPATH, "//*[@data-slot='alert-description']")

    def enter_email(self, email):
        try:
            self.wait_for_visibility(self.EMAIL_INPUT)
            self.enter_text(self.EMAIL_INPUT, email)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Email field not found: {e}")
            raise

    def enter_password(self, password):
        try:
            self.wait_for_visibility(self.PASSWORD_INPUT)
            self.enter_text(self.PASSWORD_INPUT, password)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Password field not found: {e}")
            raise

    def enter_new_password(self, new_password):
        try:
            self.wait_for_visibility(self.NEW_PASSWORD_INPUT)
            self.enter_text(self.NEW_PASSWORD_INPUT, new_password)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"New password field not found: {e}")
            raise

    def click_login(self):
        try:
            self.wait_for_visibility(self.LOGIN_BTN)
            self.click(self.LOGIN_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Login button not clickable: {e}")
            raise

    def enter_otp(self, otp):
        try:
            self.wait_for_visibility(self.OTP_INPUT)
            self.enter_text(self.OTP_INPUT, otp)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"OTP field not found: {e}")
            raise

    def click_verify(self):
        try:
            self.wait_for_visibility(self.VERIFY_BTN)
            self.click(self.VERIFY_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Verify button not clickable: {e}")
            raise

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def click_remember_me(self):
        try:
            self.wait_for_visibility(self.REMEMBER_ME)
            self.click(self.REMEMBER_ME)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Remember Me checkbox not clickable: {e}")
            raise

    def click_profile(self):
        try:
            self.wait_for_visibility(self.NAVIGATE_LOGOUT_BUTTON)
            self.click(self.NAVIGATE_LOGOUT_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Profile/avatar button not clickable: {e}")
            raise

    def click_logout(self):
        try:
            self.wait_for_visibility(self.LOGOUT)
            self.click(self.LOGOUT)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Logout button not clickable: {e}")
            raise

    def is_login_button_enabled(self):
        try:
            btn = self.wait_for_visibility(self.LOGIN_BTN)
            return btn.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def click_forgot_password_link(self):
        try:
            self.wait_for_visibility(self.FORGOT_PASSWORD_LINK)
            self.click(self.FORGOT_PASSWORD_LINK)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Forgot Password link not clickable: {e}")
            raise

    def click_send_otp(self):
        try:
            self.wait_for_visibility(self.SEND_OTP)
            self.click(self.SEND_OTP)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Send OTP button not clickable: {e}")
            raise

    def click_resend_password(self):
        try:
            self.wait_for_visibility(self.RESET_BUTTON)
            self.click(self.RESET_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Reset Password button not clickable: {e}")
            raise
