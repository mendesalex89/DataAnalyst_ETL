import csv
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Dados das cidades
cidades = {
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

# Produtos
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

# Gerar clientes
clientes = []
for cidade, total in cidades.items():
    for _ in range(total):
        clientes.append({
            "cliente_id": fake.uuid4(),
            "nome": fake.name(),
            "cidade": cidade
        })

# Gerar vendas
vendas = []
start_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
end_date = datetime.strptime('09/02/2025', '%d/%m/%Y')

for cliente in clientes:
    for _ in range(random.randint(1, 5)):
        produto = random.choice(products)
        data_venda = fake.date_between(start_date=start_date, end_date=end_date)
        vendas.append({
            "cliente_id": cliente["cliente_id"],
            "produto": produto["produto"],
            "preco": f"€{random.uniform(produto['min'], produto['max']):.2f}",
            "data": data_venda.strftime('%d/%m/%Y')
        })

# Criar DataFrames
df_cidades = pd.DataFrame(cidades.items(), columns=["cidade", "populacao"])
df_produtos = pd.DataFrame(products)
df_clientes = pd.DataFrame(clientes)
df_vendas = pd.DataFrame(vendas)

# Exportar para CSV
df_cidades.to_csv('dim_cidades.csv', index=False, sep=';', encoding='utf-8-sig')
df_produtos.to_csv('dim_produtos.csv', index=False, sep=';', encoding='utf-8-sig')
df_clientes.to_csv('dim_clientes.csv', index=False, sep=';', encoding='utf-8-sig')
df_vendas.to_csv('fato_vendas.csv', index=False, sep=';', encoding='utf-8-sig')
