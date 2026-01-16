from sqlj import conectar

def adicionar_treino(usuario_id, nome, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO treinos (nome, descricao, usuario_id) VALUES (?, ?, ?)",
        (nome, descricao, usuario_id)
    )
    conn.commit()
    conn.close()

def listar_treinos(usuario_id=None):
    conn = conectar()
    cursor = conn.cursor()
    if usuario_id:
        cursor.execute("SELECT id, nome, descricao FROM treinos WHERE usuario_id=?", (usuario_id,))
    else:
        cursor.execute("SELECT id, nome, descricao FROM treinos")
    treinos = cursor.fetchall()
    conn.close()
    return treinos

