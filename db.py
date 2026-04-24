import sqlite3

def get_connection():
    return sqlite3.connect("finance.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # movimentações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        value REAL,
        category TEXT,
        type TEXT, -- receita ou despesa
        date TEXT
    )
    """)

    conn.commit()
    conn.close()