import streamlit as st
import pymysql
import pandas as pd
import xml.etree.ElementTree as ET
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

# Função para extrair códigos dos arquivos XML
def extrair_codigo_xml(conteudo_xml):
    try:
        root = ET.fromstring(conteudo_xml)
        # por exemplo se o código estiver em uma tag <codigo> dentro do XML
        codigo = root.find('.//codigo')  # busca a tag 'codigo' em tudo
        if codigo is not None and codigo.text:
            return codigo.text.strip()
        else:
            return None
    except ET.ParseError:
        return None

st.title("Verificação de Etiquetas no Banco")

# Upload
arquivos = st.file_uploader("Envie até 50 arquivos .xml", type="xml", accept_multiple_files=True)

if arquivos:
    if len(arquivos) > 50:
        st.warning("Máximo 50 arquivos por vez.")
    else:
        codigos = []
        for xml_file in arquivos:
            conteudo = xml_file.read()
            codigo_extraido = extrair_codigo_xml(conteudo)
            if codigo_extraido:
                codigos.append(codigo_extraido)

        if not codigos:
            st.error("Nenhum código válido encontrado nos arquivos enviados.")
        else:
            st.success(f"{len(codigos)} código(s) extraído(s). Verificando no banco...")

            df_resultado = verificar_codigos(codigos)

            def highlight_nao_encontrado(val):
                if val == 'NÃO ENCONTRADO':
                    return 'color: red; font-weight: bold'
                return ''

            st.dataframe(df_resultado.style.applymap(highlight_nao_encontrado, subset=['Nota Fiscal']))
