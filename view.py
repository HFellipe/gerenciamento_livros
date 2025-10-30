# view.py - Exibição de tabelas no Tkinter
# Função para listar dados de forma simples em Treeview

from tkinter import ttk, Frame

def exibir_tabela(frame, colunas, dados):
    """
    Exibe uma tabela no frame dado
    colunas: lista de nomes de colunas
    dados: lista de dicionários
    """
    for widget in frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    for c in colunas:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor="center")

    for d in dados:
        valores = [d.get(c,"") for c in colunas]
        tree.insert("", "end", values=valores)

    tree.pack(expand=True, fill="both")
