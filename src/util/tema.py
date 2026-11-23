from pathlib import Path
from urllib.parse import quote

import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
LOGO_GOVBR = RAIZ / "assets" / "govbr_logo.png"

# Cores tiradas do ícone do Ministério da Fazenda e do padrão gov.br
AZUL_FAZENDA = "#1a40ff"
VERDE_ESCURO = "#009c33"
VERDE_CLARO = "#00d000"
AMARELO = "#ffcf00"
VERMELHO = "#ff0000"
AZUL_GOV = "#1351b4"
AZUL_TEXTO = "#1b3a8c"

# Cartões cinza claro (não totalmente brancos)
CARTAO_FUNDO = "#f4f4f5"
CARTAO_BORDA = "#c9c9cc"


def _svg_uri(svg: str) -> str:
    """Transforma um SVG em data URI para usar em background-image."""
    return "data:image/svg+xml;utf8," + quote(svg)


# Fundo cinza geométrico da barra lateral
SVG_SIDEBAR = _svg_uri("""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'>
<defs>
<linearGradient id='a' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#e3e3e4'/><stop offset='1' stop-color='#f3f3f4'/></linearGradient>
<linearGradient id='b' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#f2f2f3'/><stop offset='1' stop-color='#fbfbfb'/></linearGradient>
<radialGradient id='c' cx='.14' cy='.42' r='.8'><stop offset='0' stop-color='#ffffff'/><stop offset='.38' stop-color='#ececed'/><stop offset='1' stop-color='#dcdcdd'/></radialGradient>
<linearGradient id='d' x1='1' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#e8e8e9'/><stop offset='1' stop-color='#f8f8f8'/></linearGradient>
<linearGradient id='e' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#e4e4e5'/><stop offset='1' stop-color='#f1f1f2'/></linearGradient>
</defs>
<rect width='100' height='100' fill='url(#a)'/>
<polygon points='0,0 100,0 100,12 50,86' fill='url(#b)'/>
<polygon points='0,0 50,86 0,100' fill='url(#c)'/>
<polygon points='50,86 100,12 100,84' fill='url(#d)'/>
<polygon points='50,86 100,84 100,100 0,100' fill='url(#e)'/>
</svg>
""")

# Faixa amarela com blocos diagonais, no estilo do portal de Dados Abertos
SVG_FAIXA = _svg_uri("""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 10' preserveAspectRatio='none'>
<rect width='100' height='10' fill='#efdf3f'/>
<rect width='13' height='10' fill='#d9cb4b'/>
<polygon points='13,0 35,0 21.8,10 13,10' fill='#dfd47e'/>
<polygon points='88.8,0 100,0 100,10 84,10' fill='#e9d500'/>
</svg>
""")

# Ícone de casa (máscara) para o caminho da faixa
SVG_CASA = _svg_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>"
    "<path d='M12 3 2 12h3v8h5v-5h4v5h5v-8h3z'/></svg>"
)

CSS = f"""
<style>
/* ---------- Fundo da página (formas do ícone do Ministério da Fazenda) ---------- */
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
    background-color: #efdf3f !important;
    background-image: url("{SVG_FAIXA}") !important;
    background-size: 100% 100% !important;
    background-repeat: no-repeat !important;
    height: 3.75rem;
}}
.faixa-breadcrumb {{
    position: fixed;
    top: 0;
    left: 21rem;
    right: 0;
    height: 3.75rem;
    display: flex;
    align-items: center;
    pointer-events: none;
    z-index: 999990;
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .faixa-breadcrumb {{
    left: 0;
}}
.faixa-breadcrumb .caminho {{
    width: calc(100% - 3rem);
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: {AZUL_TEXTO};
}}
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .faixa-breadcrumb .caminho {{
    padding-left: 3rem;
}}
.faixa-breadcrumb .casa {{
    width: 1rem;
    height: 1rem;
    background: {AZUL_GOV};
    -webkit-mask: url("{SVG_CASA}") center / contain no-repeat;
    mask: url("{SVG_CASA}") center / contain no-repeat;
}}
.faixa-breadcrumb .seta {{
    font-size: 1.25em;
    line-height: 1;
}}

/* ---------- Barra lateral (fundo cinza geométrico) ---------- */
[data-testid="stSidebar"] {{
    background-color: #e3e3e4;
    background-image: url("{SVG_SIDEBAR}");
    background-size: 100% 100%;
    background-repeat: no-repeat;
    border-right: 1px solid #c9c9cc;
}}
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarHeader"] {{
    background: transparent !important;
}}
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] img,
[data-testid="stSidebar"] [data-testid="stLogo"] {{
    max-height: 3rem;
}}
[data-testid="stSidebarNavLink"] {{
    background: rgba(255, 255, 255, 0.6);
    border-radius: 8px;
}}
[data-testid="stSidebarNavLink"][aria-current="page"] {{
    background: {AZUL_GOV} !important;
}}
[data-testid="stSidebarNavLink"][aria-current="page"] * {{
    color: #ffffff !important;
    font-weight: 700;
}}

/* ---------- Área de conteúdo: cartões cinza claro com borda ---------- */
[data-testid="stMainBlockContainer"] {{
    width: calc(100% - 3rem);
    max-width: 1280px !important;
    margin: 4.5rem auto 2.5rem auto;
    padding: 0 !important;
}}
[class*="st-key-cartao_"] {{
    background: {CARTAO_FUNDO};
    border: 1px solid {CARTAO_BORDA};
    border-radius: 10px;
    padding: 1.5rem 2rem;
}}
[class*="st-key-cartao_"] h2,
[class*="st-key-cartao_"] h3 {{
    color: {AZUL_GOV};
}}

/* Abas: a barra de abas vira um cartão */
[data-testid="stTabs"] [role="tablist"] {{
    background: {CARTAO_FUNDO};
    border: 1px solid {CARTAO_BORDA};
    border-radius: 10px;
    padding: 0 0.75rem;
}}
[data-baseweb="tab-panel"] {{
    padding-top: 1rem;
}}
</style>
"""


def cartao(nome: str):
    """Container que aparece como um cartão cinza claro com borda.

    nome -> identificador único do cartão na página (vira a chave do container).
    Uso: with cartao("intro"): st.write(...)
    """
    return st.container(key=f"cartao_{nome}")


def aplicar_tema(titulo_pagina: str):
    """Aplica o visual inspirado no portal de Dados Abertos (gov.br).

    Só altera a aparência: logo na barra lateral, fundos, faixa amarela e cartões.
    """
    if LOGO_GOVBR.exists():
        st.logo(str(LOGO_GOVBR), size="large")

    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="faixa-breadcrumb"><div class="caminho">'
        '<span class="casa" role="img" aria-label="Início"></span>'
        '<span class="seta">›</span>'
        '<span>Distribuição de Renda</span>'
        '<span class="seta">›</span>'
        f'<span>{titulo_pagina}</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )