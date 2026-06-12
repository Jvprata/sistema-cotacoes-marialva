from pathlib import Path
from datetime import datetime

MARCADOR = "MARIALVA_V6_CLEAN_APPLE_LIKE"

CSS_EXTRA = r"""

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
"""

NEW_HERO = r'''def hero():
    st.markdown(
        """
        <div class="v6-hero">
            <div>
                <div class="v6-kicker">Supermercado Marialva</div>
                <div class="v6-title">Cotações simples, rápidas e organizadas.</div>
                <div class="v6-subtitle">Crie a lista, envie aos vendedores, receba os preços e gere o pedido final sem se perder no processo.</div>
            </div>
            <div class="v6-next">
                <div class="v6-next-label">Fluxo principal</div>
                <div class="v6-next-main">Criar → Enviar → Receber → Comparar → Pedido</div>
                <div class="v6-next-meta">Use os botões abaixo como caminho padrão de trabalho.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

'''

NEW_METRIC_CARD = r'''def metric_card(label, value, help_text=""):
    st.markdown(
        f"""
        <div class="v6-stat">
            <div class="v6-stat-label">{label}</div>
            <div class="v6-stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

'''

NEW_ACTION_CARD = r'''def action_card(icon, title, text, accent):
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

'''

NEW_TOP_NAV = r'''def top_nav():
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
    for col, (label, tela) in zip(cols, labels):
        with col:
            prefixo = "• " if st.session_state.get("tela", "inicio") == tela else ""
            if st.button(prefixo + label, key=f"nav_{tela}", use_container_width=True):
                set_tela(tela)
                st.rerun()

'''

NEW_RESUMO = r'''def resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas):
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
        return {
            "cotacao": cid,
            "status": "Aberta",
            "itens": len(itens_c),
            "respostas": fornecedores_resp,
            "acao": acao,
        }

    if not cotacoes.empty:
        ultima = cotacoes.iloc[-1]
        return {
            "cotacao": str(ultima.get("CotacaoID", "-")),
            "status": str(ultima.get("Status", "-")),
            "itens": 0,
            "respostas": 0,
            "acao": "Criar nova cotação quando precisar comprar.",
        }

    return {
        "cotacao": "Nenhuma",
        "status": "Sem cotação",
        "itens": 0,
        "respostas": 0,
        "acao": "Criar uma cotação curta para teste.",
    }

'''

NEW_TELA_INICIO = r'''def tela_inicio():
    dados = carregar_tudo()
    produtos = dados["produtos"]
    fornecedores = dados["fornecedores"]
    cotacoes = dados["cotacoes"]
    itens = dados["itens"]
    respostas = dados["respostas"]

    st.markdown('<div class="v6-shell">', unsafe_allow_html=True)
    hero()

    resumo = resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Cotação atual", resumo["cotacao"], "")
    with c2:
        metric_card("Itens na lista", resumo["itens"], "")
    with c3:
        metric_card("Fornecedores", len(fornecedores), "")
    with c4:
        metric_card("Produtos", len(produtos), "")

    st.markdown(
        f"""
        <div class="v6-next" style="margin: .2rem 0 .8rem 0; padding: 13px 16px;">
            <div class="v6-next-label">Próxima ação recomendada</div>
            <div class="v6-next-main" style="font-size:16px; margin-bottom:0;">{resumo['acao']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="v6-actions-title">Ações principais</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        action_card("📦", "Criar", "Monte a lista de produtos.", "#38BDF8")
        nav_button("Abrir", "criar")
    with cols[1]:
        action_card("📲", "Enviar", "Links para vendedores.", "#FB923C")
        nav_button("Abrir", "enviar")
    with cols[2]:
        action_card("✅", "Respostas", "Veja quem respondeu.", "#22C55E")
        nav_button("Abrir", "respostas")
    with cols[3]:
        action_card("💰", "Comparar", "Menor preço por item.", "#A78BFA")
        nav_button("Abrir", "comparar")
    with cols[4]:
        action_card("🛒", "Pedido", "Compra por vendedor.", "#F472B6")
        nav_button("Abrir", "pedido")

    st.markdown('<div class="v6-quiet-note">Cadastros, backups e bases ficam no botão “Cadastros”, no topo.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

'''


def replace_function(text, name, new_code):
    lines = text.splitlines(True)
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"def {name}("):
            start = i
            break
    if start is None:
        raise RuntimeError(f"Não encontrei a função {name} no app.py")

    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if line.strip() and not line.startswith((" ", "\t")):
            end = j
            break
    return "".join(lines[:start]) + new_code + "".join(lines[end:])


def main():
    app = Path("app.py")
    if not app.exists():
        raise FileNotFoundError("Não encontrei app.py. Rode este arquivo na pasta do projeto, junto do app.py.")

    text = app.read_text(encoding="utf-8")
    if MARCADOR in text:
        print("A V6 já foi aplicada. Nenhuma alteração feita.")
        return

    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"app_backup_antes_v6_clean_{stamp}.py"
    backup_path.write_text(text, encoding="utf-8")

    if "</style>" in text:
        text = text.replace("</style>", CSS_EXTRA + "\n</style>", 1)
    else:
        marker = "st.set_page_config("
        idx = text.find(marker)
        if idx == -1:
            raise RuntimeError("Não encontrei o bloco visual/CSS nem st.set_page_config no app.py.")
        insert_pos = text.find(")", idx) + 1
        text = text[:insert_pos] + f"\n\n# {MARCADOR}\nst.markdown('''<style>{CSS_EXTRA}</style>''', unsafe_allow_html=True)\n" + text[insert_pos:]

    text = replace_function(text, "hero", NEW_HERO)
    text = replace_function(text, "metric_card", NEW_METRIC_CARD)
    text = replace_function(text, "action_card", NEW_ACTION_CARD)
    text = replace_function(text, "top_nav", NEW_TOP_NAV)
    text = replace_function(text, "resumo_hoje", NEW_RESUMO)
    text = replace_function(text, "tela_inicio", NEW_TELA_INICIO)

    # Limpezas de nomenclatura antigas
    text = text.replace("comprar melhor", "gerar pedido")
    text = text.replace("5. 🛒 Comprar", "5. 🛒 Pedido")

    app.write_text(text, encoding="utf-8")
    print("Interface V6 clean aplicada com sucesso!")
    print(f"Backup criado em: {backup_path}")
    print("Agora rode: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
