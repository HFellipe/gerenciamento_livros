from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# =============================
# Conexão com MongoDB
# =============================
def connect():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["biblioteca"]
    return db

# =============================
# Funções CRUD - Livros
# =============================
def insert_book(titulo, autor, editora, ano_publicacao, isbn):
    db = connect()
    livro = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "ano_publicacao": ano_publicacao,
        "isbn": isbn
    }
    return db.livros.insert_one(livro).inserted_id

def list_books():
    db = connect()
    return list(db.livros.find())

def find_books_by_title(titulo):
    db = connect()
    return list(db.livros.find({"titulo": {"$regex": titulo, "$options": "i"}}))

# =============================
# Funções CRUD - Usuários
# =============================
def insert_user(nome, sobrenome, endereco, email, telefone):
    db = connect()
    usuario = {
        "nome": nome,
        "sobrenome": sobrenome,
        "endereco": endereco,
        "email": email,
        "telefone": telefone
    }
    return db.usuarios.insert_one(usuario).inserted_id

def list_users():
    db = connect()
    return list(db.usuarios.find())

def find_users_by_name(nome):
    db = connect()
    return list(db.usuarios.find({"nome": {"$regex": nome, "$options": "i"}}))

# =============================
# Funções CRUD - Empréstimos
# =============================
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao=None):
    db = connect()
    emprestimo = {
        "id_livro": ObjectId(id_livro),
        "id_usuario": ObjectId(id_usuario),
        "data_emprestimo": data_emprestimo,
        "data_devolucao": data_devolucao
    }
    return db.emprestimos.insert_one(emprestimo).inserted_id

def insert_loan_gui(livro_id, usuario_id):
    data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return insert_loan(livro_id, usuario_id, data_emprestimo)

def update_loan_return_date(id_emprestimo, data_devolucao):
    db = connect()
    db.emprestimos.update_one(
        {"_id": ObjectId(id_emprestimo)},
        {"$set": {"data_devolucao": data_devolucao}}
    )

def return_loan(loan_id):
    data_devolucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_loan_return_date(loan_id, data_devolucao)

def list_loans(active_only=False):
    db = connect()
    if active_only:
        return list(db.emprestimos.find({"data_devolucao": None}))
    else:
        return list(db.emprestimos.find())

# =============================
# Função para buscar empréstimos ativos de um livro
# =============================
def find_loans_by_book_title(titulo):
    db = connect()
    livros = find_books_by_title(titulo)
    if not livros:
        return []
    livros_ids = [l["_id"] for l in livros]
    return list(db.emprestimos.find({"id_livro": {"$in": livros_ids}, "data_devolucao": None}))

# =============================
# Funções auxiliares para debug (opcional)
# =============================
def exibir_livros():
    livros = list_books()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("📚 Livros:")
    for l in livros:
        print(f"{l['_id']} | {l['titulo']} - {l['autor']} ({l['ano_publicacao']}) ISBN:{l['isbn']}")

def exibir_usuarios():
    usuarios = list_users()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("👤 Usuários:")
    for u in usuarios:
        print(f"{u['_id']} | {u['nome']} {u['sobrenome']} - {u['email']} - {u['telefone']}")

def exibir_emprestimos():
    emprestimos = list_loans(active_only=True)
    if not emprestimos:
        print("Nenhum livro emprestado no momento.")
        return
    print("📖 Livros emprestados:")
    for e in emprestimos:
        print(f"{e['_id']} | Livro ID: {e['id_livro']} | Usuário ID: {e['id_usuario']} | Data: {e['data_emprestimo']}")