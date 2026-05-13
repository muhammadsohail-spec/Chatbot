

import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from pages.chatbot import ChatpotPage
from selenium.webdriver.support import expected_conditions as EC

from pages.chatbot_evergreenberta import ChatbotEvergreenBetaPage


class ChatbotdsldBetaPage(ChatbotEvergreenBetaPage):


    GUIDELINE_SELECTION_CONFIRMATION = (By.XPATH, "//h3[normalize-space()='Conforming']")