import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.chatbot import ChatpotPage
from selenium.webdriver.support import expected_conditions as EC

from pages.chatbot_evergreenberta import ChatbotEvergreenBetaPage


class ChatbotFsbBetaPage(ChatbotEvergreenBetaPage):
    GUIDELINE_SELECTION_CONFIRMATION = (By.XPATH, "(//button[@type='button'])[4]")
    GUIDELINE_SELECTION_GOVERNMENT = (By.XPATH, "(//button[@type='button'])[27]")
    GUIDELINE_SELECTION_JUMBO_NON_CONFIRMING = (By.XPATH, "(//button[@type='button'])[46]")
    GUIDELINE_SELECTION_NON_QM = (By.XPATH, "(//button[@type='button'])[57]")
    GUIDELINE_SELECTION_PORTFOLIO = (By.XPATH, "(//button[@type='button'])[42]")
    GUIDELINE_SELECTION_HELOC = (By.XPATH, "(//button[@type='button'])[44]")

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



    def switch_to_new_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])