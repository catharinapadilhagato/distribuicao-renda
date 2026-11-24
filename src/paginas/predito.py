from src.dados.limpezaDados import dfAgregado
from src.util.eda import renderizar_eda
from src.util.tema import cartao
from src.util.regressao.testes_estatistica import teste_cenarios

import streamlit as st
import html

with cartao("predito_titulo"):
    st.title('Predição da distruibuição de renda', text_alignment="center")

with cartao("predito_preparo"):
    st.markdown(
        '''
Para atingir o objetivo, o conjunto de dados foi mais uma vez modificado, modificando o conjunto transformado. Na modificação, 
a base inclui uma comparação do RB2 do ano atual com o anterior, e também pega os valores do ano anterior:
- O conjunto transformado foi agrupado com base no ano e ente federativo, ordenando pelo ano;
- Os valores de 2006 foram excluídos da tabela por serem os primeiros anos do conjunto de dados, logo, não possuem um ano anterior para realizar
a comparação. (se por acaso retirarem o ano de 2006 futuramente, ou adicionarem <=2005, o primeiro ano do conjunto de dados vai ser excluído da tabela);
- A coluna "Rendimentos Tributáveis Totais [R\$ milhões]" foi renomeada para "Renda Total [R\$ milhões]";
- As colunas dos anos anteriores escolhidas não fazem parte do cálculo padrão do RB2, o que acaba não comentendo vazamento de dados.

A coluna a ser predita, o nosso target, será "Renda Total [R\$ milhões]". 

E as características utilizadas para prever serão:
- Ano-calendário;
- Ente Federativo;
- Renda Total (ano anterior);
- Quantidade de Contribuintes (ano anterior);
- Rendimentos Isentos - Outros Rendimentos Isentos (ano anterior);
- Imposto Devido (ano anterior);
- Despesas Dedutíveis Totais (ano anterior);
- Bens e Direitos Totais (ano anterior);
- Dívidas e Ônus (ano anterior).

Todos os modelos testados usaram os últimos 4 anos disponíveis no conjunto de dados para teste
'''
    )

renderizar_eda(dfAgregado, 'dfAgregado')


with cartao("cenarios"):
    st.title("Verificando Cenários")
    st.markdown('''
    Primeiro, será testado através do calculo do MAE e MAPE se o ano e o estado fornecem alguma mudança significativa no erro médio absoluto.
    Para isso foram testados 5 cenários:
    - A. Só o ano anterior da renda;
    - B. Todas as colunas lags;
    - C. B + ano;
    - D. B + estado;
    - E. B + ano + estado.
    ''')
    resultado_cenarios = teste_cenarios(dfAgregado)
    st.dataframe(resultado_cenarios)
    st.markdown(f'''
O cenário que mostrou o menor erro  médio porcentual absoluto foi o cenário E, que considera todas as colunas + ano + estado, 
com {(resultado_cenarios.iloc[0, 1])*100:.2f}% de erro médio. O cenário mostra que para Regressão Linear Múltipla ele é ideal, porém, olhando apenas para o MAE, o cenário A apresenta
o menor erro médio absoluto com {resultado_cenarios.iloc[4, 0]:.2f} [em milhões de R$] podendo ser usado Regressão Linear Simples apenas para predizer o rendimento, sem considerar
o estado ou ano.
    ''')

