import streamlit as st
import pymysql
import pandas as pd
import re
from banco import conectar

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
        cursor.execute(query, (item['codigo'],))
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

st.title("Verificação de Etiquetas (ZPL) no Banco")

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
            st.error(f"Código {codigo} não encontrado na tabela.")

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
            print(fisco_extraido)

            df_resultado = verificar_codigos(codigos)

            def highlight_nao_encontrado(val):
                if val == 'NÃO ENCONTRADO':
                    return 'color: red; font-weight: bold'
                return ''

            st.dataframe(df_resultado.style.applymap(highlight_nao_encontrado, subset=['Nota Fiscal']))




 