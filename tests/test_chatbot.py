import pytest
from pages.chatbot import ChatpotPage
from config.config import INPUT_DATA_GUIDELINE_MESSAFGE, URLBeta
from utils.logger import get_logger
# //section[@aria-label='Notifications alt+T']

logger = get_logger("TestChatbot")

# ---------------------------------------------------------
# TEST DATA (SENIOR AUTOMATION BEST PRACTICE)
# You can add all 40+ chatbots to this single list!
# ---------------------------------------------------------
ALL_GUIDELINES = [
    # CONFORMING CATEGORY
    {"category": "Select Lender Partner", "toggle_name": "(Select All)"},
    {"category": "Select Lender Partner", "toggle_name": "Reverse Mortgages (HECMs)"},
    {"category": "Select Lender Partner", "toggle_name": "Snmc test bots"},
    {"category": "Select Lender Partner", "toggle_name": "test"},
    {"category": "Select Lender Partner", "toggle_name": "test bot"},
    {"category": "Select Lender Partner", "toggle_name": "Test Scratch Bot 2"},
    {"category": "Select Lender Partner", "toggle_name": "Truist"},
    {"category": "Select Lender Partner", "toggle_name": "xyz"},


]

class TestChatbot:


    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginbeta):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver
        self.chatbot_page = ChatpotPage(self.driver)

    @pytest.mark.parametrize("guideline", ALL_GUIDELINES,
    ids=lambda g: f"{g['category']}::{g['toggle_name']}")


    def test_all_guideline_chatbots(self, guideline):
        category = guideline["category"]
        toggle_label = guideline["toggle_name"]

        self.driver.refresh()
        self.chatbot_page.wait_for_url_contains("chat")

        if category == "Select Lender Partner":
            self.chatbot_page.click_lender_and_guidelines_selection()

        else:
            # For your other 4 sections, you should add your click_XX_selection() methods
            # in chatbot_evergreenberta.py and call them here!
            raise NotImplementedError(f"Add the click method for category: {category}")

        self.chatbot_page.click_select_lender_partner()
        self.chatbot_page.select_lender_partner_option_by_name(toggle_label)

        if toggle_label == "test":
            self.chatbot_page.click_guideline()
            self.chatbot_page.select_guidelines_all()

        self.chatbot_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        self.chatbot_page.click_submit_btn()

        response = self.chatbot_page.wait_for_response()
        logger.info(f"Response for {toggle_label}: {response}")

        # --- Handle alerts and system errors gracefully ---
        # if response and "ALERT_FOUND:" in response:
        #     pytest.xfail(f"Expected failure due to browser alert: {response}")
        # elif response and "ERROR_FOUND:" in response:
        #     pytest.xfail(f"Expected failure due to system error: {response}")
        # ----------------------------------------------------

        assert response, "❌ Empty user message logged in chat window"

        forbidden_keywords = ["unauthorized", "failed", "error creating session","Invalid API key. Please provide a valid API key and try again."]
        for word in forbidden_keywords:
            assert word not in response.lower(), f"Forbidden word found: {word}"