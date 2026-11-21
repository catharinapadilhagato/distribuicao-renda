import pandas as pd
import numpy as np

from pathlib import Path

import streamlit as st

#------------ EDA ------------

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