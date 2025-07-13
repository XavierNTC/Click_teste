import mysql.connector
from datetime import datetime
import pandas as pd

# Nova conexão MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_click"
    )

# Inserir etiqueta (equivalente à antiga bipagem)
def inserir_etiqueta(codigo, nota_id):
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = """
    INSERT INTO Etiqueta_02 (A02_codigo, A02_data, Notafiscal_01_A01_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (codigo, data_atual, nota_id))
    conn.commit()
    cursor.close()
    conn.close()

# Obter todas as etiquetas
def obter_etiquetas():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM Etiqueta_02", conn)
    conn.close()
    return df

# Excluir etiquetas duplicadas (mantém apenas a primeira por código)
def excluir_duplicados_etiquetas():
    conn = conectar()
    cursor = conn.cursor()

    query = """
    DELETE e1 FROM Etiqueta_02 e1
    INNER JOIN Etiqueta_02 e2 
    WHERE 
        e1.A02_codigo = e2.A02_codigo AND 
        e1.A02_id > e2.A02_id
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
