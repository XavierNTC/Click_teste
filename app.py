import streamlit as st
import pandas as pd
from banco import obter_etiquetas, excluir_duplicados_etiquetas
from processamento import classificar_codigo

st.set_page_config(page_title="Bipagem com Banco", layout="wide")

st.title("Sistema de Bipagem com Banco de Dados")

if "codigo_bipado" not in st.session_state:
    st.session_state.codigo_bipado = ""

# Função que manda o código direto pro banco sem precisar botão
def processar_bipagem():
    codigo = st.session_state.codigo_bipado
    if codigo.strip() == "":
        return
    
    # ⚠️ Supondo nota_id = 1 como teste (depois você pode automatizar ou fazer input)
    from banco import inserir_etiqueta
    inserir_etiqueta(codigo, nota_id=1)
    
    st.toast(f"Código '{codigo}' inserido com sucesso!", icon="✅")
    st.session_state.codigo_bipado = ""

# Campo pra selecionar a bipagem grandão
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
    placeholder="Escaneie o código de barras ou QR...",
)

# Mantém no input para facilitar bipagem sem parar
st.markdown(
    """
    <script>
    const input = window.parent.document.querySelector('input[data-baseweb="input"]');
    if (input) { input.focus(); }
    </script>
    """,
    unsafe_allow_html=True,
)

# Pega os dados e classifica os tipos, igual o grafico lá
df = obter_etiquetas()
df["Tipo"] = df["A02_codigo"].apply(classificar_codigo)

# Marca duplicados na coluna 'A02_codigo'
df["Duplicado"] = df.duplicated(subset=["A02_codigo"], keep=False)

def destacar_duplicados(row):
    if row["Duplicado"]:
        return ['background-color: #8B0000'] * len(row)  # cor
    else:
        return [''] * len(row)

# Cria duas colunas: tabela (70%) e contagem (30%) p ficar bonitin do lado um do outro
col1, col2 = st.columns([7, 3])

with col1:  # Aqui é a tabela
    st.subheader("Etiquetas Registradas")
    st.dataframe(
        df.iloc[::-1].style.apply(destacar_duplicados, axis=1),  # inverte o índice p/ mostrar as últimas inserções
        height=300,
        use_container_width=True
    )

with col2:
    contagem_html = """
    <div style="display: flex; flex-direction: column; gap: 14px; font-family: 'Segoe UI', sans-serif;">
    """

    for tipo, qtd in df["Tipo"].value_counts().items():
        contagem_html += f"""
        <div style="
            padding: 16px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #fff
        ">
            <span style="font-size: 20px; color: white;">{tipo}</span>
            <span style="font-size: 34px; font-weight: bold; color: #fff;">{qtd}</span>
        </div>
        """

    contagem_html += "</div>"

    st.markdown(contagem_html, unsafe_allow_html=True)

# Botão pra excluir duplicados
if st.button("Excluir Códigos Duplicados"):
    excluir_duplicados_etiquetas()
    st.success("Códigos duplicados removidos do banco!")
    st.rerun()
