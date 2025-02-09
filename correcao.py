import pandas as pd

# Lista de arquivos CSV
arquivos = {
    "fato_vendas": r"C:\Users\alexm\Documents\Altice_DataAnalyst\fato_vendas.csv",
    "dim_clientes": r"C:\Users\alexm\Documents\Altice_DataAnalyst\dim_clientes.csv",
    "dim_cidades": r"C:\Users\alexm\Documents\Altice_DataAnalyst\dim_cidades.csv",
    "dim_produtos": r"C:\Users\alexm\Documents\Altice_DataAnalyst\dim_produtos.csv"
}

# Função para corrigir e salvar os CSVs
def corrigir_csv(nome, caminho):
    try:
        df = pd.read_csv(caminho, dtype=str)  # Ler como string para evitar problemas
        df = df.apply(lambda x: x.str.strip())  # Remover espaços extras
        novo_caminho = caminho.replace(".csv", "_corrigido.csv")  # Novo arquivo
        df.to_csv(novo_caminho, index=False, encoding="utf-8")
        print(f"{nome} corrigido e salvo em: {novo_caminho}")
    except Exception as e:
        print(f"Erro ao processar {nome}: {e}")

# Processar todos os arquivos
for nome, caminho in arquivos.items():
    corrigir_csv(nome, caminho)
 