from contextlib import _RedirectStream
import streamlit as st
import pandas as pd
from conexao import conectar
from banco import obter_etiquetas, excluir_duplicados_etiquetas, inserir_fisco, obter_id_nf_do_codigo, inserir_etiqueta
from processamento import classificar_codigo
import datetime

st.set_page_config(page_title="Gerenciamento de bipagem", layout="wide")
st.title("Gerenciamento de bipagem")

if "codigo_bipado" not in st.session_state:
    st.session_state.codigo_bipado = ""


# Função que manda o código direto pro banco sem precisar botão
def processar_bipagem():
    conn = conectar()
    cursor = conn.cursor()

    codigo = st.session_state.codigo_bipado.strip()
    if codigo == "":
        return

     # tenta achar NF vinculada ao código (de hoje)
    nota_id = obter_id_nf_do_codigo(codigo)

    if nota_id is None:
        nota_id = inserir_fisco(cursor)  #se não, criar uma temporaria

    inserir_etiqueta(codigo, nota_id)

    st.toast(f"Código '{codigo}' inserido com sucesso!", icon="✅")
    st.session_state.codigo_bipado = ""

st.markdown(
    """
    <style>
    div.stTextInput > label, div.stTextInput > div > input {
        font-size: 2.5rem;
        height: 3.5rem;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
#campo de adicionar a bipagem
st.text_input(
    "Digite ou bip o código de barras:",
    key="codigo_bipado",
    on_change=processar_bipagem,
    label_visibility="collapsed",
    placeholder="Escaneie o código de barras ou QR..."
)


df = obter_etiquetas()
# Convertendo coluna de data 
df["A02_data"] = pd.to_datetime(df["A02_data"])

# Selecionar data (padrão: hoje)
col_data, col_vazio = st.columns([1, 9])  # 1 parte pra data, 9 para o resto

with col_data:
    st.markdown("<small><strong>Data dos registros:</strong></small>", unsafe_allow_html=True)
    data_escolhida = st.date_input(
        label="",
        value=datetime.date.today(),
        label_visibility="collapsed",
        format="DD/MM/YYYY"
    )

with col_vazio:
        # Botão para excluir duplicados
    if st.button("Excluir Códigos Duplicados"):
        excluir_duplicados_etiquetas()
        st.toast("Códigos duplicados removidos!", icon="✅")

# Filtrar os dados apenas da data escolhida
df = df[df["A02_data"].dt.date == data_escolhida]

df["Tipo"] = df["codigo"].apply(classificar_codigo)


df = df.rename(columns={
    "A02_data": "Data",
    "Notafiscal_01_A01_id": "Nota Fiscal"
})

if not df.empty and "codigo" in df.columns:
    df["Tipo"] = df["codigo"].apply(classificar_codigo)
    df["Duplicado"] = df.duplicated(subset=["codigo"], keep=False)
else:
    df["Tipo"] = pd.Series([pd.NA] * len(df), index=df.index)
    df["Duplicado"] = pd.Series([False] * len(df), index=df.index)


def destacar_duplicados(linha):
    if linha["Duplicado"]:
        return ['background-color: #8B0000'] * len(linha)
    else:
        return [''] * len(linha)


col1, col2 = st.columns([7, 3])

with col1:
    st.subheader("Etiquetas Registradas")
    st.dataframe(
        df.iloc[::-1].style.apply(destacar_duplicados, axis=1),  # mostra últimas inserções em cima
        height=300,
        use_container_width=True
    )

agora = datetime.datetime.now()
data_hora_str = agora.strftime("%d/%m/%Y %H:%M")

with col2:
    tipos_contagem = df["Tipo"].value_counts() if "Tipo" in df.columns else pd.Series(dtype=int)
    total = tipos_contagem.sum()

    # Início do HTML com f-string para incluir o total
    contagem_html = f"""
    <div style="display: flex; flex-direction: column; gap: 14px; font-family: 'Segoe UI', sans-serif;">
        <div style="
            padding: 16px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #fff;
            background-color: #444;
            color: white;
        ">
            <span style="font-size: 20px;">Total</span>
            <span style="font-size: 34px; font-weight: bold;">{total}</span>
        </div>
    """

    # Adiciona os cartões por tipo
    for tipo, qtd in tipos_contagem.items():
        contagem_html += f""""
        <div style="
            padding: 16px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #fff;
            background-color: #20232a;
            color: white;
        ">
            <span style="font-size: 20px;">{tipo}</span>
            <span style="font-size: 34px; font-weight: bold;">{qtd}</span>
        </div>
        """

    contagem_html += "</div>"

    # Renderiza o HTML final
    st.markdown(contagem_html, unsafe_allow_html=True)

  #  st.markdown(f"<div style='color:red;'>Data e hora atual: {data_escolhida}</div>", unsafe_allow_html=True)

