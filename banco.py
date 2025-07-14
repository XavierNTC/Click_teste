import mysql.connector
from datetime import datetime
import pandas as pd

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Altere se necessário
        password="",        # Altere se necessário
        database="db_click"
    )

def inserir_etiqueta(codigo, nota_id):
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
        INSERT INTO etiqueta_02 (codigo, A02_data, Notafiscal_01_A01_id)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (codigo, data_atual, nota_id))
    conn.commit()
    cursor.close()
    conn.close()

def obter_etiquetas():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM etiqueta_02", conn)
    conn.close()
    return df

def excluir_duplicados_etiquetas():
    conn = conectar()
    cursor = conn.cursor()

    query = """
    DELETE e1 FROM etiqueta_02 e1
    INNER JOIN etiqueta_02 e2 
    ON e1.codigo = e2.codigo AND e1.id > e2.id
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
