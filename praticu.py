"""
Praticu - Versao refatorada usando principios da Programacao Orientada a Objetos (POO)

Principais conceitos aplicados:
- Encapsulamento: cada janela guarda seus proprios widgets e dados como atributos de
  instancia (self.xxx), eliminando variaveis globais e closures soltas do codigo original.
- Abstracao: as classes Usuario e Treino representam os dados do dominio; as classes
  UsuarioRepository e TreinoRepository escondem os detalhes de acesso ao banco (SQL).
  Quem usa um repositorio so chama metodos como criar(), listar_por_usuario(), etc.
- Heranca: a mixin JanelaComFundo e reaproveitada por mais de uma janela (Login e
  Tela Principal); todas as janelas secundarias herdam de tk.Toplevel.
- Polimorfismo: cada janela implementa seu proprio metodo _construir_interface(),
  chamado de forma uniforme no __init__, mas com comportamento especifico em cada classe.
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from sqlj import conectar, criar_tabelas
from funções import adicionar_treino, listar_treinos


# ============================================================
# MODELOS (entidades do dominio) -> ABSTRACAO
# ============================================================

class Usuario:
    """Representa um usuario do sistema."""

    def __init__(self, id_usuario, nome, senha=None):
        self._id = id_usuario
        self._nome = nome
        self._senha = senha

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        if not novo_nome:
            raise ValueError("Nome de usuario nao pode ser vazio")
        self._nome = novo_nome


class Treino:
    """Representa um treino pertencente a um usuario."""

    def __init__(self, id_treino, nome, descricao, usuario_id):
        self.id = id_treino
        self.nome = nome
        self.descricao = descricao
        self.usuario_id = usuario_id


# ============================================================
# REPOSITORIOS (acesso a dados) -> ABSTRACAO / ENCAPSULAMENTO
# Ninguem fora destas classes precisa saber como o SQL e escrito.
# ============================================================

class UsuarioRepository:
    """Centraliza todo o acesso a tabela 'usuarios'."""

    def autenticar(self, nome, senha):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, usuario FROM usuarios WHERE usuario=? AND senha=?",
            (nome, senha),
        )
        resultado = cursor.fetchone()
        conn.close()
        return Usuario(*resultado) if resultado else None

    def buscar_por_id(self, usuario_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario FROM usuarios WHERE id=?", (usuario_id,))
        dados = cursor.fetchone()
        conn.close()
        return Usuario(*dados) if dados else None

    def criar(self, nome, senha):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (nome, senha)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def atualizar(self, usuario_id, novo_nome, nova_senha=None):
        conn = conectar()
        cursor = conn.cursor()
        if nova_senha:
            cursor.execute(
                "UPDATE usuarios SET usuario=?, senha=? WHERE id=?",
                (novo_nome, nova_senha, usuario_id),
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET usuario=? WHERE id=?", (novo_nome, usuario_id)
            )
        conn.commit()
        conn.close()


class TreinoRepository:
    """Centraliza todo o acesso aos dados de treinos."""

    def listar_por_usuario(self, usuario_id):
        dados = listar_treinos(usuario_id=usuario_id)
        return [Treino(d[0], d[1], d[2], usuario_id) for d in dados]

    def criar(self, usuario_id, nome, descricao):
        adicionar_treino(usuario_id, nome, descricao)

    def atualizar(self, treino_id, usuario_id, nome, descricao):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE treinos SET nome=?, descricao=? WHERE id=? AND usuario_id=?",
            (nome, descricao, treino_id, usuario_id),
        )
        conn.commit()
        conn.close()

    def excluir(self, treino_id, usuario_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM treinos WHERE id=? AND usuario_id=?",
            (treino_id, usuario_id),
        )
        conn.commit()
        conn.close()


# ============================================================
# MIXIN DE INTERFACE -> HERANCA / POLIMORFISMO
# ============================================================

class JanelaComFundo:
    """
    Mixin reaproveitada por mais de uma janela (heranca).
    Cada janela que a usa pode ter uma imagem de fundo diferente,
    mas todas chamam o mesmo metodo (polimorfismo de uso).
    """

    def _definir_imagem_fundo(self, caminho, tamanho):
        try:
            imagem = Image.open(caminho).resize(tamanho)
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_fundo = tk.Label(self, image=imagem_tk)
            label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
            label_fundo.image = imagem_tk  # evita garbage collection
            return label_fundo
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo ({caminho}):", e)
            return None


# ============================================================
# JANELAS (camada de apresentacao) -> ENCAPSULAMENTO
# Cada janela guarda seus proprios widgets e estado em self,
# em vez de variaveis globais como no codigo original.
# ============================================================

class JanelaCadastro(tk.Toplevel):
    """Janela de cadastro de novo usuario."""

    def __init__(self, master, usuario_repo: UsuarioRepository):
        super().__init__(master)
        self.usuario_repo = usuario_repo
        self.title("Cadastro")
        self.geometry("400x300")
        self.resizable(False, False)
        self._construir_interface()

    def _construir_interface(self):
        tk.Label(self, text="Criar Conta", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Nome de usuario").pack()
        self.entry_usuario = tk.Entry(self, width=30)
        self.entry_usuario.pack(pady=5)

        tk.Label(self, text="Senha").pack()
        self.entry_senha = tk.Entry(self, width=30, show="*")
        self.entry_senha.pack(pady=5)

        tk.Label(self, text="Confirmar senha").pack()
        self.entry_confirmar = tk.Entry(self, width=30, show="*")
        self.entry_confirmar.pack(pady=5)

        tk.Button(self, text="Cadastrar", width=15, command=self._cadastrar).pack(pady=15)

    def _cadastrar(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()

        if not usuario or not senha or not confirmar:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas nao coincidem")
            return

        if self.usuario_repo.criar(usuario, senha):
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Esse nome de usuario ja existe")


class JanelaPerfil(tk.Toplevel):
    """Janela de edicao do perfil do usuario logado."""

    def __init__(self, master, usuario_repo: UsuarioRepository, usuario: Usuario):
        super().__init__(master)
        self.usuario_repo = usuario_repo
        self.usuario = usuario
        self.title("Perfil")
        self.geometry("400x300")
        self.resizable(False, False)
        self._construir_interface()

    def _construir_interface(self):
        tk.Label(self, text="Meu Perfil", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Nome de usuario").pack()
        self.entry_nome = tk.Entry(self, width=30)
        self.entry_nome.pack(pady=5)
        self.entry_nome.insert(0, self.usuario.nome)

        tk.Label(self, text="Nova senha").pack()
        self.entry_senha = tk.Entry(self, width=30, show="*")
        self.entry_senha.pack(pady=5)

        tk.Label(self, text="Confirmar senha").pack()
        self.entry_confirmar = tk.Entry(self, width=30, show="*")
        self.entry_confirmar.pack(pady=5)

        tk.Button(self, text="Salvar", width=15, command=self._salvar).pack(pady=15)

    def _salvar(self):
        novo_nome = self.entry_nome.get()
        nova_senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()

        try:
            self.usuario.nome = novo_nome  # usa o setter com validacao (encapsulamento)
        except ValueError as erro:
            messagebox.showwarning("Aviso", str(erro))
            return

        if nova_senha and nova_senha != confirmar:
            messagebox.showerror("Erro", "As senhas nao coincidem")
            return

        self.usuario_repo.atualizar(
            self.usuario.id, novo_nome, nova_senha if nova_senha else None
        )
        messagebox.showinfo("Sucesso", "Perfil atualizado!")
        self.destroy()


class JanelaTreinos(tk.Toplevel):
    """Janela de CRUD (criar, editar, excluir) de treinos do usuario."""

    def __init__(self, master, treino_repo: TreinoRepository, usuario_id):
        super().__init__(master)
        self.treino_repo = treino_repo
        self.usuario_id = usuario_id
        self.treinos = []  # cache local da lista carregada

        self.title("Treinos")
        self.geometry("650x650")
        self.resizable(False, False)
        self._construir_interface()
        self._carregar_treinos()

    def _construir_interface(self):
        tk.Label(self, text="Seus treinos", font=("Arial", 14, "bold")).pack(pady=5)

        self.lista = tk.Listbox(self, width=50)
        self.lista.pack(pady=5)
        self.lista.bind("<<ListboxSelect>>", self._selecionar_treino)

        tk.Label(self, text="Nome do treino").pack()
        self.entry_nome = tk.Entry(self, width=50)
        self.entry_nome.pack()

        tk.Label(self, text="Descricao do treino").pack()
        self.entry_desc = tk.Text(self, width=60, height=8)
        self.entry_desc.pack(pady=5)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Criar", width=12, command=self._criar_treino).grid(
            row=0, column=0, padx=5
        )
        tk.Button(frame_botoes, text="Editar", width=12, command=self._editar_treino).grid(
            row=0, column=1, padx=5
        )
        tk.Button(
            frame_botoes,
            text="Excluir",
            width=12,
            bg="#e74c3c",
            fg="white",
            command=self._excluir_treino,
        ).grid(row=0, column=2, padx=5)

    def _carregar_treinos(self):
        self.treinos = self.treino_repo.listar_por_usuario(self.usuario_id)
        self.lista.delete(0, tk.END)
        for treino in self.treinos:
            self.lista.insert(tk.END, treino.nome)

    def _treino_selecionado(self):
        selecao = self.lista.curselection()
        if not selecao:
            return None
        return self.treinos[selecao[0]]

    def _selecionar_treino(self, event=None):
        treino = self._treino_selecionado()
        if treino is None:
            return
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, treino.nome)
        self.entry_desc.delete("1.0", tk.END)
        self.entry_desc.insert(tk.END, treino.descricao)

    def _limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_desc.delete("1.0", tk.END)

    def _criar_treino(self):
        nome = self.entry_nome.get()
        descricao = self.entry_desc.get("1.0", tk.END).strip()

        if not nome or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        self.treino_repo.criar(self.usuario_id, nome, descricao)
        messagebox.showinfo("Sucesso", "Treino criado!")
        self._limpar_campos()
        self._carregar_treinos()

    def _editar_treino(self):
        treino = self._treino_selecionado()
        if treino is None:
            messagebox.showwarning("Aviso", "Selecione um treino")
            return

        nome = self.entry_nome.get()
        descricao = self.entry_desc.get("1.0", tk.END).strip()

        self.treino_repo.atualizar(treino.id, self.usuario_id, nome, descricao)
        messagebox.showinfo("Sucesso", "Treino atualizado!")
        self._carregar_treinos()

    def _excluir_treino(self):
        treino = self._treino_selecionado()
        if treino is None:
            messagebox.showwarning("Aviso", "Selecione um treino")
            return

        if not messagebox.askyesno("Confirmacao", "Deseja excluir este treino?"):
            return

        self.treino_repo.excluir(treino.id, self.usuario_id)
        messagebox.showinfo("Excluido", "Treino removido!")
        self._limpar_campos()
        self._carregar_treinos()


class JanelaPrincipal(tk.Toplevel, JanelaComFundo):
    """Tela inicial exibida apos o login (herda de Toplevel e do mixin de fundo)."""

    def __init__(self, master, usuario_repo, treino_repo, usuario: Usuario):
        super().__init__(master)
        self.usuario_repo = usuario_repo
        self.treino_repo = treino_repo
        self.usuario = usuario

        self.title("Praticu")
        self.geometry("800x500")
        self.resizable(False, False)
        self._construir_interface()

    def _construir_interface(self):
        self._definir_imagem_fundo("telainicial.png", (800, 500))

        tk.Label(self, text=f"Bem-vindo, {self.usuario.nome}!", bg="#ffffff").place(
            x=350, y=230
        )

        tk.Button(
            self, text="Treinos", width=20, height=2, command=self._abrir_treinos
        ).place(x=310, y=270)

        tk.Button(self, text="Sair", width=20, height=2, command=self.destroy).place(
            x=310, y=370
        )

        try:
            imagem = Image.open("perfil1.jpeg").resize((70, 70))
            self._imagem_perfil = ImageTk.PhotoImage(imagem)  # mantem referencia
            tk.Button(
                self,
                image=self._imagem_perfil,
                command=self._abrir_perfil,
                bd=0,
                bg="#800080",
                activebackground="#C5C5C5",
                highlightthickness=3,
            ).place(x=700, y=30)
        except Exception as e:
            print("Erro ao carregar imagem de perfil:", e)

    def _abrir_perfil(self):
        JanelaPerfil(self, self.usuario_repo, self.usuario)

    def _abrir_treinos(self):
        JanelaTreinos(self, self.treino_repo, self.usuario.id)


class AplicativoLogin(tk.Tk, JanelaComFundo):
    """Janela principal da aplicacao: tela de login (herda do mixin de fundo)."""

    def __init__(self):
        super().__init__()
        self.usuario_repo = UsuarioRepository()
        self.treino_repo = TreinoRepository()

        self.title("Login")
        self.geometry("800x500")
        self.resizable(False, False)
        self._construir_interface()

    def _construir_interface(self):
        self._definir_imagem_fundo("tela3bloqueio.png", (800, 500))

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.place(x=270, y=213, width=200, height=25)

        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.place(x=270, y=270, width=200, height=25)

        tk.Button(self, text="Entrar", width=10, command=self._fazer_login).place(
            x=270, y=320
        )
        tk.Button(self, text="Cadastrar", width=10, command=self._abrir_cadastro).place(
            x=378, y=320
        )

    def _fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        usuario_autenticado = self.usuario_repo.autenticar(usuario, senha)
        if usuario_autenticado:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.withdraw()
            JanelaPrincipal(self, self.usuario_repo, self.treino_repo, usuario_autenticado)
        else:
            messagebox.showerror("Erro", "Usuario ou senha incorretos")

    def _abrir_cadastro(self):
        JanelaCadastro(self, self.usuario_repo)


if __name__ == "__main__":
    criar_tabelas()
    app = AplicativoLogin()
    app.mainloop()