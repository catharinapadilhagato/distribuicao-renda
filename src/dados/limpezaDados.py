from pathlib import Path

import pandas as pd

from src.dados.extracaoDados import main
from src.util.funcaoLog import configurar_log

#------------ LOGS ------------ 

PASTA_LOGS = Path(__file__).parent / "logs"
PASTA_LOGS.mkdir(parents=True, exist_ok=True)


logger = configurar_log('limpeza',
                        PASTA_LOGS,
                        'limpeza.log')

#------------ TRADUÇÃO ------------ 

dfO = main()

nome_colunas = [
    "Ano-calendário",
    "Ente Federativo",
    "Centil",
    "Quantidade de Contribuintes",
    "Rendimentos Tributáveis - Limite Superior da RB2 do Centil [R$ milhões]",
    "Rendimentos Tributáveis - Soma da RB2 do Centil [R$ milhões]",
    "Rendimentos Tributáveis - RB2 Acumulada do Centil [R$ milhões]",
    "Rendimentos Tributáveis - Média da RB2 do Centil [R$]",
    "Rendimentos Sujeitos à Tribut. Exclusiva [R$ milhões]",
    "Rendimentos Isentos - Lucros e dividendos [R$ milhões]",
    "Rendimentos Isentos - Rendim. Sócio/Titular ME/EPP Opt SIMPLES [R$ milhões]",
    "Rendimentos Isentos - Outros Rendimentos Isentos [R$ milhões]",
    "Despesas Dedutíveis - Previdência [R$ milhões]",
    "Despesas Dedutíveis - Dependentes [R$ milhões]",
    "Despesas Dedutíveis - Instrução [R$ milhões]",
    "Despesas Dedutíveis - Médicas [R$ milhões]",
    "Despesas Dedutíveis - Pensão Alimentícia [R$ milhões]",
    "Despesas Dedutíveis - Livro-Caixa [R$ milhões]",
    "Imposto Devido [R$ milhões]",
    "Bens e Direitos - Imóveis [R$ milhões]",
    "Bens e Direitos - Móveis [R$ milhões]",
    "Bens e Direitos - Financeiros [R$ milhões]",
    "Bens e Direitos - Outros Bens e Direitos [R$ milhões]",
    "Dívidas e Ônus [R$ milhões]",
]

colunas_unicas = [
    "Ano-calendário",
    "Ente Federativo",
    "Centil",
    "Quantidade de Contribuintes",
    "Rendimentos Sujeitos à Tribut. Exclusiva [R$ milhões]",
    "Imposto Devido [R$ milhões]",
    "Dívidas e Ônus [R$ milhões]",
]

assert len(dfO.columns) == len(nome_colunas), logger.error(f'"{len(dfO.columns)} colunas no DataFrame, {len(nome_colunas)} nomes na lista"')

for antigo, novo in zip(dfO.columns, nome_colunas):
    logger.info(f"coluna '{antigo}' alterada para '{novo}'")

dfO.columns = nome_colunas

#------------ MUDANÇA DE TIPO ------------ 

COLUNAS_IGNORADAS = [
    "Ano-calendário",
    "Ente Federativo",
    "Centil",
    "Quantidade de Contribuintes",
]

def converter_tipos(df, colunas_ignoradas=COLUNAS_IGNORADAS):
    '''
    Converte o tipo das colunas para decimal
    '''

    df = df.copy()

    for coluna in df.columns:
        if coluna in colunas_ignoradas:
            continue
        df[coluna] = _para_float(df[coluna])
        logger.info(f"coluna '{coluna}' convertida para float")

    qtd = "Quantidade de Contribuintes"
    df[qtd] = _para_float(df[qtd]).round().astype("Int64")
    logger.info(f"coluna '{qtd}' convertida para inteiro")

    return df


def _para_float(serie):
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)

    serie = (
        serie.astype(str)
        .str.strip()
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False) 
    )
    return pd.to_numeric(serie, errors="coerce")

dfO = converter_tipos(dfO)
dfT = dfO[colunas_unicas].copy()

#------------ DATASET COMPACTADO ------------ 

grupos_compactados = {
    "Rendimentos Tributáveis Totais [R$ milhões]": [
        "Rendimentos Tributáveis - Limite Superior da RB2 do Centil [R$ milhões]",
        "Rendimentos Tributáveis - Soma da RB2 do Centil [R$ milhões]",
        "Rendimentos Tributáveis - RB2 Acumulada do Centil [R$ milhões]",
        "Rendimentos Tributáveis - Média da RB2 do Centil [R$]",
    ],
    "Rendimentos Isentos Totais [R$ milhões]": [
        "Rendimentos Isentos - Lucros e dividendos [R$ milhões]",
        "Rendimentos Isentos - Rendim. Sócio/Titular ME/EPP Opt SIMPLES [R$ milhões]",
        "Rendimentos Isentos - Outros Rendimentos Isentos [R$ milhões]",
    ],
    "Despesas Dedutíveis Totais [R$ milhões]": [
        "Despesas Dedutíveis - Previdência [R$ milhões]",
        "Despesas Dedutíveis - Dependentes [R$ milhões]",
        "Despesas Dedutíveis - Instrução [R$ milhões]",
        "Despesas Dedutíveis - Médicas [R$ milhões]",
        "Despesas Dedutíveis - Pensão Alimentícia [R$ milhões]",
        "Despesas Dedutíveis - Livro-Caixa [R$ milhões]",
    ],
    "Bens e Direitos Totais [R$ milhões]": [
        "Bens e Direitos - Imóveis [R$ milhões]",
        "Bens e Direitos - Móveis [R$ milhões]",
        "Bens e Direitos - Financeiros [R$ milhões]",
        "Bens e Direitos - Outros Bens e Direitos [R$ milhões]",
    ],
}

dfT = dfO[colunas_unicas].copy()

for nome_coluna, colunas in grupos_compactados.items():
    dfT[nome_coluna] = dfO[colunas].sum(axis=1)