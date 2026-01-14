# praticu.py

from sqlj import conectar
import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================= APP PRINCIPAL =================

def abrir_app(nome_usuario):
    app = tk.Tk()
    app.title("Praticu")
    app.geometry("360x520")
    app.resizable(False, False)
    app.configure(bg="#f2f2f2")

    topo = tk.Frame(app, bg="#2c3e50", height=60)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Praticu",
        bg="#2c3e50",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    conteudo = tk.Frame(app, bg="#f2f2f2")
    conteudo.pack(expand=True)

    tk.Label(
        conteudo,
        text=f"Bem-vindo, {nome_usuario}!",
        bg="#f2f2f2",
        font=("Arial", 14)
    ).pack(pady=30)

    tk.Button(
        conteudo, text="Treinos",
        width=20, height=2,
        bg="#1d567c", fg="white",
        font=("Arial", 12),
        command=abrir_treinos
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

        if not usuario or not senha:
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
        "Treino A - Peito e Tríceps": "Supino reto – 3x10\nSupino inclinado – 3x10",
        "Treino B - Costas e Bíceps": "Puxada frontal – 3x10\nRosca direta – 3x10",
        "Treino C - Pernas": "Agachamento – 4x10\nLeg press – 3x12"
    }

    tela = tk.Toplevel()
    tela.title("Treinos")
    tela.geometry("400x450")

    lista = tk.Listbox(tela, width=45)
    lista.pack(pady=10)

    for treino in treinos:
        lista.insert(tk.END, treino)

    texto = tk.Text(tela, width=45, height=12)
    texto.pack()

    def mostrar():
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, treinos[lista.get(tk.ACTIVE)])

    tk.Button(tela, text="Ver treino", command=mostrar).pack(pady=10)

janela.mainloop()
