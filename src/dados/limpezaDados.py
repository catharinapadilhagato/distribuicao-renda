from pathlib import Path

import pandas as pd

from src.dados.extracaoDados import main
from src.util.funcaoLog import configurar_log

# ---------------------------------------------------------------- logging

PASTA_LOGS = Path(__file__).parent / "logs"
PASTA_LOGS.mkdir(parents=True, exist_ok=True)


logger = configurar_log('limpeza',
                        PASTA_LOGS,
                        'limpeza.log')

df = main()

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

assert len(df.columns) == len(nome_colunas), logger.error(f'"{len(df.columns)} colunas no DataFrame, {len(nome_colunas)} nomes na lista"')

for antigo, novo in zip(df.columns, nome_colunas):
    logger.info(f"coluna '{antigo}' alterada para '{novo}'")


df.columns = nome_colunas