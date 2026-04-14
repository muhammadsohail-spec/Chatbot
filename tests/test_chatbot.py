import time
import pytest
from pages.chatbot import ChatpotPage
from config.config import INPUT_DATA_GUIDELINE_MESSAFGE, URLBeta
from utils.logger import get_logger

logger = get_logger("TestChatbot")

class TestChatbot:

    FORBIDDEN_WORDS = ["Unauthorized", "Error fetching response", "not available", "exception"]

    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginbeta):
        """Automatically passes the authenticated driver to all tests. loginbeta logs in for us!"""
        self.__class__.driver = driver

    def test_chatbot_response_with_partner_new_beta_with_select_all_guidelines(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("New Beta")
        chatbot_page.click_guideline()
        chatbot_page.select_guidelines_all()

        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.wait_for_response()
        logger.info(f"Response: {response}")
        
        assert response, "❌ Empty response from chatbot"
        for word in self.FORBIDDEN_WORDS:
            assert word not in response.lower(), f"Forbidden word found: {word}"

    def test_chatbot_response_with_partner_new_beta_fannie_mae(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("New Beta")
        chatbot_page.click_guideline()
        chatbot_page.select_guidelines_option_by_index(1)

        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.wait_for_response()
        logger.info(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"
        for word in self.FORBIDDEN_WORDS:
            assert word not in response.lower(), f"Forbidden word found: {word}"

    def test_chatbot_response_with_partner_new_beta_freddie_mac(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("New Beta")
        chatbot_page.click_guideline()
        chatbot_page.select_guidelines_option_by_index(2)

        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.wait_for_response()
        logger.info(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"
        assert "Error creating session" not in response
        assert "unauthorized" not in response.lower(), f"❌ Test Failed - Unauthorized response received: {response}"

    def test_chatbot_response_with_partner_reverse_mortgages(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("Reverse Mortgages (HECMs)")
        
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.wait_for_response()
        logger.info(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"
        assert "Error creating session" not in response
        assert "Error creating session" not in response, f"❌ Test Failed - Unauthorized response received: {response}"

    def test_chatbot_response_with_partner_snmc_test_bots(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("Snmc test bots")
        
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response = chatbot_page.get_error_message2()
        logger.info(f"Response: {response}")

        assert response, "❌ Empty response from chatbot"
        assert "Error creating session" not in response, f"❌ Test Failed - Unauthorized response received: {response}"

    def test_chatbot_response_with_partner_truist(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("Truist")
        
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response1 = chatbot_page.get_error_message()
        logger.info(f"Response: {response1}")

        assert response1, "❌ Empty response from chatbot"
        assert "Unauthorized" not in response1, f"❌ Test Failed - Unauthorized response received: {response1}"

    def test_chatbot_response_with_partner_xyz(self):
        self.driver.get(URLBeta)
        chatbot_page = ChatpotPage(self.driver)
        chatbot_page.click_lender_and_guidelines_selection()
        chatbot_page.click_select_lender_partner()
        chatbot_page.select_lender_partner_option_by_name("xyz")
        
        chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        chatbot_page.click_submit_btn()

        response2 = chatbot_page.get_error_message2()
        logger.info(f"Response: {response2}")
        
        assert response2, "❌ Empty response from chatbot"
        assert "Error creating session" not in response2, f"❌ Test Failed - Unauthorized response received: {response2}"