from tkinter import Tk, Frame, Label, Button, Entry, Text, Scrollbar, END, Y
from PIL import Image, ImageTk
from pymongo import MongoClient
from datetime import datetime
from tkinter import messagebox

# --- Conexão MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]
livros = db["livros"]
usuarios = db["usuarios"]
emprestimos = db["emprestimos"]

# --- Cores ---
BRANCO = "#F9F9F9"
PRETO = "#1C1C1C"
VERDE = "#4FA882"
AZUL = "#3498DB"
TOPO = "#2980B9"
CINZA = "#ECECEC"

# --- Janela ---
janela = Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("950x600")
janela.configure(bg=BRANCO)
janela.resizable(False, False)

# --- Frames ---
frameTopo = Frame(janela, bg=TOPO, height=70)
frameTopo.pack(side="top", fill="x")
frameMenu = Frame(janela, bg=PRETO, width=220)
frameMenu.pack(side="left", fill="y")
frameMenu.pack_propagate(False)
frameConteudo = Frame(janela, bg=BRANCO)
frameConteudo.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# --- Logo e título ---
img_logo = ImageTk.PhotoImage(Image.open("icones/cabecalho.png").resize((50,50)))
Label(frameTopo, image=img_logo, bg=TOPO).pack(side="left", padx=15)
Label(frameTopo, text="Sistema de Biblioteca", font=("Helvetica",22,"bold"), fg=BRANCO, bg=TOPO).pack(side="left")

# --- Auxiliares ---
def limpar_conteudo():
    for w in frameConteudo.winfo_children(): w.destroy()

def criar_botao(texto, func, icone=None):
    if icone:
        img = ImageTk.PhotoImage(Image.open(icone).resize((25,25)))
    else: img = None
    btn = Button(frameMenu, text=texto, image=img, compound="left", anchor="w",
                 bg=PRETO, fg="white", font=("Helvetica",11,"bold"), relief="flat", command=func)
    btn.image = img
    btn.pack(fill="x", padx=10, pady=5)
    btn.bind("<Enter>", lambda e: btn.config(bg=AZUL))
    btn.bind("<Leave>", lambda e: btn.config(bg=PRETO))
    return btn

def mostrar_lista(items, campos, titulo="Registros"):
    limpar_conteudo()
    Label(frameConteudo, text=titulo, font=("Helvetica",16,"bold"), bg=BRANCO).pack(pady=10)
    if not items:
        Label(frameConteudo, text=f"Nenhum {titulo.lower()} encontrado.", bg=BRANCO).pack(pady=10)
        return
    for i in items:
        card = Frame(frameConteudo, bg=CINZA, padx=10, pady=5)
        card.pack(fill="x", pady=5)
        text = " | ".join(str(i.get(c,"")) for c in campos)
        Label(card, text=text, bg=CINZA, font=("Helvetica",11)).pack(anchor="w")

# --- Formulários ---
def form_novo_usuario():
    limpar_conteudo()
    Label(frameConteudo, text="Novo Usuário", font=("Helvetica",16,"bold"), bg=BRANCO).pack(pady=15)
    f = Frame(frameConteudo, bg=BRANCO); f.pack(pady=10)
    campos = ["Nome","Sobrenome","Email","Telefone"]
    entradas = {}
    for idx,c in enumerate(campos):
        Label(f,text=c+":", bg=BRANCO).grid(row=idx,column=0,sticky="e",padx=5,pady=5)
        e = Entry(f,width=40); e.grid(row=idx,column=1,padx=5,pady=5)
        entradas[c.lower()] = e
    def salvar():
        data = {k:v.get() for k,v in entradas.items()}
        if all(data.values()):
            data["id_usuario"] = usuarios.count_documents({})+1
            usuarios.insert_one(data)
            messagebox.showinfo("Sucesso","Usuário cadastrado!")
            form_novo_usuario()
        else: messagebox.showwarning("Erro","Preencha todos os campos!")
    Button(frameConteudo, text="Cadastrar", bg=VERDE, fg=BRANCO, width=20, command=salvar).pack(pady=15)

def form_novo_livro():
    limpar_conteudo()
    Label(frameConteudo, text="Novo Livro", font=("Helvetica",16,"bold"), bg=BRANCO).pack(pady=15)
    f = Frame(frameConteudo, bg=BRANCO); f.pack(pady=10)
    campos = ["Título","Autor","Ano","ISBN"]
    entradas = {}
    for idx,c in enumerate(campos):
        Label(f,text=c+":", bg=BRANCO).grid(row=idx,column=0,sticky="e",padx=5,pady=5)
        e = Entry(f,width=40); e.grid(row=idx,column=1,padx=5,pady=5)
        entradas[c.lower()] = e
    def salvar():
        data = {k:v.get() for k,v in entradas.items()}
        if all(data.values()):
            try: data["ano"] = int(data["ano"])
            except: messagebox.showwarning("Erro","Ano inválido"); return
            data["id_livro"] = livros.count_documents({})+1
            livros.insert_one(data)
            messagebox.showinfo("Sucesso","Livro cadastrado!")
            form_novo_livro()
        else: messagebox.showwarning("Erro","Preencha todos os campos!")
    Button(frameConteudo, text="Cadastrar", bg=VERDE, fg=BRANCO, width=20, command=salvar).pack(pady=15)

def listar_todos_livros(): mostrar_lista(list(livros.find()),["id_livro","titulo","autor","ano","isbn"],"Todos os Livros")
def listar_todos_usuarios(): mostrar_lista(list(usuarios.find()),["id_usuario","nome","sobrenome","email","telefone"],"Todos os Usuários")

def form_emprestimo():
    limpar_conteudo()
    Label(frameConteudo,text="Realizar Empréstimo", font=("Helvetica",16,"bold"), bg=BRANCO).pack(pady=15)
    f = Frame(frameConteudo,bg=BRANCO); f.pack(pady=10)
    Label(f,text="Livro (Título):", bg=BRANCO).grid(row=0,column=0,sticky="e",padx=5,pady=5)
    e_livro=Entry(f,width=40); e_livro.grid(row=0,column=1)
    Label(f,text="Usuário (Nome):", bg=BRANCO).grid(row=1,column=0,sticky="e",padx=5,pady=5)
    e_usuario=Entry(f,width=40); e_usuario.grid(row=1,column=1)
    def salvar():
        l = livros.find_one({"titulo":{"$regex": e_livro.get(), "$options":"i"}})
        u = usuarios.find_one({"nome":{"$regex": e_usuario.get(), "$options":"i"}})
        if not l or not u: messagebox.showwarning("Erro","Livro ou usuário não encontrado!"); return
        emprestimos.insert_one({"id_livro":l["id_livro"],"id_usuario":u["id_usuario"],
                                "data_emprestimo":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "data_devolucao":None})
        messagebox.showinfo("Sucesso","Empréstimo realizado!")
        form_emprestimo()
    Button(frameConteudo,text="Emprestar", bg=VERDE, fg=BRANCO, width=20, command=salvar).pack(pady=15)

def form_devolucao():
    limpar_conteudo()
    Label(frameConteudo,text="Devolução de Empréstimos", font=("Helvetica",16,"bold"), bg=BRANCO).pack(pady=15)
    f = Frame(frameConteudo,bg=BRANCO); f.pack(pady=10)
    Label(f,text="Título do Livro:", bg=BRANCO).grid(row=0,column=0,sticky="e",padx=5,pady=5)
    e_livro=Entry(f,width=40); e_livro.grid(row=0,column=1)
    Label(f,text="Nome do Usuário:", bg=BRANCO).grid(row=1,column=0,sticky="e",padx=5,pady=5)
    e_usuario=Entry(f,width=40); e_usuario.grid(row=1,column=1)
    def devolver():
        l = livros.find_one({"titulo":{"$regex": e_livro.get(), "$options":"i"}})
        u = usuarios.find_one({"nome":{"$regex": e_usuario.get(), "$options":"i"}})
        if not l or not u: messagebox.showwarning("Erro","Livro ou usuário não encontrado!"); return
        e = emprestimos.find_one({"id_livro":l["id_livro"],"id_usuario":u["id_usuario"],"data_devolucao":None})
        if not e: messagebox.showinfo("Info","Nenhum empréstimo ativo encontrado."); return
        emprestimos.update_one({"_id":e["_id"]},{"$set":{"data_devolucao":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        messagebox.showinfo("Sucesso","Devolução registrada!")
        form_devolucao()
    Button(frameConteudo,text="Devolver", bg=VERDE, fg=BRANCO, width=20, command=devolver).pack(pady=15)

def listar_emprestados():
    itens=[]
    for e in emprestimos.find({"data_devolucao":None}):
        l = livros.find_one({"id_livro":e["id_livro"]})
        u = usuarios.find_one({"id_usuario":e["id_usuario"]})
        itens.append({"Livro": l["titulo"] if l else "Desconhecido", "Usuário": u["nome"] if u else "Desconhecido",
                      "Data": e["data_emprestimo"]})
    mostrar_lista(itens,["Livro","Usuário","Data"],"Livros Emprestados")

# --- Botões do menu ---
criar_botao("Novo Usuário", form_novo_usuario, "icones/adicionar_usuario.png")
criar_botao("Novo Livro", form_novo_livro, "icones/adicionar.png")
criar_botao("Todos os Livros", listar_todos_livros, "icones/livros_na_biblioteca.png")
criar_botao("Todos os Usuários", listar_todos_usuarios, "icones/usuarios.png")
criar_botao("Realizar Empréstimo", form_emprestimo, "icones/emprestar.png")
criar_botao("Devolução", form_devolucao, "icones/devolver.png")
criar_botao("Livros Emprestados", listar_emprestados, "icones/livro_emprestado.png")

janela.mainloop()
