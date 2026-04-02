import time

import allure
import pytest
from pages.login_page import LoginPage
from pages.signup_page import Signup

from utils.helpers import generate_unique_email
from config.config import URL, USERNAME, PASSWORD
import logging


class TestSignUp:

    @pytest.mark.parametrize("first,last,company,title,email,cellphone,password,confirm_password", [
        ("First", "Tester", "Test Company","Company title",[generate_unique_email()],"0345343333","DefaultPassword123.","DefaultPassword123."),
    ])
    @pytest.mark.skip(reason="Not need to test every time")
    def test_signup_with_email(self, driver,first,last,company,title,email,cellphone,password,confirm_password):
        driver.get(URL)
        signup_page = Signup(driver)
        signup_page.click_signup()
        signup_page.enter_firstname(first)
        signup_page.enter_lastname(last)
        signup_page.enter_company(company)
        signup_page.enter_title(title)
        updated_ramdom=generate_unique_email()
        print("Newly User Email ==="+updated_ramdom)
        signup_page.enter_email(updated_ramdom)
        time.sleep(2)
        signup_page.enter_cellphone(cellphone)
        signup_page.enter_confirmpassword(confirm_password)
        print("Newly User Password ===" + password)
        signup_page.click_submit()
        signup_page.enter_otp("712312")
        success_msg=signup_page.get_success_message()
        assert "Welcome to Guideline Buddy" in success_msg

    def test_signup_with_google(self,driver):
        driver.get(URL)
        signup_page = Signup(driver)
        signup_page.click_signup_btn_google()
        time.sleep(10)