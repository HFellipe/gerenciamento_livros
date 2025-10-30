# dados.py - Funções de acesso a dados usando MongoDB
# Desenvolvido para um sistema de biblioteca
# =========================================================

from pymongo import MongoClient
from datetime import datetime

# =========================================================
# Conexão com MongoDB
# =========================================================
# Substitua "biblioteca" pelo nome do seu banco
client = MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]

# Coleções
USUARIOS = db["usuarios"]
LIVROS = db["livros"]
EMPRESTIMOS = db["emprestimos"]
VENDAS = db["vendas"]

# =========================================================
# ---------- Usuários ----------
# =========================================================
def insert_user(nome, sobrenome, email, telefone):
    """Adiciona um novo usuário ao banco"""
    USUARIOS.insert_one({
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email,
        "telefone": telefone
    })

def list_users():
    """Retorna todos os usuários"""
    return list(USUARIOS.find())

def update_user(user_id, dados):
    """Atualiza os dados do usuário pelo _id"""
    USUARIOS.update_one({"_id": user_id}, {"$set": dados})

def find_user(registro):
    """
    Busca usuário a partir de um empréstimo ou venda
    registro: dicionário que contém "id_usuario"
    """
    user_id = registro.get("id_usuario")
    if user_id:
        return USUARIOS.find_one({"_id": user_id})
    return None

# =========================================================
# ---------- Livros ----------
# =========================================================
def insert_book(titulo, autor, ano_publicacao, isbn, quantidade=1, preco=0):
    """Adiciona um novo livro ao banco"""
    LIVROS.insert_one({
        "titulo": titulo,
        "autor": autor,
        "ano_publicacao": ano_publicacao,
        "isbn": isbn,
        "quantidade": quantidade,
        "preco": preco
    })

def list_books():
    """Retorna todos os livros"""
    return list(LIVROS.find())

def update_book(book_id, dados):
    """Atualiza os dados do livro pelo _id"""
    LIVROS.update_one({"_id": book_id}, {"$set": dados})

def find_book(registro):
    """
    Busca livro a partir de um empréstimo ou venda
    registro: dicionário que contém "id_livro"
    """
    book_id = registro.get("id_livro")
    if book_id:
        return LIVROS.find_one({"_id": book_id})
    return None

# =========================================================
# ---------- Empréstimos ----------
# =========================================================
def insert_loan(book_id, user_id):
    """Registra um novo empréstimo"""
    EMPRESTIMOS.insert_one({
        "id_livro": book_id,
        "id_usuario": user_id,
        "data_emprestimo": datetime.now(),
        "ativo": True
    })

def list_loans(active_only=False):
    """Retorna todos os empréstimos ou apenas os ativos"""
    if active_only:
        return list(EMPRESTIMOS.find({"ativo": True}))
    return list(EMPRESTIMOS.find())

def return_loan(loan_id):
    """Marca um empréstimo como devolvido"""
    EMPRESTIMOS.update_one({"_id": loan_id}, {"$set": {"ativo": False}})

# =========================================================
# ---------- Vendas ----------
# =========================================================
def insert_sale(book_id, user_id, quantidade=1, preco=0):
    """Registra uma venda"""
    VENDAS.insert_one({
        "id_livro": book_id,
        "id_usuario": user_id,
        "quantidade": quantidade,
        "preco": preco,
        "data_venda": datetime.now()
    })

def list_sales():
    """Retorna todas as vendas"""
    return list(VENDAS.find())
