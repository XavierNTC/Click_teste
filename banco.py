import sqlite3
from datetime import datetime
import pandas as pd

def conectar():
    return sqlite3.connect("bipagens.db")

def inserir_bipagem(codigo):
    conn = conectar()
    cursor = conn.cursor()
    hora = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO bipagem (codigo, hora) VALUES (?, ?)", (codigo, hora))
    conn.commit()
    conn.close()

def obter_bipagens():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM bipagem", conn)
    conn.close()
    return df
