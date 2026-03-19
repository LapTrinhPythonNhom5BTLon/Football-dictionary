from selenium import webdriver
from selenium.webdriver.edge.service import Service

service = Service("D:\sieurac\edgedriver_win64\msedgedriver.exe")  # sửa path

driver = webdriver.Edge(service=service)

driver.get("https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats")

print(len(driver.page_source))