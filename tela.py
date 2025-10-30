# tela.py - Sistema de Biblioteca completo
# Desenvolvido por um dev junior para apresentação acadêmica
# ------------------------------------------------------------------

import os
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
import requests
from io import BytesIO
import customtkinter as ctk

from dados import *
from view import exibir_tabela

# =========================================================
# Cores / Janela principal
# =========================================================
CO_BRANCO = "#FEFEFE"
CO_PRETO = "#1C1C1C"
CO_AZUL = "#3498DB"
CO_VERDE = "#4FA882"
CO_DEGRADE_TOPO = "#2980B9"

janela = Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("1000x600")
janela.configure(bg=CO_BRANCO)
janela.resizable(False, False)
janela.grid_columnconfigure(0, weight=0)
janela.grid_columnconfigure(1, weight=1)
janela.grid_rowconfigure(0, weight=0)
janela.grid_rowconfigure(1, weight=1)

# =========================================================
# Frames
# =========================================================
frameTopo = Frame(janela, bg=CO_DEGRADE_TOPO, height=70)
frameTopo.grid(row=0, column=0, columnspan=2, sticky="nsew")

frameMenu = Frame(janela, bg=CO_PRETO, width=220)
frameMenu.grid(row=1, column=0, sticky="ns")
frameMenu.grid_propagate(False)

frameConteudo = Frame(janela, bg=CO_BRANCO)
frameConteudo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# =========================================================
# Cabeçalho (logo + título)
# =========================================================
def carregar_icone_local(nome, tamanho=(40,40)):
    """Carrega ícone da pasta 'icones'"""
    path = os.path.join("icones", nome)
    if os.path.exists(path):
        try:
            img = Image.open(path).resize(tamanho)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None
    return None

_image_cache = {}  # evita que o Tkinter descarregue imagens

img_logo = carregar_icone_local("cabecalho.png")
if img_logo:
    Label(frameTopo, image=img_logo, bg=CO_DEGRADE_TOPO).pack(side="left", padx=12, pady=10)

Label(frameTopo, text="Sistema de Biblioteca", font=("Arial", 20, "bold"),
      fg=CO_BRANCO, bg=CO_DEGRADE_TOPO).pack(side="left", pady=15)

# =========================================================
# Funções utilitárias
# =========================================================
def limpar_conteudo():
    """Limpa o frame de conteúdo"""
    for w in frameConteudo.winfo_children():
        w.destroy()

def criar_botao_menu(texto, comando, icone_nome=None):
    """Cria botão lateral do menu com ou sem ícone"""
    img = None
    if icone_nome:
        img = carregar_icone_local(icone_nome, tamanho=(24,24))
        if img: _image_cache[icone_nome] = img
    if img:
        btn = Button(frameMenu, text="  " + texto, image=img, compound=LEFT, anchor="w",
                     bg=CO_PRETO, fg=CO_BRANCO, font=("Arial", 10, "bold"),
                     relief="flat", command=comando)
        btn.image = img
    else:
        btn = Button(frameMenu, text=texto, bg=CO_PRETO, fg=CO_BRANCO,
                     font=("Arial", 10, "bold"), relief="flat", anchor="w", command=comando)
    btn.pack(fill="x", pady=6, padx=8)
    btn.bind("<Enter>", lambda e: btn.config(bg=CO_AZUL))
    btn.bind("<Leave>", lambda e: btn.config(bg=CO_PRETO))
    return btn

# =========================================================
# Google Books para capa
# =========================================================
def buscar_google_books(titulo='', isbn=''):
    """Busca informações do livro pelo Google Books"""
    try:
        q = f"isbn:{isbn}" if isbn else f"intitle:{titulo}"
        url = "https://www.googleapis.com/books/v1/volumes"
        resp = requests.get(url, params={"q": q, "maxResults": 5}, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items")
        if not items: return None
        vi = items[0].get("volumeInfo", {})
        titulo_api = vi.get("title","")
        autores = ", ".join(vi.get("authors",[])) if vi.get("authors") else ""
        published = vi.get("publishedDate","")
        ano = published.split("-")[0] if published else ""
        thumbnail = vi.get("imageLinks",{}).get("thumbnail")
        descricao = vi.get("description","") or ""
        return {"titulo":titulo_api,"autores":autores,"ano":ano,"thumbnail":thumbnail,"descricao":descricao}
    except Exception as e:
        print("Erro Google Books:",e)
        return None

def baixar_imagem_url(url, tamanho=(140,200)):
    """Baixa imagem de uma URL"""
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).resize(tamanho)
        photo = ImageTk.PhotoImage(img)
        _image_cache[url] = photo
        return photo
    except Exception:
        return None

# =========================================================
# ---------- Usuários ----------
# Novo Usuário
def form_novo_usuario():
    limpar_conteudo()
    Label(frameConteudo, text="Novo Usuário", font=("Arial",14,"bold"), bg=CO_BRANCO).pack(pady=10)
    frm = Frame(frameConteudo,bg=CO_BRANCO); frm.pack(pady=6)
    Label(frm,text="Nome:",bg=CO_BRANCO).grid(row=0,column=0,sticky="e",padx=5)
    Label(frm,text="Sobrenome:",bg=CO_BRANCO).grid(row=1,column=0,sticky="e",padx=5)
    Label(frm,text="Email:",bg=CO_BRANCO).grid(row=2,column=0,sticky="e",padx=5)
    Label(frm,text="Telefone:",bg=CO_BRANCO).grid(row=3,column=0,sticky="e",padx=5)

    e_nome = Entry(frm,width=42); e_nome.grid(row=0,column=1)
    e_sob = Entry(frm,width=42); e_sob.grid(row=1,column=1)
    e_email = Entry(frm,width=42); e_email.grid(row=2,column=1)
    e_tel = Entry(frm,width=42); e_tel.grid(row=3,column=1)

    def salvar():
        nome = e_nome.get().strip(); sobrenome = e_sob.get().strip()
        email = e_email.get().strip(); telefone = e_tel.get().strip()
        if not nome or not sobrenome or not email or not telefone:
            messagebox.showwarning("Erro","Preencha todos os campos!"); return
        insert_user(nome,sobrenome,email,telefone)
        messagebox.showinfo("Sucesso",f"Usuário '{nome}' cadastrado!"); form_novo_usuario()

    Button(frameConteudo,text="Cadastrar",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# Alterar Usuário
def form_alterar_usuario():
    limpar_conteudo()
    Label(frameConteudo,text="Alterar Usuário",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    usuarios = list_users()
    if not usuarios:
        Label(frameConteudo,text="Nenhum usuário cadastrado.",bg=CO_BRANCO).pack(); return
    sel = ctk.CTkOptionMenu(frameConteudo, values=[u["nome"] for u in usuarios], width=400)
    sel.pack(pady=6)
    frm = Frame(frameConteudo,bg=CO_BRANCO); frm.pack(pady=6)
    Label(frm,text="Nome:",bg=CO_BRANCO).grid(row=0,column=0,sticky="e",padx=5)
    Label(frm,text="Sobrenome:",bg=CO_BRANCO).grid(row=1,column=0,sticky="e",padx=5)
    Label(frm,text="Email:",bg=CO_BRANCO).grid(row=2,column=0,sticky="e",padx=5)
    Label(frm,text="Telefone:",bg=CO_BRANCO).grid(row=3,column=0,sticky="e",padx=5)

    e_nome = Entry(frm,width=42); e_nome.grid(row=0,column=1)
    e_sob = Entry(frm,width=42); e_sob.grid(row=1,column=1)
    e_email = Entry(frm,width=42); e_email.grid(row=2,column=1)
    e_tel = Entry(frm,width=42); e_tel.grid(row=3,column=1)

    def carregar_usuario(*_):
        u = [x for x in usuarios if x["nome"]==sel.get()][0]
        e_nome.delete(0,END); e_nome.insert(0,u["nome"])
        e_sob.delete(0,END); e_sob.insert(0,u["sobrenome"])
        e_email.delete(0,END); e_email.insert(0,u["email"])
        e_tel.delete(0,END); e_tel.insert(0,u["telefone"])
        sel.usuario_atual = u["_id"]

    sel.configure(command=carregar_usuario)

    def salvar():
        if not hasattr(sel,"usuario_atual"): return
        dados = {"nome": e_nome.get().strip(),"sobrenome": e_sob.get().strip(),
                 "email": e_email.get().strip(),"telefone": e_tel.get().strip()}
        update_user(sel.usuario_atual,dados)
        messagebox.showinfo("Sucesso","Usuário atualizado!")
        form_alterar_usuario()

    Button(frameConteudo,text="Salvar Alterações",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# Listar Usuários
def listar_usuarios():
    limpar_conteudo()
    dados = list_users()
    if not dados:
        Label(frameConteudo,text="Nenhum usuário cadastrado.",bg=CO_BRANCO).pack(); return
    colunas = ["nome","sobrenome","email","telefone"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# ---------- Livros ----------
# Novo Livro
def form_novo_livro():
    limpar_conteudo()
    Label(frameConteudo,text="Novo Livro",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    frm = Frame(frameConteudo,bg=CO_BRANCO); frm.pack(pady=6)
    Label(frm,text="Título:",bg=CO_BRANCO).grid(row=0,column=0,sticky="e",padx=5)
    Label(frm,text="Autor:",bg=CO_BRANCO).grid(row=1,column=0,sticky="e",padx=5)
    Label(frm,text="Ano:",bg=CO_BRANCO).grid(row=2,column=0,sticky="e",padx=5)
    Label(frm,text="ISBN:",bg=CO_BRANCO).grid(row=3,column=0,sticky="e",padx=5)
    Label(frm,text="Quantidade:",bg=CO_BRANCO).grid(row=4,column=0,sticky="e",padx=5)
    Label(frm,text="Preço:",bg=CO_BRANCO).grid(row=5,column=0,sticky="e",padx=5)

    e_titulo = Entry(frm,width=42); e_titulo.grid(row=0,column=1)
    e_autor = Entry(frm,width=42); e_autor.grid(row=1,column=1)
    e_ano = Entry(frm,width=42); e_ano.grid(row=2,column=1)
    e_isbn = Entry(frm,width=42); e_isbn.grid(row=3,column=1)
    e_qtd = Entry(frm,width=42); e_qtd.grid(row=4,column=1)
    e_preco = Entry(frm,width=42); e_preco.grid(row=5,column=1)

    lbl_capa = Label(frm,bg=CO_BRANCO)
    lbl_capa.grid(row=0,column=2,rowspan=6,padx=10)

    def mostrar_capa():
        info = buscar_google_books(titulo=e_titulo.get(),isbn=e_isbn.get())
        if info and info.get("thumbnail"):
            img = baixar_imagem_url(info["thumbnail"])
            if img:
                lbl_capa.config(image=img)
                lbl_capa.image = img

    Button(frm,text="Google Livro",bg=CO_AZUL,fg=CO_BRANCO,command=mostrar_capa).grid(row=6,column=1,pady=6)

    def salvar():
        insert_book(e_titulo.get().strip(),e_autor.get().strip(),e_ano.get().strip(),
                    e_isbn.get().strip(),quantidade=int(e_qtd.get() or 1),preco=e_preco.get())
        messagebox.showinfo("Sucesso","Livro cadastrado!")
        form_novo_livro()

    Button(frameConteudo,text="Cadastrar",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# Alterar Livro
def form_alterar_livro():
    limpar_conteudo()
    Label(frameConteudo,text="Alterar Livro",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    livros = list_books()
    if not livros:
        Label(frameConteudo,text="Nenhum livro cadastrado.",bg=CO_BRANCO).pack(); return
    sel = ctk.CTkOptionMenu(frameConteudo, values=[l["titulo"] for l in livros], width=400)
    sel.pack(pady=6)
    frm = Frame(frameConteudo,bg=CO_BRANCO); frm.pack(pady=6)
    Label(frm,text="Título:",bg=CO_BRANCO).grid(row=0,column=0,sticky="e",padx=5)
    Label(frm,text="Autor:",bg=CO_BRANCO).grid(row=1,column=0,sticky="e",padx=5)
    Label(frm,text="Ano:",bg=CO_BRANCO).grid(row=2,column=0,sticky="e",padx=5)
    Label(frm,text="ISBN:",bg=CO_BRANCO).grid(row=3,column=0,sticky="e",padx=5)
    Label(frm,text="Quantidade:",bg=CO_BRANCO).grid(row=4,column=0,sticky="e",padx=5)
    Label(frm,text="Preço:",bg=CO_BRANCO).grid(row=5,column=0,sticky="e",padx=5)

    e_titulo = Entry(frm,width=42); e_titulo.grid(row=0,column=1)
    e_autor = Entry(frm,width=42); e_autor.grid(row=1,column=1)
    e_ano = Entry(frm,width=42); e_ano.grid(row=2,column=1)
    e_isbn = Entry(frm,width=42); e_isbn.grid(row=3,column=1)
    e_qtd = Entry(frm,width=42); e_qtd.grid(row=4,column=1)
    e_preco = Entry(frm,width=42); e_preco.grid(row=5,column=1)

    lbl_capa = Label(frm,bg=CO_BRANCO)
    lbl_capa.grid(row=0,column=2,rowspan=6,padx=10)

    def carregar_livro(*_):
        l = [x for x in livros if x["titulo"]==sel.get()][0]
        e_titulo.delete(0,END); e_titulo.insert(0,l["titulo"])
        e_autor.delete(0,END); e_autor.insert(0,l["autor"])
        e_ano.delete(0,END); e_ano.insert(0,l.get("ano_publicacao",""))
        e_isbn.delete(0,END); e_isbn.insert(0,l.get("isbn",""))
        e_qtd.delete(0,END); e_qtd.insert(0,l.get("quantidade",1))
        e_preco.delete(0,END); e_preco.insert(0,l.get("preco",""))
        sel.livro_atual = l["_id"]

    sel.configure(command=carregar_livro)

    def mostrar_capa():
        info = buscar_google_books(titulo=e_titulo.get(),isbn=e_isbn.get())
        if info and info.get("thumbnail"):
            img = baixar_imagem_url(info["thumbnail"])
            if img:
                lbl_capa.config(image=img)
                lbl_capa.image = img

    Button(frm,text="Google Livro",bg=CO_AZUL,fg=CO_BRANCO,command=mostrar_capa).grid(row=6,column=1,pady=6)

    def salvar():
        if not hasattr(sel,"livro_atual"): return
        dados = {"titulo": e_titulo.get().strip(),"autor": e_autor.get().strip(),
                 "ano_publicacao": e_ano.get().strip(),"isbn": e_isbn.get().strip(),
                 "quantidade": int(e_qtd.get() or 1),"preco": e_preco.get()}
        update_book(sel.livro_atual,dados)
        messagebox.showinfo("Sucesso","Livro atualizado!")
        form_alterar_livro()

    Button(frameConteudo,text="Salvar Alterações",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# Listar Livros
def listar_livros():
    limpar_conteudo()
    dados = list_books()
    if not dados:
        Label(frameConteudo,text="Nenhum livro cadastrado.",bg=CO_BRANCO).pack(); return
    colunas = ["titulo","autor","ano_publicacao","isbn","quantidade","preco"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# ---------- Empréstimos ----------
def form_emprestimos():
    limpar_conteudo()
    Label(frameConteudo,text="Empréstimos",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    livros = [l for l in list_books() if l.get("quantidade",0)>0]
    usuarios = list_users()
    if not livros or not usuarios:
        Label(frameConteudo,text="Não há livros disponíveis ou usuários cadastrados.",bg=CO_BRANCO).pack()
        return

    sel_livro = ctk.CTkOptionMenu(frameConteudo, values=[l["titulo"] for l in livros], width=400); sel_livro.pack(pady=6)
    sel_usuario = ctk.CTkOptionMenu(frameConteudo, values=[u["nome"] for u in usuarios], width=400); sel_usuario.pack(pady=6)

    def salvar():
        l = [x for x in livros if x["titulo"]==sel_livro.get()][0]
        u = [x for x in usuarios if x["nome"]==sel_usuario.get()][0]
        insert_loan(l["_id"],u["_id"])
        update_book(l["_id"],{"quantidade": l.get("quantidade",0)-1})
        messagebox.showinfo("Sucesso","Empréstimo realizado!")
        form_emprestimos()

    Button(frameConteudo,text="Emprestar",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# =========================================================
# ---------- Devoluções ----------
def form_devolucoes():
    limpar_conteudo()
    Label(frameConteudo,text="Devoluções",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    emprestimos_ativos = list_loans(active_only=True)
    if not emprestimos_ativos:
        Label(frameConteudo,text="Nenhum empréstimo ativo.",bg=CO_BRANCO).pack(); return

    valores = []
    emprestimos_validos = []
    for e in emprestimos_ativos:
        l = find_book(e.get("id_livro"))
        u = find_user(e.get("id_usuario"))
        if l and u:
            valores.append(f"{l['titulo']} - {u['nome']}")
            emprestimos_validos.append(e)

    if not valores:
        Label(frameConteudo,text="Nenhum empréstimo válido.",bg=CO_BRANCO).pack(); return

    sel = ctk.CTkOptionMenu(frameConteudo, values=valores, width=400); sel.pack(pady=6)

    def devolver():
        escolha = sel.get()
        idx = valores.index(escolha)
        e = emprestimos_validos[idx]
        return_loan(e["_id"])
        l = find_book(e.get("id_livro"))
        if l:
            update_book(l["_id"], {"quantidade": l.get("quantidade",0)+1})
        messagebox.showinfo("Sucesso","Devolução realizada!")
        form_devolucoes()

    Button(frameConteudo,text="Devolver",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=devolver).pack(pady=10)

# =========================================================
# ---------- Vendas ----------
def form_vendas():
    limpar_conteudo()
    Label(frameConteudo,text="Vendas",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    livros = [l for l in list_books() if l.get("quantidade",0)>0]
    usuarios = list_users()
    if not livros or not usuarios:
        Label(frameConteudo,text="Não há livros disponíveis ou usuários cadastrados.",bg=CO_BRANCO).pack()
        return

    sel_livro = ctk.CTkOptionMenu(frameConteudo, values=[l["titulo"] for l in livros], width=400); sel_livro.pack(pady=6)
    sel_usuario = ctk.CTkOptionMenu(frameConteudo, values=[u["nome"] for u in usuarios], width=400); sel_usuario.pack(pady=6)
    e_qtd = Entry(frameConteudo); e_qtd.pack(pady=6)

    def vender():
        l = [x for x in livros if x["titulo"]==sel_livro.get()][0]
        u = [x for x in usuarios if x["nome"]==sel_usuario.get()][0]
        qtd = int(e_qtd.get() or 1)
        if qtd > l.get("quantidade",0):
            messagebox.showwarning("Erro","Quantidade maior que disponível!")
            return
        insert_sale(l["_id"],u["_id"],quantidade=qtd,preco=l.get("preco"))
        update_book(l["_id"],{"quantidade": l.get("quantidade",0)-qtd})
        messagebox.showinfo("Sucesso","Venda realizada!")
        form_vendas()

    Button(frameConteudo,text="Vender",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=vender).pack(pady=10)

# =========================================================
# ---------- Histórico de Vendas ----------
def historico_vendas():
    limpar_conteudo()
    Label(frameConteudo,text="Histórico de Vendas",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    vendas = list_sales()
    dados = []
    for v in vendas:
        l = find_book(v.get("id_livro"))
        u = find_user(v.get("id_usuario"))
        if l and u:
            dados.append({"Livro":l["titulo"],"Usuário":u["nome"],"Quantidade":v.get("quantidade",1),
                          "Preço":v.get("preco"),"Data":v.get("data_venda")})
    if not dados:
        Label(frameConteudo,text="Nenhuma venda registrada.",bg=CO_BRANCO).pack(); return
    colunas = ["Livro","Usuário","Quantidade","Preço","Data"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# Botões Menu (mantendo nomes originais dos ícones)
# =========================================================
criar_botao_menu("Novo Usuário", form_novo_usuario, "usuario.png")
criar_botao_menu("Alterar Usuário", form_alterar_usuario, "editar_usuario.png")
criar_botao_menu("Listar Usuários", listar_usuarios, "lista_usuarios.png")
criar_botao_menu("Novo Livro", form_novo_livro, "livro.png")
criar_botao_menu("Alterar Livro", form_alterar_livro, "editar_livro.png")
criar_botao_menu("Listar Livros", listar_livros, "lista.png")
criar_botao_menu("Empréstimos", form_emprestimos, "emprestimo.png")
criar_botao_menu("Devoluções", form_devolucoes, "devolucao.png")
criar_botao_menu("Vendas", form_vendas, "venda.png")
criar_botao_menu("Histórico de Vendas", historico_vendas, "historico.png")

# =========================================================
# Inicia o Tkinter
# =========================================================
janela.mainloop()
