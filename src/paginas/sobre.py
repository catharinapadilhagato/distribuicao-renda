from src.dados.limpezaDados import dfO, dfT

from src.util.eda import *

import streamlit as st

import pandas as pd
import numpy as np

import html

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
    colunas_irrelevantes = ['Ano-calendário', 'Centil', 'Ente Federativo'] #Colunas que não são relevantes para o describe
    st.dataframe(
    data.drop(columns=colunas_irrelevantes, errors="ignore").describe(include="all"))

    st.divider()
    st.subheader("Exibição do conjunto de dados")

    c_esq, c_dir = st.columns(2)

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
            width='stretch',
            height=400
                     )


# Troque `df2` pelo nome da sua segunda variável de DataFrame
aba1, aba2 = st.tabs(['Conjunto original', 'Conjunto transformado'])

with aba1:
    renderizar_analise_dataset(dfO, prefixo='dfO')

with aba2:
    renderizar_analise_dataset(dfT, prefixo='dfT')