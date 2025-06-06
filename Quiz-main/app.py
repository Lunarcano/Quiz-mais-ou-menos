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
# ---------------------------- IMPORTAÇÕES ------------------------------------#
import customtkinter as ctk 
import random
import json
import os 

# --------------------------- CONFIGURAÇÕES -----------------------------------#
ctk.set_appearance_mode("System")# APARÊNCIA (CLARO/ESCURO)
app = ctk.CTk()# JANELA
app.geometry("900x900")# TAMANHO JANELA
app.title("Mais ou Menos?")# TITULO

# ------------------------------- VARIÁVEIS -----------------------------------#
indice_pergunta = 0
pontuacao = 0
vidas = 3 #TOTAL DE TENTATIVAS
usuarios = []
botoes_usuarios = []
usuario_selecionado = None

#--------------------------- PERGUNTAS COM RESPOSTAS---------------------------#
perguntas = [ 
    {"pergunta": "Ano de lançamento mais recente?1", "opcoes": ["Senhor dos Anéis", "Matilda"], "correta": "Matilda"},
    {"pergunta": "Ano de lançamento mais recente?2", "opcoes": ["Orgulho e preconceito", "Pânico"], "correta": "Orgulho e preconceito"},
    {"pergunta": "Ano de lançamento mais recente?3", "opcoes": ["Norbite", "As Branquelas"], "correta": "Norbite"},
    {"pergunta": "Ano de lançamento mais recente?4", "opcoes": ["Meninas malvadas", "Jumanji"], "correta": "Jumanji"},
]
# ----------------------------- INICIAR JOGO ----------------------------------#
def iniciar_quiz():
    global indice_pergunta, pontuacao, vidas
    indice_pergunta = 0
    pontuacao = 0
    vidas = 3
    random.shuffle(perguntas)
    pontuacao_label.configure(text=f"Pontuação: {pontuacao} | Vidas {vidas}")
    tabela.place_forget()
    frame_usuario.place_forget()
    frame_inicial.place_forget()
    frame_quiz.place(relx=0.5, rely=0.5, anchor="center")
    carregar_pergunta()

#------------------------------ PERGUNTA ATUAL --------------------------------#
def carregar_pergunta(): 
    global indice_pergunta
    pergunta_atual = perguntas[indice_pergunta]
    pergunta_label.configure(text=pergunta_atual['pergunta'])# PERGUNTA
    botao_opcao1.configure(text=pergunta_atual["opcoes"][0])# BOTÃO PRIMEIRA OPÇÃO  
    botao_opcao2.configure(text=pergunta_atual["opcoes"][1])# BOTÃO SEGUNDA OPÇÃO    

#---------------------------- VERIFICAR RESPOSTA-------------------------------#
def verificar_resposta(opcao_escolhida): 
    global indice_pergunta, pontuacao, vidas 
    correta = perguntas[indice_pergunta]["correta"]
    # SE ACERTAR
    if opcao_escolhida == correta:
        pontuacao += 1 # AUMENTA PONTUAÇÃO
    # SE ERRAR
    else:
        vidas -= 1 # PERDE VIDA
    pontuacao_label.configure(text=f"Pontuação: {pontuacao} | Vidas {vidas}")
    # SE AINDA TIVER VIDA
    if vidas > 0:
        indice_pergunta += 1
        if indice_pergunta < len(perguntas):
            carregar_pergunta()
        else:
            finalizar_quiz("Parabéns! Você completou todas as perguntas.")
    # SE NÃO TIVER VIDA
    else:
        finalizar_quiz("Fim de jogo! Você não tem mais vidas.")

#------------------------------ FINAL DO JOGO ---------------------------------#
def finalizar_quiz(mensagem):
    frame_quiz.place_forget()
    entrada_nome_label.configure(text=mensagem + "\nDigite seu nome e email:")
    frame_usuario.place(relx=0.5, rely=0.5, anchor="center")
    botao_salvar.pack(pady=10)

#------------------------------ SALVA PONTUAÇÃO--------------------------------#
def salvar_score():
    pontuacao_label.configure(text=f"Pontuação salva: {pontuacao}")
    botao_salvar.configure(state="disabled")

# ------------------------=----- SALVAR USUÁRIO -------=-----------------------#
def salvar_usuario():
    nome = entrada_nome.get().strip()
    email = entrada_email.get().strip()
    if nome and email:
        usuarios.append({"nome": nome, "email": email, "pontuacao": pontuacao})
        salvar_dados()
        entrada_nome.delete(0, "end")
        entrada_email.delete(0, "end")
        frame_usuario.place_forget()
        atualizar_tabela()
        tabela.place(relx=0.5, rely=0.5, anchor="center")

#---------------------------- ATUALIZAR RANKING -------------------------------#
def atualizar_tabela():
    global usuario_selecionado, botoes_usuarios
    usuario_selecionado = None
    botoes_usuarios = []
    for widget in tabela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(tabela, text="Usuários cadastrados", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    usuarios_ordenados = sorted(usuarios, key=lambda x: x["pontuacao"], reverse=True)

    for i, user in enumerate(usuarios_ordenados): #EM ORDEM DECRECENTE
        texto = f"{user['nome']} | {user['email']} | Pontuação: {user['pontuacao']}"
        botao = ctk.CTkButton(
            tabela, text=texto, font=ctk.CTkFont(size=14),
            fg_color="#DDD",# COR DE FUNDO
            hover_color="#CCC",# COR COM MAUSE
            text_color="black",# COR TEXTO
            anchor="w", width=500,
            command=lambda i=i: selecionar_usuario(i)
        )
        botao.pack(pady=2)
        botoes_usuarios.append(botao)
    # BOTÕES (EDITAR, DELETAR E JOGAR)
    botoes_acao = ctk.CTkFrame(tabela)
    botoes_acao.pack(pady=10)
    ctk.CTkButton(botoes_acao, text="Editar Selecionado", width=140, fg_color="black", command=editar_usuario_selecionado).pack(side="left", padx=5)
    ctk.CTkButton(botoes_acao, text="Deletar Selecionado", width=140, fg_color="black", command=deletar_usuario_selecionado).pack(side="left", padx=5)
    ctk.CTkButton(tabela, text="Jogar", fg_color="black", hover_color="#333", command=voltar_ao_inicio).pack(pady=10)

#--------------------------- SELECIONAR USUÁRIO --------------------------------#
def selecionar_usuario(indice):
    global usuario_selecionado
    usuario_selecionado = indice
    for i, botao in enumerate(botoes_usuarios):
        botao.configure(fg_color="#999"# CINZA ESCURO PARA SELECIONADO
    if i == indice else "#DDD")# CINZA CLARO PARA OS OUTROS

#-------------------------------- EDITAR ---------------------------------------#
def editar_usuario_selecionado():
    if usuario_selecionado is not None:
        editar_usuario(usuario_selecionado)

#-------------------------------- DELETAR --------------------------------------#
def deletar_usuario_selecionado():
    if usuario_selecionado is not None:
        deletar_usuario(usuario_selecionado)

#-------------------------- INTERFACE DE EDIÇÃO --------------------------------#
def editar_usuario(indice):
    user = usuarios[indice]
    entrada_nome.delete(0, "end")
    entrada_email.delete(0, "end")
    entrada_nome.insert(0, user['nome'])
    entrada_email.insert(0, user['email'])
    tabela.place_forget()
    frame_usuario.place(relx=0.5, rely=0.5, anchor="center")
    usuarios.pop(indice)# REMOVE PRA DEPOIS SALVAR COMO NOVO

#---------------------------------- EXCLUI -------------------------------------#
def deletar_usuario(indice):
    usuarios.pop(indice)
    salvar_dados()
    atualizar_tabela()

#--==------------------------------ RANKING ------------------------------------#
def mostrar_ranking():
    frame_inicial.place_forget()
    atualizar_tabela()
    tabela.place(relx=0.5, rely=0.5, anchor="center")

#----------------------- VOLTAR PARA O MENU INICIAL ----------------------------#
def voltar_ao_inicio():
    tabela.place_forget()
    frame_usuario.place_forget()
    frame_quiz.place_forget()
    frame_inicial.place(relx=0.5, rely=0.5, anchor="center")

# --------------------------- ARQUIVO USUARIOS ---------------------------------#

def salvar_dados():
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f)

def carregar_dados():
    global usuarios
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)

# -------------------------- FRAME E BOTÕES INICIAL ----------------------------#

frame_inicial = ctk.CTkFrame(app, width=400, height=400)
frame_inicial.place(relx=0.5, rely=0.5, anchor="center")
frame_inicial.pack_propagate(False)

#TITULO
titulo = ctk.CTkLabel(frame_inicial, text="Mais ou Menos?", font=ctk.CTkFont(size=20, weight="bold"))
titulo.pack(pady=10)

#BOTÕES
botoes_iniciais = ctk.CTkFrame(frame_inicial)
botoes_iniciais.pack(pady=10)

botao_iniciar = ctk.CTkButton(botoes_iniciais, text="Iniciar", command=iniciar_quiz, fg_color="black", hover_color="#333")
botao_iniciar.pack(side="left", padx=10)

#RANKING
botao_ranking = ctk.CTkButton(botoes_iniciais, text="Ranking", command=mostrar_ranking, fg_color="black", hover_color="#333")
botao_ranking.pack(side="left", padx=10)

#---------------------------- FRAME E BOTÕES JOGO ------------------------------#
frame_quiz = ctk.CTkFrame(app, width=300, height=250)
frame_quiz.pack_propagate(False)

#PERGUNTA
pergunta_label = ctk.CTkLabel(frame_quiz, text="", wraplength=280, font=ctk.CTkFont(size=16))
pergunta_label.pack(pady=(10, 10))

#BOTÕES
botoes_opcoes = ctk.CTkFrame(frame_quiz)
botoes_opcoes.pack(pady=5)

botao_opcao1 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao1.cget("text")), fg_color="black", hover_color="#333")
botao_opcao1.pack(side="left", padx=10)

botao_opcao2 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao2.cget("text")), fg_color="black", hover_color="#333")
botao_opcao2.pack(side="left", padx=10)

#PONTUAÇÃO E VIDA
pontuacao_label = ctk.CTkLabel(frame_quiz, text="Pontuação: 0 | Vidas 3")
pontuacao_label.pack(pady=(10, 0))

#-------------------------------- FRAME USUARIO -------------------------------#
frame_usuario = ctk.CTkFrame(app)

entrada_nome_label = ctk.CTkLabel(frame_usuario, text="Digite seu nome e email:", font=ctk.CTkFont(size=16))
entrada_nome_label.pack(pady=(10, 5))

entrada_nome = ctk.CTkEntry(frame_usuario, placeholder_text="Nome", width=300, font=ctk.CTkFont(size=14))
entrada_nome.pack(pady=5)

entrada_email = ctk.CTkEntry(frame_usuario, placeholder_text="Email", width=300, font=ctk.CTkFont(size=14))
entrada_email.pack(pady=5)

botao_salvar = ctk.CTkButton(frame_usuario, text="Salvar Pontuação", command=salvar_usuario, fg_color="black", hover_color="#333")

# -------------------------------- EXECUÇÃO -----------------------------------#
tabela = ctk.CTkFrame(app)
carregar_dados()
app.mainloop()
