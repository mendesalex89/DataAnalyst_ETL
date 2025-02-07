# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Semente para reprodutibilidade
random.seed(42)
np.random.seed(42)

# Distribuição aproximada de clientes por cidade (valores ajustados para totalizar 10.000)
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

# Lista de produtos com respectivas faixas de preço (valores em euros)
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

# Período para a data de assinatura (de 01/01/2018 até 31/12/2023)
start_date = datetime(2018, 1, 1)
end_date = datetime(2023, 12, 31)

# Lista para armazenar os dados
data = []
client_id = 1

# Gerar os registros para cada cidade conforme a distribuição
for city, count in cities_distribution.items():
    for _ in range(count):
        nome = f"Cliente_{client_id}"
        # Seleciona aleatoriamente um produto e define seu preço
        prod = random.choice(products)
        produto_nome = prod["produto"]
        valor = round(random.uniform(prod["min"], prod["max"]), 2)
        data_assinatura = random_date(start_date, end_date).strftime("%Y-%m-%d")
        
        data.append({
            "ClienteID": client_id,
            "Nome": nome,
            "Cidade": city,
            "Produto": produto_nome,
            "Valor_Euro": valor,
            "Data_Assinatura": data_assinatura
        })
        client_id += 1

# Criação do DataFrame com os dados gerados
df = pd.DataFrame(data)

# Embaralha os registros para não manter agrupamento por cidade
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Salva o dataset em um arquivo CSV
df.to_csv("clientes_altice.csv", index=False)
print("CSV 'clientes_altice.csv' gerado com sucesso!")
