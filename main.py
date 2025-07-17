import streamlit as st
from app import app_main
from comparador import comparador_main

query_params = st.experimental_get_query_params()
page = query_params.get("page", ["app"])[0]

if page == "comparador":
    comparador_main()
else:
    app_main()