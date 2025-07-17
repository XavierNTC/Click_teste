from contextlib import _RedirectStream
import streamlit as st
import pandas as pd
from banco import obter_etiquetas, excluir_duplicados_etiquetas, inserir_etiqueta, inserir_fisco
from processamento import classificar_codigo
import datetime
import comparador

st.set_page_config(page_title="Bipagem com Banco", layout="wide")
st.title("Sistema de Bipagem com Banco de Dados")

if "codigo_bipado" not in st.session_state:
    st.session_state.codigo_bipado = ""


# Função que manda o código direto pro banco sem precisar botão
def processar_bipagem():
    codigo = st.session_state.codigo_bipado.strip()
    if codigo == "":
        return

    nota_id = inserir_fisco()  # cria a nota fiscal temporaria
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
st.text_input(
    "Digite ou bip o código de barras:",
    key="codigo_bipado",
    on_change=processar_bipagem,
    label_visibility="collapsed",
    placeholder="Escaneie o código de barras ou QR..."
)

df = obter_etiquetas()
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


def destacar_duplicados(row):
    if row["Duplicado"]:
        return ['background-color: #8B0000'] * len(row)
    else:
        return [''] * len(row)


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
    contagem_html = """
    <div style="display: flex; flex-direction: column; gap: 14px; font-family: 'Segoe UI', sans-serif;">
    """
    tipos_contagem = df["Tipo"].value_counts() if "Tipo" in df.columns else pd.Series(dtype=int)

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
        ""  >
            <span style="font-size: 20px;">{tipo}</span>
            <span style="font-size: 34px; font-weight: bold;">{qtd}</span>
        </div>
        """

    contagem_html += "</div>"
    st.markdown(contagem_html, unsafe_allow_html=True)

    st.markdown(f"<div style='color:red;'>Data e hora atual: {data_hora_str}</div>", unsafe_allow_html=True)

# Botão para excluir duplicados
if st.button("Excluir Códigos Duplicados"):
    excluir_duplicados_etiquetas()
    st.toast("Códigos duplicados removidos!", icon="✅")

