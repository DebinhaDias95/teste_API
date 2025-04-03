import pandas as pd
import sqlite3
import glob  # Para pegar múltiplos arquivos automaticamente

# Conectar ao banco de dados
conn = sqlite3.connect("dados_operadoras.db")
cursor = conn.cursor()

# Lista de arquivos CSV/Excel que deseja processar (use "*.csv" ou "*.xlsx")
arquivos = glob.glob("C:/Users/My/Desktop/teste-de-nivelamento-teste/arquivos dos ultimos 2 anos da ANS/*.csv")  # Substitua "dados/" pelo diretório correto

# Criar estrutura da tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas_contabeis (
    DATA DATE,
    REG_ANS INTEGER,
    CD_CONTA_CONTABIL TEXT,
    DESCRICAO TEXT,
    VL_SALDO_INICIAL REAL,
    VL_SALDO_FINAL REAL
);
""")
conn.commit()

# Loop pelos arquivos encontrados
for arquivo in arquivos:
    print(f"Processando: {arquivo}")

    # Carregar os dados (suporta CSV e Excel)
    if arquivo.endswith(".csv"):
        df = pd.read_csv(arquivo, delimiter=";", encoding="utf-8")
    elif arquivo.endswith(".xlsx"):
        df = pd.read_excel(arquivo)

    # Renomear colunas para evitar espaços ou caracteres especiais
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # Empilhar os dados no banco de dados
    df.to_sql("contas_contabeis", conn, if_exists="append", index=False)

print("Dados importados com sucesso!")

# Fechar conexão
conn.close()
