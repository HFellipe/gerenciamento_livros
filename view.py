# view.py - Funções de exibição de tabelas
from tkinter import *
from tkinter import ttk

def exibir_tabela(frame, colunas, dados):
    """
    Exibe tabela genérica usada pelo tela.py
    colunas = lista de strings
    dados = lista de dicionários
    """
    tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=12)

    # Cabeçalhos
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=150)

    # Inserir dados
    for item in dados:
        linha = [item.get(col, "") for col in colunas]
        tabela.insert("", "end", values=linha)

    tabela.pack(fill="both", expand=True, pady=10)
