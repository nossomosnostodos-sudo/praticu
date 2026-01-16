import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk


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
    app.geometry("1280x720")
    app.resizable(False, False)
    app.configure(bg="#f2f2f2")

    # Topo

    topo = tk.Frame(app, bg="#C5C5C5", height=100)
    topo.grid(row=0, column=0, sticky="ew")
    topo.grid_columnconfigure(0, weight=1)
    topo.grid_columnconfigure(1, weight=1)

    #Praticu

    imagem_pu = Image.open("/home/aluno/Documentos/Praticu.jpeg")
    imagem_pu = imagem_pu.resize((260, 50))
    imagem_tk = ImageTk.PhotoImage(imagem_pu)

    label_img = tk.Label(topo, image=imagem_tk)
    label_img.image = imagem_tk  # evita a imagem sumir
    label_img.grid(row=0, column=0, sticky="w",padx=1,pady=0)

    #Perfil
    def perfil():
        print("")

    imagem = Image.open("/home/aluno/Documentos/perfil1.jpeg")
    imagem = imagem.resize((50, 50))
    imagem_tk = ImageTk.PhotoImage(imagem)

    botao_pf = tk.Button(
    topo,
    image=imagem_tk,
    command=perfil,
    bd=0,
    bg="#C5C5C5",
    activebackground="#C5C5C5"
    )

    botao_pf.image = imagem_tk  # evita a imagem sumir
    botao_pf.grid(row=0, column=1, sticky="e", padx=10, pady=10)


    # Conteúdo
    conteudo = tk.Frame(app, bg="#f2f2f2")
    conteudo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    for i in range(4):
       conteudo.grid_columnconfigure(i, weight=1)

    tk.Label(
        conteudo,
        text=f"Bem-vindo, {nome_usuario}!",
        bg="#f2f2f2",
        font=("Arial", 14)
    ).grid(row=0, column=2, columnspan=4, pady=10, sticky="n")

    #Treino

    tk.Button(
    conteudo, text="Treinos",
    width=20, height=2,
    bg="#1d567c", fg="white",
    font=("Arial", 12),
    command=abrir_treinos
    ).grid(row=2, column=2,columnspan=3, padx=10, pady=10)

    #Matricula

    tk.Button(
    conteudo, text="Planos de Matrícula",
    width=20, height=2,
    bg="#8e44ad", fg="white",
    font=("Arial", 12),
    command=abrir_planos
    ).grid(row=3, column=2,columnspan=3, padx=10, pady=10)

    #Sair

    tk.Button(
        conteudo, text="Sair",
        width=20, height=2,
        bg="#e74c3c", fg="white",
        font=("Arial", 12),
        command=app.destroy
    ).grid(row=4, column=2,columnspan=3, padx=10, pady=10)


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

# ================= TELA PLANOS =================

planos_matricula = [
    {
        "nome": "Básico",
        "duracao": "1 mês",
        "preco": "R$ 99",
        "beneficios": ["Acesso à academia"]
    },
    {
        "nome": "Padrão",
        "duracao": "3 meses",
        "preco": "R$ 270",
        "beneficios": ["Acesso à academia", "Treinos guiados"]
    },
    {
        "nome": "Premium",
        "duracao": "6 meses",
        "preco": "R$ 480",
        "beneficios": ["Acesso à academia", "Treinos guiados", "Avaliação física"]
    },
    {
        "nome": "VIP",
        "duracao": "12 meses",
        "preco": "R$ 900",
        "beneficios": ["Todos os benefícios anteriores", "Personal trainer 2x por semana"]
    }
]

def abrir_planos():
    tela = tk.Toplevel()
    tela.title("Planos de Matrícula")
    tela.geometry("450x450")
    tela.resizable(False, False)

    tk.Label(tela, text="Escolha um plano", font=("Arial", 14, "bold")).pack(pady=10)

    lista_planos = tk.Listbox(tela, width=50, height=6)
    lista_planos.pack(pady=10)

    for plano in planos_matricula:
        lista_planos.insert(tk.END, plano["nome"])

    texto = tk.Text(tela, width=50, height=10)
    texto.pack(pady=10)

    def mostrar_plano():
        if not lista_planos.curselection():
            messagebox.showwarning("Aviso", "Selecione um plano")
            return

        selecionado = lista_planos.get(lista_planos.curselection())
        for plano in planos_matricula:
            if plano["nome"] == selecionado:
                beneficios = "\n- ".join(plano["beneficios"])
                texto.delete("1.0", tk.END)
                texto.insert(tk.END,
                    f"Plano: {plano['nome']}\n"
                    f"Duração: {plano['duracao']}\n"
                    f"Preço: {plano['preco']}\n"
                    f"Benefícios:\n- {beneficios}"
                )
                break

    def escolher_plano():
        if not lista_planos.curselection():
            messagebox.showwarning("Aviso", "Selecione um plano")
            return
        selecionado = lista_planos.get(lista_planos.curselection())
        messagebox.showinfo("Plano escolhido", f"Você escolheu o plano: {selecionado}")

    tk.Button(tela, text="Ver plano", width=20, command=mostrar_plano).pack(pady=5)
    tk.Button(tela, text="Escolher plano", width=20, bg="#2ecc71", fg="white", command=escolher_plano).pack(pady=5)
    tk.Button(tela, text="Voltar", width=20, bg="#e74c3c", fg="white", command=tela.destroy).pack(pady=10)


janela.mainloop()
