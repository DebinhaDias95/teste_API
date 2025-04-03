# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Carregar o CSV com as operadoras
csv_path = "C:/Users/My/Desktop/teste-de-nivelamento-teste/Relatorio_cadop.csv"  
df = pd.read_csv('C:/Users/My/Desktop/teste-de-nivelamento-teste/Relatorio_cadop.csv ', delimiter=';', low_memory=False)

# Rota para buscar operadoras
@app.route('/', methods=['GET'])
def search(csv_path="default.csv"):
    query = request.args.get('query', '')  # Recebe a busca do usuário
    if query:
        # Realiza a busca no DataFrame
        results = df[df['nome'].str.contains(query, case=False, na=False)]
    else:
        # Se não houver consulta, retorna tudo
        results = df

    # Formatar o resultado como uma lista de dicionários
    results_list = results.to_dict(orient='records')
    
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)


