from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
PATH = r"C:\Users\yuval\Desktop\Python projects\chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)
driver.get(
    "https://twitter.com/search?q=%23DBFZ_BGK&src=typed_query&f=live")
actions = ActionChains(driver)
try:
  element = WebDriverWait(driver, 10).until(
              EC.presence_of_all_elements_located((By.XPATH, "//span[text()='View']//ancestor::div[contains(@role,'button')]")))
  print(element.get_attribute('class'))
except:
  driver.quit()



