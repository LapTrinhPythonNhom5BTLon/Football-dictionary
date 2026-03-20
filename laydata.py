from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, Comment

service = Service(r"D:\sieurac\edgedriver_win64\msedgedriver.exe")

options = Options()
options.add_argument(r"user-data-dir=D:\edge_profile_test")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Edge(service=service, options=options)

driver.get("https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats")

print("⏳ Đợi Cloudflare verify...")

# 🔥 CHỜ khi element thật xuất hiện
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

# ⚠️ check thêm: phải KHÔNG còn chữ "Just a moment"
WebDriverWait(driver, 30).until_not(
    EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Just a moment")
)

print("✅ Đã vào trang thật")

html = driver.page_source

# ===== parse =====
soup = BeautifulSoup(html, "html.parser")

comments = soup.find_all(string=lambda text: isinstance(text, Comment))

table = None

for c in comments:
    if "stats_standard" in c:
        soup2 = BeautifulSoup(c, "html.parser")
        table = soup2.find("table_container is_setup")
        break

if table:
    print("✅ Lấy được bảng!")
    print(table.text[:500])
else:
    print("❌ Vẫn chưa có bảng")

driver.quit()