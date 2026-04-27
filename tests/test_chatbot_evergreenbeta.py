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
    {"category": "Conforming", "toggle_name": "Fannie Mae (Conforming)"},
    {"category": "Conforming", "toggle_name": "Freddie Mac (Conforming)"},
    {"category": "Conforming", "toggle_name": "US Bank (Conforming)"},

    # GOVERNMENT CATEGORY
    {"category": "Government", "toggle_name": "FHA Chenoa"},
    {"category": "Government", "toggle_name": "FHA (Government)"},
    {"category": "Government", "toggle_name": "Section 184"},
    {"category": "Government", "toggle_name": "USDA (Government)"},
    {"category": "Government", "toggle_name": "VA"},

    # Jumbo & Non-Conforming CATEGORY
    {"category": "Jumbo & Non-Conforming", "toggle_name": "BAML"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Campeer"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Chase"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Citi"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Luxury Mortgage"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "MaxEx"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Radian"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Redwood"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "Truist"},
    {"category": "Jumbo & Non-Conforming", "toggle_name": "US Bank (Non Conforming)"},

    # Non-QM CATEGORY
    {"category": "Non-QM", "toggle_name": "Deephaven"},
    {"category": "Non-QM", "toggle_name": "NQM Funding"},
    {"category": "Non-QM", "toggle_name": "Onslow Bay"},


    # Construction
    {"category": "Construction", "toggle_name": "Fannie Mae (Construction)"},
    {"category": "Construction", "toggle_name": "FHA (Construction)"},
    {"category": "Construction", "toggle_name": "Freddie Mac (Construction)"},
    {"category": "Construction", "toggle_name": "Global Lot Loan"},
    {"category": "Construction", "toggle_name": "Global Two Step"},
    {"category": "Construction", "toggle_name": "USDA (Construction)"},

    # Portfolio
    {"category": "Portfolio", "toggle_name": "BridgeLoan"},

    # HELOC
    {"category": "HELOC", "toggle_name": "Figure Lending"},
    {"category": "HELOC", "toggle_name": "GBC"},
    {"category": "HELOC", "toggle_name": "US Bank (HELOC)"},

]

class TestChatbotEvergreen:


    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginevergreenbeta):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver

    @pytest.mark.parametrize(
        "guideline",
        ALL_GUIDELINES,
        ids=lambda g: f"{g['category']}::{g['toggle_name']}"
    )
    def test_response_with_chatbot(self, guideline):
        evergreen_beta_page = ChatbotEvergreenBetaPage(self.driver)

        category = guideline["category"]
        toggle_label = guideline["toggle_name"]

        # 1. Start from a completely fresh State. This is the #1 best practice
        # so tests don't pollute each other (meaning no more clicking "Change" and "Cross")
        self.driver.refresh()
        evergreen_beta_page.wait_for_url_contains("chat")

        # 2. Click the Category
        # We use a dynamic dictionary mapping to handle click actions based on category name.
        category_actions = {
            "Conforming": evergreen_beta_page.click_confirmation_guideline_selection,
            "Government": evergreen_beta_page.click_government_guideline_selection,
            "Jumbo & Non-Conforming": evergreen_beta_page.click_jumbo_now_confirming_guideline_selection,
            "Non-QM": evergreen_beta_page.click_non_qm_guideline_selection,
            "Construction": evergreen_beta_page.click_construction_guideline_selection,
            "Portfolio": evergreen_beta_page.click_portfolio_guideline_selection,
            "HELOC": evergreen_beta_page.click_heloc_guideline_selection,
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
        evergreen_beta_page.click_chatbot_toggle(toggle_label)

        # 4. Message the bot
        evergreen_beta_page.enter_guideline_message(INPUT_DATA_GUIDELINE_MESSAFGE)
        evergreen_beta_page.click_submit_btn()

        # 5. Get the user payload verification
        response = evergreen_beta_page.wait_for_response()
        assert response, "❌ Empty user message logged in chat window"

        forbidden_keywords = ["Unauthorized", "Invalid","error creating session","Invalid API key. Please provide a valid API key and try again."]
        for word in forbidden_keywords:
            assert word not in response.lower(), f"Forbidden word found: {word}"



