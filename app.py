
import os
import re
import shutil
from datetime import date, datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st

# =========================================================
# SISTEMA DE COTAÇÕES MARIALVA — INTERFACE V5
# Foco: operação simples, visual, fluxo guiado e tela do vendedor.
# =========================================================

st.set_page_config(
    page_title="Sistema de Cotações Marialva",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Ajuste visual V5.1 — esconder barra superior do Streamlit
st.markdown("""
<style>
/* MARIALVA_HIDE_STREAMLIT_HEADER_V51 */

[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

.block-container {
    padding-top: 0.8rem !important;
}


    /* MARIALVA_V51_REFINOS_USABILIDADE */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
    }

    #MainMenu, footer {
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 0.75rem !important;
        max-width: 1120px !important;
    }

    .hero {
        padding: 20px 26px !important;
        border-radius: 24px !important;
        margin-bottom: 14px !important;
    }

    .hero-title {
        font-size: 26px !important;
        margin-bottom: 4px !important;
    }

    .hero-subtitle {
        font-size: 15px !important;
        margin-bottom: 14px !important;
    }

    .flow-step {
        padding: 8px 12px !important;
        font-size: 13px !important;
    }

    .today-box {
        padding: 16px 18px !important;
        border-radius: 20px !important;
        margin: 10px 0 18px 0 !important;
    }

    .today-line {
        line-height: 1.55 !important;
    }

    .attention-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        margin: 4px 8px 4px 0;
        padding: 8px 11px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,.25);
        background: rgba(15,23,42,.72);
        color: #DCEBFF;
        font-size: 13px;
        font-weight: 800;
    }

    .attention-pill strong {
        color: #FFFFFF;
        font-weight: 950;
    }

    .mini-alert {
        margin-top: 10px;
        padding: 11px 13px;
        border-radius: 14px;
        background: rgba(56,189,248,.08);
        border: 1px solid rgba(56,189,248,.22);
        color: #BAE6FD;
        font-size: 14px;
        font-weight: 750;
    }

    .metric-card {
        min-height: 92px !important;
        padding: 16px 18px !important;
        border-radius: 20px !important;
    }

    .metric-value {
        font-size: 29px !important;
    }

    .action-card {
        min-height: 146px !important;
        padding: 18px 20px 16px 20px !important;
        border-radius: 22px !important;
    }

    .icon-badge {
        width: 44px !important;
        height: 44px !important;
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        font-size: 22px !important;
    }

    .action-title {
        font-size: 17px !important;
    }

    .action-text {
        font-size: 14px !important;
        min-height: 38px !important;
    }

    .section-title {
        margin: 18px 0 10px 0 !important;
        font-size: 21px !important;
    }

    .clean-table {
        width: 100%;
        border-collapse: collapse;
        overflow: hidden;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,.22);
        background: rgba(15,23,42,.62);
        font-size: 14px;
    }

    .clean-table th {
        text-align: left;
        color: #AFC3E2;
        padding: 12px 13px;
        border-bottom: 1px solid rgba(148,163,184,.18);
        background: rgba(15,23,42,.86);
        font-size: 13px;
    }

    .clean-table td {
        padding: 12px 13px;
        color: #F8FAFC;
        border-bottom: 1px solid rgba(148,163,184,.10);
    }

    .clean-table tr:last-child td {
        border-bottom: none;
    }

    .clean-table .muted {
        color: #9FB4D0;
    }



    /* MARIALVA_V6_CLEAN_APPLE_LIKE */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
    }

    #MainMenu, footer { visibility: hidden !important; }

    .block-container {
        padding-top: 0.35rem !important;
        padding-bottom: 1.2rem !important;
        max-width: 1080px !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 20% 8%, rgba(59,130,246,.10), transparent 28%),
            radial-gradient(circle at 82% 2%, rgba(168,85,247,.09), transparent 32%),
            linear-gradient(180deg, #070A12 0%, #090D16 100%) !important;
    }

    div[data-testid="stVerticalBlock"] { gap: 0.65rem !important; }
    .element-container { margin-bottom: 0 !important; }

    /* Navegação: mais discreta, estilo abas/pílulas */
    div.stButton > button {
        border-radius: 999px !important;
        min-height: 42px !important;
        padding: 0.46rem 0.85rem !important;
        border: 1px solid rgba(148,163,184,.26) !important;
        background: rgba(15,23,42,.58) !important;
        color: #F8FAFC !important;
        font-weight: 850 !important;
        letter-spacing: -0.02em !important;
        box-shadow: 0 10px 25px rgba(0,0,0,.16) !important;
        transition: all .16s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        border-color: rgba(255,255,255,.42) !important;
        background: rgba(30,41,59,.76) !important;
        box-shadow: 0 14px 36px rgba(0,0,0,.24) !important;
    }

    .v6-shell {
        min-height: calc(100vh - 32px);
    }

    .v6-hero {
        display: grid;
        grid-template-columns: 1.25fr .75fr;
        gap: 18px;
        align-items: center;
        padding: 22px 26px;
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,.12);
        background:
            radial-gradient(circle at 12% 20%, rgba(56,189,248,.18), transparent 34%),
            radial-gradient(circle at 95% 10%, rgba(167,139,250,.19), transparent 42%),
            rgba(15,23,42,.58);
        box-shadow: 0 24px 80px rgba(0,0,0,.26);
        backdrop-filter: blur(22px);
        margin: 0.25rem 0 0.85rem 0;
    }

    .v6-kicker {
        color: #93C5FD;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin-bottom: 6px;
    }

    .v6-title {
        color: #FFFFFF;
        font-size: 30px;
        line-height: 1.05;
        letter-spacing: -0.045em;
        font-weight: 950;
        margin: 0;
    }

    .v6-subtitle {
        color: #B8C7DD;
        font-size: 14px;
        line-height: 1.45;
        margin-top: 10px;
        max-width: 620px;
    }

    .v6-next {
        border-radius: 24px;
        border: 1px solid rgba(56,189,248,.20);
        background: rgba(2,132,199,.10);
        padding: 16px 17px;
    }

    .v6-next-label {
        color: #7DD3FC;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 8px;
    }

    .v6-next-main {
        color: #F8FAFC;
        font-size: 17px;
        font-weight: 950;
        line-height: 1.22;
        margin-bottom: 7px;
    }

    .v6-next-meta {
        color: #AFC3E2;
        font-size: 13px;
        line-height: 1.35;
    }

    .v6-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 0 0 .85rem 0;
    }

    .v6-stat {
        border-radius: 22px;
        border: 1px solid rgba(148,163,184,.18);
        background: rgba(15,23,42,.50);
        padding: 12px 14px;
        min-height: 72px;
        backdrop-filter: blur(16px);
    }

    .v6-stat-label {
        color: #AFC3E2;
        font-size: 12px;
        font-weight: 850;
        margin-bottom: 6px;
    }

    .v6-stat-value {
        color: #FFFFFF;
        font-size: 25px;
        line-height: 1;
        font-weight: 950;
        letter-spacing: -0.04em;
    }

    .v6-actions-title {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 950;
        letter-spacing: -0.03em;
        margin: 0.15rem 0 0.55rem 0;
    }

    .v6-action {
        position: relative;
        height: 122px;
        border-radius: 26px;
        border: 1px solid rgba(148,163,184,.18);
        background: rgba(15,23,42,.52);
        overflow: hidden;
        padding: 16px 15px 12px 15px;
        box-shadow: 0 18px 50px rgba(0,0,0,.16);
        backdrop-filter: blur(18px);
    }

    .v6-action::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 12% 0%, var(--accent-soft), transparent 46%);
        pointer-events: none;
    }

    .v6-action-icon {
        position: relative;
        display: inline-flex;
        width: 38px;
        height: 38px;
        border-radius: 15px;
        align-items: center;
        justify-content: center;
        background: var(--accent-bg);
        border: 1px solid var(--accent-line);
        font-size: 20px;
        margin-bottom: 10px;
    }

    .v6-action-title {
        position: relative;
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 950;
        letter-spacing: -0.025em;
        margin-bottom: 4px;
    }

    .v6-action-text {
        position: relative;
        color: #AFC3E2;
        font-size: 12px;
        line-height: 1.28;
    }

    .v6-quiet-note {
        color: #8EA8C8;
        font-size: 12px;
        margin-top: .55rem;
        text-align: center;
    }

    .hero, .today-box, .metric-card, .section-title, .clean-table {
        display: none !important;
    }

    @media (max-width: 900px) {
        .v6-hero { grid-template-columns: 1fr; }
        .v6-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .v6-title { font-size: 26px; }
    }



    /* MARIALVA_V6_CORRIGIDA_CLEAN_61 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
    }
    #MainMenu, footer { visibility: hidden !important; }

    .block-container {
        padding-top: 0.55rem !important;
        padding-bottom: 0.8rem !important;
        max-width: 1010px !important;
    }

    div[data-testid="stVerticalBlock"] { gap: 0.45rem !important; }
    .element-container { margin-bottom: 0 !important; }
    .v6-shell { min-height: auto !important; }

    .v6-hero {
        display: grid !important;
        grid-template-columns: 1.35fr .65fr !important;
        gap: 14px !important;
        align-items: center !important;
        padding: 18px 22px !important;
        border-radius: 26px !important;
        margin: 0.45rem 0 0.65rem 0 !important;
        border: 1px solid rgba(255,255,255,.13) !important;
        background:
            radial-gradient(circle at 18% 0%, rgba(59,130,246,.22), transparent 38%),
            radial-gradient(circle at 92% 10%, rgba(168,85,247,.18), transparent 40%),
            rgba(15,23,42,.58) !important;
        box-shadow: 0 18px 55px rgba(0,0,0,.23) !important;
        backdrop-filter: blur(22px) !important;
    }

    .v6-kicker {
        color: #93C5FD !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: .08em !important;
        margin-bottom: 4px !important;
    }

    .v6-title {
        color: #FFFFFF !important;
        font-size: 28px !important;
        line-height: 1.05 !important;
        letter-spacing: -0.045em !important;
        font-weight: 950 !important;
        margin: 0 !important;
    }

    .v6-subtitle {
        color: #B8C7DD !important;
        font-size: 13.5px !important;
        line-height: 1.35 !important;
        margin-top: 9px !important;
        max-width: 640px !important;
    }

    .v6-next {
        border-radius: 21px !important;
        border: 1px solid rgba(56,189,248,.20) !important;
        background: rgba(2,132,199,.10) !important;
        padding: 13px 14px !important;
    }

    .v6-next-label {
        color: #7DD3FC !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: .06em !important;
        margin-bottom: 6px !important;
    }

    .v6-next-main {
        color: #F8FAFC !important;
        font-size: 15px !important;
        font-weight: 950 !important;
        line-height: 1.22 !important;
        margin-bottom: 0 !important;
    }

    .v6-next-meta {
        color: #AFC3E2 !important;
        font-size: 12px !important;
        line-height: 1.3 !important;
    }

    .v6-strip {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 10px !important;
        margin: 0 0 .55rem 0 !important;
    }

    .v6-stat {
        border-radius: 19px !important;
        border: 1px solid rgba(148,163,184,.18) !important;
        background: rgba(15,23,42,.50) !important;
        padding: 10px 13px !important;
        min-height: 64px !important;
        backdrop-filter: blur(16px) !important;
    }

    .v6-stat-label {
        color: #AFC3E2 !important;
        font-size: 11.5px !important;
        font-weight: 850 !important;
        margin-bottom: 5px !important;
    }

    .v6-stat-value {
        color: #FFFFFF !important;
        font-size: 23px !important;
        line-height: 1 !important;
        font-weight: 950 !important;
        letter-spacing: -0.04em !important;
    }

    .v6-actions-title {
        color: #F8FAFC !important;
        font-size: 14px !important;
        font-weight: 950 !important;
        letter-spacing: -0.02em !important;
        margin: 0.15rem 0 0.45rem 0 !important;
    }

    .v6-action {
        height: 104px !important;
        border-radius: 22px !important;
        padding: 13px 13px 11px 13px !important;
        border: 1px solid rgba(148,163,184,.18) !important;
        background: rgba(15,23,42,.52) !important;
        overflow: hidden !important;
        box-shadow: 0 14px 40px rgba(0,0,0,.14) !important;
        backdrop-filter: blur(18px) !important;
    }

    .v6-action-icon {
        width: 34px !important;
        height: 34px !important;
        border-radius: 13px !important;
        font-size: 18px !important;
        margin-bottom: 8px !important;
    }

    .v6-action-title {
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 950 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 3px !important;
    }

    .v6-action-text {
        color: #AFC3E2 !important;
        font-size: 11.5px !important;
        line-height: 1.25 !important;
    }

    div.stButton > button {
        min-height: 38px !important;
        padding: 0.35rem 0.7rem !important;
        border-radius: 999px !important;
        border: 1px solid rgba(148,163,184,.24) !important;
        background: rgba(15,23,42,.58) !important;
        color: #F8FAFC !important;
        font-weight: 850 !important;
        box-shadow: none !important;
    }

    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        background: rgba(30,41,59,.78) !important;
        border-color: rgba(255,255,255,.42) !important;
    }

    .v6-quiet-note {
        display: none !important;
    }

    @media (max-width: 900px) {
        .v6-hero { grid-template-columns: 1fr !important; }
        .v6-strip { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
        .v6-title { font-size: 24px !important; }
    }

</style>
""", unsafe_allow_html=True)


PASTA_DADOS = "dados"
PASTA_BACKUPS = "backups"

ARQUIVOS = {
    "produtos": os.path.join(PASTA_DADOS, "produtos.csv"),
    "fornecedores": os.path.join(PASTA_DADOS, "fornecedores.csv"),
    "cotacoes": os.path.join(PASTA_DADOS, "cotacoes.csv"),
    "itens_cotacao": os.path.join(PASTA_DADOS, "itens_cotacao.csv"),
    "respostas": os.path.join(PASTA_DADOS, "respostas.csv"),
}

COLUNAS = {
    "produtos": ["ProdutoID", "Produto", "Marca", "Tamanho", "Categoria", "Unidade", "Ativo", "Observacao"],
    "fornecedores": ["FornecedorID", "Vendedor", "Empresa", "WhatsApp", "CategoriaForte", "Ativo", "Observacao"],
    "cotacoes": ["CotacaoID", "Data", "Prazo", "Status", "Responsavel", "Observacao"],
    "itens_cotacao": ["ItemID", "CotacaoID", "ProdutoID", "QuantidadeDesejada", "Observacao"],
    "respostas": ["RespostaID", "CotacaoID", "FornecedorID", "ProdutoID", "Preco", "TemProduto", "Observacao"],
}

# -------------------------
# CSS / VISUAL
# -------------------------
st.markdown(
    """
<style>
    :root {
        --bg: #070B13;
        --panel: #0E172A;
        --panel2: #111C32;
        --text: #F8FAFC;
        --muted: #9FB4D0;
        --line: rgba(148,163,184,.22);
        --blue: #38BDF8;
        --orange: #FB923C;
        --green: #22C55E;
        --purple: #A78BFA;
        --pink: #F472B6;
        --yellow: #FACC15;
        --red: #EF4444;
    }

    .block-container {
        padding-top: 2.0rem !important;
        padding-bottom: 4rem !important;
        max-width: 1180px;
    }

    header[data-testid="stHeader"] {
        background: rgba(7, 11, 19, 0.72);
        backdrop-filter: blur(14px);
    }

    [data-testid="stSidebar"] {
        background: #080D18;
    }

    h1, h2, h3, h4, p, label, span {
        letter-spacing: -0.01em;
    }

    .hero {
        padding: 26px 30px;
        border-radius: 28px;
        background: radial-gradient(circle at 15% 20%, rgba(56,189,248,.26), transparent 32%),
                    radial-gradient(circle at 90% 10%, rgba(167,139,250,.28), transparent 38%),
                    linear-gradient(135deg, #0B1B2E 0%, #161B3B 100%);
        border: 1px solid rgba(148,163,184,.24);
        box-shadow: 0 24px 70px rgba(0,0,0,.25);
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 28px;
        font-weight: 900;
        color: var(--text);
        margin: 0 0 6px 0;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #C7D7EF;
        margin: 0 0 18px 0;
    }

    .flow {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
    }

    .flow-step {
        padding: 10px 14px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.12);
        background: rgba(3,7,18,.48);
        color: #E5EEF9;
        font-weight: 800;
        font-size: 14px;
    }

    .today-box {
        padding: 18px 20px;
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(15,23,42,.98), rgba(15,23,42,.72));
        border: 1px solid rgba(148,163,184,.24);
        margin: 12px 0 20px 0;
    }

    .today-title {
        color: white;
        font-size: 20px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .today-line {
        color: #C7D7EF;
        font-size: 15px;
        line-height: 1.45;
    }

    .metric-card {
        padding: 18px 20px;
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(15,23,42,.98), rgba(15,23,42,.74));
        border: 1px solid rgba(148,163,184,.24);
        min-height: 104px;
        box-shadow: 0 16px 50px rgba(0,0,0,.18);
    }

    .metric-label {
        color: var(--muted);
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--text);
        font-size: 32px;
        font-weight: 950;
        line-height: 1;
    }

    .metric-help {
        color: #8EA8C8;
        font-size: 12px;
        margin-top: 7px;
    }

    .action-card {
        position: relative;
        padding: 22px 22px 20px 22px;
        border-radius: 24px;
        background: linear-gradient(145deg, rgba(15,23,42,.96), rgba(15,23,42,.76));
        border: 1px solid rgba(148,163,184,.24);
        min-height: 170px;
        overflow: hidden;
        box-shadow: 0 18px 60px rgba(0,0,0,.18);
        transition: all .18s ease;
    }

    .action-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,.36);
        box-shadow: 0 22px 70px rgba(0,0,0,.24);
    }

    .action-card:before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 7px;
        background: var(--accent);
        box-shadow: 0 0 28px var(--accent);
    }

    .icon-badge {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        background: color-mix(in srgb, var(--accent) 26%, transparent);
        border: 1px solid color-mix(in srgb, var(--accent) 58%, transparent);
        font-size: 24px;
        margin-bottom: 16px;
    }

    .action-title {
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 950;
        margin-bottom: 8px;
    }

    .action-text {
        color: #C7D7EF;
        font-size: 15px;
        line-height: 1.45;
        min-height: 44px;
    }

    .tiny-note {
        color: #91A7C7;
        font-size: 13px;
        margin-top: 8px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 950;
        color: white;
        margin: 22px 0 12px 0;
    }

    .status-chip {
        display: inline-flex;
        align-items: center;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 900;
        border: 1px solid rgba(255,255,255,.16);
        background: rgba(15,23,42,.95);
    }

    .chip-green { color:#86EFAC; border-color:rgba(34,197,94,.35); }
    .chip-blue { color:#7DD3FC; border-color:rgba(56,189,248,.35); }
    .chip-yellow { color:#FDE68A; border-color:rgba(250,204,21,.35); }
    .chip-red { color:#FCA5A5; border-color:rgba(239,68,68,.35); }
    .chip-gray { color:#CBD5E1; border-color:rgba(148,163,184,.30); }

    div.stButton > button {
        border-radius: 16px !important;
        border: 1px solid rgba(148,163,184,.30) !important;
        background: rgba(15,23,42,.72) !important;
        color: white !important;
        font-weight: 900 !important;
        min-height: 46px;
        transition: all .15s ease;
    }

    div.stButton > button:hover {
        border-color: rgba(255,255,255,.46) !important;
        background: rgba(30,41,59,.92) !important;
        transform: translateY(-1px);
    }

    .vendor-hero {
        padding: 24px 28px;
        border-radius: 26px;
        background: linear-gradient(135deg, rgba(34,197,94,.20), rgba(56,189,248,.18)), #0E172A;
        border: 1px solid rgba(148,163,184,.24);
        margin-bottom: 18px;
    }

    .warning-box {
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(250,204,21,.08);
        border: 1px solid rgba(250,204,21,.22);
        color: #FDE68A;
        font-weight: 700;
        margin: 8px 0 14px 0;
    }

    .success-box {
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(34,197,94,.08);
        border: 1px solid rgba(34,197,94,.22);
        color: #BBF7D0;
        font-weight: 700;
        margin: 8px 0 14px 0;
    }

    .admin-small {
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(15,23,42,.64);
        border: 1px solid rgba(148,163,184,.22);
        color: #C7D7EF;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(148,163,184,.18) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# FUNÇÕES DE DADOS
# -------------------------

def criar_arquivos_iniciais():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    os.makedirs(PASTA_BACKUPS, exist_ok=True)
    for nome, caminho in ARQUIVOS.items():
        if not os.path.exists(caminho):
            pd.DataFrame(columns=COLUNAS[nome]).to_csv(caminho, index=False, encoding="utf-8-sig")


def carregar(nome):
    caminho = ARQUIVOS[nome]
    if not os.path.exists(caminho):
        pd.DataFrame(columns=COLUNAS[nome]).to_csv(caminho, index=False, encoding="utf-8-sig")
    df = pd.read_csv(caminho, encoding="utf-8-sig", dtype=str).fillna("")
    for col in COLUNAS[nome]:
        if col not in df.columns:
            df[col] = ""
    return df[COLUNAS[nome]].copy()


def salvar(nome, df):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    df = df.copy()
    for col in COLUNAS[nome]:
        if col not in df.columns:
            df[col] = ""
    df[COLUNAS[nome]].to_csv(ARQUIVOS[nome], index=False, encoding="utf-8-sig")


def gerar_id(prefixo, df, coluna_id):
    if df.empty or coluna_id not in df.columns:
        return f"{prefixo}001"
    nums = df[coluna_id].astype(str).str.extract(r"(\d+)")[0]
    nums = pd.to_numeric(nums, errors="coerce").dropna()
    prox = int(nums.max()) + 1 if not nums.empty else 1
    return f"{prefixo}{prox:03d}"


def moeda(v):
    try:
        f = float(str(v).replace("R$", "").replace(".", "").replace(",", ".").strip())
        return f"R$ {f:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return ""


def preco_float(v):
    try:
        s = str(v).replace("R$", "").strip()
        if "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", ".")
        return float(s)
    except Exception:
        return None


def normalizar_texto(txt):
    txt = str(txt).lower().strip()
    txt = re.sub(r"\s+", " ", txt)
    return txt


def produto_label(row):
    partes = [row.get("Produto", ""), row.get("Marca", ""), row.get("Tamanho", "")]
    desc = " ".join([str(p).strip() for p in partes if str(p).strip()])
    return f"{row.get('ProdutoID','')} — {desc}".strip()


def fornecedor_label(row):
    partes = [row.get("Vendedor", ""), row.get("Empresa", "")]
    desc = " / ".join([str(p).strip() for p in partes if str(p).strip()])
    return f"{row.get('FornecedorID','')} — {desc}".strip()


def status_chip(status):
    s = str(status).strip().lower()
    if "final" in s or "pedido" in s:
        klass, icon = "chip-green", "●"
    elif "abert" in s:
        klass, icon = "chip-blue", "●"
    elif "aguard" in s or "parcial" in s:
        klass, icon = "chip-yellow", "●"
    elif "atras" in s or "cancel" in s:
        klass, icon = "chip-red", "●"
    else:
        klass, icon = "chip-gray", "●"
    return f'<span class="status-chip {klass}">{icon} {status}</span>'


def backup_geral():
    os.makedirs(PASTA_BACKUPS, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta = os.path.join(PASTA_BACKUPS, f"backup_{stamp}")
    os.makedirs(pasta, exist_ok=True)
    for nome, caminho in ARQUIVOS.items():
        if os.path.exists(caminho):
            shutil.copy2(caminho, os.path.join(pasta, os.path.basename(caminho)))
    if os.path.exists("app.py"):
        shutil.copy2("app.py", os.path.join(pasta, "app.py"))
    return pasta


def get_query_param(nome):
    try:
        val = st.query_params.get(nome, "")
        if isinstance(val, list):
            return val[0] if val else ""
        return val
    except Exception:
        try:
            val = st.experimental_get_query_params().get(nome, [""])
            return val[0] if isinstance(val, list) else val
        except Exception:
            return ""


def set_tela(nome):
    st.session_state.tela = nome


def carregar_tudo():
    return {
        "produtos": carregar("produtos"),
        "fornecedores": carregar("fornecedores"),
        "cotacoes": carregar("cotacoes"),
        "itens": carregar("itens_cotacao"),
        "respostas": carregar("respostas"),
    }

criar_arquivos_iniciais()

# -------------------------
# TELA DO VENDEDOR
# -------------------------

def tela_vendedor():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]
    respostas = dados["respostas"]

    cotacao_id = get_query_param("cotacao") or get_query_param("cotacao_id")
    fornecedor_id = get_query_param("fornecedor") or get_query_param("fornecedor_id")

    st.markdown(
        """
        <div class="vendor-hero">
            <div class="hero-title">🛒 Cotação — Supermercado Marialva</div>
            <div class="hero-subtitle">Preencha apenas os preços dos itens disponíveis. Se não tiver, marque como indisponível.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not cotacao_id or not fornecedor_id:
        st.error("Link incompleto. Peça ao responsável da cotação para reenviar o link correto.")
        return

    if cotacao_id not in cotacoes["CotacaoID"].astype(str).tolist():
        st.error(f"Cotação {cotacao_id} não encontrada.")
        return

    if fornecedor_id not in fornecedores["FornecedorID"].astype(str).tolist():
        st.error(f"Fornecedor {fornecedor_id} não encontrado.")
        return

    cot = cotacoes[cotacoes["CotacaoID"].astype(str) == cotacao_id].iloc[0]
    forn = fornecedores[fornecedores["FornecedorID"].astype(str) == fornecedor_id].iloc[0]
    nome_vendedor = forn.get("Vendedor", fornecedor_id)

    itens_cot = itens[itens["CotacaoID"].astype(str) == cotacao_id].merge(produtos, on="ProdutoID", how="left")
    if itens_cot.empty:
        st.warning("Essa cotação ainda não possui itens.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Cotação", cotacao_id)
    col2.metric("Vendedor", nome_vendedor)
    col3.metric("Itens", len(itens_cot))

    st.markdown('<div class="warning-box">Dica: use vírgula ou ponto no preço. Exemplo: 9,15 ou 9.15.</div>', unsafe_allow_html=True)

    ja_resp = respostas[(respostas["CotacaoID"].astype(str) == cotacao_id) & (respostas["FornecedorID"].astype(str) == fornecedor_id)]
    if not ja_resp.empty:
        st.info("Já existem respostas salvas para essa cotação. Se enviar novamente, os itens preenchidos serão atualizados.")

    with st.form(f"form_vendedor_{cotacao_id}_{fornecedor_id}"):
        novos_registros = []
        st.subheader("Itens da cotação")
        for _, row in itens_cot.iterrows():
            pid = str(row["ProdutoID"])
            desc = " ".join([str(row.get("Produto", "")), str(row.get("Marca", "")), str(row.get("Tamanho", ""))]).strip()
            qtd = row.get("QuantidadeDesejada", "")

            existente = ja_resp[ja_resp["ProdutoID"].astype(str) == pid]
            preco_atual = ""
            tem_atual = True
            obs_atual = ""
            if not existente.empty:
                preco_atual = str(existente.iloc[-1].get("Preco", ""))
                tem_atual = str(existente.iloc[-1].get("TemProduto", "Sim")) != "Não"
                obs_atual = str(existente.iloc[-1].get("Observacao", ""))

            with st.container(border=True):
                st.markdown(f"**{desc}**  ")
                st.caption(f"Código: {pid} | Quantidade solicitada: {qtd if str(qtd).strip() else '-'}")
                c1, c2, c3 = st.columns([1.2, 1.1, 2.2])
                tem_produto = c1.checkbox("Tenho", value=tem_atual, key=f"tem_{pid}_{fornecedor_id}_{cotacao_id}")
                preco = c2.text_input("Preço", value=preco_atual, placeholder="Ex: 9,15", key=f"preco_{pid}_{fornecedor_id}_{cotacao_id}")
                obs = c3.text_input("Observação", value=obs_atual, placeholder="Opcional", key=f"obs_{pid}_{fornecedor_id}_{cotacao_id}")
                novos_registros.append((pid, tem_produto, preco, obs))

        enviar = st.form_submit_button("✅ Enviar cotação")

    if enviar:
        respostas_novas = respostas.copy()
        # remove respostas anteriores desse fornecedor/cotacao para evitar duplicidade
        mask = ~((respostas_novas["CotacaoID"].astype(str) == cotacao_id) & (respostas_novas["FornecedorID"].astype(str) == fornecedor_id))
        respostas_novas = respostas_novas[mask].copy()
        for pid, tem, preco_txt, obs in novos_registros:
            tem_prod = "Sim" if tem else "Não"
            preco_val = preco_float(preco_txt) if tem else None
            if tem and preco_val is None:
                # se tem produto mas preço vazio, não cadastra o item
                continue
            novo_id = gerar_id("RESP", respostas_novas, "RespostaID")
            novo = pd.DataFrame([{
                "RespostaID": novo_id,
                "CotacaoID": cotacao_id,
                "FornecedorID": fornecedor_id,
                "ProdutoID": pid,
                "Preco": preco_val if preco_val is not None else "",
                "TemProduto": tem_prod,
                "Observacao": obs,
            }])
            respostas_novas = pd.concat([respostas_novas, novo], ignore_index=True)
        salvar("respostas", respostas_novas)
        st.success("Cotação enviada com sucesso. Obrigado!")
        st.balloons()

# -------------------------
# COMPONENTES INTERNOS
# -------------------------

def hero():
    st.markdown(
        """
        <div class="v6-hero">
            <div>
                <div class="v6-kicker">Supermercado Marialva</div>
                <div class="v6-title">Cotações simples.</div>
                <div class="v6-subtitle">Monte a lista, envie aos vendedores, compare os preços e gere o pedido final.</div>
            </div>
            <div class="v6-next">
                <div class="v6-next-label">Fluxo principal</div>
                <div class="v6-next-main">Criar → Enviar → Respostas → Comparar → Pedido</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def metric_card(label, value, help_text=""):
    st.markdown(
        f"""
        <div class="v6-stat">
            <div class="v6-stat-label">{label}</div>
            <div class="v6-stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def action_card(icon, title, text, accent):
    accent_map = {
        "#38BDF8": ("rgba(56,189,248,.22)", "rgba(56,189,248,.15)", "rgba(56,189,248,.36)"),
        "#FB923C": ("rgba(251,146,60,.22)", "rgba(251,146,60,.14)", "rgba(251,146,60,.36)"),
        "#22C55E": ("rgba(34,197,94,.20)", "rgba(34,197,94,.13)", "rgba(34,197,94,.34)"),
        "#A78BFA": ("rgba(167,139,250,.22)", "rgba(167,139,250,.14)", "rgba(167,139,250,.36)"),
        "#F472B6": ("rgba(244,114,182,.22)", "rgba(244,114,182,.14)", "rgba(244,114,182,.36)"),
        "#FACC15": ("rgba(250,204,21,.20)", "rgba(250,204,21,.12)", "rgba(250,204,21,.34)"),
    }
    soft, bg, line = accent_map.get(accent, ("rgba(148,163,184,.18)", "rgba(148,163,184,.12)", "rgba(148,163,184,.30)"))
    st.markdown(
        f"""
        <div class="v6-action" style="--accent-soft:{soft};--accent-bg:{bg};--accent-line:{line};">
            <div class="v6-action-icon">{icon}</div>
            <div class="v6-action-title">{title}</div>
            <div class="v6-action-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def nav_button(label, tela):
    chave = f"acao_{tela}_{label}".replace(" ", "_").replace("/", "_").lower()
    if st.button(label, key=chave, use_container_width=True):
        set_tela(tela)
        st.rerun()

def top_nav():
    labels = [
        ("Início", "inicio"),
        ("Criar", "criar"),
        ("Enviar", "enviar"),
        ("Respostas", "respostas"),
        ("Comparar", "comparar"),
        ("Pedido", "pedido"),
        ("Cadastros", "cadastros"),
    ]
    cols = st.columns(len(labels))
    atual = st.session_state.get("tela", "inicio")
    for col, (label, tela) in zip(cols, labels):
        with col:
            texto = f"• {label}" if atual == tela else label
            if st.button(texto, key=f"topnav_{tela}", use_container_width=True):
                set_tela(tela)
                st.rerun()

def resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas):
    abertas = cotacoes[cotacoes["Status"].astype(str).str.lower().str.contains("abert|aguard|parcial", regex=True, na=False)]
    if not abertas.empty:
        cid = str(abertas.iloc[-1]["CotacaoID"])
        itens_c = itens[itens["CotacaoID"].astype(str) == cid]
        resp_c = respostas[respostas["CotacaoID"].astype(str) == cid]
        fornecedores_resp = resp_c["FornecedorID"].nunique() if not resp_c.empty else 0
        if len(itens_c) == 0:
            acao = "Adicionar produtos à cotação aberta."
        elif fornecedores_resp == 0:
            acao = "Enviar links aos vendedores."
        else:
            acao = "Comparar respostas recebidas."
        return {"cotacao": cid, "itens": len(itens_c), "respostas": fornecedores_resp, "acao": acao}

    if not cotacoes.empty:
        ultima = cotacoes.iloc[-1]
        return {"cotacao": str(ultima.get("CotacaoID", "-")), "itens": 0, "respostas": 0, "acao": "Criar nova cotação quando precisar comprar."}

    return {"cotacao": "Nenhuma", "itens": 0, "respostas": 0, "acao": "Criar uma cotação curta para teste."}

# -------------------------
# TELAS INTERNAS
# -------------------------

def tela_inicio():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]
    respostas = dados["respostas"]

    hero()
    resumo = resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Cotação atual", resumo["cotacao"])
    with c2:
        metric_card("Itens na lista", resumo["itens"])
    with c3:
        metric_card("Fornecedores", len(fornecedores))
    with c4:
        metric_card("Produtos", len(produtos))

    st.markdown(
        f"""
        <div class="v6-next" style="margin:.1rem 0 .55rem 0;">
            <div class="v6-next-label">Próxima ação</div>
            <div class="v6-next-main">{resumo['acao']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="v6-actions-title">Ações principais</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        action_card("📦", "Criar", "Lista de produtos", "#38BDF8")
        nav_button("Abrir", "criar")
    with cols[1]:
        action_card("📲", "Enviar", "Links WhatsApp", "#FB923C")
        nav_button("Abrir", "enviar")
    with cols[2]:
        action_card("✅", "Respostas", "Quem respondeu", "#22C55E")
        nav_button("Abrir", "respostas")
    with cols[3]:
        action_card("💰", "Comparar", "Menor preço", "#A78BFA")
        nav_button("Abrir", "comparar")
    with cols[4]:
        action_card("🛒", "Pedido", "Compra final", "#F472B6")
        nav_button("Abrir", "pedido")

def tela_criar():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]

    st.markdown('<div class="section-title">📦 Criar cotação</div>', unsafe_allow_html=True)
    st.caption("Monte uma lista de produtos para enviar aos fornecedores. Comece pequeno se for uma cotação de teste.")

    with st.expander("1. Criar nova cotação", expanded=True):
        with st.form("form_nova_cotacao_v5"):
            c1, c2, c3 = st.columns(3)
            data_cotacao = c1.date_input("Data", value=date.today())
            prazo = c2.text_input("Prazo", placeholder="Ex: Hoje até 15h")
            responsavel = c3.text_input("Responsável", value="João")
            obs = st.text_input("Observação", placeholder="Ex: Cotação semanal de mercearia")
            criar = st.form_submit_button("Criar cotação")
        if criar:
            novo_id = gerar_id("COT", cotacoes, "CotacaoID")
            novo = pd.DataFrame([{
                "CotacaoID": novo_id,
                "Data": str(data_cotacao),
                "Prazo": prazo,
                "Status": "Aberta",
                "Responsavel": responsavel,
                "Observacao": obs,
            }])
            cotacoes = pd.concat([cotacoes, novo], ignore_index=True)
            salvar("cotacoes", cotacoes)
            st.session_state.cotacao_atual = novo_id
            st.success(f"Cotação criada: {novo_id}")
            st.rerun()

    if cotacoes.empty:
        st.warning("Crie uma cotação para adicionar itens.")
        return

    st.divider()
    st.subheader("2. Adicionar produtos à cotação")

    cotacao_default = st.session_state.get("cotacao_atual", cotacoes.iloc[-1]["CotacaoID"])
    cotacao_lista = cotacoes["CotacaoID"].astype(str).tolist()
    idx = cotacao_lista.index(cotacao_default) if cotacao_default in cotacao_lista else len(cotacao_lista)-1
    cotacao_id = st.selectbox("Cotação", cotacao_lista, index=idx)
    st.session_state.cotacao_atual = cotacao_id

    produtos_ativos = produtos[produtos["Ativo"].astype(str).str.lower().ne("não")].copy()
    termo = st.text_input("Buscar produto", placeholder="Digite parte do produto, marca ou tamanho. Ex: atum coqueiro 170g")
    if termo.strip():
        terms = normalizar_texto(termo).split()
        mask = pd.Series(True, index=produtos_ativos.index)
        base = (produtos_ativos["Produto"].astype(str) + " " + produtos_ativos["Marca"].astype(str) + " " + produtos_ativos["Tamanho"].astype(str) + " " + produtos_ativos["Categoria"].astype(str)).map(normalizar_texto)
        for t in terms:
            mask &= base.str.contains(re.escape(t), na=False)
        produtos_filtrados = produtos_ativos[mask].head(80)
    else:
        produtos_filtrados = produtos_ativos.head(80)

    opcoes = {produto_label(row): row["ProdutoID"] for _, row in produtos_filtrados.iterrows()}
    selecionados = st.multiselect("Selecione produtos", list(opcoes.keys()), placeholder="Escolha um ou vários produtos")
    quantidade = st.number_input("Quantidade padrão", min_value=0, step=1, value=1)

    if st.button("Adicionar selecionados", use_container_width=True):
        novos = 0
        for label in selecionados:
            pid = opcoes[label]
            ja_existe = ((itens["CotacaoID"].astype(str) == cotacao_id) & (itens["ProdutoID"].astype(str) == pid)).any()
            if ja_existe:
                continue
            novo_id = gerar_id("ITEM", itens, "ItemID")
            novo = pd.DataFrame([{
                "ItemID": novo_id,
                "CotacaoID": cotacao_id,
                "ProdutoID": pid,
                "QuantidadeDesejada": quantidade,
                "Observacao": "",
            }])
            itens = pd.concat([itens, novo], ignore_index=True)
            novos += 1
        salvar("itens_cotacao", itens)
        st.success(f"{novos} item(ns) adicionados à cotação.")
        st.rerun()

    st.subheader("Itens já adicionados")
    itens_cot = itens[itens["CotacaoID"].astype(str) == cotacao_id].merge(produtos, on="ProdutoID", how="left")
    if itens_cot.empty:
        st.info("Nenhum item nessa cotação ainda.")
    else:
        st.dataframe(itens_cot[["ItemID", "ProdutoID", "Produto", "Marca", "Tamanho", "Categoria", "QuantidadeDesejada"]], use_container_width=True, hide_index=True)
        remover = st.selectbox("Remover item", [""] + itens_cot["ItemID"].astype(str).tolist())
        if remover and st.button("Remover item selecionado"):
            itens = itens[itens["ItemID"].astype(str) != remover]
            salvar("itens_cotacao", itens)
            st.success("Item removido.")
            st.rerun()


def tela_enviar():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]

    st.markdown('<div class="section-title">📲 Enviar aos vendedores</div>', unsafe_allow_html=True)
    st.caption("Gere um link individual para cada fornecedor preencher a cotação. Copie a mensagem e envie no WhatsApp.")

    if cotacoes.empty:
        st.warning("Crie uma cotação primeiro.")
        return
    if fornecedores.empty:
        st.warning("Cadastre fornecedores primeiro.")
        return

    cotacao_id = st.selectbox("Cotação", cotacoes["CotacaoID"].astype(str).tolist(), index=len(cotacoes)-1)
    itens_cot = itens[itens["CotacaoID"].astype(str) == cotacao_id].merge(produtos, on="ProdutoID", how="left")
    st.metric("Itens nessa cotação", len(itens_cot))

    base_link = st.text_input("Link base do sistema", value="http://localhost:8501", help="Use o link do Ngrok quando for enviar para alguém fora do seu computador.")
    base_link = base_link.strip().rstrip("/")

    fornecedores_ativos = fornecedores[fornecedores["Ativo"].astype(str).str.lower().ne("não")].copy()
    filtro = st.text_input("Filtrar vendedor", placeholder="Ex: Marcio, Paulo, Rogério")
    if filtro.strip():
        base = (fornecedores_ativos["Vendedor"].astype(str) + " " + fornecedores_ativos["Empresa"].astype(str)).map(normalizar_texto)
        fornecedores_ativos = fornecedores_ativos[base.str.contains(normalizar_texto(filtro), na=False)]

    for _, f in fornecedores_ativos.iterrows():
        fid = str(f["FornecedorID"])
        nome = str(f.get("Vendedor", fid))
        link = f"{base_link}?modo=vendedor&cotacao={quote(cotacao_id)}&fornecedor={quote(fid)}"
        msg = f"""Bom dia, {nome}!

Segue cotação do Supermercado Marialva.
Por favor, preencha os preços pelo link abaixo:

{link}

Caso não tenha algum produto, marque como indisponível.
Obrigado."""
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**{nome}**")
                st.caption(f"{fid} | {f.get('Empresa','')}")
                st.code(link, language=None)
            with c2:
                st.text_area("Mensagem para WhatsApp", msg, height=150, key=f"msg_{fid}_{cotacao_id}")


def tela_respostas():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    respostas = dados["respostas"]
    itens = dados["itens"]

    st.markdown('<div class="section-title">✅ Respostas dos vendedores</div>', unsafe_allow_html=True)

    if cotacoes.empty:
        st.warning("Nenhuma cotação criada.")
        return

    cotacao_id = st.selectbox("Cotação", cotacoes["CotacaoID"].astype(str).tolist(), index=len(cotacoes)-1)
    itens_cot = itens[itens["CotacaoID"].astype(str) == cotacao_id]
    resp_cot = respostas[respostas["CotacaoID"].astype(str) == cotacao_id]

    c1, c2, c3 = st.columns(3)
    c1.metric("Itens da cotação", len(itens_cot))
    c2.metric("Fornecedores com resposta", resp_cot["FornecedorID"].nunique() if not resp_cot.empty else 0)
    c3.metric("Preços lançados", len(resp_cot))

    st.subheader("Resumo por fornecedor")
    if fornecedores.empty:
        st.info("Nenhum fornecedor cadastrado.")
    else:
        linhas = []
        for _, f in fornecedores.iterrows():
            fid = str(f["FornecedorID"])
            qtd = len(resp_cot[resp_cot["FornecedorID"].astype(str) == fid])
            status = "Respondido" if qtd > 0 else "Aguardando"
            linhas.append({"FornecedorID": fid, "Vendedor": f.get("Vendedor", ""), "Empresa": f.get("Empresa", ""), "Itens respondidos": qtd, "Status": status})
        df_status = pd.DataFrame(linhas)
        st.dataframe(df_status, use_container_width=True, hide_index=True)

    with st.expander("Importar resposta colada do WhatsApp", expanded=False):
        if fornecedores.empty:
            st.warning("Cadastre fornecedores primeiro.")
        else:
            fornecedor_opcoes = {fornecedor_label(row): row["FornecedorID"] for _, row in fornecedores.iterrows()}
            forn_label = st.selectbox("Fornecedor", list(fornecedor_opcoes.keys()))
            texto = st.text_area("Cole a resposta do WhatsApp", placeholder="PROD001 - 9,15\nPROD002 - NT")
            if st.button("Importar resposta em bloco"):
                fid = fornecedor_opcoes[forn_label]
                respostas_novas = respostas.copy()
                count = 0
                for linha in texto.splitlines():
                    linha = linha.strip()
                    if not linha:
                        continue
                    m = re.match(r"([A-Za-z]+\d+)\s*[-–:]\s*(.+)", linha)
                    if not m:
                        continue
                    pid, valor = m.group(1).strip(), m.group(2).strip()
                    tem = "Não" if valor.upper() in ["NT", "N/T", "NAO TEM", "NÃO TEM", "SEM"] else "Sim"
                    preco = "" if tem == "Não" else preco_float(valor)
                    if tem == "Sim" and preco is None:
                        continue
                    novo_id = gerar_id("RESP", respostas_novas, "RespostaID")
                    novo = pd.DataFrame([{
                        "RespostaID": novo_id,
                        "CotacaoID": cotacao_id,
                        "FornecedorID": fid,
                        "ProdutoID": pid,
                        "Preco": preco,
                        "TemProduto": tem,
                        "Observacao": "Importado do WhatsApp",
                    }])
                    respostas_novas = pd.concat([respostas_novas, novo], ignore_index=True)
                    count += 1
                salvar("respostas", respostas_novas)
                st.success(f"{count} resposta(s) importadas.")
                st.rerun()

    st.subheader("Respostas lançadas")
    if resp_cot.empty:
        st.info("Nenhuma resposta para essa cotação ainda.")
    else:
        vis = resp_cot.merge(produtos, on="ProdutoID", how="left").merge(fornecedores, on="FornecedorID", how="left")
        st.dataframe(vis[["RespostaID", "FornecedorID", "Vendedor", "ProdutoID", "Produto", "Marca", "Tamanho", "Preco", "TemProduto", "Observacao"]], use_container_width=True, hide_index=True)


def calcular_comparativo(cotacao_id=None):
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    respostas = dados["respostas"]
    itens = dados["itens"]

    df = respostas.copy()
    if cotacao_id:
        df = df[df["CotacaoID"].astype(str) == str(cotacao_id)]
    df = df[df["TemProduto"].astype(str).str.lower().eq("sim")].copy()
    df["PrecoNum"] = df["Preco"].map(preco_float)
    df = df.dropna(subset=["PrecoNum"])
    if df.empty:
        return pd.DataFrame()
    df = df.merge(produtos, on="ProdutoID", how="left").merge(fornecedores, on="FornecedorID", how="left")
    idx = df.groupby(["CotacaoID", "ProdutoID"])["PrecoNum"].idxmin()
    vencedores = df.loc[idx].copy()
    maior = df.groupby(["CotacaoID", "ProdutoID"])["PrecoNum"].max().reset_index().rename(columns={"PrecoNum": "MaiorPreco"})
    qtd_resp = df.groupby(["CotacaoID", "ProdutoID"])["FornecedorID"].nunique().reset_index().rename(columns={"FornecedorID": "QtdFornecedores"})
    itens_qty = itens[["CotacaoID", "ProdutoID", "QuantidadeDesejada"]].copy()
    vencedores = vencedores.merge(maior, on=["CotacaoID", "ProdutoID"], how="left").merge(qtd_resp, on=["CotacaoID", "ProdutoID"], how="left").merge(itens_qty, on=["CotacaoID", "ProdutoID"], how="left")
    vencedores["EconomiaUnit"] = vencedores["MaiorPreco"] - vencedores["PrecoNum"]
    vencedores["QuantidadeDesejadaNum"] = pd.to_numeric(vencedores["QuantidadeDesejada"], errors="coerce").fillna(0)
    vencedores["EconomiaTotal"] = vencedores["EconomiaUnit"] * vencedores["QuantidadeDesejadaNum"]
    return vencedores


def tela_comparar():
    dados = carregar_tudo()
    cotacoes = dados["cotacoes"]

    st.markdown('<div class="section-title">💰 Comparar preços</div>', unsafe_allow_html=True)

    if cotacoes.empty:
        st.warning("Nenhuma cotação criada.")
        return

    cotacao_id = st.selectbox("Cotação", cotacoes["CotacaoID"].astype(str).tolist(), index=len(cotacoes)-1)
    comp = calcular_comparativo(cotacao_id)
    if comp.empty:
        st.info("Ainda não há preços válidos para comparar nessa cotação.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Itens com vencedor", len(comp))
    c2.metric("Fornecedores vencedores", comp["FornecedorID"].nunique())
    c3.metric("Economia estimada", moeda(comp["EconomiaTotal"].sum()))

    resultado = comp[["ProdutoID", "Produto", "Marca", "Tamanho", "Categoria", "Vendedor", "PrecoNum", "MaiorPreco", "EconomiaUnit", "QtdFornecedores", "QuantidadeDesejada"]].copy()
    resultado = resultado.rename(columns={
        "Vendedor": "Vendedor vencedor",
        "PrecoNum": "Menor preço",
        "MaiorPreco": "Maior preço",
        "EconomiaUnit": "Economia un.",
        "QtdFornecedores": "Qtd fornecedores",
        "QuantidadeDesejada": "Qtd",
    })
    st.dataframe(resultado, use_container_width=True, hide_index=True)


def tela_pedido():
    dados = carregar_tudo()
    cotacoes = dados["cotacoes"]

    st.markdown('<div class="section-title">🛒 Pedido final por vendedor</div>', unsafe_allow_html=True)
    st.caption("Use essa tela depois de comparar preços. Ela separa automaticamente o que comprar de cada fornecedor vencedor.")

    if cotacoes.empty:
        st.warning("Nenhuma cotação criada.")
        return

    cotacao_id = st.selectbox("Cotação", cotacoes["CotacaoID"].astype(str).tolist(), index=len(cotacoes)-1)
    comp = calcular_comparativo(cotacao_id)
    if comp.empty:
        st.info("Ainda não há vencedores para gerar pedido.")
        return

    for vendedor, grupo in comp.groupby("Vendedor"):
        total = grupo["PrecoNum"].sum()
        with st.container(border=True):
            st.subheader(f"🚚 {vendedor}")
            linhas_msg = []
            vis = grupo[["ProdutoID", "Produto", "Marca", "Tamanho", "QuantidadeDesejada", "PrecoNum"]].copy()
            vis = vis.rename(columns={"QuantidadeDesejada": "Qtd", "PrecoNum": "Preço"})
            st.dataframe(vis, use_container_width=True, hide_index=True)
            for _, row in grupo.iterrows():
                desc = " ".join([str(row.get("Produto", "")), str(row.get("Marca", "")), str(row.get("Tamanho", ""))]).strip()
                qtd = row.get("QuantidadeDesejada", "")
                linhas_msg.append(f"- {desc} | Qtd: {qtd if str(qtd).strip() else '-'} | {moeda(row['PrecoNum'])}")
            msg = f"Pedido Supermercado Marialva — Cotação {cotacao_id}\n\n{chr(10).join(linhas_msg)}"
            st.text_area("Mensagem do pedido", msg, height=150, key=f"pedido_{cotacao_id}_{vendedor}")


def tela_cadastros():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]
    respostas = dados["respostas"]

    st.markdown('<div class="section-title">⚙️ Cadastros e administração</div>', unsafe_allow_html=True)
    st.caption("Área administrativa. Use quando precisar corrigir produtos, fornecedores, backups ou bases.")

    tab1, tab2, tab3, tab4 = st.tabs(["Produtos", "Fornecedores", "Backups", "Bases"])

    with tab1:
        st.subheader("Produtos")
        with st.form("novo_produto_v5"):
            c1, c2, c3 = st.columns(3)
            produto = c1.text_input("Produto")
            marca = c2.text_input("Marca")
            tamanho = c3.text_input("Tamanho")
            c4, c5, c6 = st.columns(3)
            categoria = c4.text_input("Categoria", value="Mercearia")
            unidade = c5.text_input("Unidade", value="Unidade")
            obs = c6.text_input("Observação")
            salvar_prod = st.form_submit_button("Salvar produto")
        if salvar_prod:
            novo_id = gerar_id("PROD", produtos, "ProdutoID")
            novo = pd.DataFrame([{"ProdutoID": novo_id, "Produto": produto, "Marca": marca, "Tamanho": tamanho, "Categoria": categoria, "Unidade": unidade, "Ativo": "Sim", "Observacao": obs}])
            produtos = pd.concat([produtos, novo], ignore_index=True)
            salvar("produtos", produtos)
            st.success(f"Produto salvo: {novo_id}")
            st.rerun()

        busca = st.text_input("Buscar produto cadastrado", placeholder="Ex: atum coqueiro")
        prod_vis = produtos.copy()
        if busca.strip():
            base = (prod_vis["Produto"].astype(str) + " " + prod_vis["Marca"].astype(str) + " " + prod_vis["Tamanho"].astype(str) + " " + prod_vis["Categoria"].astype(str)).map(normalizar_texto)
            for t in normalizar_texto(busca).split():
                prod_vis = prod_vis[base.str.contains(re.escape(t), na=False)]
        st.dataframe(prod_vis.head(300), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Fornecedores")
        with st.form("novo_fornecedor_v5"):
            c1, c2, c3 = st.columns(3)
            vendedor = c1.text_input("Vendedor")
            empresa = c2.text_input("Empresa")
            whatsapp = c3.text_input("WhatsApp")
            c4, c5 = st.columns(2)
            categoria = c4.text_input("Categoria forte")
            obs = c5.text_input("Observação")
            salvar_forn = st.form_submit_button("Salvar fornecedor")
        if salvar_forn:
            novo_id = gerar_id("FOR", fornecedores, "FornecedorID")
            novo = pd.DataFrame([{"FornecedorID": novo_id, "Vendedor": vendedor, "Empresa": empresa, "WhatsApp": whatsapp, "CategoriaForte": categoria, "Ativo": "Sim", "Observacao": obs}])
            fornecedores = pd.concat([fornecedores, novo], ignore_index=True)
            salvar("fornecedores", fornecedores)
            st.success(f"Fornecedor salvo: {novo_id}")
            st.rerun()
        st.dataframe(fornecedores, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Cópias de segurança")
        st.markdown('<div class="admin-small">Crie backup antes de grandes importações ou alterações no sistema.</div>', unsafe_allow_html=True)
        if st.button("Criar backup agora"):
            pasta = backup_geral()
            st.success(f"Backup criado em: {pasta}")
        if os.path.exists(PASTA_BACKUPS):
            backups = sorted(os.listdir(PASTA_BACKUPS), reverse=True)[:20]
            st.write(backups)

    with tab4:
        base = st.selectbox("Ver base", ["produtos", "fornecedores", "cotacoes", "itens_cotacao", "respostas"])
        st.dataframe(carregar(base), use_container_width=True, hide_index=True)

# -------------------------
# ROTEAMENTO
# -------------------------

modo = get_query_param("modo")
if modo == "vendedor" or get_query_param("cotacao") or get_query_param("fornecedor"):
    tela_vendedor()
    st.stop()

if "tela" not in st.session_state:
    st.session_state.tela = "inicio"

hero_placeholder = None
top_nav()

pages = {
    "inicio": tela_inicio,
    "criar": tela_criar,
    "enviar": tela_enviar,
    "respostas": tela_respostas,
    "comparar": tela_comparar,
    "pedido": tela_pedido,
    "cadastros": tela_cadastros,
}

pages.get(st.session_state.tela, tela_inicio)()
