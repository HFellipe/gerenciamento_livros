import sqlite3

# conectar ao banco de dados
def connect():
    conn = sqlite3.connect('dados.db')
    return conn

# Função para inserir um novo livro
def insert_book(titulo, autor, editora, ano_publicacao, isbn):
    conn = connect()
    conn.execute("INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn)\
                 VALUES (?, ?, ?, ?, ?)",(titulo, autor, editora, ano_publicacao, isbn))
    conn.commit()
    conn.close()
    
# Funcao para inserir usuarios
def insert_user(nome, sobrenome, endereco, email, telefone):
    conn = connect()
    conn.execute("INSERT INTO usuarios(nome, sobrenome, endereco, email, telefone)\
                 VALUES(?, ?, ?, ?, ?)",(nome, sobrenome, endereco, email, telefone))
    conn.commit()
    conn.close()

# Funcao para exibir os livros
def exibir_livros():
    conn = connect()
    livros = conn.execute("SELECT * FROM livros").fetchall()
    conn.close()

    if not livros:
        print("Nenhum livro encontrado na biblioteca.")
        return
    
    print("Livros na biblioteca: ")
    for livro in livros:
        print(f"ID: {livro[0]}")
        print(f"Titulo: {livro[1]}")
        print(f"Autor: {livro[2]}")
        print(f"Editora: {livro[3]}")
        print(f"Ano de Publicacao: {livro[4]}")
        print(f"ISBN: {livro[5]}")
        print(f"\n")

# Funcao para realizar emprestimos
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao):
    conn = connect()
    conn.execute("INSERT INTO emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao)\
                 VALUES(?, ?, ?, ?)",(id_livro, id_usuario, data_emprestimo, data_devolucao))
    conn.commit()
    conn.close()

# Funcao para exibir todos os livros emprestados no momento
def get_books_on_loan():
    conn = connect()
    result = conn.execute("SELECT livros.titulo, usuarios.nome, usuarios.sobrenome, emprestimos.data_emprestimo, emprestimos.data_devolucao\
                          FROM livros\
                          INNER JOIN emprestimos ON livros.id = emprestimos.id_livro\
                          INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario\
                          WHERE emprestimos.data_devolucao IS NULL").fetchall()
    conn.close()
    return result

#Funcao para atualizar a data de devolucao de emprestimo
def update_loan_return_date(id_emprestimo, data_devolucao):
    conn = connect()
    conn.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (id_emprestimo, data_devolucao))
    conn.commit()
    conn.close()

# Exemplo de uso das funcoes
# insert_book("Dom Quixote", "Miguel", "Editora 1", 1855, "123456")
# insert_user("Joao", "Silva", "Brasil,Osasco", "joao@gmail.com", "+55 999")
# insert_loan(1,1,"2025-09-10", None)
livros_emprestados = get_books_on_loan()

print(livros_emprestados)

# update_loan_return_date(1, "2025-09-11")
exibir_livros()