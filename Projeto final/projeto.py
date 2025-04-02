import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Funções do banco de dados
def conectar():
    return sqlite3.connect('leads.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL,
        interesse TEXT NOT NULL,
        status TEXT NOT NULL              
        )       
    ''')
    conn.commit()
    conn.close()

# Funções CRUD
def inserir_lead():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    interesse = combo_interesse.get()
    status = combo_status.get()
    
    if nome and email and telefone and interesse and status:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO leads(nome, email, telefone, interesse, status) VALUES(?,?,?,?,?)', 
                 (nome, email, telefone, interesse, status))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'LEAD CADASTRADO COM SUCESSO!') 
        mostrar_lead()
    else:
        messagebox.showerror('ERRO', 'PREENCHA TODOS OS CAMPOS!') 

def mostrar_lead():
    for row in tree.get_children():   
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()    
    c.execute('SELECT * FROM leads')
    leads = c.fetchall()
    for lead in leads:
        tree.insert("", "end", values=(lead[0], lead[1], lead[2], lead[3], lead[4], lead[5]))
    conn.close()

def delete_lead():
    dado_del = tree.selection()
    if dado_del:
       lead_id = tree.item(dado_del)['values'][0]
       conn = conectar()
       c = conn.cursor()    
       c.execute('DELETE FROM leads WHERE id = ? ',(lead_id,))
       conn.commit()
       conn.close()
       messagebox.showinfo('', 'LEAD REMOVIDO')
       mostrar_lead()
    else:
       messagebox.showerror('', 'SELECIONE UM LEAD PARA REMOVER')  

def editar():
    selecao = tree.selection()
    if selecao:
        lead_id = tree.item(selecao)['values'][0]
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_telefone = entry_telefone.get()
        novo_interesse = combo_interesse.get()
        novo_status = combo_status.get()

        if novo_nome and novo_email and novo_telefone and novo_interesse and novo_status:
            conn = conectar()
            c = conn.cursor()    
            c.execute('''UPDATE leads SET 
                       nome = ?, 
                       email = ?, 
                       telefone = ?,
                       interesse = ?,
                       status = ?
                       WHERE id = ? ''',
                       (novo_nome, novo_email, novo_telefone, novo_interesse, novo_status, lead_id))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'LEAD ATUALIZADO')
            mostrar_lead()
        else:
            messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')
    else:
        messagebox.showerror('','SELECIONE UM LEAD PARA EDITAR')

# Interface gráfica
janela = tk.Tk()
janela.title('Sistema de Gerenciamento de Leads')
janela.configure(bg='#B8D8FF') 

# Formulário

label_nome = tk.Label(janela, text='Nome:',bg='#B8D8FF', )
label_nome.grid(row=0, column=0, padx=10, pady=5)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_email = tk.Label(janela, text='Email:',bg='#B8D8FF')
label_email.grid(row=1, column=0, padx=10, pady=5)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=10, pady=5)

label_telefone = tk.Label(janela, text='Telefone:',bg='#B8D8FF')
label_telefone.grid(row=2, column=0, padx=10, pady=5)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=2, column=1, padx=10, pady=5)

label_interesse = tk.Label(janela, text='Interesse:',bg='#B8D8FF')
label_interesse.grid(row=3, column=0, padx=10, pady=5)
interesses = ['Site', 'Redes Sociais', 'SEO', 'Google Ads', 'Outro']
combo_interesse = ttk.Combobox(janela, values=interesses)
combo_interesse.grid(row=3, column=1, padx=10, pady=5)

label_status = tk.Label(janela, text='Status:',bg='#B8D8FF')
label_status.grid(row=4, column=0, padx=10, pady=5)
status_opcoes = ['Novo', 'Em andamento', 'Convertido', 'Perdido']
combo_status = ttk.Combobox(janela, values=status_opcoes)
combo_status.grid(row=4, column=1, padx=10, pady=5)

# Botões
btn_salvar = tk.Button(janela, text='Salvar',  bg='#4CAF50', fg='white' ,command=inserir_lead)
btn_salvar.grid(row=5, column=0, padx=5, pady=10)

btn_deletar = tk.Button(janela, text='Deletar',bg='#F44336', fg='white', command=delete_lead)
btn_deletar.grid(row=5, column=1, padx=5, pady=10)

btn_atualizar = tk.Button(janela, text='Atualizar', bg='#2196F3', fg='white', command=editar)
btn_atualizar.grid(row=5, column=2, padx=5, pady=10)

# Lista de leads
columns = ('ID', 'Nome', 'Email', 'Telefone', 'Interesse', 'Status')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Configurar cabeçalhos e colunas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Inicialização
criar_tabela()
mostrar_lead()

janela.mainloop()