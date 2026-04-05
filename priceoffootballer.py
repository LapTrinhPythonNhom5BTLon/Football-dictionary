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

conn.commit()





with SB(uc=True) as sb:

    sb.open("https://www.footballtransfers.com/en/search")

    for row in rows:

        sb.type('input[name="search_value"]', f"{str(*row)}\n")

        sb.wait_for_element(f'a[title="{str(*row)}"]', timeout=7)

        html=sb.get_page_source()

        soup=BeautifulSoup(html,"html.parser")

        cauthu=soup.find("a",{"title":str(*row)})

        pri=''  

        if cauthu:

            pri=cauthu.find("div",{"class":"player-price"}).find("span",{"class":"player-tag"}).text

            

        else:

            pri="N/A"

        curs.execute("""

            INSERT INTO prices VALUES (?,?)

            """, (

                str(*row),

                pri

            ))

        conn.commit()

    conn.close()