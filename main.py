# %%
import pandas as pd
from src.dados.limpezaDados import df

# %%
# Análise exploratória
print(df.shape) #(linhas, colunas)
print(df.columns) #nomes das colunas
print(df.head())  #primeiras 5 linhas
print(df.tail())  #últimas 5 linhas
print(df.info())  #tipos de dados e contagem de não nulos

# %%
df.describe()  # média, desvio padrão, quartis e extremos (numéricos)
df.describe(include="object")  # contagem, valores únicos e moda (texto/categorias)
df["categoria"].value_counts()  # frequência de cada categoria
df["categoria"].unique()  # valores únicos
