import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "quest_master.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        difficulty TEXT CHECK(difficulty IN ('Легкий','Средний','Сложный','Эпический')),
        reward INTEGER,
        description TEXT,
        deadline TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quest_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quest_id INTEGER,
        title TEXT,
        difficulty TEXT,
        reward INTEGER,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (quest_id) REFERENCES quests(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quest_id INTEGER,
        x REAL,
        y REAL,
        type TEXT,
        label TEXT,
        FOREIGN KEY (quest_id) REFERENCES quests(id)
    )
    """)
    
    conn.commit()
    conn.close()

def save_quest(data):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id FROM quests WHERE title = ?", (data['title'],))
        row = cur.fetchone()
        
        if row:
            quest_id = row['id']
            cur.execute("""
                UPDATE quests SET difficulty=?, reward=?, description=?, deadline=?
                WHERE id=?
            """, (data['difficulty'], data['reward'], data['description'], data['deadline'], quest_id))
        else:
            cur.execute("""
                INSERT INTO quests (title, difficulty, reward, description, deadline)
                VALUES (?, ?, ?, ?, ?)
            """, (data['title'], data['difficulty'], data['reward'], data['description'], data['deadline']))
            quest_id = cur.lastrowid

        cur.execute("""
            INSERT INTO quest_versions (quest_id, title, difficulty, reward, description)
            VALUES (?, ?, ?, ?, ?)
        """, (quest_id, data['title'], data['difficulty'], data['reward'], data['description']))

        conn.commit()
        return quest_id
    except Exception as e:
        print(f"DB Error: {e}")
        return None
    finally:
        conn.close()

def get_quest_by_title(title):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM quests WHERE title = ?", (title,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def add_location(quest_id, x, y, l_type, label):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO locations (quest_id, x, y, type, label) VALUES (?, ?, ?, ?, ?)",
                (quest_id, x, y, l_type, label))
    conn.commit()
    conn.close()

def delete_last_location(quest_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM locations WHERE quest_id = ? ORDER BY id DESC LIMIT 1", (quest_id,))
    row = cur.fetchone()
    if row:
        cur.execute("DELETE FROM locations WHERE id = ?", (row[0],))
        conn.commit()
    conn.close()

init_db()
