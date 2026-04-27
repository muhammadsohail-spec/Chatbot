import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.chatbot import ChatpotPage
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from pages.chatbot_evergreenberta import ChatbotEvergreenBetaPage
logger = get_logger("ChatbotPage")

class ChatbotFsbBetaPage(ChatbotEvergreenBetaPage,BasePage):

    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    def click_chatbot_toggle(self, toggle_label: str):
        locator = (By.XPATH, f"//button[@aria-label='Toggle {toggle_label}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")
            print(f"button not clickable: {e}")

    def click_chatbot_category(self, category_label: str):
        locator = (By.XPATH, f"//button[@aria-label='Toggle {category_label}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")
            print(f"button not clickable: {e}")

    def open_link(self, url):
        self.driver.execute_script("window.open(arguments[0]);", url)


    def click_submit_btn(self):
        try:
            self.wait_for_visibility(self.SUBMIT_BUTTON)
            self.click(self.SUBMIT_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Submit button not clickable: {e}")



    def switch_to_new_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])