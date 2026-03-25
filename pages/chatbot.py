
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from utils.helpers import generate_unique_email


class ChatpotPage(BasePage):


  SELECT_LENDER_PARTNER=(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(2) > main:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > div:nth-child(1)")
  SELECT_guideline = (By.XPATH, "//button[@aria-controls='radix-_r_8_']")
  MESSAGE_GUIDELINE_BUDDY=(By.XPATH,"//textarea[@placeholder='Message Guideline Buddy...']")
  SELECT_LENDER_PARTNER_OPTION=(By.XPATH,"//span[normalize-space()='Reverse Mortgages (HECMs)']")
  SUBMIT_BUTTON=(By.XPATH,"//button[@type='submit']")
  ERROR_MESSAGE=(By.XPATH,"//*[normalize-space()='Unauthorized']")

  def click_select_lender_partner(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER)
          self.click(self.SELECT_LENDER_PARTNER)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def select_lender_partner_option(self):
      try:
          self.wait_for_visibility(self.SELECT_LENDER_PARTNER_OPTION)
          self.click(self.SELECT_LENDER_PARTNER_OPTION)
      except (TimeoutException, NoSuchElementException) as e:
          print(f"button not clickable: {e}")

  def click_guideline(self):
      try:
          self.wait_for_visibility(self.SELECT_guideline)
          self.click(self.SELECT_guideline)
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
