from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Initialize Chrome driver
service = Service()
driver = webdriver.Chrome(service=service)

# Maximize window
driver.maximize_window()

# Open website
driver.get("https://practice.expandtesting.com/checkboxes")

# Find checkboxes
elements = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

# Click all checkboxes
for checkbox in elements:
    checkbox.click()

time.sleep(5)

# Close browser
driver.quit()