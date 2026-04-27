import pdb
import time

import pytest
from config.config import INPUT_DATA_GUIDELINE_MESSAFGE
from pages.fsbbeta import ChatbotFsbBetaPage
from utils.helpers import generate_dynamic_chat_message, extract_link

ALL_GUIDELINES = [

    # CONFORMING CATEGORY
    {"category": "Conforming", "toggle_name": "Ameri Home (Conforming)"},
    {"category": "Conforming", "toggle_name": "Bayview Loan Servicing (Conforming)"},
    {"category": "Conforming", "toggle_name": "Dollar Bank (Conforming)"},
    {"category": "Conforming", "toggle_name": "Fannie"},
    {"category": "Conforming", "toggle_name": "FHLB"},
    {"category": "Conforming", "toggle_name": "Freddie"},
    {"category": "Conforming", "toggle_name": "Freedom Mortgage (Conforming)"},
    {"category": "Conforming", "toggle_name": "JP Morgan Chase"},
    {"category": "Conforming", "toggle_name": "Maxex (Conforming)"},
    {"category": "Conforming", "toggle_name": "Mr Cooper (Conforming)"},
    {"category": "Conforming", "toggle_name": "NewRez (Conforming)"},
    {"category": "Conforming", "toggle_name": "NexBank (Conforming)"},
    {"category": "Conforming", "toggle_name": "Penny Mac (Conforming)"},
    {"category": "Conforming", "toggle_name": "PHH (Conforming)"},
    {"category": "Conforming", "toggle_name": "Planet Home Lending"},
    {"category": "Conforming", "toggle_name": "Plaza Home Mortgage"},
    {"category": "Conforming", "toggle_name": "Truist (Conforming)"},

    # GOVERNMENT CATEGORY
    {"category": "Government", "toggle_name": "Ameri Home (Government)"},
    {"category": "Government", "toggle_name": "Bayview Loan Servicing (Government)"},
    {"category": "Government", "toggle_name": "Chase (Government)"},
    {"category": "Government", "toggle_name": "FHA"},
    {"category": "Government", "toggle_name": "Freedom Mortgage (Government)"},
    {"category": "Government", "toggle_name": "Mr Cooper (Government)"},
    {"category": "Government", "toggle_name": "NewRez (Government)"},
    {"category": "Government", "toggle_name": "NexBank (Government)"},
    {"category": "Government", "toggle_name": "Penny Mac (Government)"},
    {"category": "Government", "toggle_name": "PHH (Government)"},
    {"category": "Government", "toggle_name": "Plaza Home (Government)"},
    {"category": "Government", "toggle_name": "Truist (Government)"},
    {"category": "Government", "toggle_name": "USDA"},
    {"category": "Government", "toggle_name": "VA"},
    {"category": "Government", "toggle_name": "Village Capital"},


    # Jumbo CATEGORY
    {"category": "Jumbo", "toggle_name": "AFCU Broker"},
    {"category": "Jumbo", "toggle_name": "Ameri Home (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Bayview (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Chase (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Dollar Bank (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Maxex (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "NewRez (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "NewRez (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Plaza Home (Jumbo)"},
    {"category": "Jumbo", "toggle_name": "Truist (Jumbo)"},

    #Non-QM CATEGORY
    {"category": "Non-QM", "toggle_name": "Ameri Home (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "Bayview (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "Chase (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "Maxex (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "Mr Cooper (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "NewRez (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "NexBank (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "PHH (Non-QM)"},
    {"category": "Non-QM", "toggle_name": "Plaza Home (Non-QM)"},

   # Portfolio CATEGORY
   {"category": "Portfolio", "toggle_name": "Portfolio"},
]

class TestChatbotFSB:


    @pytest.fixture(autouse=True)
    def attach_fixtures(self, driver, loginfsbbeta):
        """Automatically passes the authenticated driver to all tests."""
        self.__class__.driver = driver

    @pytest.mark.parametrize(
        "guideline",
        ALL_GUIDELINES,
        ids=lambda g: f"{g['category']}::{g['toggle_name']}"
    )
    def test_response_with_chatbot(self,guideline):
        fsb_beta_page = ChatbotFsbBetaPage(self.driver)
        category = guideline["category"]
        toggle_label = guideline["toggle_name"]

        self.driver.refresh()
        fsb_beta_page.wait_for_url_contains("chat")

        category_actions = {
            "Conforming": fsb_beta_page.click_confirmation_guideline_selection,
            "Government": fsb_beta_page.click_government_guideline_selection,
            "Jumbo": fsb_beta_page.click_jumbo_guideline_selection,
            "Non-QM": fsb_beta_page.click_non_qm_guideline_selection,
            "Portfolio": fsb_beta_page.click_portfolio_guideline_selection,
        }

        # Dynamically fetch and execute the corresponding action
        action = category_actions.get(category)
        if action:
            action()
        else:
            # For your other 4 sections, you should add your click_XX_selection() methods
            # in chatbot_evergreenberta.py and call them here!
            raise NotImplementedError(f"Add the click method for category: {category}")

        fsb_beta_page.click_chatbot_toggle(toggle_label)
        random_input = generate_dynamic_chat_message()

        # 4. Message the bot
        fsb_beta_page.enter_guideline_message(random_input)
        fsb_beta_page.click_submit_btn()

        # 5. Get the user payload verification
        response = fsb_beta_page.wait_for_response()

        print("This is Response in Chatbot=="+response)
        assert response, "❌ Empty user message logged in chat window"


        forbidden_keywords = ["Unauthorized", "Invalid", "error creating session",
                              "Invalid API key. Please provide a valid API key and try again.","network error"]
        for word in forbidden_keywords:
            assert word not in response, f"Forbidden word found: {word}"


