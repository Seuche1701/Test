import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / 'data.db'


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        balance REAL DEFAULT 0
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        amount REAL DEFAULT 0,
        due_date TEXT,
        recurring INTEGER DEFAULT 0,
        done INTEGER DEFAULT 0,
        FOREIGN KEY(child_id) REFERENCES children(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        task_id INTEGER,
        amount REAL,
        timestamp TEXT,
        note TEXT,
        FOREIGN KEY(child_id) REFERENCES children(id),
        FOREIGN KEY(task_id) REFERENCES tasks(id)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
