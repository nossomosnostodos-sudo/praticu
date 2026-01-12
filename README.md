# praticu


import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================= BANCO DE DADOS =================

def conectar():
    return sqlite3.connect("usuarios.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

# ================= APP PRINCIPAL =================

def abrir_app(nome_usuario):
    app = tk.Tk()
    app.title("Praticu")
    app.geometry("360x520")
    app.resizable(False, False)
    app.configure(bg="#f2f2f2")

    # Topo
    topo = tk.Frame(app, bg="#2c3e50", height=60)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Praticu",
        bg="#2c3e50",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    # Conteúdo
    conteudo = tk.Frame(app, bg="#f2f2f2")
    conteudo.pack(expand=True)

    tk.Label(
        conteudo,
        text=f"Bem-vindo, {nome_usuario}!",
        bg="#f2f2f2",
        font=("Arial", 14)
    ).pack(pady=30)

    def opcao1():
        messagebox.showinfo("Opção 1", "Você clicou na opção 1")

    def opcao2():
        messagebox.showinfo("Opção 2", "Você clicou na opção 2")

    tk.Button(
    conteudo, text="Treinos",
    width=20, height=2,
    bg="#1d567c", fg="white",
    font=("Arial", 12),
    command=abrir_treinos
    ).pack(pady=10)

    tk.Button(
        conteudo, text="Matricula",
        width=20, height=2,
        bg="#1d567c", fg="white",
        font=("Arial", 12),
        command=opcao2
    ).pack(pady=10)

    tk.Button(
        conteudo, text="Sair",
        width=20, height=2,
        bg="#e74c3c", fg="white",
        font=("Arial", 12),
        command=app.destroy
    ).pack(pady=30)

    app.mainloop()

# ================= LOGIN =================

def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        janela.destroy()
        abrir_app(usuario)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

def abrir_tela_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro")
    cadastro.geometry("300x230")
    cadastro.resizable(False, False)

    tk.Label(cadastro, text="Novo Usuário:").pack(pady=(15, 0))
    entry_novo_usuario = tk.Entry(cadastro)
    entry_novo_usuario.pack()

    tk.Label(cadastro, text="Nova Senha:").pack(pady=(10, 0))
    entry_nova_senha = tk.Entry(cadastro, show="*")
    entry_nova_senha.pack()

    def cadastrar():
        usuario = entry_novo_usuario.get()
        senha = entry_nova_senha.get()

        if usuario == "" or senha == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                (usuario, senha)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            cadastro.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe")

    tk.Button(cadastro, text="Cadastrar", width=15, command=cadastrar).pack(pady=20)

# ================= TELA LOGIN =================

janela = tk.Tk()
janela.title("Login")
janela.geometry("300x240")
janela.resizable(False, False)

tk.Label(janela, text="Usuário:").pack(pady=(20, 0))
entry_usuario = tk.Entry(janela)
entry_usuario.pack()

tk.Label(janela, text="Senha:").pack(pady=(10, 0))
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack()

tk.Button(janela, text="Entrar", width=15, command=fazer_login).pack(pady=10)
tk.Button(janela, text="Cadastrar", width=15, command=abrir_tela_cadastro).pack()

# ================= TELA TREINOS =================
def abrir_treinos():
    treinos = {
        "Treino A - Peito e Tríceps": 
            "Supino reto – 3x10\nSupino inclinado – 3x10\nCrucifixo – 3x12\nTríceps pulley – 3x12\nMergulho – 3x10",

        "Treino B - Costas e Bíceps":
            "Puxada frontal – 3x10\nRemada curvada – 3x10\nRemada baixa – 3x12\nRosca direta – 3x10\nRosca alternada – 3x12",

        "Treino C - Pernas":
            "Agachamento – 4x10\nLeg press – 3x12\nCadeira extensora – 3x12\nMesa flexora – 3x12\nPanturrilha – 4x15",

        "Treino D - Ombro":
            "Desenvolvimento – 3x10\nElevação lateral – 3x12\nElevação frontal – 3x12\nRemada alta – 3x10",

        "Treino E - Cardio":
            "Esteira – 20 min\nBicicleta – 15 min\nCorda – 10 min"
    }

    tela = tk.Toplevel()
    tela.title("Treinos")
    tela.geometry("400x450")
    tela.resizable(False, False)

    tk.Label(tela, text="Escolha um treino", font=("Arial", 14, "bold")).pack(pady=10)

    lista = tk.Listbox(tela, width=45, height=8)
    lista.pack(pady=10)

    for treino in treinos:
        lista.insert(tk.END, treino)

    texto = tk.Text(tela, width=45, height=12)
    texto.pack(pady=10)

    def mostrar_treino():
        selecionado = lista.get(tk.ACTIVE)
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, treinos[selecionado])

    tk.Button(tela, text="Ver treino", width=20, command=mostrar_treino).pack(pady=5)

janela.mainloop()

