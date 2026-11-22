from src.dados.limpezaDados import dfO, dfT
from src.util.graficos import corr_dados, disp_dados, bar_lateral_dados, bplot_dados

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

def n_valores(data:pd.DataFrame, n:int=5, primeiros:bool=True):
    '''
    Função para exibir n valores de um dataset

    data -> Recebe um dataframe;
    n -> Recebe um número inteiro (por padrão, 5) que indica a quantidade de valores a serem exibidos;
    primeiros -> Recebe True/False  (por padrão, True), se verdadeiro, retorna os primeiros itens, se falso, os últimos.
    '''
    if primeiros:
        return data.head(n)

    return data.tail(n)

st.title("Distribuição de renda de cada estado", text_alignment="center")
st.markdown(
    "O trabalho tem como objetivo analisar a distribuição de renda de cada estado, "
    "e predizer em R$ a quantidade de imposto de renda total que o estado terá em um determinado ano.",
    text_alignment="center",
)
st.divider()

st.subheader("Sobre os dados")
st.markdown("""
Os dados foram obtidos através do portal de dados abertos: <https://dados.gov.br/dados/conjuntos-dados/distribuio-de-renda>.

O site fornece 3 conjuntos de dados:
- Distribuição da renda tributável;
- Distribuição da renda tributável, dos sócios e dividendos;
- Distribuição da renda tributável, dos sócios, dividendos e tributada exclusivamente na fonte.

Cada um tem a própria documentação que explica o que cada atributo significa; o conjunto escolhido foi o terceiro, por ser mais completo.
""")

ESTILO_TABELA_HTML = """<style>
.info-table {
    width: 100%;
    border-collapse: collapse;
    font-family: sans-serif;
}
.info-header {
    display: flex;
    justify-content: space-between;
    padding: 8px 4px;
    border-bottom: 1.5px solid rgba(128, 128, 128, 0.35);
    color: rgba(128, 128, 128, 0.9);
    font-size: 0.9rem;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 4px;
    border-bottom: 1px solid rgba(128, 128, 128, 0.18);
    gap: 16px;
}
.info-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 4px;
}
.info-desc {
    font-size: 0.88rem;
    color: rgba(128, 128, 128, 0.9);
}
.info-right {
    font-size: 1.15rem;
    color: rgba(128, 128, 128, 0.95);
    white-space: nowrap;
    text-align: right;
}
</style>"""


def renderizar_analise_dataset(data:pd.DataFrame, prefixo: str):
    col1, col2, col3 = st.columns(3)
    col1.metric("Linhas (características)", f"{len(data):,}".replace(",", "."))
    col2.metric("Colunas (atributos)", len(data.columns))
    col3.metric("Valores nulos", int(data.isna().sum().sum()))

    linhas_html = []
    for col in data.columns:
        nome_col = html.escape(str(col))
        qtd_valores = f"{int(data[col].count()):,}".replace(",", ".")
        tipo_dado = html.escape(str(data[col].dtype))

        linhas_html.append(f"""<div class="info-row">
<div class="info-left">
<div class="info-title">{nome_col}</div>
<div class="info-desc">Tipo de dado (dtype): <code>{tipo_dado}</code></div>
</div>
<div class="info-right">{qtd_valores} valores</div>
</div>""")

    tabela_html = f"""{ESTILO_TABELA_HTML}
<div class="info-table">
<div class="info-header">
<span>Coluna</span>
<span>Quantidade de valores</span>
</div>
{"".join(linhas_html)}
</div>"""

    st.markdown(tabela_html, unsafe_allow_html=True)

    st.divider()
    st.subheader('Descrição do conjunto de dados')
    colunas_irrelevantes = ['Ano-calendário', 'Centil', 'Subcentil', 'Nivel', 'Ente Federativo'] #Colunas que não são relevantes para o describe
    st.dataframe(
    data.drop(columns=colunas_irrelevantes, errors="ignore").describe(include="all"))

    st.divider()
    st.subheader("Exibição do conjunto de dados")

    c_esq, c_dir = st.columns([1, 3])

    with c_esq:
        n = st.number_input(
            "Escolha a quantidade de linhas:",
            min_value=1,
            max_value=max(1, len(data)),
            value=min(5, max(1, len(data))),
            step=1,
            key=f"num_linhas_{prefixo}",
            width=150
        )

        opcao = st.radio(
            "Selecione quais linhas vão ser exibidas:",
            ("Primeiras", "Últimas"),
            key=f"radio_linhas_{prefixo}",
        )
        opcao_bool = opcao == "Primeiras"

    with c_dir:
        st.dataframe(
            n_valores(data, n=n, primeiros=opcao_bool),
            width="stretch"
                     )


aba1, aba2 = st.tabs(['Conjunto original', 'Conjunto transformado'])

with aba1:
    renderizar_analise_dataset(dfO, prefixo='dfO')

with aba2:
    st.markdown('''
Para melhor compreensão e facilidade nas analises que serão realizadas, algumas colunas foram compactadas, sendo elas:
- Rendimentos Tributáveis Totais [R$ milhões]
- Rendimentos Isentos Totais [R$ milhões]
- Despesas Dedutíveis Totais [R$ milhões]
- Bens e Direitos Totais [R$ milhões]
    ''')
    st.divider()
    renderizar_analise_dataset(dfT, prefixo='dfT')
    
    st.divider()

    dfN = dfT[dfT["Nivel"] == 0].copy()
    metricas = [c for c in dfT.columns if c not in COLUNAS_ID]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Correlação entre os dados')
        fig_corr = corr_dados(dfN.drop(columns=['Nivel']))
        st.pyplot(fig_corr)
        plt.close(fig_corr)
        st.write('''
Todos os dados, exceto o que representa o ano e a quantidade de contribuintes, possuem uma correlação positiva. Têm destaque Rend. Sujeitos à Tribut., que tem uma correlação forte com Rend. Isentos e Bens e Direitos.
        ''')

        st.subheader('Comparação entre os entes federativos')
        opcao_bar = st.selectbox('Selecione um parâmetro', metricas, key='sel_bar_lateral')
        fig_bar_lat, top5 = bar_lateral_dados(dfN, eixo_x=opcao_bar, eixo_y='Ente Federativo')
        st.pyplot(fig_bar_lat)
        plt.close(fig_bar_lat)
        st.markdown(f"""Os principais Entes Federativos relacionados ao **{opcao_bar}**:

{top5}""")

    with col2:
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

        fig_disp = disp_dados(dfN, max_colunas=n)
        st.pyplot(fig_disp)
        plt.close(fig_disp)

        st.subheader('Distribuição dos centis')
        opcao_bp = st.selectbox('Selecione um parâmetro', metricas, key='sel_boxplot')
        fig_bp = bplot_dados(dfN, eixo_x='Centil', eixo_y=opcao_bp)
        st.pyplot(fig_bp)
        plt.close(fig_bp)