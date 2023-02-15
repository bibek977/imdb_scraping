from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

from selenium.webdriver.chrome.options import Options

# To parse the data from utilites
import configparser
config = configparser.ConfigParser()
config.read("Utilities/data.properties")


# to Headless
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(config.get("Urls", "base_url"))
time.sleep(2)

search_movie = driver.find_element(By.XPATH,config.get("Xpath", "search_path"))
search_movie.send_keys(config.get("Credentials", "search_movie"))
time.sleep(2)

driver.find_element(By.XPATH,"//button[@id='suggestion-search-button']//*[name()='svg']").click()
time.sleep(2)

# movie_name = driver.find_elements(By.XPATH,config.get("Xpath", "suggestion_movie_title_path"))
# movie_year = driver.find_elements(By.XPATH,config.get("Xpath", "suggestion_movie_year_path"))

movie_list = driver.find_elements(By.XPATH, config.get("Xpath", "searched_movies"))

for i in movie_list:
    if "Ben Affleck" in i.text:
        i.click()
        break
    else:
        print('Not Found')
time.sleep(2)

current_url = driver.current_url
movie_trailor = driver.find_element(By.XPATH,"//a[@class='ipc-lockup-overlay sc-e4a5af48-0 gOsOae ipc-focusable']").get_attribute('href')
movie_name = driver.find_element(By.XPATH,"//div[@class='sc-b5e8e7ce-1 kNhUtn']/h1").text
movie_type = [driver.find_element(By.XPATH,"//div[@class='ipc-chip-list__scroller']").text]
movie_summary = driver.find_element(By.XPATH,"//div[@class='sc-663f405c-4 hQbEKe']//p[@data-testid='plot']").text
movie_casts = driver.find_elements(By.XPATH,"//section[@data-testid='title-cast']/div[@role='group']//div[@data-testid='title-cast-item']")

movie_cast = []
for cast in movie_casts:
    movie_cast.append(cast.text)

data = f"""page url = {current_url}

movie name = {movie_name}

movie trailor = {movie_trailor}

movie type = {movie_type}

movie summary = {movie_summary}

movie cast = {movie_cast}
"""

with open(f"{movie_name}.txt", "w") as f:
    f.write(data)

driver.quit()