import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Semente para reprodutibilidade
random.seed(42)
np.random.seed(42)

# Distribuição aproximada de clientes por cidade (totalizando 10.000)
cities_distribution = {
    "Lisboa": 2660,
    "Porto": 1150,
    "Braga": 876,
    "Coimbra": 508,
    "Faro": 290,
    "Cascais": 970,
    "Vila Nova de Gaia": 901,
    "Sintra": 1825,
    "Funchal": 542,
    "Évora": 278
}

# Lista de produtos com respectivas faixas de preço
products = [
    {"produto": "Internet 100 Mbps", "min": 30, "max": 50},
    {"produto": "Internet 200 Mbps", "min": 50, "max": 70},
    {"produto": "Telefone Fixo Ilimitado", "min": 20, "max": 30},
    {"produto": "Pacote TV HD", "min": 25, "max": 40},
    {"produto": "Pacote Mobile Empresarial", "min": 15, "max": 30},
    {"produto": "Pacote Integrado (TV, Internet, Telefone)", "min": 80, "max": 150},
    {"produto": "Cloud", "min": 200, "max": 500},
    {"produto": "Net segura", "min": 100, "max": 300}
]

# Função para gerar uma data aleatória entre duas datas
def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

# Período para a data de assinatura
start_date = datetime(2018, 1, 1)
end_date = datetime(2023, 12, 31)

# Lista para armazenar os dados
data = []
client_id = 1

# Gerar os registros para cada cidade conforme a distribuição
for city, count in cities_distribution.items():
    for _ in range(count):
        nome = f"Cliente_{client_id}"
        prod = random.choice(products)
        produto_nome = prod["produto"]
        valor = round(random.uniform(prod["min"], prod["max"]), 2)
        data_assinatura = random_date(start_date, end_date).strftime("%Y-%m-%d")
        
        data.append({
            "ClienteID": client_id,
            "Nome": nome.strip(),
            "Cidade": city.strip(),
            "Produto": produto_nome.strip(),
            "Valor_Euro": valor,
            "Data": data_assinatura
        })
        client_id += 1

# Criar DataFrame
clientes_df = pd.DataFrame(data)

# Criar tabelas de dimensão
dim_cidades = clientes_df[['Cidade']].drop_duplicates().reset_index(drop=True)
dim_cidades['CidadeID'] = dim_cidades.index + 1
dim_cidades['Cidade'] = dim_cidades['Cidade'].str.strip()  # Remover espaços extras

dim_produtos = clientes_df[['Produto']].drop_duplicates().reset_index(drop=True)
dim_produtos['ProdutoID'] = dim_produtos.index + 1
dim_produtos['Produto'] = dim_produtos['Produto'].str.strip()  # Remover espaços extras

dim_clientes = clientes_df[['ClienteID', 'Nome']].drop_duplicates().reset_index(drop=True)
dim_clientes['Nome'] = dim_clientes['Nome'].str.strip()  # Remover espaços extras

# Criar tabela de fatos
fato_vendas = clientes_df.merge(dim_cidades, on='Cidade', how='left') \
                        .merge(dim_produtos, on='Produto', how='left') \
                        .drop(columns=['Nome', 'Cidade', 'Produto'])

# Adicionar coluna Ano_Mes
fato_vendas["Ano_Mes"] = fato_vendas["Data"].str[:7]

# Garantir que as colunas de ID sejam inteiros e valores numéricos estejam corretos
dim_cidades['CidadeID'] = dim_cidades['CidadeID'].astype(int)
dim_produtos['ProdutoID'] = dim_produtos['ProdutoID'].astype(int)
fato_vendas['Valor_Euro'] = fato_vendas['Valor_Euro'].apply(pd.to_numeric, errors='coerce')

# Salvar os arquivos CSV com a codificação UTF-8 e sem espaços extras
dim_cidades.to_csv("dim_cidades.csv", index=False, encoding='utf-8', sep=',')
dim_produtos.to_csv("dim_produtos.csv", index=False, encoding='utf-8', sep=',')
dim_clientes.to_csv("dim_clientes.csv", index=False, encoding='utf-8', sep=',')
fato_vendas.to_csv("fato_vendas.csv", index=False, encoding='utf-8', sep=',')

print("Arquivos CSV gerados com sucesso!")
