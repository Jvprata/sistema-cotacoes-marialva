
import os
import re
from datetime import date, datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st
from supabase import create_client

# =====================================================
# Sistema de Cotações Marialva — V7 Supabase / Cloud
# =====================================================

st.set_page_config(
    page_title="Sistema de Cotações Marialva",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------
# CSS clean
# -------------------------
st.markdown(
    """
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
    height: 0 !important;
}
#MainMenu, footer { visibility: hidden !important; }
.block-container {
    padding-top: .35rem !important;
    padding-bottom: .5rem !important;
    max-width: 1080px;
}
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #111827 0, #050816 42%, #030712 100%) !important;
}
:root {
    --bg-card: rgba(15, 23, 42, .82);
    --line: rgba(148, 163, 184, .22);
    --text: #f8fafc;
    --muted: #a7b4c8;
    --blue: #38bdf8;
    --green: #34d399;
    --amber: #fbbf24;
    --red: #fb7185;
}
.main-card {
    border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(14, 116, 144, .30), rgba(88, 28, 135, .24));
    border-radius: 22px;
    padding: 18px 22px;
    box-shadow: 0 10px 34px rgba(0,0,0,.22);
}
.card {
    border: 1px solid var(--line);
    background: var(--bg-card);
    border-radius: 18px;
    padding: 12px 14px;
    min-height: 72px;
}
.card h3, .main-card h1 { margin: 0 0 8px 0; }
.card small, .muted { color: var(--muted); }
.metric-number {
    font-size: 24px;
    line-height: 1;
    font-weight: 900;
    color: white;
    margin-top: 2px;
    margin-bottom: 2px;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border: 1px solid var(--line);
    background: rgba(15, 23, 42, .62);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 800;
    margin-right: 6px;
    margin-bottom: 4px;
}
.notice {
    border: 1px solid rgba(56,189,248,.36);
    background: rgba(8, 47, 73, .62);
    border-radius: 20px;
    padding: 14px 16px;
    font-weight: 800;
}
.stButton > button {
    border-radius: 14px !important;
    border: 1px solid rgba(148, 163, 184, .26) !important;
    background: rgba(15, 23, 42, .88) !important;
    color: white !important;
    font-weight: 800 !important;
    min-height: 38px;
}
.stButton > button:hover {
    border-color: rgba(56, 189, 248, .72) !important;
    transform: translateY(-1px);
}
input, textarea, [data-baseweb="select"] { border-radius: 14px !important; }
h1, h2, h3, h4, p, span, label { color: #f8fafc; }
hr { border-color: rgba(148,163,184,.18); }

.status-line {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.status-chip {
    border: 1px solid rgba(148, 163, 184, .24);
    background: rgba(15, 23, 42, .58);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 800;
    color: #f8fafc;
}
.main-card {
    min-height: 0 !important;
}
.main-card h1 {
    margin-bottom: 8px !important;
}


/* AJUSTE ESPACAMENTO HOME V10 */
.main-card {
    margin-bottom: 14px !important;
}

div[data-testid="stMarkdownContainer"]:has(.main-card) {
    margin-bottom: 14px !important;
}
/* FIM AJUSTE ESPACAMENTO HOME V10 */

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# Conexão Supabase
# -------------------------
def get_secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)

@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_KEY") or get_secret("SUPABASE_ANON_KEY") or get_secret("SUPABASE_PUBLISHABLE_KEY")

    if not url or not key:
        st.error("Configuração do Supabase não encontrada. Confira o arquivo .streamlit/secrets.toml ou os Secrets do Streamlit Cloud.")
        st.stop()

    return create_client(url, key)

supabase = get_supabase_client()

# -------------------------
# Segurança simples opcional
# -------------------------
def proteger_app():
    senha = get_secret("APP_PASSWORD", "")
    if not senha:
        return

    if st.session_state.get("autenticado"):
        return

    st.markdown('<div class="main-card"><h1>🛒 Sistema de Cotações Marialva</h1><p class="muted">Acesso protegido.</p></div>', unsafe_allow_html=True)
    tentativa = st.text_input("Senha de acesso", type="password")
    if st.button("Entrar", key="btn_login_v7", width="stretch"):
        if tentativa == senha:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

# Página do vendedor não deve exigir senha interna se vier por link
query_params = dict(st.query_params)
modo_vendedor = str(query_params.get("modo", "")).lower() == "vendedor"
if not modo_vendedor:
    proteger_app()

# -------------------------
# Helpers Supabase
# -------------------------
@st.cache_data(ttl=45, show_spinner=False)
def fetch_all(table, order_col=None):
    registros = []
    step = 500
    start = 0

    while True:
        res = supabase.table(table).select("*").range(start, start + step - 1).execute()
        data = res.data or []
        registros.extend(data)

        if len(data) < step:
            break

        start += step

    if order_col and registros:
        try:
            registros = sorted(registros, key=lambda x: str(x.get(order_col, "") or "").lower())
        except Exception:
            pass

    return registros

def clear_cache():
    st.cache_data.clear()

def df_table(table, order_col=None):
    return pd.DataFrame(fetch_all(table, order_col=order_col))

def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()

def to_float(value):
    if value is None or value == "":
        return None
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(value)
    except Exception:
        return None

def next_id(table, col, prefix):
    dados = fetch_all(table)
    maior = 0
    width = 3
    for item in dados:
        valor = str(item.get(col, ""))
        if valor.upper().startswith(prefix):
            numeros = re.findall(r"\d+", valor)
            if numeros:
                maior = max(maior, int(numeros[-1]))
                width = max(width, len(numeros[-1]))
    return f"{prefix}{maior + 1:0{width}d}"

def upsert_one(table, payload, conflict):
    supabase.table(table).upsert(payload, on_conflict=conflict).execute()
    clear_cache()

def insert_one(table, payload):
    supabase.table(table).insert(payload).execute()
    clear_cache()

def produto_nome(produto):
    if not produto:
        return "Produto não encontrado"
    partes = [produto.get("produto"), produto.get("marca"), produto.get("tamanho")]
    return " ".join([str(p) for p in partes if p and str(p).strip()])

def status_aberto(status):
    return str(status or "").strip().lower() in ["aberta", "aberto", "em andamento", "andamento"]

def formatar_real(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "-"

def base_app_url():
    return get_secret("APP_URL", "").strip()

# -------------------------
# Carregamentos centrais
# -------------------------
def carregar_base():
    produtos = fetch_all("produtos", "produto")
    fornecedores = fetch_all("fornecedores", "vendedor")
    cotacoes = fetch_all("cotacoes", "cotacao_id")
    itens = fetch_all("itens_cotacao", "item_id")
    respostas = fetch_all("respostas", "resposta_id")
    return produtos, fornecedores, cotacoes, itens, respostas

def mapas_base(produtos, fornecedores):
    return (
        {p.get("produto_id"): p for p in produtos},
        {f.get("fornecedor_id"): f for f in fornecedores},
    )

def cotacao_atual(cotacoes):
    abertas = [c for c in cotacoes if status_aberto(c.get("status"))]
    if abertas:
        return sorted(abertas, key=lambda x: x.get("cotacao_id", ""))[-1]
    if cotacoes:
        return sorted(cotacoes, key=lambda x: x.get("cotacao_id", ""))[-1]
    return None

# -------------------------
# Interface vendedor por link
# -------------------------
def tela_vendedor():
    cotacao_id = query_params.get("cotacao_id") or query_params.get("cotacao")
    fornecedor_id = query_params.get("fornecedor_id") or query_params.get("fornecedor")
    if isinstance(cotacao_id, list):
        cotacao_id = cotacao_id[0]
    if isinstance(fornecedor_id, list):
        fornecedor_id = fornecedor_id[0]

    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    produtos_map, fornecedores_map = mapas_base(produtos, fornecedores)
    fornecedor = fornecedores_map.get(fornecedor_id)
    itens_cot = [i for i in itens if i.get("cotacao_id") == cotacao_id]

    st.markdown('<div class="main-card"><h1>🛒 Cotação Marialva</h1><p class="muted">Preencha os preços abaixo e envie sua resposta.</p></div>', unsafe_allow_html=True)

    if not cotacao_id or not fornecedor_id or not fornecedor:
        st.error("Link de cotação inválido. Peça um novo link ao responsável de compras.")
        return

    st.markdown(f"### Olá, {fornecedor.get('vendedor', 'vendedor')} 👋")
    st.caption(f"Cotação: {cotacao_id} · Empresa: {fornecedor.get('empresa', '-')}")

    if not itens_cot:
        st.warning("Esta cotação ainda não possui produtos.")
        return

    existentes = {
        (r.get("produto_id")): r
        for r in respostas
        if r.get("cotacao_id") == cotacao_id and r.get("fornecedor_id") == fornecedor_id
    }

    with st.form("form_vendedor_respostas"):
        dados_envio = []
        for item in itens_cot:
            produto = produtos_map.get(item.get("produto_id"), {})
            nome = produto_nome(produto)
            existente = existentes.get(item.get("produto_id"), {})
            st.markdown(f"**{nome}**")
            c1, c2 = st.columns([1, 1])
            preco = c1.text_input("Preço", value=str(existente.get("preco", "") or ""), key=f"vend_preco_{item.get('item_id')}")
            tem = c2.selectbox("Tem produto?", ["Sim", "Não"], index=0 if str(existente.get("tem_produto", "Sim")).lower() != "não" else 1, key=f"vend_tem_{item.get('item_id')}")
            obs = st.text_input("Observação", value=existente.get("observacao", "") or "", key=f"vend_obs_{item.get('item_id')}")
            dados_envio.append((item, preco, tem, obs, existente))
            st.divider()

        enviar = st.form_submit_button("Enviar cotação", width="stretch")

    if enviar:
        for item, preco, tem, obs, existente in dados_envio:
            resposta_id = existente.get("resposta_id") or next_id("respostas", "resposta_id", "RESP")
            payload = {
                "resposta_id": resposta_id,
                "cotacao_id": cotacao_id,
                "fornecedor_id": fornecedor_id,
                "produto_id": item.get("produto_id"),
                "preco": to_float(preco),
                "tem_produto": tem,
                "observacao": obs,
            }
            upsert_one("respostas", payload, "resposta_id")
        st.success("Resposta enviada com sucesso. Obrigado!")
        st.cache_data.clear()

if modo_vendedor:
    tela_vendedor()
    st.stop()

# -------------------------
# Navegação interna
# -------------------------
if "tela" not in st.session_state:
    st.session_state.tela = "Início"

PAGES = ["Início", "Criar", "Enviar", "Respostas", "Comparar", "Pedido", "Cadastros"]
cols = st.columns(len(PAGES))
for idx, page in enumerate(PAGES):
    label = f"• {page}" if st.session_state.tela == page else page
    if cols[idx].button(label, key=f"nav_v7_{page}", width="stretch"):
        st.session_state.tela = page
        st.rerun()

# -------------------------
# Páginas
# -------------------------
def tela_inicio():
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    atual = cotacao_atual(cotacoes)
    atual_id = atual.get("cotacao_id") if atual else "Nenhuma"
    itens_atual = [i for i in itens if i.get("cotacao_id") == atual_id]
    resp_atual = [r for r in respostas if r.get("cotacao_id") == atual_id]
    fornecedores_resp = len(set(r.get("fornecedor_id") for r in resp_atual if r.get("fornecedor_id")))
    total_fornecedores = len(fornecedores)
    pendentes_atual = max(total_fornecedores - fornecedores_resp, 0)
    prazo_atual = atual.get("prazo", "—") if atual else "—"

    if not atual:
        status_fluxo = "Sem cotação"
    elif len(itens_atual) == 0:
        status_fluxo = "Adicionar produtos"
    elif fornecedores_resp == 0:
        status_fluxo = "Enviar aos fornecedores"
    elif pendentes_atual > 0:
        status_fluxo = "Aguardando respostas"
    else:
        status_fluxo = "Pronto para comparar"

    if not atual:
        proxima = "Criar a primeira cotação."
    elif len(itens_atual) == 0:
        proxima = "Adicionar produtos à cotação aberta."
    elif fornecedores_resp == 0:
        proxima = "Enviar a lista aos fornecedores."
    else:
        proxima = "Comparar preços e montar pedido."

    st.markdown(
        f"""
<div class="main-card">
    <div class="muted" style="font-weight:900;letter-spacing:.08em;font-size:11px;">SUPERMERCADO MARIALVA</div>
    <h1>Painel de cotações</h1>
    <div class="status-line">
        <span class="status-chip">Cotação: {atual_id}</span>
        <span class="status-chip">Prazo: {prazo_atual}</span>
        <span class="status-chip">Status: {status_fluxo}</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        ("Produtos", len(produtos), "Base online"),
        ("Fornecedores", total_fornecedores, "Contatos"),
        ("Itens", len(itens_atual), "Cotação atual"),
        ("Responderam", fornecedores_resp, "Cotação atual"),
        ("Pendentes", pendentes_atual, "Fornecedores"),
    ]
    for col, (titulo, numero, subtitulo) in zip([c1, c2, c3, c4, c5], cards):
        col.markdown(f'<div class="card"><small>{titulo}</small><div class="metric-number">{numero}</div><small>{subtitulo}</small></div>', unsafe_allow_html=True)

    # Tela inicial compacta: ações principais ficam no menu superior.
def tela_criar():
    st.header("Criar cotação")
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    produtos_map, _ = mapas_base(produtos, fornecedores)

    with st.expander("Nova cotação", expanded=False):
        with st.form("form_nova_cotacao"):
            c1, c2, c3 = st.columns(3)
            data = c1.date_input("Data", value=date.today())
            prazo = c2.text_input("Prazo", value="Hoje até 16:30")
            responsavel = c3.text_input("Responsável", value="Compras")
            obs = st.text_input("Observação", value="Cotação de compras")
            criar = st.form_submit_button("Criar cotação", width="stretch")
        if criar:
            cotacao_id = next_id("cotacoes", "cotacao_id", "COT")
            insert_one("cotacoes", {
                "cotacao_id": cotacao_id,
                "data": str(data),
                "prazo": prazo,
                "status": "Aberta",
                "responsavel": responsavel,
                "observacao": obs,
            })
            st.success(f"Cotação {cotacao_id} criada.")
            st.rerun()

    opcoes_cot = [c.get("cotacao_id") for c in cotacoes]
    if not opcoes_cot:
        st.info("Crie uma cotação para começar.")
        return

    atual = cotacao_atual(cotacoes)
    default_idx = opcoes_cot.index(atual.get("cotacao_id")) if atual and atual.get("cotacao_id") in opcoes_cot else 0
    cotacao_id = st.selectbox("Cotação", opcoes_cot, index=default_idx)

    st.subheader("Adicionar produtos")
    busca = st.text_input("Buscar produto", placeholder="Digite parte do nome, marca ou categoria")
    produtos_filtrados = produtos
    if busca:
        b = busca.lower()
        produtos_filtrados = [p for p in produtos if b in produto_nome(p).lower() or b in str(p.get("categoria", "")).lower()]
    produtos_filtrados = produtos_filtrados[:80]

    if produtos_filtrados:
        opcoes = {f"{produto_nome(p)} · {p.get('produto_id')}": p.get("produto_id") for p in produtos_filtrados}
        escolhido_label = st.selectbox("Produto", list(opcoes.keys()))
        produto_id = opcoes[escolhido_label]
        c1, c2 = st.columns([1, 2])
        qtd = c1.text_input("Quantidade desejada", value="")
        obs_item = c2.text_input("Observação do item", value="")
        if st.button("Adicionar à cotação", key="btn_add_item_cot", width="stretch"):
            item_id = next_id("itens_cotacao", "item_id", "ITEM")
            insert_one("itens_cotacao", {
                "item_id": item_id,
                "cotacao_id": cotacao_id,
                "produto_id": produto_id,
                "quantidade_desejada": qtd,
                "observacao": obs_item,
            })
            st.success("Produto adicionado.")
            st.rerun()
    else:
        st.warning("Nenhum produto encontrado nessa busca.")

    st.subheader("Itens da cotação")
    itens_cot = [i for i in itens if i.get("cotacao_id") == cotacao_id]
    linhas = []
    for item in itens_cot:
        p = produtos_map.get(item.get("produto_id"), {})
        linhas.append({
            "Item": item.get("item_id"),
            "Produto": produto_nome(p),
            "Quantidade": item.get("quantidade_desejada"),
            "Observação": item.get("observacao"),
        })
    st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True)


def tela_enviar():
    st.header("Enviar aos fornecedores")
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    produtos_map, fornecedores_map = mapas_base(produtos, fornecedores)
    cotacoes_ids = [c.get("cotacao_id") for c in cotacoes]
    if not cotacoes_ids:
        st.warning("Nenhuma cotação cadastrada.")
        return
    cotacao_id = st.selectbox("Cotação", cotacoes_ids, index=len(cotacoes_ids)-1)
    itens_cot = [i for i in itens if i.get("cotacao_id") == cotacao_id]
    if not itens_cot:
        st.warning("Esta cotação ainda não possui produtos.")
        return

    nomes_itens = [f"- {produto_nome(produtos_map.get(i.get('produto_id'), {}))}" for i in itens_cot]
    lista_produtos = "\n".join(nomes_itens)
    app_url = base_app_url() or "COLE_AQUI_O_LINK_DO_SISTEMA_QUANDO_PUBLICAR"

    st.caption("Copie a mensagem ou use o link do WhatsApp.")
    for f in fornecedores:
        fornecedor_id = f.get("fornecedor_id")
        link_vendedor = f"{app_url}?modo=vendedor&cotacao_id={cotacao_id}&fornecedor_id={fornecedor_id}"
        mensagem = (
            f"Olá, {f.get('vendedor', '')}! Tudo bem?\n\n"
            f"Segue cotação {cotacao_id} do Supermercado Marialva.\n\n"
            f"Produtos:\n{lista_produtos}\n\n"
            f"Você pode responder pelo link:\n{link_vendedor}\n\nObrigado!"
        )
        whatsapp = re.sub(r"\D", "", str(f.get("whatsapp", "")))
        link_whats = f"https://wa.me/55{whatsapp}?text={quote(mensagem)}" if whatsapp else ""
        with st.expander(f"{f.get('vendedor')} · {f.get('empresa')}"):
            st.text_area("Mensagem", mensagem, height=210, key=f"msg_{fornecedor_id}")
            st.code(link_vendedor)
            if link_whats:
                st.link_button("Abrir WhatsApp", link_whats, width="stretch")


def tela_respostas():
    st.header("Respostas")
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    produtos_map, fornecedores_map = mapas_base(produtos, fornecedores)
    cotacoes_ids = [c.get("cotacao_id") for c in cotacoes]
    if not cotacoes_ids:
        st.warning("Nenhuma cotação cadastrada.")
        return
    cotacao_id = st.selectbox("Cotação", cotacoes_ids, index=len(cotacoes_ids)-1, key="resp_cotacao")

    st.subheader("Lançar resposta manual")
    fornecedores_ops = {f"{f.get('vendedor')} · {f.get('empresa')} · {f.get('fornecedor_id')}": f.get("fornecedor_id") for f in fornecedores}
    itens_cot = [i for i in itens if i.get("cotacao_id") == cotacao_id]
    produtos_ops = {f"{produto_nome(produtos_map.get(i.get('produto_id'), {}))} · {i.get('produto_id')}": i.get("produto_id") for i in itens_cot}

    if fornecedores_ops and produtos_ops:
        with st.form("form_resp_manual"):
            fornecedor_label = st.selectbox("Fornecedor", list(fornecedores_ops.keys()))
            produto_label = st.selectbox("Produto", list(produtos_ops.keys()))
            c1, c2 = st.columns(2)
            preco = c1.text_input("Preço", placeholder="Ex.: 4,99")
            tem = c2.selectbox("Tem produto?", ["Sim", "Não"])
            obs = st.text_input("Observação")
            salvar = st.form_submit_button("Salvar resposta", width="stretch")
        if salvar:
            resposta_id = next_id("respostas", "resposta_id", "RESP")
            insert_one("respostas", {
                "resposta_id": resposta_id,
                "cotacao_id": cotacao_id,
                "fornecedor_id": fornecedores_ops[fornecedor_label],
                "produto_id": produtos_ops[produto_label],
                "preco": to_float(preco),
                "tem_produto": tem,
                "observacao": obs,
            })
            st.success("Resposta salva.")
            st.rerun()

    st.subheader("Respostas recebidas")
    linhas = []
    for r in respostas:
        if r.get("cotacao_id") != cotacao_id:
            continue
        linhas.append({
            "Fornecedor": fornecedores_map.get(r.get("fornecedor_id"), {}).get("vendedor", r.get("fornecedor_id")),
            "Produto": produto_nome(produtos_map.get(r.get("produto_id"), {})),
            "Preço": formatar_real(r.get("preco")),
            "Tem produto": r.get("tem_produto"),
            "Observação": r.get("observacao"),
        })
    st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True)


def comparativo(cotacao_id):
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()
    produtos_map, fornecedores_map = mapas_base(produtos, fornecedores)
    itens_ids = [i.get("produto_id") for i in itens if i.get("cotacao_id") == cotacao_id]
    linhas = []
    for produto_id in itens_ids:
        rs = [r for r in respostas if r.get("cotacao_id") == cotacao_id and r.get("produto_id") == produto_id and str(r.get("tem_produto", "Sim")).lower() != "não" and r.get("preco") is not None]
        if not rs:
            linhas.append({"Produto": produto_nome(produtos_map.get(produto_id, {})), "Fornecedor vencedor": "Sem resposta", "Menor preço": None, "FornecedorID": ""})
            continue
        melhor = sorted(rs, key=lambda x: float(x.get("preco") or 999999999))[0]
        forn = fornecedores_map.get(melhor.get("fornecedor_id"), {})
        linhas.append({
            "ProdutoID": produto_id,
            "Produto": produto_nome(produtos_map.get(produto_id, {})),
            "FornecedorID": melhor.get("fornecedor_id"),
            "Fornecedor vencedor": forn.get("vendedor", melhor.get("fornecedor_id")),
            "Empresa": forn.get("empresa", ""),
            "Menor preço": melhor.get("preco"),
            "Preço formatado": formatar_real(melhor.get("preco")),
        })
    return pd.DataFrame(linhas)


def tela_comparar():
    st.header("Comparar preços")
    cotacoes = fetch_all("cotacoes", "cotacao_id")
    cotacoes_ids = [c.get("cotacao_id") for c in cotacoes]
    if not cotacoes_ids:
        st.warning("Nenhuma cotação cadastrada.")
        return
    cotacao_id = st.selectbox("Cotação", cotacoes_ids, index=len(cotacoes_ids)-1, key="comp_cot")
    df = comparativo(cotacao_id)
    if df.empty:
        st.info("Ainda não há itens para comparar.")
    else:
        st.dataframe(df[["Produto", "Fornecedor vencedor", "Empresa", "Preço formatado"]], width="stretch", hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Baixar comparativo CSV", csv, f"comparativo_{cotacao_id}.csv", "text/csv", width="stretch")


def tela_pedido():
    st.header("Pedido final")
    cotacoes = fetch_all("cotacoes", "cotacao_id")
    cotacoes_ids = [c.get("cotacao_id") for c in cotacoes]
    if not cotacoes_ids:
        st.warning("Nenhuma cotação cadastrada.")
        return
    cotacao_id = st.selectbox("Cotação", cotacoes_ids, index=len(cotacoes_ids)-1, key="pedido_cot")
    df = comparativo(cotacao_id)
    if df.empty or "FornecedorID" not in df.columns:
        st.info("Ainda não há pedido para montar.")
        return
    df = df[df["FornecedorID"].fillna("") != ""]
    if df.empty:
        st.info("Nenhum fornecedor vencedor encontrado.")
        return
    for fornecedor, grupo in df.groupby("Fornecedor vencedor"):
        total = grupo["Menor preço"].fillna(0).astype(float).sum()
        with st.expander(f"{fornecedor} · Total estimado {formatar_real(total)}", expanded=True):
            st.dataframe(grupo[["Produto", "Preço formatado"]], width="stretch", hide_index=True)


def tela_cadastros():
    st.header("Cadastros")
    aba1, aba2 = st.tabs(["Produtos", "Fornecedores"])
    produtos, fornecedores, cotacoes, itens, respostas = carregar_base()

    with aba1:
        st.subheader("Cadastrar produto")
        with st.form("form_cad_produto"):
            c1, c2, c3 = st.columns(3)
            produto = c1.text_input("Produto")
            marca = c2.text_input("Marca")
            tamanho = c3.text_input("Tamanho")
            c4, c5, c6 = st.columns(3)
            categoria = c4.text_input("Categoria")
            unidade = c5.text_input("Unidade")
            ativo = c6.selectbox("Ativo", ["Sim", "Não"])
            obs = st.text_input("Observação")
            salvar = st.form_submit_button("Salvar produto", width="stretch")
        if salvar and produto:
            produto_id = next_id("produtos", "produto_id", "PROD")
            insert_one("produtos", {"produto_id": produto_id, "produto": produto, "marca": marca, "tamanho": tamanho, "categoria": categoria, "unidade": unidade, "ativo": ativo, "observacao": obs})
            st.success("Produto cadastrado.")
            st.rerun()

        busca = st.text_input("Buscar na base", key="busca_cad_prod")
        dados = produtos
        if busca:
            b = busca.lower()
            dados = [p for p in produtos if b in produto_nome(p).lower() or b in str(p.get("categoria", "")).lower()]
        st.dataframe(pd.DataFrame(dados[:300]), width="stretch", hide_index=True)

    with aba2:
        st.subheader("Cadastrar fornecedor")
        with st.form("form_cad_fornecedor"):
            c1, c2 = st.columns(2)
            vendedor = c1.text_input("Vendedor")
            empresa = c2.text_input("Empresa")
            c3, c4, c5 = st.columns(3)
            whatsapp = c3.text_input("WhatsApp")
            categoria = c4.text_input("Categoria forte")
            ativo = c5.selectbox("Ativo", ["Sim", "Não"], key="ativo_forn")
            obs = st.text_input("Observação", key="obs_forn")
            salvar = st.form_submit_button("Salvar fornecedor", width="stretch")
        if salvar and vendedor:
            fornecedor_id = next_id("fornecedores", "fornecedor_id", "FOR")
            insert_one("fornecedores", {"fornecedor_id": fornecedor_id, "vendedor": vendedor, "empresa": empresa, "whatsapp": whatsapp, "categoria_forte": categoria, "ativo": ativo, "observacao": obs})
            st.success("Fornecedor cadastrado.")
            st.rerun()
        st.dataframe(pd.DataFrame(fornecedores), width="stretch", hide_index=True)

# Roteamento
if st.session_state.tela == "Início":
    tela_inicio()
elif st.session_state.tela == "Criar":
    tela_criar()
elif st.session_state.tela == "Enviar":
    tela_enviar()
elif st.session_state.tela == "Respostas":
    tela_respostas()
elif st.session_state.tela == "Comparar":
    tela_comparar()
elif st.session_state.tela == "Pedido":
    tela_pedido()
elif st.session_state.tela == "Cadastros":
    tela_cadastros()
