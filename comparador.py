import streamlit as st
import pymysql
import pandas as pd
import re
from banco import conectar

def verificar_codigos(codigos):
    conn = conectar()
    cursor = conn.cursor()

    resultado = []

    for codigo in codigos:
        query = """
            SELECT e.codigo, nf.A01_codigo AS nota_fiscal
            FROM etiqueta_02 e
            LEFT JOIN notafiscal_01 nf ON e.Notafiscal_01_A01_id = nf.A01_id
            WHERE e.codigo = %s
            LIMIT 1
        """
        cursor.execute(query, (codigo,))
        dados = cursor.fetchone()

        if dados:
            resultado.append({
                'Código': dados[0],
                'Nota Fiscal': dados[1] or 'Sem NF'
            })
        else:
            resultado.append({
                'Código': codigo,
                'Nota Fiscal': 'NÃO ENCONTRADO'
            })

    conn.close()
    return pd.DataFrame(resultado)

# Função para extrair códigos dos arquivos zpl
def extrair_codigo_zpl(conteudo_bytes):
    try:
        conteudo = conteudo_bytes.decode('utf-8', errors='ignore')

        # Tenta extrair do código de barras ^FD>:45149061470^FS
        procurar_etiqueta = re.search(r"\^FD>:\s*(\d{10,})\^FS", conteudo)
        if procurar_etiqueta:
            return procurar_etiqueta.group(1)

        # Fallback: extrair do QR Code JSON {"id":"45149061470","t":"lm"}
        procurar_qr = re.search(r'"id"\s*:\s*"(\d{10,})"', conteudo)
        if procurar_qr:
            return procurar_qr.group(1)

        return None
    except Exception:
        return None

st.title("Verificação de Etiquetas (ZPL) no Banco")

# Upload de arquivos ZPL
arquivos = st.file_uploader("Envie até 50 arquivos .zpl", type="zpl", accept_multiple_files=True)

if arquivos:
    if len(arquivos) > 50:
        st.warning("Máximo 50 arquivos por vez.")
    else:
        codigos = []
        for zpl_file in arquivos:
            conteudo = zpl_file.read()
            codigo_extraido = extrair_codigo_zpl(conteudo)
            if codigo_extraido:
                codigos.append(codigo_extraido)

        if not codigos:
            st.error("Nenhum código válido encontrado nos arquivos enviados.")
            print(codigo_extraido)
            print(conteudo)
        else:
            st.success(f"{len(codigos)} código(s) extraído(s). Verificando no banco...")

            df_resultado = verificar_codigos(codigos)

            def highlight_nao_encontrado(val):
                if val == 'NÃO ENCONTRADO':
                    return 'color: red; font-weight: bold'
                return ''

            st.dataframe(df_resultado.style.applymap(highlight_nao_encontrado, subset=['Nota Fiscal']))
