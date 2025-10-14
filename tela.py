import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
from datetime import datetime
import customtkinter as ctk

# =========================================================
# 🔗 Conexão com MongoDB
# =========================================================
client = MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]
colecao_livros = db["livros"]
colecao_usuarios = db["usuarios"]
colecao_emprestimos = db["emprestimos"]

# =========================================================
# 🎨 Cores
# =========================================================
co_branco = "#FEFEFE"
co_preto = "#1C1C1C"
co_verde = "#4FA882"
co_vermelho = "#E74C3C"
co_azul = "#3498DB"
co_degrade_topo = "#2980B9"

# =========================================================
# 🪟 Janela
# =========================================================
janela = Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("900x550")
janela.configure(bg=co_branco)
janela.resizable(False, False)

# Layout grid
janela.grid_columnconfigure(0, weight=0)
janela.grid_columnconfigure(1, weight=1)
janela.grid_rowconfigure(0, weight=0)
janela.grid_rowconfigure(1, weight=1)

# =========================================================
# 🧱 Frames
# =========================================================
frameTopo = Frame(janela, bg=co_degrade_topo, height=60)
frameTopo.grid(row=0, column=0, columnspan=2, sticky="nsew")

frameMenu = Frame(janela, bg=co_preto, width=200)
frameMenu.grid(row=1, column=0, sticky="ns")
frameMenu.grid_propagate(False)

frameConteudo = Frame(janela, bg=co_branco)
frameConteudo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# =========================================================
# Logo e título
# =========================================================
try:
    img_logo = Image.open("icones/cabecalho.png").resize((40, 40))
    img_logo = ImageTk.PhotoImage(img_logo)
    Label(frameTopo, image=img_logo, bg=co_degrade_topo).pack(side="left", padx=10, pady=10)
except:
    pass

Label(frameTopo, text="Sistema de Biblioteca", font=("Arial", 20, "bold"),
      fg=co_branco, bg=co_degrade_topo).pack(side="left", pady=15)

# =========================================================
# Funções auxiliares
# =========================================================
def limpar_conteudo():
    for w in frameConteudo.winfo_children():
        w.destroy()

def carregar_icone(nome_arquivo, tamanho=(24, 24)):
    path = os.path.join("icones", nome_arquivo)
    if os.path.exists(path):
        try:
            img = Image.open(path).resize(tamanho)
            return ImageTk.PhotoImage(img)
        except:
            return None
    return None

def criar_botao_menu_ctk(texto, comando, icone_arquivo=None):
    img = carregar_icone(icone_arquivo) if icone_arquivo else None
    btn = ctk.CTkButton(
        frameMenu,
        text=texto,
        image=img,
        compound="left",
        fg_color=co_preto,
        text_color=co_branco,
        hover_color=co_azul,
        width=180,
        command=comando
    )
    btn.image = img
    # Alinha todos os botões à esquerda
    btn.pack(fill="x", pady=5, padx=0, anchor="w")
    return btn

# =========================================================
# Cadastro de Usuários
# =========================================================
def form_novo_usuario():
    limpar_conteudo()
    Label(frameConteudo, text="Novo Usuário", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=15)
    frm = Frame(frameConteudo, bg=co_branco); frm.pack(pady=10)

    campos = [("Nome:", "nome"), ("Sobrenome:", "sobrenome"), ("Email:", "email"), ("Telefone:", "telefone")]
    entradas = {}
    for i, (lbl, key) in enumerate(campos):
        Label(frm, text=lbl, bg=co_branco).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entradas[key] = Entry(frm, width=40)
        entradas[key].grid(row=i, column=1, padx=5, pady=5)

    def salvar():
        if any(not entradas[k].get().strip() for k in entradas):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return
        colecao_usuarios.insert_one({k: entradas[k].get().strip() for k in entradas})
        messagebox.showinfo("Sucesso", f"Usuário '{entradas['nome'].get()}' cadastrado!")
        form_novo_usuario()

    ctk.CTkButton(frameConteudo, text="Cadastrar", fg_color=co_verde, command=salvar).pack(pady=10)

# =========================================================
# Cadastro de Livros
# =========================================================
def form_novo_livro():
    limpar_conteudo()
    Label(frameConteudo, text="Novo Livro", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=15)
    frm = Frame(frameConteudo, bg=co_branco); frm.pack(pady=10)

    campos = [("Título:", "titulo"), ("Autor:", "autor"), ("Ano de Publicação:", "ano"), ("ISBN:", "isbn")]
    entradas = {}
    for i, (lbl, key) in enumerate(campos):
        Label(frm, text=lbl, bg=co_branco).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entradas[key] = Entry(frm, width=40)
        entradas[key].grid(row=i, column=1, padx=5, pady=5)

    def salvar():
        if any(not entradas[k].get().strip() for k in entradas):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return
        try:
            entradas["ano"] = int(entradas["ano"].get())
        except:
            messagebox.showwarning("Erro", "Ano deve ser um número!")
            return
        colecao_livros.insert_one({
            "titulo": entradas["titulo"].get(),
            "autor": entradas["autor"].get(),
            "ano_publicacao": entradas["ano"],
            "isbn": entradas["isbn"].get()
        })
        messagebox.showinfo("Sucesso", f"Livro '{entradas['titulo'].get()}' cadastrado!")
        form_novo_livro()

    ctk.CTkButton(frameConteudo, text="Cadastrar", fg_color=co_verde, command=salvar).pack(pady=10)

# =========================================================
# Listagem de livros e usuários
# =========================================================
def listar_livros():
    limpar_conteudo()
    Label(frameConteudo, text="Todos os Livros", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=10)
    text = Text(frameConteudo, width=70, height=20); text.pack(padx=10, pady=5)
    scroll = Scrollbar(frameConteudo, command=text.yview); scroll.pack(side="right", fill=Y)
    text.config(yscrollcommand=scroll.set)
    for l in colecao_livros.find():
        text.insert("end", f"{l['titulo']} - {l['autor']} ({l['ano_publicacao']}) ISBN: {l['isbn']}\n")

def listar_usuarios():
    limpar_conteudo()
    Label(frameConteudo, text="Todos os Usuários", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=10)
    text = Text(frameConteudo, width=70, height=20); text.pack(padx=10, pady=5)
    scroll = Scrollbar(frameConteudo, command=text.yview); scroll.pack(side="right", fill=Y)
    text.config(yscrollcommand=scroll.set)
    for u in colecao_usuarios.find():
        text.insert("end", f"{u['nome']} {u['sobrenome']} - {u['email']} - {u['telefone']}\n")

# =========================================================
# Empréstimos
# =========================================================
def form_emprestimo():
    limpar_conteudo()
    Label(frameConteudo, text="Realizar Empréstimo", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=15)
    frm = ctk.CTkFrame(frameConteudo, fg_color="white")
    frm.pack(pady=10, padx=10, fill="x")

    livros_lista = [l["titulo"] for l in colecao_livros.find()] or [""]
    usuarios_lista = [u["nome"] for u in colecao_usuarios.find()] or [""]

    # Dropdown Livro
    Label(frm, text="Livro:", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    livro_dropdown = ctk.CTkOptionMenu(frm, values=livros_lista, width=300)
    livro_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    # Dropdown Usuário
    Label(frm, text="Usuário:", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    usuario_dropdown = ctk.CTkOptionMenu(frm, values=usuarios_lista, width=300)
    usuario_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    def salvar():
        livro = colecao_livros.find_one({"titulo": {"$regex": livro_dropdown.get(), "$options": "i"}})
        usuario = colecao_usuarios.find_one({"nome": {"$regex": usuario_dropdown.get(), "$options": "i"}})
        if not livro or not usuario:
            messagebox.showwarning("Erro", "Livro ou usuário não encontrado!")
            return
        if colecao_emprestimos.find_one({"id_livro": livro["_id"], "data_devolucao": None}):
            messagebox.showwarning("Aviso", "Este livro já está emprestado.")
            return
        colecao_emprestimos.insert_one({
            "id_livro": livro["_id"],
            "id_usuario": usuario["_id"],
            "data_emprestimo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_devolucao": None
        })
        messagebox.showinfo("Sucesso", f"Livro '{livro['titulo']}' emprestado para {usuario['nome']}!")
        form_emprestimo()

    ctk.CTkButton(frameConteudo, text="Emprestar", width=200, command=salvar).pack(pady=15)

# =========================================================
# Devolução
# =========================================================
def form_devolucao():
    limpar_conteudo()
    Label(frameConteudo, text="Devolução de Empréstimos", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=15)
    frm = ctk.CTkFrame(frameConteudo, fg_color="white")
    frm.pack(pady=10, padx=10, fill="x")

    emprestimos_ativos = list(colecao_emprestimos.find({"data_devolucao": None}))
    if not emprestimos_ativos:
        Label(frm, text="Nenhum empréstimo ativo.", bg="white").pack(pady=10)
        return

    opcoes = []
    for e in emprestimos_ativos:
        l = colecao_livros.find_one({"_id": e["id_livro"]})
        u = colecao_usuarios.find_one({"_id": e["id_usuario"]})
        titulo = l.get("titulo", "(desconhecido)") if l else "(desconhecido)"
        nome = u.get("nome", "(desconhecido)") if u else "(desconhecido)"
        opcoes.append(f"{titulo} — {nome}")

    selecionado_dropdown = ctk.CTkOptionMenu(frm, values=opcoes, width=400)
    selecionado_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    Label(frm, text="Selecione empréstimo:", bg="white").grid(row=0,column=0, padx=5, pady=5)

    def devolver():
        try:
            titulo, nome = [s.strip() for s in selecionado_dropdown.get().split("—")]
        except:
            messagebox.showwarning("Erro", "Opção inválida.")
            return
        livro = colecao_livros.find_one({"titulo": {"$regex": titulo, "$options": "i"}})
        usuario = colecao_usuarios.find_one({"nome": {"$regex": nome, "$options": "i"}})
        if not livro or not usuario:
            messagebox.showwarning("Erro", "Documento não encontrado.")
            return
        emprestimo = colecao_emprestimos.find_one({"id_livro": livro["_id"], "id_usuario": usuario["_id"], "data_devolucao": None})
        if not emprestimo:
            messagebox.showinfo("Info", "Empréstimo não encontrado ou já devolvido.")
            return
        colecao_emprestimos.update_one({"_id": emprestimo["_id"]}, {"$set": {"data_devolucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' devolvido por {nome}!")
        form_devolucao()

    ctk.CTkButton(frm, text="Registrar Devolução", width=200, command=devolver).grid(row=1,column=1, pady=10, sticky="w")

# =========================================================
# Listar livros emprestados
# =========================================================
def listar_emprestados():
    limpar_conteudo()
    Label(frameConteudo, text="Livros Emprestados", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=10)
    text = Text(frameConteudo, width=70, height=20); text.pack(padx=10, pady=5)
    scroll = Scrollbar(frameConteudo, command=text.yview); scroll.pack(side="right", fill=Y)
    text.config(yscrollcommand=scroll.set)

    emprestimos = list(colecao_emprestimos.find({"data_devolucao": None}))
    if not emprestimos:
        text.insert("end", "Nenhum livro emprestado no momento.\n")
    else:
        for e in emprestimos:
            livro = colecao_livros.find_one({"_id": e["id_livro"]})
            usuario = colecao_usuarios.find_one({"_id": e["id_usuario"]})
            text.insert("end", f"{livro['titulo']} - {usuario['nome']} ({e['data_emprestimo']})\n")

# =========================================================
# Histórico de empréstimos
# =========================================================
def exibir_historico():
    limpar_conteudo()
    Label(frameConteudo, text="Histórico de Empréstimos", font=("Arial", 14, "bold"), bg=co_branco).pack(pady=15)
    text = Text(frameConteudo, width=70, height=20)
    text.pack(padx=10, pady=5)
    scroll = Scrollbar(frameConteudo, command=text.yview)
    scroll.pack(side="right", fill=Y)
    text.config(yscrollcommand=scroll.set)

    emprestimos = list(colecao_emprestimos.find())
    if not emprestimos:
        text.insert("end", "Nenhum histórico de empréstimos.\n")
    else:
        for e in emprestimos:
            livro = colecao_livros.find_one({"_id": e["id_livro"]})
            usuario = colecao_usuarios.find_one({"_id": e["id_usuario"]})
            devolucao = e["data_devolucao"] or "Ainda não devolvido"
            text.insert("end", f"{livro['titulo']} - {usuario['nome']} ({e['data_emprestimo']}) → {devolucao}\n")

# =========================================================
# Botões do menu (CTkButton)
# =========================================================
criar_botao_menu_ctk("Novo Usuário", form_novo_usuario, "adicionar_usuario.png")
criar_botao_menu_ctk("Novo Livro", form_novo_livro, "adicionar.png")
criar_botao_menu_ctk("Exibir Todos os Livros", listar_livros, "livros_na_biblioteca.png")
criar_botao_menu_ctk("Exibir Todos os Usuários", listar_usuarios, "usuarios.png")
criar_botao_menu_ctk("Realizar Empréstimo", form_emprestimo, "emprestar.png")
criar_botao_menu_ctk("Devolução de Empréstimos", form_devolucao, "devolver.png")
criar_botao_menu_ctk("Livros Emprestados", listar_emprestados, "livro_emprestado.png")
criar_botao_menu_ctk("Histórico", exibir_historico, "historico.png")

# =========================================================
# Rodar app
# =========================================================
janela.mainloop()
