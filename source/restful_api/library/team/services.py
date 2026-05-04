import os
import sqlite3

def get_team_data(name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(cur_dir, "../../../players.db"))
    
    conn = sqlite3.connect(db_path)
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM players WHERE team = ?"
    cursor.execute(query, (name,))
    
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]