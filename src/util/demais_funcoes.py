import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

from bcb import Expectativas, sgs


FORMATO = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


def configurar_log(
    nome: str,
    pasta: str | Path,
    arquivo: str = "app.log",
    nivel: int = logging.DEBUG,
    console: bool = False,
) -> logging.Logger:
    """Cria (ou reaproveita) um logger que grava em `pasta/arquivo`.
    
    nome -> recebe uma string referente ao nome do logger, identificando ele. chamar logging.getLogger("exemplo") em qualquer arquivo retorna ele
    pasta -> recebe uma string ou Path, refere-se a pasta que o arquivo de log será gravada
    arquivo -> recebe uma string que da o nome do arquivo log
    nível -> por padrão recebe .DEBUG, mas pode ser alterado para qualquer nível (DEBUG, INFO, WARNING, ERROR ou CRITICAL)
    console -> definido como False, caso seja True faz com que as mesnagens de log aparecam no terminal
    
    """

    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = (pasta / arquivo).resolve()

    logger = logging.getLogger(nome)
    logger.setLevel(nivel)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(FORMATO, datefmt=FORMATO_DATA)

        arquivo_handler = RotatingFileHandler(
            caminho, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
        )
        arquivo_handler.setFormatter(formatter)
        logger.addHandler(arquivo_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger

def obter_inflacao_anual(ano: int) -> float:
    """Retorna o IPCA anual (%) para um determinado ano.

    - Anos passados: retorna o IPCA efetivo acumulado no ano (SGS 13522).
    - Ano atual ou futuros: retorna a mediana mais recente do Boletim Focus.
    """
    ano_atual = datetime.now().year

    if ano < ano_atual:
        # Código 13522 = IPCA acumulado em 12 meses (%)
        df_historico = sgs.get(
            {'ipca': 13522}, start=f'{ano}-12-01', end=f'{ano}-12-31'
        )

        if df_historico.empty:
            raise ValueError(
                f'Dados históricos do IPCA não encontrados para o ano {ano}.'
            )

        return float(df_historico['ipca'].iloc[-1])
    
    else:
        em = Expectativas()
        ep = em.get_endpoint('ExpectativasMercadoAnuais')

        df_focus = (
            ep.query()
            .filter(ep.Indicador == 'IPCA')
            .filter(ep.DataReferencia == str(ano))
            .filter(ep.baseCalculo == 0)  # Base 0 = projeções mais recentes
            .select(ep.Data, ep.Mediana)
            .collect()
        )

        if df_focus.empty:
            raise ValueError(
                f'Projeção do Boletim Focus não encontrada para o ano {ano}.'
            )
        
        df_focus = df_focus.sort_values('Data')
        return float(df_focus['Mediana'].iloc[-1])
