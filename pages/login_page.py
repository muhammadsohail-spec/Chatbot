# pages/login_page.py

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from utils.helpers import generate_unique_email


class LoginPage(BasePage):

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    NEW_PASSWORD_INPUT = (By.ID, "new-password")
    LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Login']")
    OTP_INPUT = (By.ID, "otp")
    SEND_OTP= (By.XPATH, "//button[@type='submit']")
    VERIFY_BTN = (By.XPATH, "//button[contains(text(),'Verify OTP')]")
    REMEMBER_ME= (By.ID,"remember-me")
    NAVIGATE_LOGOUT_BUTTON=(By.XPATH,"//span[@class='bg-muted flex size-full items-center justify-center rounded-full']")
    LOGOUT=(By.XPATH,"//div[normalize-space()='Logout']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    RESET_BUTTON=(By.XPATH, "//button[normalize-space()='Reset Password']")
    ERROR_MESSAGE = (By.XPATH, "//*[@data-slot='alert-description']")

    def enter_email(self, email):
        try:
            self.wait_for_visibility(self.EMAIL_INPUT)
            self.enter_text(self.EMAIL_INPUT, email)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Email field not found: {e}")

    def enter_password(self, password):
        try:
            self.wait_for_visibility(self.PASSWORD_INPUT)
            self.enter_text(self.PASSWORD_INPUT, password)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Password field not found: {e}")

    def enter_new_password(self, newpassword):
        try:
            self.wait_for_visibility(self.NEW_PASSWORD_INPUT)
            self.enter_text(self.NEW_PASSWORD_INPUT, newpassword)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Password field not found: {e}")

    def click_login(self):
        try:
            self.wait_for_visibility(self.LOGIN_BTN)
            self.click(self.LOGIN_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login button not clickable: {e}")

    def enter_otp(self, otp):
        try:
            self.wait_for_visibility(self.OTP_INPUT)
            self.enter_text(self.OTP_INPUT, otp)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"OTP field not found: {e}")

    def click_verify(self):
        try:
            self.wait_for_visibility(self.VERIFY_BTN)
            self.click(self.VERIFY_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Verify button not clickable: {e}")

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def click_remember_me(self):
        try:
            self.wait_for_visibility(self.REMEMBER_ME)
            self.click(self.REMEMBER_ME)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login button not clickable: {e}")

    def click_profile(self):
        try:
            self.wait_for_visibility(self.NAVIGATE_LOGOUT_BUTTON)
            self.click(self.NAVIGATE_LOGOUT_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login button not clickable: {e}")

    def click_logout(self):
        try:
            self.wait_for_visibility(self.LOGOUT)
            self.click(self.LOGOUT)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login button not clickable: {e}")

    def is_login_button_enabled(self):
        try:
            btn = self.wait_for_visibility(self.LOGIN_BTN)
            return btn.is_enabled()
        except:
            return False

    def click_forgot_password_link(self):
        try:
            self.wait_for_visibility(self.FORGOT_PASSWORD_LINK)
            self.click(self.FORGOT_PASSWORD_LINK)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_send_otp(self):
        try:
            self.wait_for_visibility(self.SEND_OTP)
            self.click(self.SEND_OTP)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_resend_password(self):
        try:
            self.wait_for_visibility(self.RESET_BUTTON)
            self.click(self.RESET_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")


