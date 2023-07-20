import pandas as pd
import sqlite3
from fbprophet import Prophet

# Conectar ao banco de dados
conn = sqlite3.connect('crash.db')  # Substitua pelo nome do seu banco de dados

# Query para selecionar apenas os valores acima de 100
query = "SELECT * FROM crash WHERE crash_point > 100"

# Carregar os dados do banco de dados para um DataFrame
df = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Renomear as colunas para atender ao formato exigido pelo Prophet
df.rename(columns={'created_at': 'ds', 'crash_point': 'y'}, inplace=True)

# Criar e ajustar o modelo Prophet
model = Prophet()
model.fit(df)

# Criar um DataFrame com as datas futuras para prever
horarios_futuros = model.make_future_dataframe(periods=10, freq='T')  # Prever os próximos 10 horários (a cada minuto)
previsao = model.predict(horarios_futuros)

# Filtrar apenas os horários com valores acima de 100
previsao_acima_100 = previsao[previsao['yhat'] > 100]

# Exibir os horários previstos acima de 100
print(previsao_acima_100[['ds', 'yhat']])
