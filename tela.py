# tela.py - Sistema de Biblioteca completo
# ------------------------------------------------------------------

import os
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
import requests
from io import BytesIO
import customtkinter as ctk

# importa funções de dados e view (presume-se que dados.py e view.py estão corretos)
from dados import *
from view import exibir_tabela

# =========================================================
# Configurações visuais e janela principal
# =========================================================
CO_BRANCO = "#FEFEFE"
CO_PRETO = "#1C1C1C"
CO_AZUL = "#3498DB"
CO_VERDE = "#4FA882"
CO_AZUL_MARINHO = "#001F3F"
CO_AZUL_ROYAL = "#4169E1"
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
# Frames (topo, menu lateral, conteúdo)
# =========================================================
frameTopo = Frame(janela, bg=CO_DEGRADE_TOPO, height=70)
frameTopo.grid(row=0, column=0, columnspan=2, sticky="nsew")

frameMenu = Frame(janela, bg=CO_AZUL_MARINHO, width=220)
frameMenu.grid(row=1, column=0, sticky="ns")
frameMenu.grid_propagate(False)

frameConteudo = Frame(janela, bg=CO_BRANCO)
frameConteudo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# =========================================================
# Carregamento de ícones locais (pasta 'icones')
# =========================================================
_image_cache = {}  # manter referência para evitar coleta do Tk

def carregar_icone_local(nome, tamanho=(40, 40)):
    """Carrega um ícone da pasta 'icones' e retorna PhotoImage (ou None)."""
    path = os.path.join("icones", nome)
    if os.path.exists(path):
        try:
            img = Image.open(path).resize(tamanho)
            photo = ImageTk.PhotoImage(img)
            _image_cache[nome] = photo
            return photo
        except Exception:
            return None
    return None

# cabeçalho (logo + título)
img_logo = carregar_icone_local("cabecalho.png")
if img_logo:
    Label(frameTopo, image=img_logo, bg=CO_DEGRADE_TOPO).pack(side="left", padx=12, pady=10)

Label(frameTopo, text="Sistema de Biblioteca", font=("Arial", 20, "bold"),
      fg=CO_BRANCO, bg=CO_DEGRADE_TOPO).pack(side="left", pady=15)

# =========================================================
# Utilitários gerais
# =========================================================
def limpar_conteudo():
    """Remove todos os widgets do frame de conteúdo."""
    for w in frameConteudo.winfo_children():
        w.destroy()

def criar_botao_menu(texto, comando, icone_nome=None):
    """Cria um botão no menu lateral com possível ícone."""
    img = None
    if icone_nome:
        img = carregar_icone_local(icone_nome, (24, 24))
    if img:
        btn = Button(frameMenu, text="  " + texto, image=img, compound=LEFT, anchor="w",
                     bg=CO_AZUL_ROYAL, fg=CO_BRANCO, font=("Arial", 10, "bold"),
                     relief="flat", command=comando)
        btn.image = img
    else:
        btn = Button(frameMenu, text=texto, bg=CO_AZUL_ROYAL, fg=CO_BRANCO,
                     font=("Arial", 10, "bold"), relief="flat", anchor="w", command=comando)
    btn.pack(fill="x", pady=6, padx=8)
    btn.bind("<Enter>", lambda e: btn.config(bg=CO_AZUL))
    btn.bind("<Leave>", lambda e: btn.config(bg=CO_AZUL_ROYAL))
    return btn

# =========================================================
# Google Books (busca de metadados e thumbnail)
# =========================================================
def buscar_google_books(titulo='', isbn=''):
    """Consulta Google Books (retorna dicionário com titulo, autores, ano, thumbnail, descricao)."""
    try:
        q = f"isbn:{isbn}" if isbn else f"intitle:{titulo}"
        url = "https://www.googleapis.com/books/v1/volumes"
        resp = requests.get(url, params={"q": q, "maxResults": 5}, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items")
        if not items:
            return None
        vi = items[0].get("volumeInfo", {})
        titulo_api = vi.get("title","")
        autores = ", ".join(vi.get("authors",[])) if vi.get("authors") else ""
        published = vi.get("publishedDate","")
        ano = published.split("-")[0] if published else ""
        thumbnail = vi.get("imageLinks",{}).get("thumbnail")
        descricao = vi.get("description","") or ""
        return {"titulo":titulo_api,"autores":autores,"ano":ano,"thumbnail":thumbnail,"descricao":descricao}
    except Exception as e:
        print("Erro Google Books:", e)
        return None

def baixar_imagem_url(url, tamanho=(140,200)):
    """Baixa imagem de URL e converte para PhotoImage (cache)."""
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
# =========================================================
def form_novo_usuario():
    """Formulário para cadastrar novo usuário."""
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

def form_alterar_usuario():
    """Formulário para alterar usuário existente."""
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
        # procura pelo nome selecionado (se houver duplicidade, pega o primeiro)
        try:
            u = next(x for x in usuarios if x.get("nome") == sel.get())
        except StopIteration:
            return
        sel.usuario_atual = u.get("_id")
        e_nome.delete(0,END); e_nome.insert(0,u.get("nome",""))
        e_sob.delete(0,END); e_sob.insert(0,u.get("sobrenome",""))
        e_email.delete(0,END); e_email.insert(0,u.get("email",""))
        e_tel.delete(0,END); e_tel.insert(0,u.get("telefone",""))

    sel.configure(command=carregar_usuario)

    def salvar():
        if not hasattr(sel,"usuario_atual"): return
        dados = {"nome": e_nome.get().strip(),"sobrenome": e_sob.get().strip(),
                 "email": e_email.get().strip(),"telefone": e_tel.get().strip()}
        update_user(sel.usuario_atual,dados)
        messagebox.showinfo("Sucesso","Usuário atualizado!"); form_alterar_usuario()

    Button(frameConteudo,text="Salvar Alterações",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

def listar_usuarios():
    """Mostra todos os usuários em tabela (usa view.exibir_tabela)."""
    limpar_conteudo()
    dados = list_users()
    if not dados:
        Label(frameConteudo,text="Nenhum usuário cadastrado.",bg=CO_BRANCO).pack(); return
    colunas = ["nome","sobrenome","email","telefone"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# ---------- Livros ----------
# =========================================================
def form_novo_livro():
    """Formulário para cadastrar novo livro e opção de buscar capa no Google."""
    limpar_conteudo()
    Label(frameConteudo,text="Novo Livro",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    frm = Frame(frameConteudo,bg=CO_BRANCO); frm.pack(pady=6, fill="x")
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
        info = buscar_google_books(titulo=e_titulo.get().strip(), isbn=e_isbn.get().strip())
        if info and info.get("thumbnail"):
            im = baixar_imagem_url(info["thumbnail"])
            if im:
                lbl_capa.config(image=im); lbl_capa.image = im

    Button(frm,text="Google Livro",bg=CO_AZUL,fg=CO_BRANCO,command=mostrar_capa).grid(row=6,column=1,pady=6,sticky="w")

    def salvar():
        try:
            insert_book(e_titulo.get().strip(), e_autor.get().strip(), e_ano.get().strip(),
                        e_isbn.get().strip(), quantidade=int(e_qtd.get() or 1), preco=e_preco.get())
            messagebox.showinfo("Sucesso","Livro cadastrado!"); form_novo_livro()
        except Exception as ex:
            messagebox.showerror("Erro", str(ex))

    Button(frameConteudo,text="Cadastrar",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

def form_alterar_livro():
    """Formulário para alterar livro (com busca de capa também)."""
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
        try:
            l = next(x for x in livros if x.get("titulo")==sel.get())
        except StopIteration:
            return
        sel.livro_atual = l.get("_id")
        e_titulo.delete(0,END); e_titulo.insert(0,l.get("titulo",""))
        e_autor.delete(0,END); e_autor.insert(0,l.get("autor",""))
        e_ano.delete(0,END); e_ano.insert(0,l.get("ano_publicacao",""))
        e_isbn.delete(0,END); e_isbn.insert(0,l.get("isbn",""))
        e_qtd.delete(0,END); e_qtd.insert(0,l.get("quantidade",1))
        e_preco.delete(0,END); e_preco.insert(0,l.get("preco",""))

    sel.configure(command=carregar_livro)

    def mostrar_capa():
        info = buscar_google_books(titulo=e_titulo.get().strip(), isbn=e_isbn.get().strip())
        if info and info.get("thumbnail"):
            im = baixar_imagem_url(info["thumbnail"])
            if im:
                lbl_capa.config(image=im); lbl_capa.image = im

    Button(frm,text="Google Livro",bg=CO_AZUL,fg=CO_BRANCO,command=mostrar_capa).grid(row=6,column=1,pady=6,sticky="w")

    def salvar():
        if not hasattr(sel,"livro_atual"): return
        dados = {"titulo": e_titulo.get().strip(),"autor": e_autor.get().strip(),
                 "ano_publicacao": e_ano.get().strip(),"isbn": e_isbn.get().strip(),
                 "quantidade": int(e_qtd.get() or 1),"preco": e_preco.get()}
        update_book(sel.livro_atual,dados)
        messagebox.showinfo("Sucesso","Livro atualizado!"); form_alterar_livro()

    Button(frameConteudo,text="Salvar Alterações",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

def listar_livros():
    """Mostra todos os livros em tabela (usa view.exibir_tabela)."""
    limpar_conteudo()
    dados = list_books()
    if not dados:
        Label(frameConteudo,text="Nenhum livro cadastrado.",bg=CO_BRANCO).pack(); return
    colunas = ["titulo","autor","ano_publicacao","isbn","quantidade","preco"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# ---------- Empréstimos ----------
# =========================================================
def form_emprestimos():
    limpar_conteudo()
    Label(frameConteudo,text="Empréstimos",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)

    livros = [l for l in list_books() if l.get("quantidade",0)>0]
    usuarios = list_users()
    if not livros or not usuarios:
        Label(frameConteudo,text="Não há livros disponíveis ou usuários cadastrados.",bg=CO_BRANCO).pack(); return

    sel_livro = ctk.CTkOptionMenu(frameConteudo, values=[l.get("titulo","") for l in livros], width=400)
    sel_livro.pack(pady=6)
    sel_usuario = ctk.CTkOptionMenu(frameConteudo, values=[u.get("nome","") for u in usuarios], width=400)
    sel_usuario.pack(pady=6)

    def salvar():
        try:
            l = next(x for x in livros if x.get("titulo")==sel_livro.get())
            u = next(x for x in usuarios if x.get("nome")==sel_usuario.get())
        except StopIteration:
            messagebox.showwarning("Erro","Seleção inválida."); return

        insert_loan(l["_id"], u["_id"])
        update_book(l["_id"],{"quantidade": max(0, l.get("quantidade",0)-1)})
        messagebox.showinfo("Sucesso","Empréstimo realizado!")
        form_emprestimos()

    Button(frameConteudo,text="Emprestar",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=salvar).pack(pady=10)

# =========================================================
# ---------- Devoluções ----------
# =========================================================
def form_devolucoes():
    """Lista empréstimos ativos válidos e permite registrar devolução (com data/hora)."""
    limpar_conteudo()
    Label(frameConteudo,text="Devoluções",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)

    emprestimos_ativos = list_loans(active_only=True)
    if not emprestimos_ativos:
        Label(frameConteudo,text="Nenhum empréstimo ativo.",bg=CO_BRANCO).pack(); return

    valores = []
    emprestimos_validos = []

    # preparar lista ignorando registros incompletos
    for e in emprestimos_ativos:
        book_id = e.get("id_livro")
        user_id = e.get("id_usuario")
        if not book_id or not user_id:
            continue
        l = find_book(book_id)
        u = find_user(user_id)
        if l and u:
            valores.append(f"{l.get('titulo','(sem título)')} - {u.get('nome','(sem nome)')}")
            emprestimos_validos.append(e)

    if not valores:
        Label(frameConteudo,text="Nenhum empréstimo válido para devolução.",bg=CO_BRANCO).pack(); return

    sel = ctk.CTkOptionMenu(frameConteudo, values=valores, width=400); sel.pack(pady=6)

    def devolver():
        escolha = sel.get()
        try:
            idx = valores.index(escolha)
        except ValueError:
            messagebox.showwarning("Erro","Selecione um item válido."); return
        e = emprestimos_validos[idx]
        # registra devolução no banco (dados.return_loan já marca 'ativo': False; aqui
        # assumimos que return_loan também grava data_devolucao se a função em dados.py foi atualizada)
        return_loan(e["_id"])

        # atualizar quantidade do livro (se ainda existir)
        book_id = e.get("id_livro")
        livro = find_book(book_id)
        if livro:
            update_book(livro["_id"], {"quantidade": livro.get("quantidade",0)+1})

        messagebox.showinfo("Sucesso","Devolução realizada!")
        form_devolucoes()

    Button(frameConteudo,text="Devolver",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=devolver).pack(pady=10)

    # Mostrar histórico de devoluções (últimos devolvidos)
    Label(frameConteudo, text="Últimas Devoluções", font=("Arial",12,"bold"), bg=CO_BRANCO).pack(pady=(12,4))
    tabela = ttk.Treeview(frameConteudo, columns=("Livro","Usuário","Data Empréstimo","Data Devolução"), show="headings", height=6)
    tabela.heading("Livro", text="Livro"); tabela.heading("Usuário", text="Usuário")
    tabela.heading("Data Empréstimo", text="Data Empréstimo"); tabela.heading("Data Devolução", text="Data Devolução")
    tabela.pack(fill="x", pady=6)

    # carregar todos empréstimos (inclui ativos e inativos) e filtrar devolvidos
    todos = list_loans(active_only=False)
    for emp in reversed(todos):  # mostrar do mais recente para o mais antigo
        if not emp.get("data_devolucao"):
            continue
        book = find_book(emp.get("id_livro")); user = find_user(emp.get("id_usuario"))
        if not book or not user:
            continue
        # formatar datas se forem datetime
        de = emp.get("data_emprestimo")
        dd = emp.get("data_devolucao")
        if isinstance(de, datetime):
            de_display = de.strftime("%d/%m/%Y %H:%M")
        else:
            de_display = str(de)
        if isinstance(dd, datetime):
            dd_display = dd.strftime("%d/%m/%Y %H:%M")
        else:
            dd_display = str(dd)
        tabela.insert("", "end", values=(book.get("titulo"), user.get("nome"), de_display, dd_display))

# =========================================================
# ---------- Vendas ----------
# =========================================================
def form_vendas():
    limpar_conteudo()
    Label(frameConteudo,text="Vendas",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)

    livros = [l for l in list_books() if l.get("quantidade",0)>0]
    usuarios = list_users()
    if not livros or not usuarios:
        Label(frameConteudo,text="Não há livros disponíveis ou usuários cadastrados.",bg=CO_BRANCO).pack(); return

    sel_livro = ctk.CTkOptionMenu(frameConteudo, values=[l.get("titulo","") for l in livros], width=400); sel_livro.pack(pady=6)
    sel_usuario = ctk.CTkOptionMenu(frameConteudo, values=[u.get("nome","") for u in usuarios], width=400); sel_usuario.pack(pady=6)
    e_qtd = Entry(frameConteudo); e_qtd.pack(pady=6); e_qtd.insert(0,"1")

    def vender():
        try:
            l = next(x for x in livros if x.get("titulo")==sel_livro.get())
            u = next(x for x in usuarios if x.get("nome")==sel_usuario.get())
        except StopIteration:
            messagebox.showwarning("Erro","Seleção inválida."); return
        qtd = int(e_qtd.get() or 1)
        if qtd > l.get("quantidade",0):
            messagebox.showwarning("Erro","Quantidade maior que disponível!"); return
        insert_sale(l["_id"], u["_id"], quantidade=qtd, preco=l.get("preco"))
        update_book(l["_id"], {"quantidade": l.get("quantidade",0)-qtd})
        messagebox.showinfo("Sucesso","Venda realizada!"); form_vendas()

    Button(frameConteudo,text="Vender",bg=CO_VERDE,fg=CO_BRANCO,width=18,command=vender).pack(pady=10)

# =========================================================
# Histórico de Empréstimos
# =========================================================
def historico_emprestimos():
    """Mostra histórico (todos) de empréstimos com tratamento de registros incompletos."""
    limpar_conteudo()
    Label(frameConteudo, text="Histórico de Empréstimos", font=("Arial",14,"bold"), bg=CO_BRANCO).pack(pady=10)
    emprestimos = list_loans(active_only=False)
    dados = []
    for e in emprestimos:
        # ignorar registros incompletos
        if not e.get("id_livro") or not e.get("id_usuario"):
            continue
        l = find_book(e.get("id_livro")); u = find_user(e.get("id_usuario"))
        if not l or not u:
            continue
        de = e.get("data_emprestimo")
        dd = e.get("data_devolucao")
        de_display = de.strftime("%d/%m/%Y %H:%M") if isinstance(de, datetime) else str(de or "")
        dd_display = dd.strftime("%d/%m/%Y %H:%M") if isinstance(dd, datetime) else (str(dd) if dd else "Não devolvido")
        dados.append({"Livro": l.get("titulo"), "Usuário": u.get("nome"), "Data Empréstimo": de_display, "Data Devolução": dd_display})
    if not dados:
        Label(frameConteudo, text="Nenhum histórico de empréstimos.", bg=CO_BRANCO).pack(); return
    colunas = ["Livro","Usuário","Data Empréstimo","Data Devolução"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# Histórico de Vendas
# =========================================================
def historico_vendas():
    limpar_conteudo()
    Label(frameConteudo,text="Histórico de Vendas",font=("Arial",14,"bold"),bg=CO_BRANCO).pack(pady=10)
    vendas = list_sales()
    dados = []
    for v in vendas:
        # validar estrutura
        if not v.get("id_livro") or not v.get("id_usuario"):
            continue
        l = find_book(v.get("id_livro")); u = find_user(v.get("id_usuario"))
        if not l or not u:
            continue
        dv = v.get("data_venda")
        dv_display = dv.strftime("%d/%m/%Y %H:%M") if isinstance(dv, datetime) else str(dv or "")
        dados.append({"Livro": l.get("titulo"), "Usuário": u.get("nome"), "Quantidade": v.get("quantidade",1), "Preço": v.get("preco"), "Data": dv_display})
    if not dados:
        Label(frameConteudo, text="Nenhuma venda registrada.", bg=CO_BRANCO).pack(); return
    colunas = ["Livro","Usuário","Quantidade","Preço","Data"]
    exibir_tabela(frameConteudo,colunas,dados)

# =========================================================
# Botões de Menu (mantendo os nomes originais dos ícones)
# =========================================================
criar_botao_menu("Novo Usuário", form_novo_usuario, "usuario.png")
criar_botao_menu("Alterar Usuário", form_alterar_usuario, "editar_usuario.png")
criar_botao_menu("Listar Usuários", listar_usuarios, "lista_usuarios.png")

criar_botao_menu("Novo Livro", form_novo_livro, "livro.png")
criar_botao_menu("Alterar Livro", form_alterar_livro, "editar_livro.png")
criar_botao_menu("Listar Livros", listar_livros, "lista.png")

criar_botao_menu("Empréstimos", form_emprestimos, "emprestimo.png")
criar_botao_menu("Devoluções", form_devolucoes, "devolucao.png")

criar_botao_menu("Vendas", form_vendas, "vendas.png")

criar_botao_menu("Histórico Empréstimos", historico_emprestimos, "historico.png")
criar_botao_menu("Histórico Vendas", historico_vendas, "historico_vendas.png")

# =========================================================
# Inicializa exibindo a lista de livros
# =========================================================
listar_livros()

janela.mainloop()
