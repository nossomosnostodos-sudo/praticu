import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
from sqlj import conectar, criar_tabelas
from funções import adicionar_treino, listar_treinos

criar_tabelas()

# ================= TELA LOGIN =================
janela = tk.Tk()
janela.title("Login")
janela.geometry("800x500")
janela.resizable(False, False)

# ---- IMAGEM DE FUNDO ----
try:
    img_login = Image.open("tela3bloqueio.png").resize((800, 500))
    img_login_tk = ImageTk.PhotoImage(img_login)
    label_fundo = tk.Label(janela, image=img_login_tk)
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fundo.image = img_login_tk
except Exception as e:
    print("Erro ao carregar imagem de fundo:", e)

# ---- CAMPOS LOGIN (livres para posicionar) ----
entry_usuario = tk.Entry(janela)
entry_usuario.place(x=100, y=150, width=200, height=25)  # posição inicial

entry_senha = tk.Entry(janela, show="*")
entry_senha.place(x=100, y=200, width=200, height=25)

btn_entrar = tk.Button(janela, text="Entrar", width=15)
btn_entrar.place(x=100, y=250)

btn_cadastrar = tk.Button(janela, text="Cadastrar", width=15)
btn_cadastrar.place(x=100, y=300)

# ================= FUNÇÕES =================
def abrir_app(nome_usuario, user_id):
    app = tk.Toplevel(janela)
    app.title("Praticu")
    app.geometry("800x500")
    app.resizable(False, False)

    try:
        img_app = Image.open("telalogin.png").resize((800,500))
        img_app_tk = ImageTk.PhotoImage(img_app)
        label_fundo_app = tk.Label(app, image=img_app_tk)
        label_fundo_app.place(x=0, y=0, relwidth=1, relheight=1)
        label_fundo_app.image = img_app_tk
    except Exception as e:
        print("Erro ao carregar imagem app:", e)

    # ---- BOTÕES E LABELS LIVRES ----
    lbl_bemvindo = tk.Label(app, text=f"Bem-vindo, {nome_usuario}!", bg="#ffffff")
    lbl_bemvindo.place(x=50, y=50)

    btn_treinos = tk.Button(app, text="Treinos", width=20, height=2, command=lambda: abrir_treinos(user_id))
    btn_treinos.place(x=50, y=100)

    btn_sair = tk.Button(app, text="Sair", width=20, height=2, command=app.destroy)
    btn_sair.place(x=50, y=160)

def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        user_id = resultado[0]
        nome_usuario = resultado[1]
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        janela.withdraw()
        abrir_app(nome_usuario, user_id)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

btn_entrar.config(command=fazer_login)

def abrir_treinos(usuario_id):
    treinos = listar_treinos(usuario_id=usuario_id)
    tela = tk.Toplevel()
    tela.title("Treinos")
    tela.geometry("500x500")
    # lista, texto e botões livres
    lista = tk.Listbox(tela, width=50)
    lista.place(x=20, y=20)
    for treino in treinos:
        lista.insert(tk.END, treino[1])
    texto = tk.Text(tela, width=50, height=12)
    texto.place(x=20, y=250)
    # criar treino e mostrar treino...
    # você pode reposicionar os widgets manualmente

btn_cadastrar.config(command=lambda: messagebox.showinfo("Cadastro", "Você vai criar a tela de cadastro aqui"))

janela.mainloop()
