from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.login_page import LoginPage


class Signup(BasePage):

    SIGNUP_BTN = (By.XPATH, "//span[normalize-space()='Sign Up']")
    FIRSTNAME_INPUT = (By.ID, "first-name")
    LASTNAME_INPUT = (By.ID, "last-name")
    COMPANY_INPUT = (By.ID, "company")
    TITLE_INPUT = (By.ID, "title")
    EMAIL_INPUT = (By.ID, "email")
    CELLPHONE_INPUT = (By.ID, "phone_number")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password")
    SUBMIT_BTN=(By.XPATH,"//button[@type='submit']")
    SIGNUP_BTN_GOOGLE=(By.XPATH,"//button[ @data-slot = 'button'][2]")
    SUCCESS_MESSAGE=(By.XPATH,"//*[normalize-space()='Welcome to Guideline Buddy']")
    OTP_INPUT=(By.ID,"otp")



    def click_signup(self):
        try:
            self.wait_for_visibility(self.SIGNUP_BTN)
            self.click(self.SIGNUP_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login button not clickable: {e}")

    def enter_firstname(self, firstname):
        try:
            self.wait_for_visibility(self.FIRSTNAME_INPUT)
            self.enter_text(self.FIRSTNAME_INPUT, firstname)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"First field not found: {e}")

    def enter_lastname(self, lastname):
        try:
            self.wait_for_visibility(self.LASTNAME_INPUT)
            self.enter_text(self.LASTNAME_INPUT,lastname)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Last field not found: {e}")


    def enter_company(self, company):
        try:
            self.wait_for_visibility(self.COMPANY_INPUT)
            self.enter_text(self.COMPANY_INPUT,company)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Company field not found: {e}")


    def enter_title(self, title):
        try:
            self.wait_for_visibility(self.TITLE_INPUT)
            self.enter_text(self.TITLE_INPUT,title)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Title field not found: {e}")

    def enter_email(self, title):
        try:
            self.wait_for_visibility(self.EMAIL_INPUT)
            self.enter_text(self.EMAIL_INPUT, title)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Email field not found: {e}")

    def enter_cellphone(self, cellphone):
        try:
            self.wait_for_visibility(self.CELLPHONE_INPUT)
            self.enter_text(self.CELLPHONE_INPUT, cellphone)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"cell phone field not found: {e}")


    def enter_password(self, password):
        try:
            self.wait_for_visibility(self.PASSWORD_INPUT)
            self.enter_text(self.PASSWORD_INPUT, password)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"password field not found: {e}")

    def enter_confirmpassword(self, confirmpassword):
        try:
            self.wait_for_visibility(self.CONFIRM_PASSWORD_INPUT)
            self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirmpassword)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Confirm password field not found: {e}")

    def click_submit(self):
        try:
            self.wait_for_visibility(self.SUBMIT_BTN)
            self.click(self.SUBMIT_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"SIGN button not clickable: {e}")

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def enter_otp(self, otp):
        try:
            self.wait_for_visibility(self.OTP_INPUT)
            self.enter_text(self.OTP_INPUT, otp)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"OTP field not found: {e}")

    def click_signup_btn_google(self):
        try:
            self.wait_for_visibility(self.SIGNUP_BTN_GOOGLE)
            self.click(self.SIGNUP_BTN_GOOGLE)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")