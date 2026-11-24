from src.util.regressao.modelos import avaliar, baseline_ano_anterior

import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

import pandas as pd

def teste_cenarios(data:pd.DataFrame):
    cenarios = {
        "A. Só o ano anterior da renda":       dict(usar_ano=False, usar_ente=False, so_lag_renda=True),
        "B. Todas as colunas lags":         dict(usar_ano=False, usar_ente=False),
        "C. B + ano":            dict(usar_ano=True,  usar_ente=False),
        "D. B + estado":         dict(usar_ano=False, usar_ente=True),
        "E. B + ano + estado":   dict(usar_ano=True,  usar_ente=True),
    }

    resultados = {"Baseline (ano anterior)": baseline_ano_anterior(data)}
    for nome, params in cenarios.items():
        resultados[nome] = avaliar(data, **params)

    return pd.DataFrame(resultados).T.sort_values("MAPE")