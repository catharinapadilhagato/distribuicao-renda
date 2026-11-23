from src.dados.limpezaDados import dfO, dfT
from src.util.graficos import corr_dados, disp_dados, bar_lateral_dados,  bplot_dados
from src.util.eda import renderizar_eda
from src.util.tema import cartao

import streamlit as st
import html

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

COLUNAS_ID = ['Ano-calendário', 'Ente Federativo', 'Centil', 'Subcentil', 'Nivel', 'Quantidade de Contribuintes']


def colunas_formatadas(data:pd.DataFrame):
    return "\n".join(
    f"- {col.replace('$', r'\$')}" for col in data.columns
)

with cartao("sobre_titulo"):
    st.title("Distribuição de renda de cada estado", text_alignment="center")
    st.markdown(
        "O trabalho tem como objetivo analisar a distribuição de renda de cada estado, "
        "e predizer em R$ a quantidade de imposto de renda total que o estado terá em um determinado ano.",
        text_alignment="center",
    )

with cartao("sobre_dados"):
    st.subheader("Sobre os dados")
    st.markdown("""
Os dados foram obtidos através do portal de dados abertos: <https://dados.gov.br/dados/conjuntos-dados/distribuio-de-renda>.

O site fornece 3 conjuntos de dados:
- Distribuição da renda tributável;
- Distribuição da renda tributável, dos sócios e dividendos;
- Distribuição da renda tributável, dos sócios, dividendos e tributada exclusivamente na fonte.

Cada um tem a própria documentação que explica o que cada atributo significa; o conjunto escolhido foi o terceiro, por ser mais completo.

No conjunto, a coluna "Centil" tem subgrupos apartir do 100° centil, que devide em 100.01 - 100.10 os mais ricos e 100.10.01 - 100.10.10. Para facilitar a compreensão dessa coluna, foram criadas duas novas, a "Subcentil" que recebe o subgrupo e "Nivel" que filtra qual tipo de centil vai aparecer (o que está no subgrupo ou o número inteiro daquele centil)
""")

aba1, aba2 = st.tabs(['Conjunto original', 'Conjunto transformado'])

with aba1:
    renderizar_eda(dfO, prefixo='dfO')

with aba2:
    with cartao("sobre_compactadas"):
        st.markdown('''
Para melhor compreensão e facilidade nas analises que serão realizadas, algumas colunas foram compactadas, sendo elas:
- Rendimentos Tributáveis Totais [R$ milhões];
- Rendimentos Isentos Totais [R$ milhões];
- Despesas Dedutíveis Totais [R$ milhões];
- Bens e Direitos Totais [R$ milhões].
        ''')

    renderizar_eda(dfT, prefixo='dfT')

    metricas = [c for c in dfT.columns if c not in COLUNAS_ID]

    col1, col2 = st.columns(2)
    with col1:
        with cartao("sobre_correlacao"):
            st.subheader('Correlação entre os dados')
            fig_corr = corr_dados(dfT)
            st.pyplot(fig_corr)
            plt.close(fig_corr)
            st.write('''
Todos os dados, exceto o que representa o ano e a quantidade de contribuintes, possuem uma correlação positiva. Têm destaque Rend. Sujeitos à Tribut., que tem uma correlação forte com Rend. Isentos e Bens e Direitos.
            ''')

        with cartao("sobre_comparacao"):
            st.subheader('Comparação entre os entes federativos')
            opcao_bar = st.selectbox('Selecione um parâmetro', metricas, key='sel_bar_lateral')
            fig_bar_lat, top5 = bar_lateral_dados(dfT, eixo_x=opcao_bar, eixo_y='Ente Federativo')
            st.pyplot(fig_bar_lat)
            plt.close(fig_bar_lat)
            st.markdown(f"""Os principais Entes Federativos relacionados ao **{opcao_bar}**:

{top5}""")

    with col2:
        with cartao("sobre_frequencia"):
            st.subheader('Frequência e distribuição dos dados')

            n_colunas, pqn_analise = st.columns(2)
            with n_colunas:
                n = st.number_input(
                        "Escolha a quantidade de colunas a serem exibidas:",
                        min_value=6,
                        max_value=max(1, len(dfT.columns)),
                        value=min(6, max(1, len(dfT.columns))),
                        step=1,
                        key='num_colunas_disp',
                        width=550
                        )

            with pqn_analise:
                st.markdown('Percebe-se que os dados vão se distribuindo na diagonal, exibindo a linealidade entre eles.')

            fig_disp = disp_dados(dfT, max_colunas=n)
            st.pyplot(fig_disp)
            plt.close(fig_disp)

        with cartao("sobre_centis"):
            st.subheader('Distribuição dos centis')
            opcao_bp = st.selectbox('Selecione um parâmetro', metricas, key='sel_boxplot')
            fig_bp = bplot_dados(dfT, eixo_x='Centil', eixo_y=opcao_bp)
            st.pyplot(fig_bp)
            plt.close(fig_bp)