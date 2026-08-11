import sqlite3
import json
from config import settings
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            chunks_used TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_query(question: str, answer: str, chunks_used: list):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO queries (question, answer, chunks_used, timestamp) VALUES (?, ?, ?, ?)',
        (question, answer, json.dumps(chunks_used), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_history(limit: int = 10):
    conn = get_db_connection()
    cursor = conn.execute(
        'SELECT * FROM queries ORDER BY timestamp DESC LIMIT ?', (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row["id"],
            "question": row["question"],
            "answer": row["answer"],
            "chunks_used": json.loads(row["chunks_used"]),
            "timestamp": row["timestamp"]
        })
    return history
