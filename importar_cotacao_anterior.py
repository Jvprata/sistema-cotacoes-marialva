import os
import unicodedata
from datetime import date
import pandas as pd

# =====================================================
# IMPORTADOR DE COTAÇÃO ANTERIOR — SUPERMERCADO MARIALVA
# Este arquivo deve ficar na mesma pasta do app.py.
# Ele importa produtos, cria uma cotação histórica e lança
# os menores preços informados por fornecedor.
# =====================================================

PASTA_DADOS = "dados"

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

CODIGO_IMPORTACAO = "IMPORT_COTACAO_ANTERIOR_MENORES_PRECOS_2026_06"

DADOS_COTACAO = [
    {"produto": "Molho de tomate", "marca": "Pomarola", "tamanho": "520g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Rogério", "preco": 4.20, "descricao_original": "Molho de tomate Pomarola 520g"},
    {"produto": "Extrato de tomate", "marca": "Elefante", "tamanho": "Copo tradicional", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 5.93, "descricao_original": "Extrato de tomate Elefante copo tradicional"},
    {"produto": "Atum sólido", "marca": "Coqueiro", "tamanho": "170g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 9.15, "descricao_original": "Atum Coqueiro sólido 170g"},
    {"produto": "Sardinha em óleo", "marca": "Coqueiro", "tamanho": "125g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Rogério", "preco": 4.81, "descricao_original": "Sardinha Coqueiro óleo 125g"},
    {"produto": "Sardinha", "marca": "Pescador", "tamanho": "125g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 4.81, "descricao_original": "Sardinha Pescador 125g"},
    {"produto": "Sardinha", "marca": "Gomes da Costa", "tamanho": "125g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 4.89, "descricao_original": "Sardinha Gomes da Costa 125g"},
    {"produto": "Seleta de legumes sachê", "marca": "Quero", "tamanho": "Sachê", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 3.51, "descricao_original": "Seleta de legumes sachê Quero"},
    {"produto": "Salsicha lata", "marca": "Bordon", "tamanho": "Lata", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 4.17, "descricao_original": "Salsicha lata Bordon"},
    {"produto": "Mostarda", "marca": "Quero", "tamanho": "190g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 4.81, "descricao_original": "Mostarda Quero 190g"},
    {"produto": "Lasanha", "marca": "Petybon", "tamanho": "200g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 2.89, "descricao_original": "Lasanha Petybon 200g"},
    {"produto": "Óleo de milho", "marca": "Suavit", "tamanho": "900ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 11.15, "descricao_original": "Óleo de milho Suavit 900ml"},
    {"produto": "Óleo de milho", "marca": "Sinhá", "tamanho": "900ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 11.29, "descricao_original": "Óleo de milho Sinhá 900ml"},
    {"produto": "Óleo de milho", "marca": "Soya", "tamanho": "900ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 13.62, "descricao_original": "Óleo de milho Soya 900ml"},
    {"produto": "Óleo de milho", "marca": "Liza", "tamanho": "900ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 13.99, "descricao_original": "Óleo de milho Liza 900ml"},
    {"produto": "Sabão em pó", "marca": "Ace", "tamanho": "800g", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcio", "preco": 4.99, "descricao_original": "Sabão em pó Ace 800g"},
    {"produto": "Sabão em pó", "marca": "Ace", "tamanho": "1,5kg", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcio", "preco": 9.29, "descricao_original": "Sabão em pó Ace 1,5kg"},
    {"produto": "Sabão em pó", "marca": "Ace", "tamanho": "2,2kg", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcio", "preco": 15.99, "descricao_original": "Sabão em pó Ace 2,2kg"},
    {"produto": "Álcool", "marca": "Coperalcool", "tamanho": "500ml", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Junior", "preco": 5.73, "descricao_original": "Álcool Coperalcool 500ml"},
    {"produto": "Tira manchas pote rosa/cristal", "marca": "Vanish", "tamanho": "450g", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Cíntia", "preco": 26.26, "descricao_original": "Vanish pote rosa/cristal 450g"},
    {"produto": "Lava-roupas líquido", "marca": "Brilhante", "tamanho": "3L", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Paulo", "preco": 24.18, "descricao_original": "Lava-roupas Brilhante líquido 3L"},
    {"produto": "Lava-roupas líquido", "marca": "Omo", "tamanho": "3L", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Junior", "preco": 31.26, "descricao_original": "Lava-roupas Omo líquido 3L"},
    {"produto": "Amaciante", "marca": "Ypê", "tamanho": "2L", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcio", "preco": 7.98, "descricao_original": "Amaciante Ypê 2L"},
    {"produto": "Amaciante", "marca": "Ypê", "tamanho": "500ml", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Paulo", "preco": 2.91, "descricao_original": "Amaciante Ypê 500ml"},
    {"produto": "Aromatizador Bom Ar fragrâncias", "marca": "Bom Ar", "tamanho": "Fragrâncias", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Cíntia", "preco": 10.46, "descricao_original": "Bom Ar fragrâncias"},
    {"produto": "Aromatizador Glade fragrâncias", "marca": "Glade", "tamanho": "Fragrâncias", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Cíntia", "preco": 12.05, "descricao_original": "Glade fragrâncias"},
    {"produto": "Óleo de peroba", "marca": "Óleo de Peroba", "tamanho": "100ml", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcos", "preco": 7.09, "descricao_original": "Óleo de peroba 100ml"},
    {"produto": "Óleo de peroba", "marca": "Óleo de Peroba", "tamanho": "200ml", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Marcos", "preco": 12.69, "descricao_original": "Óleo de peroba 200ml"},
    {"produto": "Óleo de peroba", "marca": "Óleo de Peroba", "tamanho": "500ml", "categoria": "Limpeza", "unidade": "Unidade", "vendedor": "Cíntia", "preco": 30.27, "descricao_original": "Óleo de peroba 500ml"},
    {"produto": "Sabão em pedra com 5 unidades", "marca": "Ypê", "tamanho": "5 unidades", "categoria": "Limpeza", "unidade": "Pacote", "vendedor": "Marcio", "preco": 9.69, "descricao_original": "Sabão em pedra Ypê com 5 unidades"},
    {"produto": "Farinha de trigo com fermento", "marca": "", "tamanho": "1kg", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 5.01, "descricao_original": "Farinha de trigo com fermento 1kg"},
    {"produto": "Bombom", "marca": "Garoto", "tamanho": "250g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 11.22, "descricao_original": "Bombom Garoto 250g"},
    {"produto": "Leite de coco", "marca": "Menina", "tamanho": "200ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 2.39, "descricao_original": "Leite de coco Menina 200ml"},
    {"produto": "Chá Matte", "marca": "Leão", "tamanho": "250g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 5.67, "descricao_original": "Chá Matte Leão 250g"},
    {"produto": "Adoçante", "marca": "Adocyl", "tamanho": "100ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 3.35, "descricao_original": "Adoçante Adocyl 100ml"},
    {"produto": "Adoçante", "marca": "Adocyl", "tamanho": "200ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 6.03, "descricao_original": "Adoçante Adocyl 200ml"},
    {"produto": "Adoçante", "marca": "Zero-Cal", "tamanho": "100ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 5.83, "descricao_original": "Adoçante Zero-Cal 100ml"},
    {"produto": "Pêssego em lata", "marca": "Schramm", "tamanho": "450ml", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcio", "preco": 9.28, "descricao_original": "Pêssego em lata Schramm 450ml"},
    {"produto": "Pêssego em lata", "marca": "Extra", "tamanho": "Lata", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 9.20, "descricao_original": "Pêssego em lata Extra"},
    {"produto": "Pêssego zero/metade", "marca": "", "tamanho": "Zero/metade", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Junior", "preco": 9.85, "descricao_original": "Pêssego zero/metade"},
    {"produto": "Maizena", "marca": "Maizena", "tamanho": "500g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Cíntia", "preco": 10.39, "descricao_original": "Maizena 500g"},
    {"produto": "Biscoito Traquinas chocolate", "marca": "Traquinas", "tamanho": "Chocolate", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 2.10, "descricao_original": "Biscoito Traquinas chocolate"},
    {"produto": "Biscoito Tucs", "marca": "Tucs", "tamanho": "Todos", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 1.40, "descricao_original": "Biscoito Tucs — todos"},
    {"produto": "Néctar de frutas", "marca": "Maguary", "tamanho": "1L", "categoria": "Bebidas", "unidade": "Unidade", "vendedor": "Junior", "preco": 3.76, "descricao_original": "Néctar de frutas Maguary 1L"},
    {"produto": "Néctar de frutas", "marca": "Maratá", "tamanho": "1L", "categoria": "Bebidas", "unidade": "Unidade", "vendedor": "Junior", "preco": 4.71, "descricao_original": "Néctar de frutas Maratá 1L"},
    {"produto": "Néctar de frutas", "marca": "Maguary", "tamanho": "200ml", "categoria": "Bebidas", "unidade": "Unidade", "vendedor": "Junior", "preco": 1.21, "descricao_original": "Néctar de frutas Maguary 200ml"},
    {"produto": "Torrada tradicional", "marca": "Bauducco", "tamanho": "Tradicional", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 3.21, "descricao_original": "Torrada Bauducco tradicional"},
    {"produto": "Torrada integral/multigrãos", "marca": "Bauducco", "tamanho": "Integral / multigrãos", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 3.21, "descricao_original": "Torrada Bauducco integral / multigrãos"},
    {"produto": "Nescau lata", "marca": "Nescau", "tamanho": "200g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Marcos", "preco": 5.59, "descricao_original": "Nescau lata 200g"},
    {"produto": "Mucilon arroz e milho", "marca": "Mucilon", "tamanho": "360g", "categoria": "Mercearia", "unidade": "Unidade", "vendedor": "Paulo", "preco": 7.55, "descricao_original": "Mucilon arroz e milho 360g"},
]


def normalizar(texto):
    texto = "" if pd.isna(texto) else str(texto)
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.split())


def garantir_arquivos():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    for nome, caminho in ARQUIVOS.items():
        if not os.path.exists(caminho):
            pd.DataFrame(columns=COLUNAS[nome]).to_csv(caminho, index=False, encoding="utf-8-sig")


def carregar(nome):
    garantir_arquivos()
    return pd.read_csv(ARQUIVOS[nome], encoding="utf-8-sig", dtype=str).fillna("")


def salvar(nome, df):
    df.to_csv(ARQUIVOS[nome], index=False, encoding="utf-8-sig")


def proximo_id(prefixo, df, coluna_id):
    if df.empty or coluna_id not in df.columns:
        return f"{prefixo}001"

    numeros = []
    for valor in df[coluna_id].astype(str):
        if valor.startswith(prefixo):
            parte = valor.replace(prefixo, "", 1)
            if parte.isdigit():
                numeros.append(int(parte))
    prox = max(numeros) + 1 if numeros else 1
    return f"{prefixo}{prox:03d}"


def buscar_ou_criar_fornecedor(nome, fornecedores):
    alvo = normalizar(nome)
    if not fornecedores.empty:
        mascara = fornecedores["Vendedor"].apply(normalizar) == alvo
        if mascara.any():
            return fornecedores.loc[mascara, "FornecedorID"].iloc[0], fornecedores, False

    novo_id = proximo_id("FOR", fornecedores, "FornecedorID")
    novo = pd.DataFrame([{
        "FornecedorID": novo_id,
        "Vendedor": nome,
        "Empresa": "",
        "WhatsApp": "",
        "CategoriaForte": "",
        "Ativo": "Sim",
        "Observacao": "Criado automaticamente pela importação da cotação anterior",
    }])
    fornecedores = pd.concat([fornecedores, novo], ignore_index=True)
    return novo_id, fornecedores, True


def buscar_ou_criar_produto(item, produtos):
    alvo = (
        normalizar(item["produto"]),
        normalizar(item["marca"]),
        normalizar(item["tamanho"]),
    )

    if not produtos.empty:
        for idx, row in produtos.iterrows():
            chave = (
                normalizar(row.get("Produto", "")),
                normalizar(row.get("Marca", "")),
                normalizar(row.get("Tamanho", "")),
            )
            if chave == alvo:
                return row["ProdutoID"], produtos, False

    novo_id = proximo_id("PROD", produtos, "ProdutoID")
    novo = pd.DataFrame([{
        "ProdutoID": novo_id,
        "Produto": item["produto"],
        "Marca": item["marca"],
        "Tamanho": item["tamanho"],
        "Categoria": item["categoria"],
        "Unidade": item["unidade"],
        "Ativo": "Sim",
        "Observacao": f"Importado da cotação anterior. Descrição original: {item['descricao_original']}",
    }])
    produtos = pd.concat([produtos, novo], ignore_index=True)
    return novo_id, produtos, True


def main():
    garantir_arquivos()

    produtos = carregar("produtos")
    fornecedores = carregar("fornecedores")
    cotacoes = carregar("cotacoes")
    itens_cotacao = carregar("itens_cotacao")
    respostas = carregar("respostas")

    # Evita duplicar a mesma importação caso o script seja rodado novamente.
    if not cotacoes.empty and cotacoes["Observacao"].astype(str).str.contains(CODIGO_IMPORTACAO, na=False).any():
        print("Esta cotação anterior já foi importada. Nenhuma alteração foi feita.")
        return

    cotacao_id = proximo_id("COT", cotacoes, "CotacaoID")
    nova_cotacao = pd.DataFrame([{
        "CotacaoID": cotacao_id,
        "Data": str(date.today()),
        "Prazo": "Cotação anterior importada",
        "Status": "Finalizada",
        "Responsavel": "João",
        "Observacao": f"{CODIGO_IMPORTACAO} - Menores preços informados anteriormente",
    }])
    cotacoes = pd.concat([cotacoes, nova_cotacao], ignore_index=True)

    produtos_criados = 0
    fornecedores_criados = 0
    itens_criados = 0
    respostas_criadas = 0

    for item in DADOS_COTACAO:
        fornecedor_id, fornecedores, fornecedor_novo = buscar_ou_criar_fornecedor(item["vendedor"], fornecedores)
        produto_id, produtos, produto_novo = buscar_ou_criar_produto(item, produtos)

        produtos_criados += int(produto_novo)
        fornecedores_criados += int(fornecedor_novo)

        item_id = proximo_id("ITEM", itens_cotacao, "ItemID")
        novo_item = pd.DataFrame([{
            "ItemID": item_id,
            "CotacaoID": cotacao_id,
            "ProdutoID": produto_id,
            "QuantidadeDesejada": "0",
            "Observacao": "Item importado da cotação anterior; quantidade não informada",
        }])
        itens_cotacao = pd.concat([itens_cotacao, novo_item], ignore_index=True)
        itens_criados += 1

        resposta_id = proximo_id("RESP", respostas, "RespostaID")
        nova_resposta = pd.DataFrame([{
            "RespostaID": resposta_id,
            "CotacaoID": cotacao_id,
            "FornecedorID": fornecedor_id,
            "ProdutoID": produto_id,
            "Preco": f"{item['preco']:.2f}",
            "TemProduto": "Sim",
            "Observacao": f"Importado: vendedor mais barato informado. Descrição original: {item['descricao_original']}",
        }])
        respostas = pd.concat([respostas, nova_resposta], ignore_index=True)
        respostas_criadas += 1

    salvar("produtos", produtos)
    salvar("fornecedores", fornecedores)
    salvar("cotacoes", cotacoes)
    salvar("itens_cotacao", itens_cotacao)
    salvar("respostas", respostas)

    print("Importação concluída com sucesso!")
    print(f"Cotação criada: {cotacao_id}")
    print(f"Produtos novos cadastrados: {produtos_criados}")
    print(f"Fornecedores novos cadastrados: {fornecedores_criados}")
    print(f"Itens adicionados à cotação: {itens_criados}")
    print(f"Respostas/menores preços lançados: {respostas_criadas}")
    print("Agora atualize o navegador do sistema com F5.")


if __name__ == "__main__":
    main()