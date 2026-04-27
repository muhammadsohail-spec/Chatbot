import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

logger = get_logger("ChatbotPage")

class ChatpotPage(BasePage):
    # Core Dropdown Locators
    SELECT_LENDER_PARTNER = (By.XPATH,"/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]")
    SELECT_GUIDELINE = (By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[2]")

    SELECT_GUIDELINE_select_all = (By.XPATH,"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]")
    
    # Interaction Locators
    MESSAGE_GUIDELINE_BUDDY = (By.XPATH,"//textarea[@placeholder='Message Guideline Buddy...']")
    Click_lender_guideline_selection = (By.XPATH,"//button[@class='flex w-full items-center justify-between gap-2 rounded-lg border px-3 py-2.5 text-left text-sm transition-colors hover:opacity-95 sm:py-3']")
    SUBMIT_BUTTON = (By.XPATH,"//button[@type='submit']")
    
    # Verification Locators
    ERROR_MESSAGE = (By.XPATH,"//*[normalize-space()='Unauthorized']")
    ERROR_MESSAGE2 = (By.XPATH, "//div[contains(text(),'Error creating session')]")
    LATEST_RESPONSE = (By.XPATH,"//div[@class='prose prose-p:my-2 prose-ul:my-2 prose-ol:my-2 max-w-none chat-message']")

    def click_select_lender_partner(self):
        try:
            self.wait_for_visibility(self.SELECT_LENDER_PARTNER)
            self.click(self.SELECT_LENDER_PARTNER)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Select Lender button not clickable: {e}")

    def click_lender_and_guidelines_selection(self):
        try:
            self.wait_for_visibility(self.Click_lender_guideline_selection)
            self.click(self.Click_lender_guideline_selection)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Guideline selection button not clickable: {e}")

    # -------------------------------------------------------------
    # SENIOR BEST PRACTICE: DYNAMIC LOCATORS
    # Replaces 5 duplicate hardcoded methods with 1 robust method
    # -------------------------------------------------------------
    def select_lender_partner_option_by_name(self, option_name: str):
        locator = (By.XPATH, f"//span[normalize-space()='{option_name}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Partner Option '{option_name}' not clickable: {e}")

    def click_guideline(self):
        try:
            self.wait_for_visibility(self.SELECT_GUIDELINE)
            self.click(self.SELECT_GUIDELINE)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Guideline button not clickable: {e}")

    def select_guidelines_all(self):
        try:
            self.wait_for_visibility(self.SELECT_GUIDELINE_select_all)
            self.click(self.SELECT_GUIDELINE_select_all)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Select All Guidelines button not clickable: {e}")

    def select_guidelines_option_by_index(self, index: int):
        # Dynamically matches the specific option dropdown structure you had
        locator = (By.XPATH, f"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[{index + 1}]/div[1]")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Guideline index {index} not clickable: {e}")

    def enter_guideline_message(self, message):
        try:
            self.wait_for_visibility(self.MESSAGE_GUIDELINE_BUDDY)
            self.enter_text(self.MESSAGE_GUIDELINE_BUDDY, message)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Message input field not found: {e}")

    def click_submit_btn(self):
        try:
            self.wait_for_visibility(self.SUBMIT_BUTTON)
            self.click(self.SUBMIT_BUTTON)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Submit button not clickable: {e}")

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def get_error_message2(self):
        return self.get_text(self.ERROR_MESSAGE2)

    def get_alert_text_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()  # or alert.dismiss() if needed
            return alert_text

        except NoAlertPresentException:
            return None

    def click_chatbot_toggle(self, toggle_label: str):
        locator = (By.XPATH, f"//button[@aria-label='Toggle {toggle_label}']")
        try:
            self.wait_for_visibility(locator)
            self.click(locator)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Toggle button not clickable for {toggle_label}: {e}")
            raise

    def get_latest_response(self) -> str:
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(self.LATEST_RESPONSE))
            return elements[-1].text.strip()
        except:
            return ""

    def wait_for_response(self, timeout=20):
        """Wait for a new message to appear and finish streaming"""
        old_len = len(self.driver.find_elements(*self.LATEST_RESPONSE))

        for _ in range(10):  # Give it 10 seconds to start replying
            time.sleep(1)

            # --- HANDLE ALERTS & ERRORS ---
            # 1. Check for Javascript Alert
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                return f"ALERT_FOUND: {alert_text}"
            except Exception:
                pass

            # 2. Check for "Error creating session" or "Unauthorized" in DOM
            error2_elements = self.driver.find_elements(*self.ERROR_MESSAGE2)
            if error2_elements and error2_elements[0].is_displayed():
                return f"ERROR_FOUND: {error2_elements[0].text}"

            error1_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            if error1_elements and error1_elements[0].is_displayed():
                return f"ERROR_FOUND: {error1_elements[0].text}"
            # ------------------------------

            new_len = len(self.driver.find_elements(*self.LATEST_RESPONSE))
            if new_len > old_len:
                break

        # Wait for the response text to stabilize
        stable_count = 0
        last_text = ""
        for _ in range(timeout):
            current_text = self.get_latest_response()
            if current_text and current_text == last_text:
                stable_count += 1
                if stable_count >= 3:  # 3 seconds without change -> stream complete
                    break
            else:
                last_text = current_text
                stable_count = 0
            time.sleep(1)

        return self.get_latest_response()
