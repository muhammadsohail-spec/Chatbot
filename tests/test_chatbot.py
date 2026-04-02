import time

import allure
import pytest

from pages.chatbot import ChatpotPage
from pages.login_page import LoginPage
from config.config import URL, USERNAME, PASSWORD,NEW_PASSWORD,INPUT_DATA_GUIDELINE_MESSAFGE
import logging
from utils.validator import ResponseValidator
import logging

class TestChatbot:

    def test_chatbot_response_with_partner_new_beta_fannie_mae(self,driver):
        driver.get(URL)
        login_page = LoginPage(driver)
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
        chatbot_page.select_lender_partner_option1()
        chatbot_page.click_guideline()
        chatbot_page.select_guidelines_option1()

        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)

        chatbot_page.click_submit_btn()

        response = chatbot_page.get_latest_response()

        print(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"

        assert ResponseValidator.is_valid(response), (
            f"❌ Test FAILED - Invalid keyword 'Unauthorized' found in response: {response}"
        )

    def test_chatbot_response_with_partner_new_beta_freddie_mac(self, driver):
        driver.get(URL)
        login_page = LoginPage(driver)
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
        chatbot_page.select_lender_partner_option1()
        chatbot_page.click_guideline()
        chatbot_page.select_guidelines_option2()

        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)

        chatbot_page.click_submit_btn()

        response = chatbot_page.get_latest_response()

        print(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"

        assert ResponseValidator.is_valid(response), (
            f"❌ Test FAILED - Invalid keyword 'Unauthorized' found in response: {response}"
        )

    # @pytest.mark.skip(reason="Not need to test every time")
    def test_chatbot_response_with_partner_reverse_mortgages(self,driver):
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
        chatbot_page.select_lender_partner_option2()
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.get_latest_response()

        print(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"

        assert "unauthorized" not in response.lower(), \
            f"❌ Test Failed - Unauthorized response received: {response}"

    # @pytest.mark.skip(reason="Not need to test every time")
    def test_chatbot_response_with_partner_snmc_test_bots(self, driver):
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
        chatbot_page.select_lender_partner_option3()
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.get_error_message2()

        print(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"

        assert "Error creating session" not in response, \
            f"❌ Test Failed - Unauthorized response received: {response}"

    # @pytest.mark.skip(reason="Not need to test every time")
    def test_chatbot_response_with_partner_truist(self, driver):
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
        chatbot_page.select_lender_partner_option4()
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response1 = chatbot_page.get_error_message()

        print(f"Response: {response1}")

        assert response1, "❌ Empty response from chatbot"

        assert "Unauthorized" not in response1, \
            f"❌ Test Failed - Unauthorized response received: {response1}"


    # @pytest.mark.skip(reason="Not need to test every time")
    def test_chatbot_response_with_partner_xyz(self, driver):
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
        chatbot_page.select_lender_partner_option5()
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response2 = chatbot_page.get_error_message2()

        print(f"Response: {response2}")
        assert response2, "❌ Empty response from chatbot"

        assert "Error creating session" not in response2, \
            f"❌ Test Failed - Unauthorized response received: {response2}"

