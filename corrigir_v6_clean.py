from pathlib import Path
from datetime import datetime

MARCADOR = "MARIALVA_V6_CORRIGIDA_CLEAN_61"

CSS_PATCH = r'''

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
'''

NEW_NAV_BUTTON = r'''def nav_button(label, tela):
    chave = f"acao_{tela}_{label}".replace(" ", "_").replace("/", "_").lower()
    if st.button(label, key=chave, use_container_width=True):
        set_tela(tela)
        st.rerun()

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
    atual = st.session_state.get("tela", "inicio")
    for col, (label, tela) in zip(cols, labels):
        with col:
            texto = f"• {label}" if atual == tela else label
            if st.button(texto, key=f"topnav_{tela}", use_container_width=True):
                set_tela(tela)
                st.rerun()

'''

NEW_HERO = r'''def hero():
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
        return {"cotacao": cid, "itens": len(itens_c), "respostas": fornecedores_resp, "acao": acao}

    if not cotacoes.empty:
        ultima = cotacoes.iloc[-1]
        return {"cotacao": str(ultima.get("CotacaoID", "-")), "itens": 0, "respostas": 0, "acao": "Criar nova cotação quando precisar comprar."}

    return {"cotacao": "Nenhuma", "itens": 0, "respostas": 0, "acao": "Criar uma cotação curta para teste."}

'''

NEW_TELA_INICIO = r'''def tela_inicio():
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
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f"app_backup_antes_correcao_v6_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    backup_path.write_text(text, encoding="utf-8")

    if MARCADOR not in text:
        if "</style>" in text:
            text = text.replace("</style>", CSS_PATCH + "\n</style>", 1)
        else:
            marker = "st.set_page_config("
            idx = text.find(marker)
            if idx == -1:
                raise RuntimeError("Não encontrei CSS nem st.set_page_config no app.py.")
            insert_pos = text.find(")", idx) + 1
            text = text[:insert_pos] + f"\n\n# {MARCADOR}\nst.markdown('''<style>{CSS_PATCH}</style>''', unsafe_allow_html=True)\n" + text[insert_pos:]

    for name, code in [
        ("nav_button", NEW_NAV_BUTTON),
        ("top_nav", NEW_TOP_NAV),
        ("hero", NEW_HERO),
        ("metric_card", NEW_METRIC_CARD),
        ("action_card", NEW_ACTION_CARD),
        ("resumo_hoje", NEW_RESUMO),
        ("tela_inicio", NEW_TELA_INICIO),
    ]:
        text = replace_function(text, name, code)

    text = text.replace("5. 🛒 Comprar", "5. 🛒 Pedido")
    text = text.replace("comprar melhor", "gerar pedido")

    app.write_text(text, encoding="utf-8")
    print("Correção V6 aplicada com sucesso!")
    print("O erro de botões duplicados foi corrigido.")
    print(f"Backup criado em: {backup_path}")
    print("Agora rode: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
