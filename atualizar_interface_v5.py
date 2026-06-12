from pathlib import Path
from datetime import datetime

APP_CODE = r'''
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
        <div class="hero">
            <div class="hero-title">🛒 Sistema de Cotações Marialva</div>
            <div class="hero-subtitle">Fluxo visual: criar lista → enviar aos vendedores → receber preços → comparar → comprar melhor.</div>
            <div class="flow">
                <span class="flow-step">1. 📦 Criar</span>
                <span class="flow-step">2. 📲 Enviar</span>
                <span class="flow-step">3. ✅ Receber</span>
                <span class="flow-step">4. 💰 Comparar</span>
                <span class="flow-step">5. 🛒 Comprar</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, help_text=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def action_card(icon, title, text, accent):
    st.markdown(
        f"""
        <div class="action-card" style="--accent:{accent};">
            <div class="icon-badge">{icon}</div>
            <div class="action-title">{title}</div>
            <div class="action-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav_button(label, tela):
    if st.button(label, use_container_width=True):
        set_tela(tela)
        st.rerun()


def top_nav():
    labels = [
        ("🏠 Início", "inicio"),
        ("📦 Criar", "criar"),
        ("📲 Enviar", "enviar"),
        ("✅ Respostas", "respostas"),
        ("💰 Comparar", "comparar"),
        ("🛒 Pedido", "pedido"),
        ("⚙️ Cadastros", "cadastros"),
    ]
    cols = st.columns(len(labels))
    for col, (label, tela) in zip(cols, labels):
        with col:
            if st.button(label, key=f"nav_{tela}", use_container_width=True):
                set_tela(tela)
                st.rerun()


def resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas):
    abertas = cotacoes[cotacoes["Status"].astype(str).str.lower().str.contains("abert|aguard|parcial", regex=True, na=False)]
    ultima = cotacoes.tail(1)
    texto = []
    if not abertas.empty:
        cid = abertas.iloc[-1]["CotacaoID"]
        itens_c = itens[itens["CotacaoID"].astype(str) == str(cid)]
        resp_c = respostas[respostas["CotacaoID"].astype(str) == str(cid)]
        fornecedores_resp = resp_c["FornecedorID"].nunique() if not resp_c.empty else 0
        texto.append(f"Você tem **{len(abertas)} cotação(ões) aberta(s)**. A mais recente é **{cid}**, com **{len(itens_c)} item(ns)** e resposta de **{fornecedores_resp} fornecedor(es)**.")
    elif not ultima.empty:
        texto.append(f"Última cotação registrada: **{ultima.iloc[-1]['CotacaoID']}** — status **{ultima.iloc[-1]['Status']}**.")
    else:
        texto.append("Nenhuma cotação criada ainda. Comece criando uma lista curta de produtos para teste.")

    if len(produtos) > 1000:
        texto.append(f"Sua base de produtos já está forte: **{len(produtos)} produtos cadastrados**.")
    else:
        texto.append("Cadastre ou importe produtos para montar cotações com mais rapidez.")

    return "<br>".join(texto)

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

    st.markdown(
        f"""
        <div class="today-box">
            <div class="today-title">🎯 O que precisa de atenção agora</div>
            <div class="today-line">{resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("📦 Produtos", len(produtos), "Base para montar listas")
    with c2:
        metric_card("🚚 Fornecedores", len(fornecedores), "Contatos de cotação")
    with c3:
        metric_card("📝 Cotações", len(cotacoes), "Histórico criado")
    with c4:
        metric_card("✅ Respostas", len(respostas), "Preços recebidos")

    st.markdown('<div class="section-title">Escolha uma ação</div>', unsafe_allow_html=True)

    row1 = st.columns(3)
    with row1[0]:
        action_card("📦", "Criar cotação", "Monte uma lista usando busca rápida e produtos recorrentes.", "#38BDF8")
        nav_button("Criar cotação", "criar")
    with row1[1]:
        action_card("📲", "Enviar aos vendedores", "Gere links simples para WhatsApp, um por fornecedor.", "#FB923C")
        nav_button("Enviar links", "enviar")
    with row1[2]:
        action_card("✅", "Ver respostas", "Acompanhe quem respondeu e quem ainda falta.", "#22C55E")
        nav_button("Ver respostas", "respostas")

    row2 = st.columns(3)
    with row2[0]:
        action_card("💰", "Comparar preços", "Veja o menor preço por item e o vendedor vencedor.", "#A78BFA")
        nav_button("Comparar", "comparar")
    with row2[1]:
        action_card("🛒", "Pedido final", "Separe automaticamente a compra por vendedor.", "#F472B6")
        nav_button("Gerar pedido", "pedido")
    with row2[2]:
        action_card("⚙️", "Cadastros", "Produtos, fornecedores, backups e bases ficam aqui.", "#FACC15")
        nav_button("Abrir cadastros", "cadastros")

    st.markdown('<div class="section-title">Últimas cotações</div>', unsafe_allow_html=True)
    if cotacoes.empty:
        st.info("Nenhuma cotação criada ainda.")
    else:
        vis = cotacoes.tail(6).copy()
        st.dataframe(vis, use_container_width=True, hide_index=True)


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
'''

def main():
    base = Path.cwd()
    app = base / "app.py"
    if not app.exists():
        raise FileNotFoundError("Não encontrei o arquivo app.py nesta pasta. Coloque este atualizador na pasta do projeto.")

    backups = base / "backups"
    backups.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backups / f"app_backup_v5_{stamp}.py"
    backup_path.write_text(app.read_text(encoding="utf-8"), encoding="utf-8")
    app.write_text(APP_CODE, encoding="utf-8")

    print("Atualização V5 concluída com sucesso!")
    print(f"Backup do app antigo criado em: {backup_path}")
    print("Agora rode: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
