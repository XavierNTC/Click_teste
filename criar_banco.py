import sqlite3

conn = sqlite3.connect("bipagens.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bipagem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    hora TEXT NOT NULL
)
""")

conn.commit()
conn.close()
