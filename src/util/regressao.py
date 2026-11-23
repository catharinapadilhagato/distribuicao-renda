from datetime import datetime

from bcb import Expectativas, sgs


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
