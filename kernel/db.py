import sqlite3

from kernel.config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database(db_file=DB_PATH):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            contrasena TEXT,
            rol TEXT
        )
    ''')
    conn.commit()
    conn.close()
