# ---------------------------- IMPORTANDO AS BIBLIOTECAS ------------------------ #
import sqlite3
import random
import json
import os
import re
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# ---------------------- BANCO DE DADOS QUIZ ------------------------------------ #
BASE_DE_DADOS = 'quiz.db'

def conectar_banco():
    try:
        conn = sqlite3.connect(BASE_DE_DADOS)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta_texto TEXT NOT NULL,
                filme_a TEXT NOT NULL,
                filme_b TEXT NOT NULL,
                resposta_correta TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return None

def atualizar_perguntas(conn, sobrescrever=False):
    cursor = conn.cursor()

    perguntas_novas = [
        ("Ano de lançamento mais recente?", "Senhor dos Anéis", "Matilda", "Matilda"),
        ("Ano de lançamento mais recente?", "Orgulho e Preconceito", "Pânico", "Orgulho e Preconceito"),
        ("Ano de lançamento mais recente?", "Norbit", "As Branquelas", "Norbit"),
        ("Ano de lançamento mais antigo?", "Meninas Malvadas", "Jumanji", "Meninas Malvadas"),
        ("Ano de lançamento mais antigo?", "Shrek", "De Repente 30", "Shrek"),
        ("Ano de lançamento mais antigo?", "O Pequenino", "Ponyo: Uma Amizade que Veio do Mar", "O Pequenino"),
        ("Qual filme foi mais indicado para premiações?", "Marcas da Maldição", "As Patricinhas de Beverly Hills", "Marcas da Maldição"),
        ("Qual filme foi mais indicado para premiações?", "O Poço", "Meninas Malvadas", "Meninas Malvadas"),
        ("Qual filme foi mais indicado para premiações?", "Nosferatu: O vampiro da noite", "Gasparzinho, o Fantasminha Camarada", "Nosferatu: O vampiro da noite"),
        ("Qual filme foi menos indicado para premiações?", "Jogos Vorazes", "Star Wars: Episódio I - A Ameaça Fantasma", "Jogos Vorazes"),
        ("Qual filme foi menos indicado para premiações?", "O Máskara", "Clube da Luta", "O Máskara"),
        ("Qual filme foi menos indicado para premiações?", "V de Vingaça", "O Espetacular Homem-Aranha", "O Espetacular Homem-Aranha"),
        ("Qual filme recebeu mais OSCARS?", "Barbie", "Star Wars: Episódio I - A Ameaça Fantasma", "Barbie"),
        ("Qual filme recebeu mais OSCARS?", "Orgulho e Preconceito ", "Shrek", "Shrek"),
        ("Qual filme recebeu mais OSCARS?", "O Senhor dos Anéis: A Sociedade do Anel", "Corra!", "O Senhor dos Anéis: A Sociedade do Anel"),
        ("Qual filme recebeu menos OSCARS?", "Interestelar", "O Exorcista", "Interestelar"),
        ("Qual filme recebeu menos OSCARS?", "Matrix", "Batman: O Cavaleiro das Trevas", "Batman: O Cavaleiro das Trevas"),
        ("Qual filme recebeu menos OSCARS?", "Jurassic Park: O Parque dos Dinossauros", "Alien, o 8º Passageiro", "Alien, o 8º Passageiro"),
        ("Qual filme tem a maior nota no IMDb?", "Os Caça-Fantasmas", "Como Eu Era Antes de Você ", "Os Caça-Fantasmas"),
        ("Qual filme tem a maior nota no IMDb?", "O Melhor Amiga da Noiva ", "Kung Fu Panda", "Kung Fu Panda"),
        ("Qual filme tem a maior nota no IMDb?", "Harry Potter e a Pedra Filosofal", "Clube da Luta", "Clube da Luta"),
        ("Qual filme tem a maior nota no IMDb?", "50 tons de cinza", "A Hora do Pesadelo 6: Pesadelo Final", "A Hora do Pesadelo 6: Pesadelo Final"),
        ("Qual filme tem a maior nota no IMDb?", "Alien vs. Predador", "Sharknado", "Alien vs. Predador"),
        ("Qual filme tem a menor nota no IMDb?", "Amnésia", "Os Vingadores", "Os Vingadores"),
        ("Qual filme tem a menor nota no IMDb?", "O Estranho Mundo de Jack", "Coraline e o Mundo Secreto", "Coraline e o Mundo Secreto"),
        ("Qual filme tem a menor nota no IMDb?", "Karatê Kid", "Zathura: Uma Aventura Espacial", "Karatê Kid"),
        ("Qual filme tem a menor nota no IMDb?", "Matrix", "Pânico", "ânico"),
        ("Qual filme tem a menor nota no IMDb?", "Barbie", "V de Vingaça", "Barbie"),
        ("Qual filme tem a menor nota no IMDb?", "O Exorcista", "As Patricinhas de Beverly Hills", "As Patricinhas de Beverly Hills"),
        ("Qual filme tem o maior tempo de duração?", "Alien, o 8º Passageiro", "Maze Runner: Correr ou Morrer", "Alien, o 8º Passageiro"),
        ("Qual filme tem o maior tempo de duração?", "Matrix", "O Senhor dos Anéis: A Sociedade do Anel", "O Senhor dos Anéis: A Sociedade do Anel"),
        ("Qual filme tem o maior tempo de duração?", "Alvin e os Esquilos", "Segurança de Shopping", "Alvin e os Esquilos"),
        ("Qual filme tem o maior tempo de duração?", "A Casa Monstro", "Uma Noite no Museu", "Uma Noite no Museu"),
        ("Qual filme tem o menor tempo de duração?", "A Noiva-Cadáver", "O Espetacular Homem-Aranha", "A Noiva-Cadáver"),
        ("Qual filme tem o menor tempo de duração?", "As Aventuras de Sharkboy e Lavagirl", "Gasparzinho, o Fantasminha Camarada", "As Aventuras de Sharkboy e Lavagirl"),
        ("Qual filme tem o menor tempo de duração?", "O Poço", "Meninas Malvadas", "O Poço"),
        ("Qual filme tem o menor tempo de duração?", "Jogos Vorazes", "50 tons de cinza", "50 tons de cinza"),
            
    ]

    if sobrescrever:
        cursor.execute("DELETE FROM perguntas")
        conn.commit()

    # Verifica quais perguntas já existem
    cursor.execute("SELECT pergunta_texto FROM perguntas")
    existentes = set(row[0] for row in cursor.fetchall())

    novas_para_inserir = [
        pergunta for pergunta in perguntas_novas if pergunta[0] not in existentes
    ]

    if novas_para_inserir:
        cursor.executemany('''
            INSERT INTO perguntas (pergunta_texto, filme_a, filme_b, resposta_correta)
            VALUES (?, ?, ?, ?)
        ''', novas_para_inserir)
        conn.commit()


# --------------------------- CONFIGURAÇÕES -----------------------------------#
ctk.set_appearance_mode("light")  # Modo claro
janela = ctk.CTk()
janela.geometry("600x600")
janela.configure(fg_color="white")
janela.title("Quiz Mais ou Menos")

# ------------------------------- VARIÁVEIS -----------------------------------#
indice_pergunta = 0
pontuacao = 0
vidas = 3 #TOTAL DE TENTATIVAS
usuarios = []
botoes_usuarios = []
usuario_selecionado = None
perguntas = []

#CARREGAR PERGUNTA
def carregar_perguntas(conn):
    global perguntas
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta_texto, filme_a, filme_b, resposta_correta FROM perguntas")
    resultado = cursor.fetchall()

    perguntas = []
    for texto, a, b, correta in resultado:
        perguntas.append({
            "pergunta": texto,
            "opcoes": [a, b],
            "correta": correta
        })

    random.shuffle(perguntas)

conn = conectar_banco()
if conn:
    atualizar_perguntas(conn, sobrescrever=True)  # True = apaga tudo e adiciona
    # atualizar_perguntas(conn, sobrescrever=False)  # False = adiciona apenas novas
print(perguntas)
#-------------------------------- ICONES ---------------------------------------#
# ICONE COMO JOGAR
img_como_jogar = Image.open(r"C:Quiz-main\resources\como_jogar.png").resize((32, 32))
img_como_jogar_tk = ctk.CTkImage(img_como_jogar, size=(32,32))

#ICONE DO JOGO
def mostrar_icone():
    icone_label.place(relx=0.5, y=70, anchor="n")

def esconder_icone():
    icone_label.place_forget()
    
# ICONE DAS VIDAS
img_cheio = Image.open(r"C:Quiz-main\resources\coracao_cheio.png").resize((32, 32))
img_vazio = Image.open(r"C:Quiz-main\resources\coracao_vazio.png").resize((26, 26))
img_cheio_tk = ctk.CTkImage(img_cheio, size=(32,32))
img_vazio_tk = ctk.CTkImage(img_vazio, size=(26,26))

#------------------------------- ATUALIZAR VIDAS ------------------------------#
def atualizar_vidas():
    # LIMPA VIDA ANTIGA
    for widget in frame_vidas.winfo_children():
        widget.destroy()

    # COLOCA VIDA NOVA
    for i in range(3):
        img = img_cheio_tk if i < vidas else img_vazio_tk
        label = ctk.CTkLabel(frame_vidas, image=img, text="")
        label.pack(side="left", padx=2)
        vidas_imagens.append(label)

# ----------------------------- INICIAR JOGO ----------------------------------#
def iniciar_quiz():
    global indice_pergunta, pontuacao, vidas
    indice_pergunta = 0
    pontuacao = 0
    vidas = 3
    carregar_perguntas(conn)
    pontuacao_label.configure(text=f"Pontuação: {pontuacao}")
    tabela.place_forget()
    frame_usuario.place_forget()
    frame_inicial.place_forget()
    frame_quiz.place(relx=0.5, rely=0.7, anchor="center")
    frame_vidas.place(relx=0.98, rely=0.02, anchor="ne")  # REAPARE VIDAS
    botao_como_jogar.place_forget()
    carregar_pergunta()
    atualizar_vidas()
    mostrar_icone()

#--------------------------------- COMO JOGAR --------------------------------#
def mostrar_como_jogar():
    frame_inicial.place_forget()
    tabela.place_forget()
    frame_usuario.place_forget()
    frame_quiz.place_forget()
    frame_como_jogar.place(relx=0.5, rely=0.5, anchor="center")
    botao_como_jogar.place_forget()
    esconder_icone()
    
#------------------------------- DESISTIR DE JOGAR ---------------------------#
def desistir():
    global pontos, vidas
    pontos = 0
    vidas = 3
    frame_quiz.place_forget()
    frame_vidas.place_forget()
    voltar_ao_inicio()

#------------------------------ PERGUNTA ATUAL --------------------------------#
def carregar_pergunta(): 
    global indice_pergunta
    if indice_pergunta < len(perguntas):
        pergunta_atual = perguntas[indice_pergunta]
        pergunta_label.configure(text=pergunta_atual['pergunta'])  # Corrige a chave
        botao_opcao1.configure(text=pergunta_atual["opcoes"][0])   # Corrige acesso à lista
        botao_opcao2.configure(text=pergunta_atual["opcoes"][1])   # Corrige acesso à lista

    
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
        atualizar_vidas()
    pontuacao_label.configure(text=f"Pontuação: {pontuacao}")
    # SE AINDA TIVER VIDA
    if vidas > 0:
        indice_pergunta += 1
        if indice_pergunta < len(perguntas):
            carregar_pergunta()
        else:
            finalizar_quiz("Obrigado por jogar!\n")
    # SE NÃO TIVER VIDA
    else:
        finalizar_quiz("Você não tem mais vidas :(\n")

#------------------------------ FINAL DO JOGO ---------------------------------#
def finalizar_quiz(mensagem):
    frame_quiz.place_forget()
    frame_vidas.place_forget()  # ESCONDE VIDAS
    entrada_nome_label.configure(text=mensagem + "\nSalve sua pontuação\nDigite seu nome e email:")
    frame_usuario.place(relx=0.5, rely=0.6, anchor="center")
    botao_salvar.pack(pady=10)
    mostrar_icone()

#------------------------------ SALVA PONTUAÇÃO--------------------------------#
def salvar_score():
    pontuacao_label.configure(text=f"Pontuação salva: {pontuacao}")
    botao_salvar.configure(state="disabled")

# ------------------------=----- SALVAR USUÁRIO -------=-----------------------#
def salvar_usuario():
    nome = entrada_nome.get().strip()
    email = entrada_email.get().strip()

    # Verifica se os campos estão preenchidos
    if not nome or not email:
        messagebox.showerror(title="Erro", message="Preencha todos os campos.")
        return

    # Verifica se o e-mail é válido
    if not email_valido(email):
        messagebox.showerror(title="Erro", message="Email inválido. Digite um e-mail válido.")
        return

    # Se estiver tudo certo, salva o usuário
    usuarios.append({"nome": nome, "email": email, "pontuacao": pontuacao})
    salvar_dados()
    entrada_nome.delete(0, "end")
    entrada_email.delete(0, "end")
    frame_usuario.place_forget()
    atualizar_tabela()
    tabela.place(relx=0.5, rely=0.5, anchor="center")
    esconder_icone()
    botao_como_jogar.place_forget()

# ------------------------------ VALIDAR E-MAIL -------------------------------#
def email_valido(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(padrao, email) is not None

#---------------------------- ATUALIZAR RANKING -------------------------------#
tabela = ctk.CTkFrame(janela)
def atualizar_tabela():
    global usuario_selecionado, botoes_usuarios
    usuario_selecionado = None
    botoes_usuarios = []

    for widget in tabela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(tabela, text="Ranking", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

    usuarios_ordenados = sorted(usuarios, key=lambda x: x["pontuacao"], reverse=True)

    # ==== PÓDIO COM IMAGEM CENTRAL ====
    if len(usuarios_ordenados) >= 1:
        frame_podio = ctk.CTkFrame(tabela, fg_color="transparent", width=300, height=250)
        frame_podio.pack(pady=10)

        # Imagem do pódio centralizada
        img_podio = Image.open(r"C:Quiz-main\resources\ranking.png").resize(size=(250, 200))

        img_podio_tk = ctk.CTkImage(img_podio, size=(250, 200))
        
        label_podio = ctk.CTkLabel(frame_podio, image=img_podio_tk, text="")
        label_podio.image = img_podio_tk
        label_podio.place(relx=0.5, rely=0.5, anchor="center")

        # Posições relativas dos 3 primeiros colocados
        posicoes_place = [
            {"relx": 0.5, "rely": 0.33},  # 1º lugar - topo central
            {"relx": 0.20, "rely": 0.47}, # 2º lugar - à esquerda
            {"relx": 0.75, "rely": 0.55}  # 3º lugar - à direita
        ]

        podio_indices = [0, 1, 2]
    for i, idx in enumerate(podio_indices):
        if idx < len(usuarios_ordenados):
            user = usuarios_ordenados[idx]
            label_nome = ctk.CTkLabel(
                frame_podio,
                text=f"{idx+1}º - {user['nome']}({user['pontuacao']})",
                font=ctk.CTkFont(size=12),
                cursor="hand2"
            )
            label_nome.place(**posicoes_place[i], anchor="center")
            label_nome.bind("<Button-1>", lambda e, i=idx: selecionar_usuario(i))
            botoes_usuarios.append(label_nome)
    # Mostra os usuários do 4º lugar em diante
    if len(usuarios_ordenados) > 3:
        frame_lista = ctk.CTkFrame(tabela)
        frame_lista.pack(pady=10)
        
    for i, user in enumerate(usuarios_ordenados[3:], start=4):
        label = ctk.CTkLabel(
            frame_lista,
            text=f"{i}º - {user['nome']} ({user['pontuacao']})",
            font=ctk.CTkFont(size=14),
            cursor="hand2"
        )
        label.pack(anchor="w", padx=20, pady=2)
        label.bind("<Button-1>", lambda e, i=i-1: selecionar_usuario(i))
        botoes_usuarios.append(label)
        
        # ==== BOTÕES DE AÇÃO ====
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
    botao_salvar.pack(pady=10)

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
    botao_como_jogar.place_forget()
    esconder_icone()

#----------------------- VOLTAR PARA O MENU INICIAL ----------------------------#
def voltar_ao_inicio():
    tabela.place_forget()
    frame_usuario.place_forget()
    frame_quiz.place_forget()
    frame_como_jogar.place_forget()
    frame_inicial.place(relx=0.5, rely=0.5, anchor="center")
    botao_como_jogar.place(relx=0.01, rely=0.01, anchor="nw")
    mostrar_icone()

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
#FRAME INICIAL
frame_inicial = ctk.CTkFrame(janela)
frame_inicial.place(relx=0.5, rely=0.5, anchor="center")

# FRAME COMO JOGAR
frame_como_jogar = ctk.CTkFrame(janela, fg_color="black")
label_instrucao = ctk.CTkLabel(
    frame_como_jogar, 
    text="""COMO JOGAR:\n
Você receberá uma pergunta, retirada do nosso sistema. \n
Todas as perguntas são baseadas nas informações fornecidas pelo banco de dados do IMDb (Internet movie database). \nApenas uma opção entre as duas está correta.\nSeu objetivo é acertar o máximo de perguntas possível, mas não se preocupe, se errar uma delas, o jogo continuará enquanto ainda tiver vidas sobrando.\n
Tome a decisão correta para obter uma maior pontuação. \nBoa sorte!\n
Observação:\nCaso desista durante o jogo, sua pontuação será perdida.
""",
    font=ctk.CTkFont(size=14), 
    justify="left",
    wraplength=400,
    text_color="white"
)
label_instrucao.pack(padx=20, pady=20)

# ICONE JOGO
icone = Image.open(r"C:Quiz-main\resources\icone.png").resize((141, 124))
icone_tk = ctk.CTkImage(light_image=icone, dark_image=icone, size=(141, 124))

# LABEL ICONE JOGO
icone_label = ctk.CTkLabel(master=janela, image=icone_tk, text="", fg_color="white")
icone_label.place(relx=0.5, y=100, anchor="n")  # CENTRALIZADO

# BOTÕES
botoes_iniciais = ctk.CTkFrame(frame_inicial, fg_color="white")
botoes_iniciais.grid(row=1, column=0)

botao_iniciar = ctk.CTkButton(botoes_iniciais, text="Iniciar", command=iniciar_quiz, fg_color="black", hover_color="#333")
botao_iniciar.grid(row=0, column=0, padx=10)

# BOTÃO VOLTAR (COMO JOGAR)
botao_voltar_como_jogar = ctk.CTkButton(
    frame_como_jogar, text="Voltar", fg_color="black", hover_color="#333", command=voltar_ao_inicio
)
botao_voltar_como_jogar.pack(pady=10)

# BOTÃO COMO JOGAR
botao_como_jogar = ctk.CTkButton(
    janela, image=img_como_jogar_tk, text="", 
    width=80, height=70,
    fg_color="white", hover_color="#444", 
    command=mostrar_como_jogar
)
botao_como_jogar.place(relx=0.01, rely=0.01, anchor="nw")

# BOTÃO RANKING
botao_ranking = ctk.CTkButton(botoes_iniciais, text="Ranking", command=mostrar_ranking, fg_color="black", hover_color="#333")
botao_ranking.grid(row=0, column=1, padx=10)

#---------------------------- FRAME E BOTÕES JOGO ------------------------------#
frame_quiz = ctk.CTkFrame(janela, width=300, height=250, fg_color="transparent")
frame_quiz.pack_propagate(False)
# FRAME VIDAS
frame_vidas = ctk.CTkFrame(janela, fg_color="transparent")
frame_vidas.place(relx=0.98, rely=0.02, anchor="ne")
vidas_imagens = []

#PERGUNTA
pergunta_label = ctk.CTkLabel(frame_quiz, text="", wraplength=280, font=ctk.CTkFont(size=24))
pergunta_label.pack(pady=(10, 10))

#BOTÕES OPÇÕES
botoes_opcoes = ctk.CTkFrame(frame_quiz, width=350)
botoes_opcoes.pack(pady=5, fill="x", expand=True)

botao_opcao1 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao1.cget("text")), fg_color="black", hover_color="#333")
botao_opcao1.pack(pady=10, padx=10, fill="x")

botao_opcao2 = ctk.CTkButton(botoes_opcoes, text="", command=lambda: verificar_resposta(botao_opcao2.cget("text")), fg_color="black", hover_color="#333")
botao_opcao2.pack(pady=10, padx=10, fill="x")

#PONTUAÇÃO
pontuacao_label = ctk.CTkLabel(
    frame_quiz,
    text="Pontuação: 0",
    font=ctk.CTkFont(size=24, weight="bold")
)
pontuacao_label.pack(pady=(10, 10))

# BOTÃO DESISTIR
botao_desistir = ctk.CTkButton(frame_quiz, text="Desistir", command=desistir, fg_color="black", hover_color="#333")
botao_desistir.pack(pady=(5, 10))

#-------------------------------- FRAME USUARIO -------------------------------#
frame_usuario = ctk.CTkFrame(janela, fg_color="white")

entrada_nome_label = ctk.CTkLabel(frame_usuario, text="Digite seu nome e email:", font=ctk.CTkFont(size=20))
text_color="black",  # texto preto para fundo branco
fg_color="white"     # fundo branco
entrada_nome_label.pack(pady=(10, 5))

entrada_nome = ctk.CTkEntry(frame_usuario, placeholder_text="Nome", width=300, font=ctk.CTkFont(size=14))
text_color="black",  # texto preto para fundo branco
fg_color="white"     # fundo branco
entrada_nome.pack(pady=5)

entrada_email = ctk.CTkEntry(frame_usuario, placeholder_text="Email", width=300, font=ctk.CTkFont(size=14))
text_color="black",  # texto preto para fundo branco
fg_color="white"     # fundo branco
entrada_email.pack(pady=5)

# BOTÃO SALVAR
botao_salvar = ctk.CTkButton(frame_usuario, text="Salvar Pontuação", command=salvar_usuario, fg_color="black", hover_color="#333")
# -------------------------------- EXECUÇÃO -----------------------------------#
tabela = ctk.CTkFrame(janela)
carregar_dados()
janela.mainloop()
