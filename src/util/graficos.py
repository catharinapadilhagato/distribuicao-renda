from src.util.funcaoLog import configurar_log

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

#------------ GRÁFICOS ------------ 
def corr_dados(data:pd.DataFrame):
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
    return fig