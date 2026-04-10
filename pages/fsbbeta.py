import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.chatbot import ChatpotPage
from selenium.webdriver.support import expected_conditions as EC



class ChatbotFsbBetaPage(ChatpotPage):

    def click_chatbot_toggle(self, toggle_label: str):
        locator = (By.XPATH, f"//button[@aria-label='Toggle {toggle_label}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")