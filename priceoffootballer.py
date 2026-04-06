import sqlite3
from seleniumbase import SB

from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import time



conn=sqlite3.connect('players.db')

curs=conn.cursor()

curs.execute("SELECT player FROM players")

rows=curs.fetchall()

curs.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        player TEXT,
        price TEXT
    )
""")

curs.execute("SELECT player FROM players")
rows = curs.fetchall()
conn.commit()

with SB(uc=True) as sb:
    sb.open("https://www.footballtransfers.com/en/search")
    
    for row in rows:
        player_name = str(row[0]).strip()
        print(f"Đang tìm giá cho: {player_name}")
        
        sb.type('input[name="search_value"]', f"{player_name}\n")
        
        pri = 'N/A'
        try:
            player_link_selector = f'a[title*="{player_name}"]'
            
            sb.wait_for_element(player_link_selector, timeout=7)
            
            price_selector = f'{player_link_selector} .player-price .player-tag'
            
            if sb.is_element_present(price_selector):
                pri = sb.get_text(price_selector).strip()
            else:
                pri = sb.get_text(f'{player_link_selector} .player-price').strip()
                
        except Exception:
            pri = 'N/A'
        
        print(f"-> Kết quả: {pri}")

        curs.execute("INSERT INTO prices (player, price) VALUES (?, ?)", (player_name, pri))
        conn.commit()

conn.close()
print("Hoàn thành!")