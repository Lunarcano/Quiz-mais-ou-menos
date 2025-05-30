# Conectando Banco de Dados
import pandas as pd
arquivo = 'Quiz-main\Resources\world_imdb_movies_top_movies_per_year.csv'
df = pd.read_csv(arquivo, sep=',', header = 0)

import sqlite3

con = sqlite3.connect('imdb.db') # Criando o banco de dados com o nome "imdb"
con.row_factory = sqlite3.Row
df.to_sql('movies', con, if_exists='replace', index=False)
rows = con.execute('SELECT * FROM movies LIMIT 2').fetchall()

for row in rows:
     print(dict(row))
     print(row['year'])

con.close()

import customtkinter as ctk
import random

# Inicialização do app
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("400x400")
app.title("Mais ou Menos?")

# Dados do quiz
perguntas = [
    {"pergunta": "Ano de lançamento?1", "opcoes": ["2000", "2023"], "correta": "2023"},
    {"pergunta": "Ano de lançamento?2", "opcoes": ["2023", "2001"], "correta": "2001"},
    {"pergunta": "Ano de lançamento?3", "opcoes": ["2001", "2010"], "correta": "2001"},
]
random.shuffle(perguntas)

indice_pergunta = 0
pontuacao = 0

def salvar_score():
    pontuacao_label.configure(text=f"Pontuação salva: {pontuacao}")
    botao_salvar.configure(state="disabled")

def carregar_pergunta():
    global indice_pergunta
    pergunta_atual = perguntas[indice_pergunta]
    pergunta_label.configure(text=pergunta_atual["pergunta"])
    botao_opcao1.configure(text=pergunta_atual["opcoes"][0])
    botao_opcao2.configure(text=pergunta_atual["opcoes"][1])
    pontuacao_label.configure(text=f"Pontuação: {pontuacao}")

def verificar_resposta(opcao_escolhida):
    global indice_pergunta, pontuacao
    correta = perguntas[indice_pergunta]["correta"]
    if opcao_escolhida == correta:
        pontuacao += 1

    indice_pergunta += 1
    if indice_pergunta < len(perguntas):
        carregar_pergunta()
    else:
        pergunta_label.configure(text="Parabéns! Você completou todas as perguntas.")
        botao_opcao1.configure(state="disabled")
        botao_opcao2.configure(state="disabled")
        botao_salvar.pack(pady=(15, 0))

def iniciar_quiz():
    frame_inicial.place_forget()
    frame_quiz.place(relx=0.5, rely=0.5, anchor="center")
    carregar_pergunta()

def menos():
    frame_inicial.place_forget()
    pergunta_label.configure(text="Você escolheu 'Menos'")
    frame_quiz.place(relx=0.5, rely=0.5, anchor="center")

# FRAME INICIAL
frame_inicial = ctk.CTkFrame(app, width=300, height=200)
frame_inicial.place(relx=0.5, rely=0.5, anchor="center")
frame_inicial.pack_propagate(False)

titulo = ctk.CTkLabel(frame_inicial, text="Mais ou Menos?", font=ctk.CTkFont(size=20, weight="bold"))
titulo.pack(pady=10)

botoes_iniciais = ctk.CTkFrame(frame_inicial)
botoes_iniciais.pack(pady=10)

botao_mais = ctk.CTkButton(botoes_iniciais, text="Mais", command=iniciar_quiz)
botao_mais.pack(side="left", padx=10)

botao_menos = ctk.CTkButton(botoes_iniciais, text="Menos", command=menos)
botao_menos.pack(side="left", padx=10)

# FRAME QUIZ
frame_quiz = ctk.CTkFrame(app, width=300, height=250)
frame_quiz.pack_propagate(False)

pergunta_label = ctk.CTkLabel(frame_quiz, text="", wraplength=280, font=ctk.CTkFont(size=16))
pergunta_label.pack(pady=(10, 10))

botoes_opcoes = ctk.CTkFrame(frame_quiz)
botoes_opcoes.pack(pady=5)

botao_opcao1 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao1.cget("text")))
botao_opcao1.pack(side="left", padx=10)

botao_opcao2 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao2.cget("text")))
botao_opcao2.pack(side="left", padx=10)

pontuacao_label = ctk.CTkLabel(frame_quiz, text="Pontuação: 0")
pontuacao_label.pack(pady=(10, 0))

# Botão SALVAR (só aparece ao final)
botao_salvar = ctk.CTkButton(frame_quiz, text="Salvar Pontuação", command=salvar_score)

# Iniciar app
app.mainloop()
