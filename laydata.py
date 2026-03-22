from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, Comment

service = Service(r"D:\sieurac\edgedriver_win64\msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get("https://youtube.com")

search=driver.find_element(By.NAME,"search_query")
search.send_keys("zweihander")
search.send_keys(Keys.RETURN)
try:
    textt=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"style-scope ytd-search"))
    )
    textt=driver.find_element(By.CLASS_NAME,"style-scope ytd-search")
    print(textt.text)
except:
    driver.quit()
input()