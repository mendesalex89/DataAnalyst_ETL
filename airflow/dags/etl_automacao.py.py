from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text
import urllib

# Função para extrair dados dos arquivos CSV
def extrair_dados():
    caminhos = {
        'dim_cidades': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_cidades.csv',
        'dim_produtos': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_produtos.csv',
        'dim_clientes': r'C:\Users\alexm\Documents\Altice_DataAnalyst\dim_clientes.csv',
        'fato_vendas': r'C:\Users\alexm\Documents\Altice_DataAnalyst\fato_vendas_ajustado.csv'
    }
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

    print("Transformação de dados concluída")
    return dfs

# Função para carregar dados no SQL Server
def carregar_dados(dfs):
    conexao_banco = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=ALEXMENDES;"
        "Database=Altice;"
        "Trusted_Connection=yes;"
    )
    params = urllib.parse.quote_plus(conexao_banco)
    engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
    schema = 'dbo'
    for nome, df in dfs.items():
        df.to_sql(nome, con=engine, schema=schema, if_exists='replace', index=False)
        print(f"Dados carregados na tabela: {nome}")

# Configurar o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_automacao',
    default_args=default_args,
    description='DAG para automatizar o processo ETL',
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id='extrair_dados',
    python_callable=extrair_dados,
    dag=dag,
)

t2 = PythonOperator(
    task_id='transformar_dados',
    python_callable=lambda: transformar_dados(t1.output),
    dag=dag,
)

t3 = PythonOperator(
    task_id='carregar_dados',
    python_callable=lambda: carregar_dados(t2.output),
    dag=dag,
)

t1 >> t2 >> t3
