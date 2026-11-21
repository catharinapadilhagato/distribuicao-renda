from src.util.funcaoLog import configurar_log

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

#------------ GRÁFICOS ------------ 
def corr_dados(data:pd.DataFrame):
    '''
    Recebe um dataframe e cria um gráfico de correlação
    '''

    corr_matrix = data.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(corr_matrix,
                annot=True,
                fmt='.2f',
                cmap="coolwarm",
                linewidths=0.5,
                cbar_kws={"shrink": 1},
                annot_kws={"size": 6},
                vmin=-1,
                vmax=1)

    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return fig

def _quebrar_texto(texto: str, largura: int = 18) -> str:
    palavras = texto.split()
    linhas = []
    atual = ""
    for palavra in palavras:
        if len(atual) + len(palavra) + (1 if atual else 0) <= largura:
            atual = f"{atual} {palavra}".strip()
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return "\n".join(linhas)


def hist_dados(data: pd.DataFrame, max_colunas: int = 6):
    """Recebe um DataFrame e retorna um PairGrid bem espaçado das colunas numéricas."""
    data_filtrado = (
        data.select_dtypes(include="number")
        .drop(columns=["Ano-calendário", "Centil"], errors="ignore")
        .astype(float)
    )

    colunas = list(data_filtrado.columns[:max_colunas])
    data_plot = data_filtrado[colunas]

    sns.set_theme(style="whitegrid", context="notebook")

    grid = sns.pairplot(
        data_plot,
        corner=True,
        plot_kws=dict(
            alpha=0.45,
            s=18,
            edgecolor="none",
        ),
        diag_kws=dict(
            bins=20,
            alpha=0.75,
        ),
        height=2.2,
        aspect=1.15,
    )

    for ax in grid.axes.flatten():
        if ax is None:
            continue

        xlabel = ax.get_xlabel()
        ylabel = ax.get_ylabel()

        if xlabel:
            ax.set_xlabel(_quebrar_texto(xlabel, largura=16), fontsize=8, labelpad=8)
        if ylabel:
            ax.set_ylabel(_quebrar_texto(ylabel, largura=16), fontsize=8, labelpad=10)

        ax.tick_params(axis="x", labelsize=7.5, rotation=30)
        ax.tick_params(axis="y", labelsize=7.5, rotation=0)

    grid.fig.subplots_adjust(
        left=0.14,
        bottom=0.14,
        right=0.98,
        top=0.90,
        wspace=0.28,
        hspace=0.28,
    )

    return grid.fig