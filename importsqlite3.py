import sqlite3
from laydata import get_players

# tạo bảng
def create_table():
    conn = sqlite3.connect("players.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS players")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player TEXT,
        nationality TEXT,
        position TEXT,
        team TEXT,
        age TEXT,
        birth_year TEXT,
        games TEXT,
        games_starts TEXT,
        minutes INTEGER,
        goals TEXT,
        assists TEXT,
        goals_assists_pens_per90 TEXT,
        goals_pens_per90 TEXT,
        goals_assists_per90 TEXT,
        assists_per90 TEXT,
        goals_per90 TEXT,
        cards_red TEXT,
        cards_yellow TEXT,
        pens_att TEXT,
        pens_made TEXT,
        goals_pens TEXT,
        goals_assists TEXT,
        minutes_90s TEXT
    )
    """)

    conn.commit()
    conn.close()


# insert dữ liệu
def insert_data(players):
    conn = sqlite3.connect("players.db")
    cursor = conn.cursor()

    for p in players:
        cursor.execute("""
        INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            p["player"], p["nationality"], p["position"], p["team"],
            p["age"], p["birth_year"], p["games"], p["games_starts"],
            int(p["minutes"].replace(",", "")),
            p["goals"], p["assists"],
            p["goals_assists_pens_per90"], p["goals_pens_per90"],
            p["goals_assists_per90"], p["assists_per90"], p["goals_per90"],
            p["cards_red"], p["cards_yellow"],
            p["pens_att"], p["pens_made"],
            p["goals_pens"], p["goals_assists"],
            p["minutes_90s"]
        ))

    conn.commit()
    conn.close()


# chạy chính
if __name__ == "__main__":
    
    create_table()
    data = get_players()
    insert_data(data)
    print("Đã lưu dữ liệu vào SQLite!")