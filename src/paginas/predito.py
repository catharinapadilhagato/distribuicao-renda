from src.dados.limpezaDados import dfAgregado
from src.util.eda import renderizar_eda
from src.util.tema import cartao

import streamlit as st
import html

with cartao("predito_titulo"):
    st.title('Predição da distruibuição de renda', text_alignment="center")
    st.markdown(
        "O programa irá tentar predizer o valor total de distribuição de um ano 'a' e de um estado 'e'",
        text_alignment="center",
    )

with cartao("predito_preparo"):
    st.markdown(
        '''
Para atingir o objetivo, o conjunto de dados foi mais uma vez modificado:
- O conjunto transformado foi agrupado com base no ano e ente federativo;
- Filtrando o nível por 0;
- Retirando os atributos "Centil", "Subcentil" e "Nivel";
- Retirada as características que o ente federativo era referente ao "BRASIL";

'''
    )

renderizar_eda(dfAgregado, 'dfAgregado')