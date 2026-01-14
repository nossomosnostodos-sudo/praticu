# praticu.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from sqlj import conectar, criar_tabelas
from funções import adicionar_treino, listar_treinos

# garante que as tabelas existam
criar_tabelas()

# ================= APP PRINCIPAL =================
def abrir_app(nome_usuario, user_id):
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

    tk.Button(
        conteudo, text="Treinos",
        width=20, height=2,
        bg="#1d567c", fg="white",
        font=("Arial", 12),
        command=lambda: abrir_treinos(user_id)
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
        "SELECT id, usuario FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        user_id = resultado[0]
        nome_usuario = resultado[1]
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        janela.destroy()
        abrir_app(nome_usuario, user_id)
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
def abrir_treinos(usuario_id):
    # filtra apenas os treinos do usuário logado
    treinos = listar_treinos(usuario_id=usuario_id)

    tela = tk.Toplevel()
    tela.title("Treinos")
    tela.geometry("500x500")

    tk.Label(tela, text="Seus treinos", font=("Arial", 14, "bold")).pack(pady=10)

    lista = tk.Listbox(tela, width=50)
    lista.pack(pady=10)

    for treino in treinos:
        lista.insert(tk.END, treino[1])  # treino[1] = nome

    texto = tk.Text(tela, width=60, height=12)
    texto.pack(pady=10)

    def mostrar_treino():
        selecionado = lista.get(tk.ACTIVE)
        for treino in treinos:
            if treino[1] == selecionado:
                texto.delete("1.0", tk.END)
                texto.insert(tk.END, treino[2])  # treino[2] = descrição

    tk.Button(tela, text="Ver treino", width=20, command=mostrar_treino).pack(pady=5)

    # ------------------ CRIAR TREINO ------------------
    tk.Label(tela, text="Criar novo treino", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(tela, text="Nome do treino:").pack()
    entry_nome = tk.Entry(tela, width=40)
    entry_nome.pack()

    tk.Label(tela, text="Descrição do treino:").pack()
    entry_desc = tk.Text(tela, width=50, height=5)
    entry_desc.pack()

    def criar_treino():
        nome = entry_nome.get()
        descricao = entry_desc.get("1.0", tk.END).strip()
        if not nome or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        adicionar_treino(usuario_id, nome, descricao)
        messagebox.showinfo("Sucesso", "Treino criado!")
        lista.insert(tk.END, nome)
        entry_nome.delete(0, tk.END)
        entry_desc.delete("1.0", tk.END)

    tk.Button(tela, text="Criar treino", width=20, command=criar_treino).pack(pady=10)


janela.mainloop()
