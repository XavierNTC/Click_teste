import mysql.connector
from datetime import datetime
import pandas as pd

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",        
        password="",        
        database="db_click"
    )
#função pra inserir a nota fiscal, botei p ser chamada na função de processar bipagem, que quando bipa ele ja insere lek
def inserir_fisco():
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
        INSERT INTO notafiscal_01 (Empresa_03_A03_id, A01_codigo, A01_data)
        VALUES (%s, %s, %s)
    """
    valores = (1, "TEMP", data_atual)
    cursor.execute(query, valores)
    conn.commit()

    nota_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return nota_id

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

#insere no banco as informações do zpl
def inserir_comparacao_diaria(codigos):
    conn = conectar()
    cursor = conn.cursor()
    
    for item in codigos:
        codigo = item['codigo']
        nota_fiscal = item['fisco']
        
        # Checar se já foi inserido hoje (evita duplicatas)
        cursor.execute("""
            SELECT A04_id FROM comparacao_diaria_04
            WHERE A04_codigo_barras = %s AND DATE(A04_data) = CURDATE()
        """, (codigo,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO comparacao_diaria_04 (A04_codigo_barras, A04_nota_fiscal)
                VALUES (%s, %s)
            """, (codigo, nota_fiscal))
    
    conn.commit()
    cursor.close()
    conn.close()

def obter_id_nf_do_codigo(codigo, A03_id=1):
    conn = conectar()
    cursor = conn.cursor()

    # Verifica se já tem NF associada ao código hoje
    cursor.execute("""
        SELECT A04_nota_fiscal
        FROM comparacao_diaria_04
        WHERE A04_codigo_barras = %s AND DATE(A04_data) = CURDATE()
        LIMIT 1
    """, (codigo,))
    row = cursor.fetchone()

    if not row or not row[0]:
        conn.close()
        return None

    nf_numero = row[0]

    # NF já cadastrada? então deixa como tá
    cursor.execute("SELECT A01_id FROM notafiscal_01 WHERE A01_codigo = %s", (nf_numero,))
    nf_row = cursor.fetchone()
    if nf_row:
        conn.close()
        return nf_row[0]

    # Inserir nova NF
    cursor.execute("""
        INSERT INTO notafiscal_01 (Empresa_03_A03_id, A01_codigo, A01_data)
        VALUES (%s, %s, NOW())
    """, (A03_id, nf_numero))
    conn.commit()
    nota_id = cursor.lastrowid
    conn.close()
    return nota_id