import pandas as pd
from db import get_connection

def add_transaction(user_id, name, value, category, type_, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions 
        (user_id, name, value, category, type, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, name, value, category, type_, date))

    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
        conn,
        params=(user_id,)
    )
    conn.close()
    return df

def delete_transaction(id_):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (id_,))
    conn.commit()
    conn.close()