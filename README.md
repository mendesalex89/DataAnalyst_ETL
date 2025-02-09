

![alt text](image.png)



# Data Analyst Project - Altice
**Candidato:** Alex Mendes  
**Vaga:** Data Analyst (ETL, SQL, Power BI)  


## 📌 Visão Geral
Projeto de automação ETL e dashboard para a Altice, desenvolvido como parte do processo seletivo para a vaga de Data Analyst. Inclui:
- **ETL automatizado** com Apache Airflow.
- **Dashboard interativo** no Power BI.
- Otimização de consultas SQL e garantia de qualidade dos dados.

## 🛠️ Ferramentas Utilizadas
- **Linguagens:** Python, SQL, DAX
- **Ferramentas:** Apache Airflow, MS SQL Server, Power BI, pyodbc, pandas
- **Ambiente:** Visual Studio Code, SQL Server Management Studio

## 📂 Estrutura do Projeto
📂 Altice_DataAnalyst_Project/
├── 📂 airflow/
│   ├── 📂 dags/                  # Pasta obrigatória para DAGs
│   │   └── 📄 altice_etl_dag.py  # Seu código de ETL
│   ├── 📂 logs/                  # Logs automáticos do Airflow
│   └── 📄 airflow.cfg            # Arquivo de configuração
├── 📂 data/
│   └── 📄 clientes_altice.csv    # Dados brutos
└── 📂 powerbi/
    └── 📄 Altice_Dashboard.pbix  # Arquivo do Power BI

