import streamlit as st
from Bipagem import app_main
from Comparador import comparador_main

page = st.query_params.get("page", "app")

col1, col2, _ = st.columns([1, 1, 8])

with col1:
    if st.button("📦 Bipagem"):
        st.query_params.update({"page": "app"})
        page = "app"

with col2:
    if st.button("🧾 Comparador"):
        st.query_params.update({"page": "comparador"})
        page = "comparador"

st.markdown("---")  # linha separadora

if page == "comparador":
    comparador_main()
else:
    app_main()
