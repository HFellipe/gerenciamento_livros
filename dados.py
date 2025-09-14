# arquivo: dados.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# --- Conexão com o MongoDB ---
def connect():
    """
    Retorna a conexão com o banco de dados 'biblioteca'.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["biblioteca"]
    return db

# --- CRUD Livros ---
def insert_book(titulo, autor, editora, ano_publicacao, isbn):
    """
    Insere um livro no banco de dados.
    Retorna o ID do livro inserido.
    """
    db = connect()
    try:
        ano_publicacao = int(ano_publicacao)
    except ValueError:
        raise ValueError("Ano de publicação deve ser um número inteiro")
    livro = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "ano_publicacao": ano_publicacao,
        "isbn": isbn
    }
    return db.livros.insert_one(livro).inserted_id

def list_books():
    """
    Retorna todos os livros cadastrados.
    """
    db = connect()
    return list(db.livros.find())

def find_books_by_title(titulo):
    """
    Busca livros pelo título (busca parcial, case-insensitive).
    """
    db = connect()
    return list(db.livros.find({"titulo": {"$regex": titulo, "$options": "i"}}))

# --- CRUD Usuários ---
def insert_user(nome, sobrenome, endereco, email, telefone):
    """
    Insere um usuário no banco de dados.
    Retorna o ID do usuário inserido.
    """
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
    """
    Retorna todos os usuários cadastrados.
    """
    db = connect()
    return list(db.usuarios.find())

def find_users_by_name(nome):
    """
    Busca usuários pelo nome (busca parcial, case-insensitive).
    """
    db = connect()
    return list(db.usuarios.find({"nome": {"$regex": nome, "$options": "i"}}))

# --- CRUD Empréstimos ---
def insert_loan(id_livro, id_usuario):
    """
    Registra um empréstimo de livro para usuário.
    Retorna o ID do empréstimo.
    """
    db = connect()
    emprestimo = {
        "id_livro": ObjectId(id_livro),
        "id_usuario": ObjectId(id_usuario),
        "data_emprestimo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_devolucao": None
    }
    return db.emprestimos.insert_one(emprestimo).inserted_id

def list_loans(active_only=False):
    """
    Lista todos os empréstimos.
    Se active_only=True, retorna apenas os não devolvidos.
    """
    db = connect()
    if active_only:
        return list(db.emprestimos.find({"data_devolucao": None}))
    return list(db.emprestimos.find())

def return_loan(loan_id):
    """
    Registra a devolução de um empréstimo pelo ID.
    Retorna True se o empréstimo foi atualizado, False caso contrário.
    """
    db = connect()
    loan_obj = ObjectId(loan_id)
    result = db.emprestimos.update_one(
        {"_id": loan_obj, "data_devolucao": None},
        {"$set": {"data_devolucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
    )
    return result.modified_count > 0

def find_loans_by_book_title(titulo):
    """
    Lista todos os empréstimos ativos de livros que contenham o título pesquisado.
    """
    db = connect()
    livros = db.livros.find({"titulo": {"$regex": titulo, "$options": "i"}})
    livros_ids = [livro["_id"] for livro in livros]
    return list(db.emprestimos.find({"id_livro": {"$in": livros_ids}, "data_devolucao": None}))