from src.dados.limpezaDados import dfAgregado
from src.util.eda import renderizar_eda
from src.util.tema import cartao

import streamlit as st
import html

with cartao("predito_titulo"):
    st.title('Predição da distruibuição de renda', text_alignment="center")

with cartao("predito_preparo"):
    st.markdown(
        '''
Para atingir o objetivo, o conjunto de dados foi mais uma vez modificado, modificando o conjunto transformado:
- O conjunto transformado foi agrupado com base no ano e ente federativo.

'''
    )

renderizar_eda(dfAgregado, 'dfAgregado')