from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
PATH = r"C:\Users\yuval\Desktop\Python projects\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(
    "https://twitter.com/search?q=%23DBFZ_A17&src=recent_search_click&f=live")
try:
    article = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "article")))
    # print(article.text)
    try:
        video = WebDriverWait(article, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        url = WebDriverWait(article, 10).until(EC.presence_of_element_located((By.XPATH, './/a[]'))) 
    except:
    
except NoSuchElementException:
    driver.quit()
