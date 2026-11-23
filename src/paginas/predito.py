from src.dados.limpezaDados import dfAgregado
from src.util.eda import renderizar_eda
from src.util.tema import cartao

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
- A coluna "Rendimentos Tributáveis Totais [R\$ milhões]" foi renomeada para "Renda Total [R$ milhões]";
- As colunas dos anos anteriores escolhidas não fazem parte do cálculo padrão do RB2, o que acaba não comentendo vazamento de dados.
'''
    )

renderizar_eda(dfAgregado, 'dfAgregado')