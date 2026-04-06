import requests
import sqlite3

conn=sqlite3.connect('players.db')

curs=conn.cursor()

curs.execute("SELECT player FROM players")

rows=curs.fetchall()
curs.execute("DROP TABLE IF EXISTS prices")

curs.execute("""

    CREATE TABLE IF NOT EXISTS prices (

        player TEXT,

        price TEXT

    )

    """)

conn.commit()

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price(name):
    url = f"https://www.footballtransfers.com/en/search?q={name}"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data[0]['transfer_value']
    except:
        return 'N/A'

def run(rows):
    for row in rows:
        name = str(*row)
        pri = get_price(name)
        curs.execute("""
            INSERT INTO prices VALUES (?,?)
        """, (name, pri))
    conn.commit()

run(rows)
conn.close()