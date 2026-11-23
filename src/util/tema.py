from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
LOGO_GOVBR = RAIZ / "assets" / "govbr_logo.png"

# Cores tiradas do ícone do Ministério da Fazenda e do padrão gov.br
AZUL_FAZENDA = "#1a40ff"
VERDE_ESCURO = "#009c33"
VERDE_CLARO = "#00d000"
AMARELO = "#ffcf00"
VERMELHO = "#ff0000"
AMARELO_FAIXA = "#ecd93b"
AZUL_GOV = "#1351b4"

CSS = f"""
<style>
/* ---------- Fundo (formas do ícone do Ministério da Fazenda) ---------- */
[data-testid="stApp"] {{
    background: {AZUL_FAZENDA};
    isolation: isolate;
}}
[data-testid="stApp"]::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: {VERDE_ESCURO};
    clip-path: polygon(34% 0, 100% 0, 100% 100%, 80% 100%);
    pointer-events: none;
    z-index: -1;
}}
[data-testid="stApp"]::after {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: -1;
    background:
        linear-gradient({VERMELHO}, {VERMELHO}) 100% 100% / 48% 20% no-repeat,
        radial-gradient(circle 62vw at 6vw calc(62vh + 62vw), {AMARELO} 99.5%, transparent 100%),
        radial-gradient(circle 36vw at 84vw -9vw, {VERDE_CLARO} 99.5%, transparent 100%);
}}
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: transparent !important;
}}

/* ---------- Faixa amarela do topo ---------- */
[data-testid="stHeader"] {{
    background: {AMARELO_FAIXA} !important;
    height: 3.75rem;
}}
.faixa-breadcrumb {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3.75rem;
    display: flex;
    align-items: center;
    padding-left: calc(21rem + 1.5rem);
    font-size: 0.875rem;
    font-weight: 500;
    color: {AZUL_GOV};
    pointer-events: none;
    z-index: 999990;
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .faixa-breadcrumb {{
    padding-left: 4rem;
}}

/* ---------- Barra lateral ---------- */
[data-testid="stSidebar"] {{
    background: #ffffff;
    border-right: 1px solid #d9d9d9;
}}
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] img,
[data-testid="stSidebar"] [data-testid="stLogo"] {{
    max-height: 3rem;
}}

/* ---------- Área de conteúdo: cartões brancos com borda ---------- */
[data-testid="stMainBlockContainer"] {{
    width: calc(100% - 3rem);
    max-width: 1280px !important;
    margin: 4.5rem auto 2.5rem auto;
    padding: 0 !important;
}}
[class*="st-key-cartao_"] {{
    background: #ffffff;
    border: 1px solid #cfcfcf;
    border-radius: 10px;
    padding: 1.5rem 2rem;
}}
[class*="st-key-cartao_"] h2,
[class*="st-key-cartao_"] h3 {{
    color: {AZUL_GOV};
}}

/* Abas: a barra de abas vira um cartão branco */
[data-testid="stTabs"] [role="tablist"] {{
    background: #ffffff;
    border: 1px solid #cfcfcf;
    border-radius: 10px;
    padding: 0 0.75rem;
}}
[data-baseweb="tab-panel"] {{
    padding-top: 1rem;
}}
</style>
"""


def cartao(nome: str):
    """Container que aparece como um cartão branco com borda.

    nome -> identificador único do cartão na página (vira a chave do container).
    Uso: with cartao("intro"): st.write(...)
    """
    return st.container(key=f"cartao_{nome}")


def aplicar_tema(titulo_pagina: str):
    """Aplica o visual inspirado no portal de Dados Abertos (gov.br).

    Só altera a aparência: logo na barra lateral, fundo, faixa amarela e bordas.
    """
    if LOGO_GOVBR.exists():
        st.logo(str(LOGO_GOVBR), size="large")

    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="faixa-breadcrumb">Dados Abertos &nbsp;›&nbsp; '
        f'Distribuição de Renda &nbsp;›&nbsp; {titulo_pagina}</div>',
        unsafe_allow_html=True,
    )