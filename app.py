import streamlit as st

st.set_page_config(layout="wide")

main_page = st.Page("src/paginas/sobre.py", title="Sobre")

pg = st.navigation([main_page])


pg.run()
#python -m streamlit run app.py