import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from sqlj import conectar, criar_tabelas
from funções import adicionar_treino, listar_treinos
from sqlj import conectar
import sqlite3

#O from import com * n esta funcionando

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

# ---- CAMPOS LOGIN (livres para posicionar) ----
entry_usuario = tk.Entry(janela)
entry_usuario.place(x=270, y=213, width=200, height=25)  # posição inicial

entry_senha = tk.Entry(janela, show="*")
entry_senha.place(x=270, y=270, width=200, height=25)

btn_entrar = tk.Button(janela, text="Entrar", width=10)
btn_entrar.place(x=270, y=320)

btn_cadastrar = tk.Button(janela, text="Cadastrar", width=10, command=abrir_tela_cadastro )
btn_cadastrar.place(x=378, y=320)




# ================= FUNÇÕES =================
def abrir_app(nome_usuario, user_id):
    app = tk.Toplevel(janela)
    app.title("Praticu")
    app.geometry("800x500")
    app.resizable(False, False)

    try:
        img_app = Image.open("telainicial.png").resize((800,500))
        img_app_tk = ImageTk.PhotoImage(img_app)
        label_fundo_app = tk.Label(app, image=img_app_tk)
        label_fundo_app.place(x=0, y=0, relwidth=1, relheight=1)
        label_fundo_app.image = img_app_tk
    except Exception as e:
        print("Erro ao carregar imagem app:", e)

    # ---- BOTÕES E LABELS LIVRES ----
    lbl_bemvindo = tk.Label(app, text=f"Bem-vindo, {nome_usuario}!", bg="#ffffff")
    lbl_bemvindo.place(x=350, y=230)

    btn_treinos = tk.Button(app, text="Treinos", width=20, height=2, command=lambda: abrir_treinos(user_id))
    btn_treinos.place(x=310, y=270)

    btn_sair = tk.Button(app, text="Sair", width=20, height=2, command=app.destroy)
    btn_sair.place(x=310, y=370)

    #PERFIL

    def perfil():
        print("")

    imagem = Image.open("perfil1.jpeg")
    imagem = imagem.resize((70, 70))
    imagem_tk = ImageTk.PhotoImage(imagem)

    botao_pf = tk.Button(
    app,
    image=imagem_tk,
    command=perfil,
    bd=0,
    bg="#C5C5C5",
    activebackground="#C5C5C5"
    )

    botao_pf.image = imagem_tk  # evita a imagem sumir
    botao_pf.place(x=700, y=30)



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



#======================== TREINOS ==========================

def abrir_treinos(usuario_id):
    tela = tk.Toplevel()
    tela.title("Treinos")
    tela.geometry("650x650")
    tela.resizable(False, False)

    # ===== LISTA =====
    tk.Label(tela, text="Seus treinos", font=("Arial", 14, "bold")).pack(pady=5)

    lista = tk.Listbox(tela, width=50)
    lista.pack(pady=5)

    # ===== CAMPOS =====
    tk.Label(tela, text="Nome do treino").pack()
    entry_nome = tk.Entry(tela, width=50)
    entry_nome.pack()

    tk.Label(tela, text="Descrição do treino").pack()
    entry_desc = tk.Text(tela, width=60, height=8)
    entry_desc.pack(pady=5)

    treinos = []  # lista mutável

    # ===== CARREGAR TREINOS =====
    def carregar_treinos():
        treinos.clear()
        lista.delete(0, tk.END)

        dados = listar_treinos(usuario_id=usuario_id)
        treinos.extend(dados)

        for t in treinos:
            lista.insert(tk.END, t[1])

    carregar_treinos()

    # ===== SELECIONAR =====
    def selecionar_treino(event=None):
        if not lista.curselection():
            return

        treino = treinos[lista.curselection()[0]]

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, treino[1])

        entry_desc.delete("1.0", tk.END)
        entry_desc.insert(tk.END, treino[2])

    lista.bind("<<ListboxSelect>>", selecionar_treino)

    # ===== CRIAR =====
    def criar_treino():
        nome = entry_nome.get()
        descricao = entry_desc.get("1.0", tk.END).strip()

        if not nome or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        adicionar_treino(usuario_id, nome, descricao)
        messagebox.showinfo("Sucesso", "Treino criado!")

        entry_nome.delete(0, tk.END)
        entry_desc.delete("1.0", tk.END)

        carregar_treinos()

    # ===== EDITAR =====
    def editar_treino():
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Selecione um treino")
            return

        treino = treinos[lista.curselection()[0]]

        nome = entry_nome.get()
        descricao = entry_desc.get("1.0", tk.END).strip()

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE treinos SET nome=?, descricao=? WHERE id=? AND usuario_id=?",
            (nome, descricao, treino[0], usuario_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Treino atualizado!")
        carregar_treinos()

    # ===== EXCLUIR =====
    def excluir_treino():
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Selecione um treino")
            return

        treino = treinos[lista.curselection()[0]]

        if not messagebox.askyesno("Confirmação", "Deseja excluir este treino?"):
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM treinos WHERE id=? AND usuario_id=?",
            (treino[0], usuario_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Excluído", "Treino removido!")

        entry_nome.delete(0, tk.END)
        entry_desc.delete("1.0", tk.END)

        carregar_treinos()

    # ===== BOTÕES =====
    frame_botoes = tk.Frame(tela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Criar", width=12, command=criar_treino).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Editar", width=12, command=editar_treino).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Excluir", width=12, bg="#e74c3c", fg="white", command=excluir_treino).grid(row=0, column=2, padx=5)


janela.mainloop()
