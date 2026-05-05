import allure
import pytest
from pages.chatbot_evergreenberta import ChatbotEvergreenBetaPage
from config.config import INPUT_DATA_GUIDELINE_MESSAFGE


ALL_GUIDELINES = [
    # CONFORMING CATEGORY
    {"category": "Conforming", "toggle_name": "Fannie"},
    {"category": "Conforming", "toggle_name": "Freddie"},

    # GOVERNMENT CATEGORY
    {"category": "Government", "toggle_name": "FHA"},
    {"category": "Government", "toggle_name": "USDA"},
    {"category": "Government", "toggle_name": "VA"},

    # Non-QM CATEGORY
    {"category": "Non-QM", "toggle_name": "Newrez"},

    # DPA CATEGORY
    {"category": "DPA", "toggle_name": "AHFA"},
    {"category": "DPA", "toggle_name": "CAFA"},
    {"category": "DPA", "toggle_name": "FHFC"},
    {"category": "DPA", "toggle_name": "Jefferson Parish"},
    {"category": "DPA", "toggle_name": "LHC"},
    {"category": "DPA", "toggle_name": "MHC"},
    {"category": "DPA", "toggle_name": "THDA"},




]

class TestChatbotDSLDBETA:


    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, logindsldbeta):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver

    @pytest.mark.parametrize(
        "guideline",
        ALL_GUIDELINES,
        ids=lambda g: f"{g['category']}::{g['toggle_name']}"
    )
    @allure.feature("Login Feature")
    @allure.story("Valid Login Test")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_response_with_chatbot_dsld(self, guideline):
        ChatbotdsldBetaPage = ChatbotEvergreenBetaPage(self.driver)

        category = guideline["category"]
        toggle_label = guideline["toggle_name"]

        # 1. Start from a completely fresh State. This is the #1 best practice
        # so tests don't pollute each other (meaning no more clicking "Change" and "Cross")
        self.driver.refresh()
        ChatbotdsldBetaPage.wait_for_url_contains("chat")

        category_actions = {
            "Conforming": ChatbotdsldBetaPage.click_confirmation_guideline_selection,
            "Government": ChatbotdsldBetaPage.click_government_guideline_selection,
            "Non-QM": ChatbotdsldBetaPage.click_non_qm_guideline_selection,
            "DPA": ChatbotdsldBetaPage.click_dpa_guideline_selection,
        }

        # Dynamically fetch and execute the corresponding action
        action = category_actions.get(category)
        if action:
            action()
        else:
            # For your other 4 sections, you should add your click_XX_selection() methods
            # in chatbot_evergreenberta.py and call them here!
            raise NotImplementedError(f"Add the click method for category: {category}")

        # 3. Select the dynamic Toggle inside that category!
        ChatbotdsldBetaPage.click_chatbot_toggle(toggle_label)

        # 4. Message the bot
        ChatbotdsldBetaPage.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        ChatbotdsldBetaPage.click_submit_btn()

        # 5. Get the user payload verification
        response = ChatbotdsldBetaPage.wait_for_response()
        assert response, "❌ Empty user message logged in chat window"
        print("This is Response in Chatbot==" + response)

        forbidden_keywords = ["Unauthorized", "Invalid", "error creating session",
                              "Invalid API key. Please provide a valid API key and try again."]
        for word in forbidden_keywords:
            assert word not in response.lower(), f"Forbidden word found: {word}"
