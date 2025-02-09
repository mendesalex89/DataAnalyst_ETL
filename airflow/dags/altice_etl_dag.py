from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pyodbc
import pandas as pd

# Configurações do SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ALEXMENDES;"
    "Database=Altice;"
    "Trusted_Connection=yes;"
    "Connection Timeout=30;"
)

# Função para extrair dados do CSV
def extract():
   df = pd.read_csv(r"C:\Users\alexm\Documents\Altice_DataAnalyst\clientes_altice.csv")
    return df

# Função para transformar dados
def transform(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='extract')
    
    # Exemplo de transformação: Padronizar nomes de cidades
    df['Cidade'] = df['Cidade'].str.upper()
    return df

# Função para carregar dados no SQL Server
def load(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='transform')
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Criação da tabela (se não existir)
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Altice' AND xtype='U')
        CREATE TABLE Altice (
            ClienteID INT PRIMARY KEY,
            Nome VARCHAR(100),
            Cidade VARCHAR(100),
            Produto VARCHAR(100),
            Valor_Euro DECIMAL(10, 2),
            Data_Assinatura DATE
        )
    ''')
    
    # Inserção dos dados
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO Altice (ClienteID, Nome, Cidade, Produto, Valor_Euro, Data_Assinatura)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', row['ClienteID'], row['Nome'], row['Cidade'], row['Produto'], row['Valor_Euro'], row['Data_Assinatura'])
    
    conn.commit()
    conn.close()

# Definir o DAG
default_args = {
    'owner': 'Alex',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'altice_etl',
    default_args=default_args,
    description='ETL para dados da Altice',
    schedule_interval=timedelta(days=1),  # Executa diariamente
)

# Definir as tarefas
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    provide_context=True,
    dag=dag,
)

# Ordem das tarefas
extract_task >> transform_task >> load_task

