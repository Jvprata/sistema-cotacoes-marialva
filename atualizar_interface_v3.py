from pathlib import Path
from datetime import datetime
import textwrap

APP = r"""
import os, re, shutil
from datetime import date, datetime
from urllib.parse import urlencode
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sistema de Cotações Marialva", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

DADOS = "dados"
BACKUPS = "backups"
ARQS = {
    "produtos": f"{DADOS}/produtos.csv",
    "fornecedores": f"{DADOS}/fornecedores.csv",
    "cotacoes": f"{DADOS}/cotacoes.csv",
    "itens": f"{DADOS}/itens_cotacao.csv",
    "respostas": f"{DADOS}/respostas.csv",
}
COLS = {
    "produtos": ["ProdutoID","Produto","Marca","Tamanho","Categoria","Unidade","Ativo","Observacao"],
    "fornecedores": ["FornecedorID","Vendedor","Empresa","WhatsApp","CategoriaForte","Ativo","Observacao"],
    "cotacoes": ["CotacaoID","Data","Prazo","Status","Responsavel","Observacao"],
    "itens": ["ItemID","CotacaoID","ProdutoID","QuantidadeDesejada","Observacao"],
    "respostas": ["RespostaID","CotacaoID","FornecedorID","ProdutoID","Preco","TemProduto","Observacao"],
}

def init():
    os.makedirs(DADOS, exist_ok=True)
    for k, path in ARQS.items():
        if not os.path.exists(path):
            pd.DataFrame(columns=COLS[k]).to_csv(path, index=False, encoding="utf-8-sig")

def load(k):
    init()
    try:
        df = pd.read_csv(ARQS[k], dtype=str, encoding="utf-8-sig").fillna("")
    except Exception:
        df = pd.DataFrame(columns=COLS[k])
    for c in COLS[k]:
        if c not in df.columns:
            df[c] = ""
    return df[COLS[k]]

def save(k, df):
    for c in COLS[k]:
        if c not in df.columns:
            df[c] = ""
    df[COLS[k]].to_csv(ARQS[k], index=False, encoding="utf-8-sig")

def gid(prefixo, df, coluna):
    if df.empty:
        return f"{prefixo}001"
    nums = df[coluna].astype(str).str.replace(prefixo, "", regex=False).str.extract(r"(\d+)", expand=False)
    nums = pd.to_numeric(nums, errors="coerce").dropna()
    return f"{prefixo}{(int(nums.max())+1 if len(nums) else 1):03d}"

def money(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except Exception:
        return "R$ 0,00"

def parse_price(txt):
    t = str(txt).replace("R$","").strip().upper()
    if t in ["", "NT", "N/T", "NÃO TEM", "NAO TEM", "-"]:
        return None
    t = t.replace(".","").replace(",",".")
    try:
        return float(t)
    except Exception:
        return None

def pdesc(row):
    return " ".join([str(row.get(c,"")).strip() for c in ["Produto","Marca","Tamanho"] if str(row.get(c,"")).strip()])

def tel(txt):
    return re.sub(r"\D", "", str(txt or ""))

def qp(k, default=""):
    try:
        v = st.query_params.get(k, default)
        return v[0] if isinstance(v, list) and v else v
    except Exception:
        return default

def rerun():
    try: st.rerun()
    except Exception: st.experimental_rerun()

init()
produtos, fornecedores, cotacoes, itens, respostas = [load(k) for k in ["produtos","fornecedores","cotacoes","itens","respostas"]]

st.markdown('''
<style>
[data-testid="stSidebar"]{display:none}.block-container{max-width:1180px;padding-top:28px}.titulo{font-size:2.1rem;font-weight:850}.sub{color:#9ca3af;margin-bottom:22px}.card{border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:18px;background:rgba(255,255,255,.04);min-height:110px}.card h3{margin:0;font-size:1.1rem}.card p{color:#aab2bf;font-size:.92rem}div.stButton>button{width:100%;border-radius:12px;min-height:48px;font-weight:700}.box{border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:15px;background:rgba(255,255,255,.035);margin:10px 0}
</style>
''', unsafe_allow_html=True)

# ===================== ÁREA DO VENDEDOR =====================
def salva_resposta(cot, forn, prod, preco, tem, obs=""):
    df = load("respostas")
    mask = (df.CotacaoID==cot)&(df.FornecedorID==forn)&(df.ProdutoID==prod)
    preco_txt = "" if tem == "Não" else str(preco).replace(".", ",")
    if mask.any():
        i = df[mask].index[0]
        df.loc[i,["Preco","TemProduto","Observacao"]] = [preco_txt, tem, obs]
    else:
        df = pd.concat([df, pd.DataFrame([{"RespostaID":gid("RESP",df,"RespostaID"),"CotacaoID":cot,"FornecedorID":forn,"ProdutoID":prod,"Preco":preco_txt,"TemProduto":tem,"Observacao":obs}])], ignore_index=True)
    save("respostas", df)

def area_vendedor():
    cot, forn = qp("cotacao"), qp("fornecedor")
    st.markdown('<div class="titulo">🛒 Cotação — Supermercado Marialva</div><div class="sub">Preencha os preços e clique em enviar.</div>', unsafe_allow_html=True)
    if not cot or not forn:
        st.error("Link incompleto. Peça um novo link ao responsável de compras."); return
    cdf, fdf = cotacoes[cotacoes.CotacaoID==cot], fornecedores[fornecedores.FornecedorID==forn]
    if cdf.empty or fdf.empty:
        st.error("Cotação ou fornecedor não encontrado."); return
    st.success(f"Fornecedor: {fdf.iloc[0]['Vendedor']} | Cotação: {cot} | Prazo: {cdf.iloc[0].get('Prazo','')}")
    its = itens[itens.CotacaoID==cot].merge(produtos, on="ProdutoID", how="left")
    if its.empty:
        st.info("Essa cotação ainda não possui produtos."); return
    resp = respostas[(respostas.CotacaoID==cot)&(respostas.FornecedorID==forn)]
    with st.form("form_vendedor"):
        payload=[]
        for _, r in its.iterrows():
            antigo = resp[resp.ProdutoID==r.ProdutoID]
            preco_antigo = parse_price(antigo.iloc[0].Preco) if not antigo.empty else 0
            tem_antigo = False if (not antigo.empty and antigo.iloc[0].TemProduto=="Não") else True
            st.markdown('<div class="box">', unsafe_allow_html=True)
            c1,c2,c3=st.columns([3,1,1])
            c1.markdown(f"**{pdesc(r)}**"); c1.caption(f"Código: {r.ProdutoID} | Qtd: {r.get('QuantidadeDesejada','')}")
            tem = c2.checkbox("Tenho", value=tem_antigo, key=f"tem_{r.ProdutoID}")
            preco = c3.number_input("Preço", min_value=0.0, step=0.01, value=float(preco_antigo or 0), format="%.2f", disabled=not tem, key=f"preco_{r.ProdutoID}")
            st.markdown('</div>', unsafe_allow_html=True)
            payload.append((r.ProdutoID, preco, "Sim" if tem else "Não"))
        if st.form_submit_button("Enviar cotação"):
            for prod, preco, tem in payload:
                salva_resposta(cot, forn, prod, preco, tem, "Enviado pelo link do vendedor")
            st.success("Cotação enviada com sucesso. Obrigado!"); st.balloons()

if qp("modo") == "vendedor":
    area_vendedor(); st.stop()

# ===================== ÁREA INTERNA =====================
def go(t):
    st.session_state.tela = t
    try: st.query_params["tela"] = t
    except Exception: pass
    rerun()

if "tela" not in st.session_state:
    st.session_state.tela = qp("tela", "painel") or "painel"

c_top1,c_top2=st.columns([5,1])
with c_top1:
    st.markdown('<div class="titulo">🛒 Sistema de Cotações — Marialva</div><div class="sub">Criar cotação → enviar link → receber respostas → comparar → gerar pedido.</div>', unsafe_allow_html=True)
with c_top2:
    if st.button("🏠 Início"): go("painel")

def resultado(cot):
    df = load("respostas")
    if df.empty: return pd.DataFrame()
    df = df[df.CotacaoID==cot].copy(); df["PrecoNum"] = df.Preco.apply(parse_price)
    df = df[(df.TemProduto=="Sim") & df.PrecoNum.notna()]
    if df.empty: return pd.DataFrame()
    df = df.merge(produtos,on="ProdutoID",how="left").merge(fornecedores,on="FornecedorID",how="left")
    idx = df.groupby("ProdutoID").PrecoNum.idxmin(); win = df.loc[idx].copy()
    maxs = df.groupby("ProdutoID").PrecoNum.max().reset_index().rename(columns={"PrecoNum":"MaiorPreco"})
    win = win.merge(maxs,on="ProdutoID",how="left"); win["Economia"] = win.MaiorPreco-win.PrecoNum
    q = itens[itens.CotacaoID==cot][["ProdutoID","QuantidadeDesejada"]]
    win = win.merge(q,on="ProdutoID",how="left")
    return win

def painel():
    st.header("Painel de compras")
    a,b,c,d=st.columns(4)
    a.metric("Produtos",len(produtos)); b.metric("Fornecedores",len(fornecedores)); c.metric("Cotações",len(cotacoes)); d.metric("Respostas",len(respostas))
    st.divider(); st.subheader("Escolha uma ação")
    cards=[("1. Criar cotação","Escolher os produtos da lista.","Criar cotação","nova"),("2. Enviar aos vendedores","Gerar link para WhatsApp.","Enviar links","enviar"),("3. Ver respostas","Acompanhar quem respondeu.","Ver respostas","respostas"),("4. Comparar preços","Ver menor preço por item.","Comparar","comparar"),("5. Pedido final","Separar compra por vendedor.","Gerar pedido","pedido"),("Cadastros","Produtos, fornecedores e backup.","Cadastros","cadastros")]
    for i in range(0,6,3):
        cols=st.columns(3)
        for col,(tit,txt,btn,tela) in zip(cols,cards[i:i+3]):
            col.markdown(f'<div class="card"><h3>{tit}</h3><p>{txt}</p></div>', unsafe_allow_html=True)
            if col.button(btn, key=tela): go(tela)
    st.divider(); st.subheader("Últimas cotações")
    st.dataframe(cotacoes.tail(10), width="stretch") if not cotacoes.empty else st.info("Nenhuma cotação criada.")

def nova():
    st.header("Criar cotação")
    with st.form("nova_cot"):
        c1,c2,c3=st.columns(3)
        data=c1.date_input("Data", value=date.today()); prazo=c2.text_input("Prazo", "Hoje até 15h"); resp=c3.text_input("Responsável", "João")
        obs=st.text_input("Observação", "Cotação semanal")
        if st.form_submit_button("Criar cotação"):
            df=load("cotacoes"); cid=gid("COT",df,"CotacaoID")
            df=pd.concat([df,pd.DataFrame([{"CotacaoID":cid,"Data":str(data),"Prazo":prazo,"Status":"Aberta","Responsavel":resp,"Observacao":obs}])],ignore_index=True); save("cotacoes",df)
            st.session_state.cot_atual=cid; st.success(f"Cotação criada: {cid}"); rerun()
    if cotacoes.empty or produtos.empty: return
    st.subheader("Adicionar produtos")
    cot_default=st.session_state.get("cot_atual",cotacoes.iloc[-1].CotacaoID); opts=cotacoes.CotacaoID.tolist(); ix=opts.index(cot_default) if cot_default in opts else len(opts)-1
    cot=st.selectbox("Cotação",opts,index=ix)
    pdf=produtos[produtos.Ativo.astype(str)!="Não"].copy(); pdf["Desc"]=pdf.ProdutoID+" — "+pdf.apply(pdesc,axis=1)+" | "+pdf.Categoria
    c1,c2=st.columns([1,2]); cat=c1.selectbox("Categoria", ["Todas"]+sorted([x for x in pdf.Categoria.unique() if str(x).strip()])); busca=c2.text_input("Buscar produto")
    filt=pdf.copy()
    if cat!="Todas": filt=filt[filt.Categoria==cat]
    if busca: filt=filt[filt.Desc.str.lower().str.contains(busca.lower(),na=False)]
    sel=st.multiselect("Produtos", filt.Desc.tolist()); qtd=st.number_input("Quantidade padrão",min_value=0,step=1,value=1)
    if st.button("Adicionar selecionados"):
        df=load("itens"); add=0
        for s in sel:
            pid=s.split(" — ")[0]
            if ((df.CotacaoID==cot)&(df.ProdutoID==pid)).any(): continue
            df=pd.concat([df,pd.DataFrame([{"ItemID":gid("ITEM",df,"ItemID"),"CotacaoID":cot,"ProdutoID":pid,"QuantidadeDesejada":str(qtd),"Observacao":""}])],ignore_index=True); add+=1
        save("itens",df); st.success(f"{add} produto(s) adicionado(s)."); rerun()
    its=load("itens"); its=its[its.CotacaoID==cot].merge(produtos,on="ProdutoID",how="left")
    st.dataframe(its, width="stretch") if not its.empty else st.info("Nenhum item nessa cotação.")

def enviar():
    st.header("Enviar link para vendedores")
    if cotacoes.empty or fornecedores.empty: st.warning("Crie cotação e fornecedores primeiro."); return
    cot=st.selectbox("Cotação",cotacoes.CotacaoID.tolist(),index=len(cotacoes)-1)
    base=st.text_input("Link base do sistema", value="", placeholder="Cole aqui o link do Ngrok: https://...ngrok-free.dev").rstrip("/")
    fdf=fornecedores.copy(); fdf["Desc"]=fdf.FornecedorID+" — "+fdf.Vendedor
    sel=st.multiselect("Vendedores",fdf.Desc.tolist())
    for s in sel:
        fid=s.split(" — ")[0]; f=fornecedores[fornecedores.FornecedorID==fid].iloc[0]
        link=f"{base}?"+urlencode({"modo":"vendedor","cotacao":cot,"fornecedor":fid})
        msg=f"Bom dia, {f.Vendedor}!\n\nSegue cotação do Supermercado Marialva.\nAcesse o link abaixo, preencha os preços e envie:\n\n{link}\n\nObrigado."
        st.subheader(f.Vendedor); st.text_area("Mensagem",msg,height=160,key=f"msg_{fid}")
        numero=tel(f.WhatsApp)
        if numero:
            if not numero.startswith("55"): numero="55"+numero
            st.link_button("Abrir WhatsApp", f"https://wa.me/{numero}?text={urlencode({'text':msg})[5:]}")

def respostas_page():
    st.header("Respostas dos vendedores")
    if cotacoes.empty: return
    cot=st.selectbox("Cotação",cotacoes.CotacaoID.tolist(),index=len(cotacoes)-1)
    total=len(itens[itens.CotacaoID==cot]); rows=[]
    for _,f in fornecedores.iterrows():
        n=len(respostas[(respostas.CotacaoID==cot)&(respostas.FornecedorID==f.FornecedorID)])
        status="Não respondeu" if n==0 else ("Parcial" if n<total else "Respondido")
        rows.append({"Vendedor":f.Vendedor,"Respostas":n,"Itens":total,"Status":status})
    st.dataframe(pd.DataFrame(rows),width="stretch")
    with st.expander("Importar resposta colada do WhatsApp"):
        fdf=fornecedores.copy(); fdf["Desc"]=fdf.FornecedorID+" — "+fdf.Vendedor
        fid=st.selectbox("Fornecedor",fdf.Desc.tolist()).split(" — ")[0]
        texto=st.text_area("Cole no padrão: PROD001 - 4,20 / PROD002 - NT",height=160)
        if st.button("Importar"):
            valid=set(itens[itens.CotacaoID==cot].ProdutoID.astype(str)); ok=0; falha=0
            for linha in texto.splitlines():
                m=re.match(r"^([A-Za-z0-9]+)\s*[-:]\s*(.+)$",linha.strip())
                if not m or m.group(1) not in valid: falha+=1; continue
                preco=parse_price(m.group(2)); salva_resposta(cot,fid,m.group(1),preco or 0,"Não" if preco is None else "Sim","Importado do WhatsApp"); ok+=1
            st.success(f"Importados: {ok}. Ignorados: {falha}."); rerun()

def comparar():
    st.header("Comparativo")
    if cotacoes.empty: return
    cot=st.selectbox("Cotação",cotacoes.CotacaoID.tolist(),index=len(cotacoes)-1); r=resultado(cot)
    if r.empty: st.info("Ainda não há preços para comparar."); return
    v=r[["ProdutoID","Produto","Marca","Tamanho","Categoria","QuantidadeDesejada","Vendedor","PrecoNum","MaiorPreco","Economia"]].rename(columns={"Vendedor":"Fornecedor vencedor","PrecoNum":"Menor preço","QuantidadeDesejada":"Qtd"})
    for c in ["Menor preço","MaiorPreco","Economia"]: v[c]=v[c].apply(money)
    st.dataframe(v,width="stretch"); st.metric("Economia potencial unitária", money(r.Economia.fillna(0).astype(float).sum()))

def pedido():
    st.header("Pedido final")
    if cotacoes.empty: return
    cot=st.selectbox("Cotação",cotacoes.CotacaoID.tolist(),index=len(cotacoes)-1); r=resultado(cot)
    if r.empty: st.info("Ainda não há vencedores."); return
    for vend,g in r.groupby("Vendedor"):
        linhas=[f"- {pdesc(x)} | Qtd: {x.get('QuantidadeDesejada','')} | Preço: {money(x.PrecoNum)}" for _,x in g.iterrows()]
        st.subheader(f"Pedido para {vend}"); st.text_area("Copiar pedido", "\n".join(linhas), height=160, key=f"ped_{vend}")

def cadastros():
    st.header("Cadastros e manutenção")
    tab1,tab2,tab3=st.tabs(["Produtos","Fornecedores","Backups"])
    with tab1:
        with st.form("prod"):
            c1,c2,c3=st.columns(3); p=c1.text_input("Produto"); m=c1.text_input("Marca"); t=c2.text_input("Tamanho"); cat=c2.text_input("Categoria","Mercearia"); u=c3.text_input("Unidade","Unidade"); obs=c3.text_input("Obs")
            if st.form_submit_button("Salvar produto"):
                df=load("produtos"); df=pd.concat([df,pd.DataFrame([{"ProdutoID":gid("PROD",df,"ProdutoID"),"Produto":p,"Marca":m,"Tamanho":t,"Categoria":cat,"Unidade":u,"Ativo":"Sim","Observacao":obs}])],ignore_index=True); save("produtos",df); st.success("Salvo"); rerun()
        st.dataframe(load("produtos").tail(200),width="stretch")
    with tab2:
        with st.form("forn"):
            c1,c2=st.columns(2); v=c1.text_input("Vendedor"); e=c1.text_input("Empresa"); w=c2.text_input("WhatsApp"); cf=c2.text_input("Categoria forte","Mercearia")
            if st.form_submit_button("Salvar fornecedor"):
                df=load("fornecedores"); df=pd.concat([df,pd.DataFrame([{"FornecedorID":gid("FOR",df,"FornecedorID"),"Vendedor":v,"Empresa":e,"WhatsApp":w,"CategoriaForte":cf,"Ativo":"Sim","Observacao":""}])],ignore_index=True); save("fornecedores",df); st.success("Salvo"); rerun()
        st.dataframe(load("fornecedores"),width="stretch")
    with tab3:
        if st.button("Criar backup agora"):
            dest=f"{BACKUPS}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"; os.makedirs(dest,exist_ok=True)
            for path in ARQS.values():
                if os.path.exists(path): shutil.copy2(path, os.path.join(dest, os.path.basename(path)))
            st.success(f"Backup criado: {dest}")

pages={"painel":painel,"nova":nova,"enviar":enviar,"respostas":respostas_page,"comparar":comparar,"pedido":pedido,"cadastros":cadastros}
pages.get(st.session_state.tela,painel)()
"""

def main():
    app_path = Path("app.py")
    if not app_path.exists():
        raise FileNotFoundError("app.py não foi encontrado. Coloque este arquivo na mesma pasta do app.py.")
    backup_name = f"app_backup_interface_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    backup_path = Path(backup_name)
    backup_path.write_text(app_path.read_text(encoding="utf-8"), encoding="utf-8")
    app_path.write_text(APP.strip() + "\n", encoding="utf-8")
    print("Atualização da interface V3 concluída com sucesso!")
    print(f"Backup do app antigo criado em: {backup_path}")
    print("Agora rode: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
