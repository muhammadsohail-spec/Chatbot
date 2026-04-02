import time
import pytest
from pages.chatbot_evergreenberta import ChatbotEvergreenBetaPage
from config.config import INPUT_DATA_GUIDELINE_MESSAFGE

# ---------------------------------------------------------
# TEST DATA (SENIOR AUTOMATION BEST PRACTICE)
# You can add all 40+ chatbots to this single list!
# ---------------------------------------------------------
ALL_GUIDELINES = [
    # CONFORMING CATEGORY
    {"category": "Conforming", "toggle_name": "Chase Community Lending"},
    {"category": "Conforming", "toggle_name": "Conforming Overlays"},
    {"category": "Conforming", "toggle_name": "Conforming PnP"},
    {"category": "Conforming", "toggle_name": "Conforming US Bank Overlays"},
    {"category": "Conforming", "toggle_name": "Fannie Mae (Conforming)"},
    {"category": "Conforming", "toggle_name": "Freddie Mac (Conforming)"},
    {"category": "Conforming", "toggle_name": "US Bank (Conforming)"},

    # GOVERNMENT CATEGORY
    {"category": "Government", "toggle_name": "FHA Chenoa"},
    {"category": "Government", "toggle_name": "FHA (Government)"},
    {"category": "Government", "toggle_name": "Govt Overlays"},
    {"category": "Government", "toggle_name": "Section 184"},
    {"category": "Government", "toggle_name": "USDA (Government)"},
    {"category": "Government", "toggle_name": "VA"},

    # Jumbo & Non-Conforming CATEGORY
    {"category": "Jumbo & Non-Conforming", "toggle_name": "BAML"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Campeer"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Chase"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Citi"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Jumbo Non Conforming PnP"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Luxury Mortgage"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "MaxEx"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Radian"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Redwood"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Truist"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "US Bank (Non Conforming)"},

]

class TestChatbotEvergreen:
    
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, login):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver

    @pytest.mark.parametrize("guideline", ALL_GUIDELINES)
    def test_all_guideline_chatbots(self, guideline):
        evergreen_beta_page = ChatbotEvergreenBetaPage(self.driver)

        category = guideline["category"]
        toggle_label = guideline["toggle_name"]

        # 1. Start from a completely fresh State. This is the #1 best practice 
        # so tests don't pollute each other (meaning no more clicking "Change" and "Cross")
        self.driver.refresh()
        evergreen_beta_page.wait_for_url_contains("chat")
        
        # 2. Click the Category
        # We will expand the category based on its name.
        if category == "Conforming":
            evergreen_beta_page.click_confirmation_guideline_selection()
        elif category == "Government":
            evergreen_beta_page.click_government_guideline_selection()
        elif category == "Jumbo & Non-Conforming":
            evergreen_beta_page.click_jubmo_now_confirming_guideline_selection()
        else:
            # For your other 4 sections, you should add your click_XX_selection() methods
            # in chatbot_evergreenberta.py and call them here!
            raise NotImplementedError(f"Add the click method for category: {category}")
            
        # 3. Select the dynamic Toggle inside that category!
        evergreen_beta_page.click_chatbot_toggle(toggle_label)

        # 4. Message the bot
        evergreen_beta_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        evergreen_beta_page.click_submit_btn()
        
        # 5. Get the user payload verification
        response = evergreen_beta_page.get_latest_response()
        assert response, "❌ Empty user message logged in chat window"
        assert "Unauthorized" not in response.lower(), \
            f"❌ Test Failed - Unauthorized response received: {response}"

        # 6. Smart Wait for the AI algorithm to finish streaming!
        # bot_response = evergreen_beta_page.wait_for_response()
        # print(f"Response via [{category}] -> [{toggle_label}]: {bot_response}")
        #
        # # 7. Check correct completion
        # assert bot_response, "❌ Chatbot generated an empty asynchronous response"
        # assert "Hello" in bot_response or "Hi" in bot_response, \
        #     f"❌ Valid greeting missing from bot reply for {toggle_label}!"
