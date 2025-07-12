import streamlit as st
import pandas as pd
from banco import inserir_bipagem, obter_bipagens
from processamento import classificar_codigo

st.set_page_config(page_title="Bipagem com Banco", layout="wide")
st.title("📦 Sistema de Bipagem com Banco de Dados")

with st.form("form_bipagem"):
    codigo = st.text_input("Digite ou bip o código de barras:")
    submitted = st.form_submit_button("Inserir bipagem")

    if submitted and codigo:
        inserir_bipagem(codigo)
        st.success(f"Código '{codigo}' inserido com sucesso!")

df = obter_bipagens()
df["Tipo"] = df["codigo"].apply(classificar_codigo)

st.subheader("📋 Bipagens Registradas")
st.dataframe(df, use_container_width=True)

st.subheader("📊 Contagem por Tipo")
st.bar_chart(df["Tipo"].value_counts())
