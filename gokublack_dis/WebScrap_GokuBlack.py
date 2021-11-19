from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
import Main
PATH = r"/home/master/discord/chromedriver"
# Path to the ChromeDriver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=PATH, options=options)
driver.get(
    "https://twitter.com/search?q=%23DBFZ_BLK&src=typed_query&f=live")
# Opens the intented twitter URL of Goku Black!
def get_links():
    ls = list()
    try:
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//video[contains(@preload,'none')]//ancestor::article[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/a")))
        # Extracts the links of the tweets with videos(*this my be invalid one day) through an XPATH
        with open("TwitterLinks_GokuBlack.txt", 'w') as file:
            for link in links:
                file.write(link.get_attribute('href') + '\n')
                ls.append(link.get_attribute('href') + '\n')
        # Writes/OverWrites the links into a file
        return ls
    except:
        driver.quit()
        return 'nothing'


original = get_links()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")


print('got links in ' + current_time)

Main.char(890631861099970631,"/home/master/discord/TwitterLinks_GokuBlack.txt")

Main.client.run(os.getenv('TOKEN'))