# dados.py - Banco de Dados (MongoDB)
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# ============================================
# Conexão MongoDB
# ============================================
client = MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]

users = db["usuarios"]
books = db["livros"]
loans = db["emprestimos"]
sales = db["vendas"]

# ============================================
# ---------- Usuários ----------
# ============================================
def insert_user(nome, sobrenome, email, telefone):
    users.insert_one({
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email,
        "telefone": telefone
    })

def list_users():
    return list(users.find())

def find_user(id):
    try:
        return users.find_one({"_id": ObjectId(id)})
    except:
        return None

def update_user(id, dados):
    users.update_one({"_id": ObjectId(id)}, {"$set": dados})

# ============================================
# ---------- Livros ----------
# ============================================
def insert_book(titulo, autor, ano_publicacao, isbn, quantidade, preco):
    books.insert_one({
        "titulo": titulo,
        "autor": autor,
        "ano_publicacao": ano_publicacao,
        "isbn": isbn,
        "quantidade": quantidade,
        "preco": preco
    })

def list_books():
    return list(books.find())

def find_book(id):
    try:
        return books.find_one({"_id": ObjectId(id)})
    except:
        return None

def update_book(id, dados):
    books.update_one({"_id": ObjectId(id)}, {"$set": dados})

# ============================================
# ---------- Empréstimos ----------
# ============================================
def insert_loan(id_livro, id_usuario):
    loans.insert_one({
        "id_livro": id_livro,
        "id_usuario": id_usuario,
        "data_emprestimo": datetime.now(),
        "data_devolucao": None,
        "ativo": True
    })

def list_loans(active_only=False):
    if active_only:
        return list(loans.find({"ativo": True}))
    return list(loans.find())

def return_loan(id):
    loans.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"ativo": False, "data_devolucao": datetime.now()}}
    )

# ============================================
# ---------- Vendas ----------
# ============================================
def insert_sale(id_livro, id_usuario, quantidade, preco):
    sales.insert_one({
        "id_livro": id_livro,
        "id_usuario": id_usuario,
        "quantidade": quantidade,
        "preco": preco,
        "data_venda": datetime.now()
    })

def list_sales():
    return list(sales.find())
