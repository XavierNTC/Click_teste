import sqlite3

conn = sqlite3.connect("bipagens.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM bipagem")
registros = cursor.fetchall()

for linha in registros:
    print(linha)

conn.close()