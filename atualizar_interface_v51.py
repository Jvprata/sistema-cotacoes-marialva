from pathlib import Path
from datetime import datetime

MARCADOR = "MARIALVA_V51_REFINOS_USABILIDADE"

CSS_EXTRA = r"""

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
"""

NEW_HERO = r'''def hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">🛒 Sistema de Cotações Marialva</div>
            <div class="hero-subtitle">Fluxo de compra: criar lista → enviar aos vendedores → receber preços → comparar → gerar pedido.</div>
            <div class="flow">
                <span class="flow-step">1. 📦 Criar</span>
                <span class="flow-step">2. 📲 Enviar</span>
                <span class="flow-step">3. ✅ Receber</span>
                <span class="flow-step">4. 💰 Comparar</span>
                <span class="flow-step">5. 🛒 Pedido</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

'''

NEW_RESUMO = r'''def resumo_hoje(produtos, fornecedores, cotacoes, itens, respostas):
    abertas = cotacoes[cotacoes["Status"].astype(str).str.lower().str.contains("abert|aguard|parcial", regex=True, na=False)]
    ultima = cotacoes.tail(1)

    if not abertas.empty:
        cid = str(abertas.iloc[-1]["CotacaoID"])
        itens_c = itens[itens["CotacaoID"].astype(str) == cid]
        resp_c = respostas[respostas["CotacaoID"].astype(str) == cid]
        fornecedores_resp = resp_c["FornecedorID"].nunique() if not resp_c.empty else 0
        principal = f"""
            <span class="attention-pill">🟦 Cotação aberta: <strong>{cid}</strong></span>
            <span class="attention-pill">📦 Itens: <strong>{len(itens_c)}</strong></span>
            <span class="attention-pill">🚚 Fornecedores que responderam: <strong>{fornecedores_resp}</strong></span>
            <div class="mini-alert">Próxima ação recomendada: enviar links aos vendedores ou acompanhar respostas.</div>
        """
    elif not ultima.empty:
        cid = str(ultima.iloc[-1]["CotacaoID"])
        status = str(ultima.iloc[-1]["Status"])
        principal = f"""
            <span class="attention-pill">✅ Última cotação: <strong>{cid}</strong></span>
            <span class="attention-pill">Status: <strong>{status}</strong></span>
            <div class="mini-alert">Próxima ação recomendada: criar uma nova cotação quando precisar comparar preços.</div>
        """
    else:
        principal = """
            <span class="attention-pill">📝 Nenhuma cotação criada ainda</span>
            <div class="mini-alert">Próxima ação recomendada: criar uma cotação curta para teste.</div>
        """

    if len(produtos) > 1000:
        base = f'<span class="attention-pill">📚 Base de produtos: <strong>{len(produtos)}</strong></span>'
    else:
        base = '<span class="attention-pill">📚 Cadastre produtos para montar listas mais rápido</span>'

    return principal + base

'''

NEW_TELA_INICIO = r'''def tela_inicio():
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
        action_card("📦", "Criar cotação", "Monte uma lista usando busca rápida.", "#38BDF8")
        nav_button("Criar cotação", "criar")
    with row1[1]:
        action_card("📲", "Enviar aos vendedores", "Gere links para WhatsApp por fornecedor.", "#FB923C")
        nav_button("Enviar links", "enviar")
    with row1[2]:
        action_card("✅", "Ver respostas", "Veja quem já respondeu e quem falta.", "#22C55E")
        nav_button("Ver respostas", "respostas")

    row2 = st.columns(3)
    with row2[0]:
        action_card("💰", "Comparar preços", "Encontre o menor preço por item.", "#A78BFA")
        nav_button("Comparar", "comparar")
    with row2[1]:
        action_card("🛒", "Pedido final", "Separe a compra por vendedor.", "#F472B6")
        nav_button("Gerar pedido", "pedido")
    with row2[2]:
        action_card("⚙️", "Administração", "Produtos, fornecedores e backups.", "#FACC15")
        nav_button("Abrir cadastros", "cadastros")

    st.markdown('<div class="section-title">Últimas cotações</div>', unsafe_allow_html=True)
    if cotacoes.empty:
        st.info("Nenhuma cotação criada ainda.")
    else:
        def esc(v):
            return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        rows = []
        for _, r in cotacoes.tail(6).iterrows():
            obs = str(r.get("Observacao", ""))
            if len(obs) > 64:
                obs = obs[:64] + "..."
            rows.append(f"""
                <tr>
                    <td><strong>{esc(r.get('CotacaoID',''))}</strong></td>
                    <td class="muted">{esc(r.get('Data',''))}</td>
                    <td>{status_chip(esc(r.get('Status','')))}</td>
                    <td class="muted">{esc(r.get('Prazo',''))}</td>
                    <td>{esc(obs)}</td>
                </tr>
            """)
        st.markdown(
            f"""
            <table class="clean-table">
                <thead>
                    <tr>
                        <th>Cotação</th>
                        <th>Data</th>
                        <th>Status</th>
                        <th>Prazo</th>
                        <th>Observação</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

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
        print("A V5.1 já foi aplicada. Nenhuma alteração feita.")
        return

    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"app_backup_antes_v51_refinos_{stamp}.py"
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
    text = replace_function(text, "resumo_hoje", NEW_RESUMO)
    text = replace_function(text, "tela_inicio", NEW_TELA_INICIO)

    text = text.replace("5. 🛒 Comprar", "5. 🛒 Pedido")
    text = text.replace("comprar melhor", "gerar pedido")

    app.write_text(text, encoding="utf-8")
    print("Refino visual V5.1 aplicado com sucesso!")
    print(f"Backup criado em: {backup_path}")
    print("Agora rode: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
