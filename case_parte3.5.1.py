import sqlite3
import pandas as pd
import unicodedata

# Função para remover acentos
def remover_acentos(texto):
    if texto is None:
        return None
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c)).lower()

# Conectar ao banco de dados
conn = sqlite3.connect("dados_operadoras.db")

# Query para pegar os dados com transformação de acentos
query_trimestre = """
SELECT 
    REG_ANS,
    SUM(VL_SALDO_FINAL) AS total_despesas
FROM contas_contabeis
WHERE DESCRICAO LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
AND DATA >= DATE((SELECT MAX(DATA) FROM contas_contabeis), '-3 months')
GROUP BY REG_ANS
ORDER BY total_despesas DESC
LIMIT 10;
"""

# Pegar os dados da consulta
df_trimestre = pd.read_sql_query(query_trimestre, conn)

# Aplicar a remoção de acentos nos resultados (caso necessário)
df_trimestre["REG_ANS"] = df_trimestre["REG_ANS"].astype(str).apply(remover_acentos)

print("\nTop 10 Operadoras com Maiores Despesas no Último Trimestre:")
print(df_trimestre)

# Query para o último ano
query_ano = """
SELECT 
    REG_ANS,
    SUM(VL_SALDO_FINAL) AS total_despesas
FROM contas_contabeis
WHERE DESCRICAO LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
AND DATA >= DATE((SELECT MAX(DATA) FROM contas_contabeis), '-12 months')
GROUP BY REG_ANS
ORDER BY total_despesas DESC
LIMIT 10;
"""

# Pegar os dados da consulta
df_ano = pd.read_sql_query(query_ano, conn)

# Aplicar remoção de acentos (caso necessário)
df_ano["REG_ANS"] = df_ano["REG_ANS"].astype(str).apply(remover_acentos)

print("\nTop 10 Operadoras com Maiores Despesas no Último Ano:")
print(df_ano)

# Fechar conexão com o banco
conn.close()
