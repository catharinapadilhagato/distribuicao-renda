import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ALVO = "Renda Total [R$ milhões]"
COL_ANO = "Ano-calendário"
COL_ENTE = "Ente Federativo"
LAG_RENDA = "Renda Total (ano anterior)"


def colunas_lag(data: pd.DataFrame) -> list[str]:
    """Retorna todas as colunas terminadas em '(ano anterior)'."""
    return [c for c in data.columns if c.endswith("(ano anterior)")]


def montar_features(data: pd.DataFrame, usar_ano: bool, usar_ente: bool, so_lag_renda: bool = False):
    """Escolhe as colunas de entrada (X) conforme o cenário. NÃO codifica nada."""
    numericas = [LAG_RENDA] if so_lag_renda else colunas_lag(data)
    if usar_ano:
        numericas = numericas + [COL_ANO]
    categoricas = [COL_ENTE] if usar_ente else []
    return data[numericas + categoricas], numericas, categoricas


def criar_pipeline(numericas: list[str], categoricas: list[str]) -> Pipeline:
    """Pipeline = pré-processamento (escala + one-hot) + modelo, tudo em sequência."""
    etapas = [("num", StandardScaler(), numericas)]
    if categoricas:
        etapas.append(("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categoricas))

    return Pipeline([
        ("prep", ColumnTransformer(etapas)),
        ("reg", Ridge(alpha=1.0)),
    ])


def dividir_por_ano(data: pd.DataFrame, anos_teste: int = 3):
    """Divisão temporal: os últimos `anos_teste` anos viram teste."""
    corte = sorted(data[COL_ANO].unique())[-anos_teste]
    return data[data[COL_ANO] < corte], data[data[COL_ANO] >= corte]


def avaliar(data: pd.DataFrame, usar_ano: bool, usar_ente: bool, so_lag_renda: bool = False) -> dict:
    treino, teste = dividir_por_ano(data)
    X_tr, num, cat = montar_features(treino, usar_ano, usar_ente, so_lag_renda)
    X_te, _, _ = montar_features(teste, usar_ano, usar_ente, so_lag_renda)

    modelo = criar_pipeline(num, cat)
    modelo.fit(X_tr, treino[ALVO])
    previsto = modelo.predict(X_te)

    return {
        "MAE [R$ milhões]": mean_absolute_error(teste[ALVO], previsto),
        "MAPE": mean_absolute_percentage_error(teste[ALVO], previsto),
    }


def baseline_ano_anterior(data: pd.DataFrame) -> dict:
    """Previsão ingênua: renda deste ano = renda do ano anterior."""
    _, teste = dividir_por_ano(data)
    return {
        "MAE [R$ milhões]": mean_absolute_error(teste[ALVO], teste[LAG_RENDA]),
        "MAPE": mean_absolute_percentage_error(teste[ALVO], teste[LAG_RENDA]),
    }

def janelas_expansivas(treino: pd.DataFrame, n_janelas: int = 4, anos_validacao: int = 1):
    anos = sorted(treino[COL_ANO].unique())
    for i in range(n_janelas, 0, -1):
        corte = len(anos) - i * anos_validacao
        anos_tr = anos[:corte]
        anos_val = anos[corte:corte + anos_validacao]
        yield treino[treino[COL_ANO].isin(anos_tr)], treino[treino[COL_ANO].isin(anos_val)]