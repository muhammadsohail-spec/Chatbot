import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.chatbot import ChatpotPage
from selenium.webdriver.support import expected_conditions as EC



class ChatbotEvergreenBetaPage(ChatpotPage):

    GUIDELINE_SELECTION_CONFIRMATION=(By.XPATH,"(//button[@type='button'])[4]")
    GUIDELINE_SELECTION_GOVERNMENT = (By.XPATH, "(//button[@type='button'])[12]")
    GUIDELINE_SELECTION_JUMBO_NON_CONFIRMING = (By.XPATH, "(//button[@type='button'])[19]")
    GUIDELINE_SELECTION_NON_QM = (By.XPATH, "(//button[@type='button'])[31]")
    GUIDELINE_SELECTION_CONSTRUCTION = (By.XPATH, "(//button[@type='button'])[35]")
    GUIDELINE_SELECTION_PORTFOLIO = (By.XPATH, "(//button[@type='button'])[42]")
    GUIDELINE_SELECTION_HELOC = (By.XPATH, "(//button[@type='button'])[44]")

    # Confirming Chatbot locaters
    # Note: Hardcoded locators have been removed in favor of dynamic generation using parameterized f-strings.


    # Change icon Locaters
    CHANGE=(By.XPATH,"//span[normalize-space()='Change']")


    # CROSS_BTN = (By.XPATH,"")
    CROSS_BTN = (By.XPATH,"(//button[contains(@class, 'ring-offset-background') and contains(@class, 'absolute') and contains(@class, 'top-4') and contains(@class, 'right-4')])[1]")
    MESSAGE=(By.XPATH,"//textarea[@placeholder='Ask me anything about mortgage guidelines...']")

    chat_message=(By.CSS_SELECTOR,"div[class='chat-message']")

    def click_confirmation_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_CONFIRMATION)
            self.click(self.GUIDELINE_SELECTION_CONFIRMATION)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_government_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_GOVERNMENT)
            self.click(self.GUIDELINE_SELECTION_GOVERNMENT)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_jubmo_now_confirming_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_JUMBO_NON_CONFIRMING)
            self.click(self.GUIDELINE_SELECTION_JUMBO_NON_CONFIRMING)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")


    def click_non_qm_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_NON_QM)
            self.click(self.GUIDELINE_SELECTION_NON_QM)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_construction_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_CONSTRUCTION)
            self.click(self.GUIDELINE_SELECTION_CONSTRUCTION)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_portfolio_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_PORTFOLIO)
            self.click(self.GUIDELINE_SELECTION_PORTFOLIO)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_heloc_guideline_selection(self):
        try:
            self.wait_for_visibility(self.GUIDELINE_SELECTION_HELOC)
            self.click(self.GUIDELINE_SELECTION_HELOC)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_cross_btn(self):
        try:
            self.wait_for_visibility(self.CROSS_BTN)
            self.click(self.CROSS_BTN)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def click_change_btn(self):
        try:
            self.wait_for_visibility(self.CHANGE)
            element = self.driver.find_element(*self.CHANGE)
            self.driver.execute_script("arguments[0].click();", element)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")


    def click_chatbot_toggle(self, toggle_label: str):
        locator = (By.XPATH, f"//button[@aria-label='Toggle {toggle_label}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"button not clickable: {e}")

    def enter_guideline_message(self, message):
        try:
            self.wait_for_visibility(self.MESSAGE)
            self.enter_text(self.MESSAGE, message)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Password field not found: {e}")

    def get_last_response1(self):
        try:
            messages = self.driver.find_elements(*self.chat_message)
            return messages[-1].text if messages else ""
        except Exception as e:
            print(f"[ERROR] Cannot get messages: {e}")
            return ""

    def wait_for_response(self, timeout=40):
        """Wait for a new message to appear and finish streaming"""
        old_len = len(self.driver.find_elements(*self.chat_message))
        for _ in range(10):  # Give it 10 seconds to start replying
            time.sleep(1)
            new_len = len(self.driver.find_elements(*self.chat_message))
            if new_len > old_len:
                break

        # Wait for the response text to stabilize (stop streaming)
        stable_count = 0
        last_text = ""
        for _ in range(timeout):
            current_text = self.get_last_response1()
            if current_text and current_text == last_text:
                stable_count += 1
                if stable_count >= 3:  # 3 seconds without change -> stream complete
                    break
            else:
                last_text = current_text
                stable_count = 0
            time.sleep(1)

        return self.get_last_response1()

