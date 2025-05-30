# Conectando Banco de Dados
import pandas as pd
arquivo = 'Quiz-main\Resources\world_imdb_movies_top_movies_per_year.csv'
df = pd.read_csv(arquivo, sep=',', header = 0)

import sqlite3

con = sqlite3.connect('imdb.db') # Criando o banco de dados com o nome "imdb"
con.row_factory = sqlite3.Row
df.to_sql('movies', con, if_exists='replace', index=False)
rows = con.execute('SELECT * FROM movies LIMIT 5').fetchall()

for row in rows:
     print(dict(row))
     print(row['year'])

con.close()

import customtkinter