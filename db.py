import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'expense_manager.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def add_expense(description, amount, type):
    try:
        cursor.execute('''
            INSERT INTO expenses (description, amount, type) VALUES (?, ?, ?)
        ''', (description, amount, type))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print('Error adding expense:', e)
        conn.rollback()
        return None

def get_all_expenses():
    try:
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print('Error fetching expenses:', e)
        return []

def close_connection():
    conn.close()
  