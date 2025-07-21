import streamlit as st
import pymysql
import pandas as pd
import re
from banco import conectar, inserir_comparacao_diaria


st.set_page_config(page_title="Comparação nota fiscal", layout="wide")

def verificar_codigos(codigos):
    conn = conectar()
    cursor = conn.cursor()

    resultado = []

    for item in codigos:
        codigo = item['codigo']
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
                'Nota Fiscal': dados[1] or 'Sem NF',
            })
        else:
            resultado.append({
                'Código': codigo,
                'Nota Fiscal': 'NÃO ENCONTRADO',
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
    


# Função para extrair nota fiscal do zpl
def extrair_nf(conteudo_bytes):
    try:
        nota_fiscal = conteudo_bytes.decode('utf-8', errors='ignore')

        # extrair nota fiscal dessa tag NF:
        procurar_nf = re.search(r"NF:\s*(\d+)", nota_fiscal)
        if procurar_nf:
            return procurar_nf.group(1)

    except Exception:
        return None

st.title("Comparação Nota Fiscal")

# Upload de arquivos ZPL
arquivos = st.file_uploader("Envie arquivos .zpl", type="zpl", accept_multiple_files=True)

# Função para atualizar a nota fiscal no banco
def atualizar_nota_fiscal(codigos):
    conn = conectar()
    cursor = conn.cursor()

    for item in codigos:
        codigo = item['codigo']
        nova_nf = item['fisco']

        if not nova_nf:
            continue  # pula se a NF não foi extraída

        # Primeiro, obtém o ID da etiqueta
        cursor.execute("SELECT id, Notafiscal_01_A01_id FROM etiqueta_02 WHERE codigo = %s", (codigo,))
        etiqueta = cursor.fetchone()

        if etiqueta:
            etiqueta_id, nf_id = etiqueta

            # Atualiza a NF na tabela notafiscal_01
            if nf_id:
                cursor.execute("UPDATE notafiscal_01 SET A01_codigo = %s WHERE A01_id = %s", (nova_nf, nf_id))
                st.success(f"Nota fiscal do código {codigo} atualizada para {nova_nf}")
            else:
                st.warning(f"Código {codigo} não possui vínculo com nota fiscal no banco.")
        else:
            st.error(f"Código {codigo} não encontrado na tabela, NF {nova_nf}")

    conn.commit()
    cursor.close()
    conn.close()

if arquivos:
        codigos = []
        for zpl_file in arquivos:
            conteudo = zpl_file.read()
            codigo_extraido = extrair_codigo_zpl(conteudo)
            fisco_extraido = extrair_nf(conteudo)
            if codigo_extraido:
                codigos.append({
                    'codigo': codigo_extraido,
                    'fisco': fisco_extraido
                    })

        for item in codigos:
            st.write(f"Código: {item['codigo']} | NF: {item['fisco']}")

        if not codigos:
            st.error("Nenhum código válido encontrado nos arquivos enviados.")
            print(codigo_extraido)
            print(conteudo)

        else:
            st.toast(f"{len(codigos)} código(s) extraído(s)")
            atualizar_nota_fiscal(codigos) #agora ele mostra as notas fiscais na tabela
            inserir_comparacao_diaria(codigos)
            print(fisco_extraido)

           #df_resultado = verificar_codigos(codigos)

            def highlight_nao_encontrado(val):
                if val == fisco_extraido:
                    return 'color: red; font-weight: bold'
                return ''

            #st.dataframe(df_resultado.style.applymap(highlight_nao_encontrado, subset=['Nota Fiscal']))

st.subheader("Histórico de comparações de hoje")
# mostra a tabela com o historico do dia, com codigo de barras, nota fiscal e situação.
def carregar_historico_hoje():
    conn = conectar()
    query = """
        SELECT cd.A04_codigo_barras, cd.A04_nota_fiscal, cd.A04_data,
               CASE 
                   WHEN e.codigo IS NOT NULL THEN 'ENCONTRADO'
                   ELSE 'NÃO ENCONTRADO'
               END AS Situacao
        FROM comparacao_diaria_04 cd
        LEFT JOIN etiqueta_02 e ON cd.A04_codigo_barras = e.codigo
        WHERE DATE(cd.A04_data) = CURDATE()
        ORDER BY cd.A04_data DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df_hoje = carregar_historico_hoje()

#st.dataframe(df_hoje, use_container_width=True)

def highlight_nao_encontrado(row):
    if row['Situacao'] == 'NÃO ENCONTRADO':
        return ['background-color: #8B0000'] * len(row)
    return [''] * len(row)

st.dataframe(df_hoje.style.apply(highlight_nao_encontrado, axis=1), use_container_width=True)




 