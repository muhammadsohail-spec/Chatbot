import time

import allure
import pytest

from pages.chatbot import ChatpotPage
from pages.login_page import LoginPage
from config.config import URL, USERNAME, PASSWORD,NEW_PASSWORD,INPUT_DATA_GUIDELINE_MESSAFGE
import logging

import logging

class TestLogin:


    def test_chatbot_response(self,driver):
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
        chatbot_page = ChatpotPage(driver)
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option()
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        # chatbot_page.click_guideline()
        chatbot_page.click_submit_btn()

        response = chatbot_page.get_error_message()

        assert not "Unauthorized" in response
        time.sleep(25)
