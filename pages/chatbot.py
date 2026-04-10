
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import generate_unique_email


class ChatpotPage(BasePage):


  SELECT_LENDER_PARTNER=(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(2) > main:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > div:nth-child(1)")
  SELECT_GUIDELINE = (By.XPATH, "/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[2]/div[1]")
  SELECT_GUIDELINE_select_all=(By.XPATH,"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]")
  SELECT_GUIDELINE_option1=(By.XPATH,"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]")
  SELECT_GUIDELINE_option2=(By.XPATH,"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]")
  MESSAGE_GUIDELINE_BUDDY=(By.XPATH,"//textarea[@placeholder='Message Guideline Buddy...']")
  SELECT_LENDER_PARTNER_OPTION1=(By.XPATH,"//span[normalize-space()='New Beta']")
  SELECT_LENDER_PARTNER_OPTION2 = (By.XPATH, "//span[normalize-space()='Reverse Mortgages (HECMs)']")
  SELECT_LENDER_PARTNER_OPTION3 = (By.XPATH, "//span[normalize-space()='Snmc test bots']")
  SELECT_LENDER_PARTNER_OPTION4 = (By.XPATH, "//span[normalize-space()='Truist']")
  SELECT_LENDER_PARTNER_OPTION5 = (By.XPATH, "//span[normalize-space()='xyz']")

  Click_lender_guideline_selection=(By.XPATH,"/html[1]/body[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]")

  SUBMIT_BUTTON=(By.XPATH,"//button[@type='submit']")
  ERROR_MESSAGE=(By.XPATH,"//*[normalize-space()='Unauthorized']")
  ERROR_MESSAGE2 = (By.XPATH, "//div[contains(text(),'Error creating session')]")

  LATEST_RESPONSE=(By.XPATH,"//div[@class='chat-message']")

  def click_select_lender_partner(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER)
          self.click(self.SELECT_LENDER_PARTNER)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def click_lender_and_guidelines_selection(self):
      try:
          self.wait_for_visibility(self.Click_lender_guideline_selection)
          self.click(self.Click_lender_guideline_selection)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option1(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION1)
          self.click(self.SELECT_LENDER_PARTNER_OPTION1)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option2(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION2)
          self.click(self.SELECT_LENDER_PARTNER_OPTION2)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option3(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION3)
          self.click(self.SELECT_LENDER_PARTNER_OPTION3)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option4(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION4)
          self.click(self.SELECT_LENDER_PARTNER_OPTION4)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option5(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION5)
          self.click(self.SELECT_LENDER_PARTNER_OPTION5)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def click_guideline(self):
      try:
          self.wait_for_visibility(self.SELECT_GUIDELINE)
          self.click(self.SELECT_GUIDELINE)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")


  def select_guidelines_option1(self):
      try:
          self.wait_for_visibility(self.SELECT_GUIDELINE_option1)
          self.click(self.SELECT_GUIDELINE_option1)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_guidelines_all(self):
      try:
          self.wait_for_visibility(self.SELECT_GUIDELINE_select_all)
          self.click(self.SELECT_GUIDELINE_select_all)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_guidelines_option2(self):
      try:
          self.wait_for_visibility(self.SELECT_GUIDELINE_option2)
          self.click(self.SELECT_GUIDELINE_option2)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def enter_guideline_message(self, message):
      try:
          self.wait_for_visibility(self.MESSAGE_GUIDELINE_BUDDY)
          self.enter_text(self.MESSAGE_GUIDELINE_BUDDY, message)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"Password field not found: {e}")

  def click_submit_btn(self):
      try:
          self.wait_for_visibility(self.SUBMIT_BUTTON)
          self.click(self.SUBMIT_BUTTON)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def get_error_message(self):
      return self.get_text(self.ERROR_MESSAGE)

  def get_error_message2(self):
      return self.get_text(self.ERROR_MESSAGE2)

  def get_latest_response(self,) -> str:
      elements = self.wait.until(
          EC.presence_of_all_elements_located(self.LATEST_RESPONSE)
      )
      return elements[-1].text.strip()

  def wait_for_response(self, timeout=40):
      """Wait for a new message to appear and finish streaming"""
      old_len = len(self.driver.find_elements(*self.LATEST_RESPONSE))
      for _ in range(10):  # Give it 10 seconds to start replying
          import time
          time.sleep(1)
          new_len = len(self.driver.find_elements(*self.LATEST_RESPONSE))
          if new_len > old_len:
              break

      # Wait for the response text to stabilize (stop streaming)
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
          import time
          time.sleep(1)

      return self.get_latest_response()
