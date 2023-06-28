import requests
import datetime
import sqlite3
import time

# Função para obter o último resultado da API e inserir na tabela
def atualizar_tabela():
    # Obter os dados da API
    response = requests.get('http://api.mxvinvest.com:63000/blaze-crash')
    data = response.json()

    # Obter o último resultado e a data e hora atuais
    ultimo_resultado = data['results'][-1]
    current_datetime = datetime.datetime.now()

    # Conectar-se ao banco de dados SQLite
    conn = sqlite3.connect('dados_crash.db')
    cursor = conn.cursor()

    # Inserir o último resultado do crash na tabela
    cursor.execute("INSERT INTO crash_results (resultado, data_hora) VALUES (?, ?)",
                   (ultimo_resultado, current_datetime))

    # Salvar as alterações no banco de dados
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

# Loop contínuo para atualizar a tabela
while True:
    atualizar_tabela()
    time.sleep(1)  # Esperar 1 segundo antes da próxima atualização
