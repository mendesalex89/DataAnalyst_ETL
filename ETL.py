import pandas as pd
from sqlalchemy import create_engine, text
import urllib

# Função para extrair dados dos arquivos CSV
def extrair_dados(caminhos):
    dfs = {}
    for nome, caminho in caminhos.items():
        dfs[nome] = pd.read_csv(caminho, sep=';')
        print(f"Dados extraídos do arquivo: {caminho}")
    return dfs

# Função para transformar dados
def transformar_dados(dfs):
    # Exemplo de transformação: renomear colunas
    dfs['dim_cidades'] = dfs['dim_cidades'].rename(columns={'id': 'cidade_id'})
    dfs['dim_produtos'] = dfs['dim_produtos'].rename(columns={'id': 'produto_id'})
    dfs['dim_clientes'] = dfs['dim_clientes'].rename(columns={'id': 'cliente_id'})
    dfs['fato_vendas'] = dfs['fato_vendas'].rename(columns={'id': 'venda_id'})

    # Garantir que as colunas de ID estejam no formato correto
    for df in ['dim_cidades', 'dim_produtos', 'dim_clientes', 'fato_vendas']:
        dfs[df] = dfs[df].astype(str)

    return dfs

# Função para carregar dados no SQL Server
def carregar_dados(dfs, conexao_banco, schema):
    params = urllib.parse.quote_plus(conexao_banco)
    engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
    
    with engine.connect() as connection:
        # Remover chaves estrangeiras
        connection.execute(text("ALTER TABLE fato_vendas DROP CONSTRAINT IF EXISTS FK_fato_vendas_dim_cidades"))
        connection.execute(text("ALTER TABLE fato_vendas DROP CONSTRAINT IF EXISTS FK_fato_vendas_dim_produtos"))
        connection.execute(text("ALTER TABLE fato_vendas DROP CONSTRAINT IF EXISTS FK_fato_vendas_dim_clientes"))
        
        for nome, df in dfs.items():
            df.to_sql(nome, con=engine, schema=schema, if_exists='replace', index=False)
            print(f"Dados carregados na tabela: {nome}")
        
        # Adicionar novamente as chaves estrangeiras
        connection.execute(text("""
            ALTER TABLE fato_vendas
            ADD CONSTRAINT FK_fato_vendas_dim_cidades FOREIGN KEY (cidade_id) REFERENCES dim_cidades(cidade_id)
        """))
        connection.execute(text("""
            ALTER TABLE fato_vendas
            ADD CONSTRAINT FK_fato_vendas_dim_produtos FOREIGN KEY (produto_id) REFERENCES dim_produtos(produto_id)
        """))
        connection.execute(text("""
            ALTER TABLE fato_vendas
            ADD CONSTRAINT FK_fato_vendas_dim_clientes FOREIGN KEY (cliente_id) REFERENCES dim_clientes(cliente_id)
        """))

# Caminhos exatos dos arquivos CSV
caminhos = {
    'dim_cidades': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_cidades.csv',
    'dim_produtos': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_produtos.csv',
    'dim_clientes': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_clientes.csv',
    'fato_vendas': r'C:\Users\alexm\Documents\Altice_DataAnalyst\fato_vendas_ajustado.csv'
}

# Conexão com o banco de dados SQL Server (ALEXMENDES)
conexao_banco = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ALEXMENDES;'
    'DATABASE=Altice;'
    'Trusted_Connection=yes;'
    'Connection Timeout=30;'
)
schema = 'dbo'

# Processo ETL
dfs = extrair_dados(caminhos)
dfs = transformar_dados(dfs)
carregar_dados(dfs, conexao_banco, schema)

print("Processo ETL concluído com sucesso!")