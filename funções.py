import sqlite3

# conecta ao banco
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# consulta todos os usuários
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()  # pega todos os resultados

# mostra na tela
for usuario in usuarios:
    print(usuario)

conn.close()
