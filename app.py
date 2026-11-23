import streamlit as st

from src.util.tema import aplicar_tema

st.set_page_config(layout="wide")

sobre_page = st.Page("src/paginas/sobre.py", title="Sobre")
predito_page = st.Page("src/paginas/predito.py", title="Predito")

pg = st.navigation([sobre_page, predito_page])

aplicar_tema(pg.title)

pg.run()
#python -m streamlit run app.py