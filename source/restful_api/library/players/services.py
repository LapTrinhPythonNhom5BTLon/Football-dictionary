import sqlite3
import os

def get_player_data(name):
    cur_dir = os.path.dirname(os.path.abspath(__file__)) # duong dan services.py
    db_path = os.path.abspath(os.path.join(cur_dir, "../../../players.db")) # tao duong dan toi players.db
    
    conn = sqlite3.connect(db_path)
    
    conn.row_factory = sqlite3.Row # dinh hinh ket qua sau truy van
    cursor = conn.cursor()
    
    query = "SELECT * FROM players WHERE player = ?"
    cursor.execute(query, (name,))
    
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]