import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

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