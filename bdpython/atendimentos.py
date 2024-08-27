import sqlite3

def conectar(db_name:str):
    """conecta a um banco de dados existente

    Args:
        db_name (str): pasta onde se localiza o banco

    Returns:
        Connection: Retorna uma conexão
    """
    conn = sqlite3.connect(db_name)
    return conn

def criar_tabela(conn:sqlite3.Connection):
    """Cria a tabela se não existir

    Args:
        conn (sqlite3.Connection): conexão inde sera criada a tabela
    """    
    sql = """
    CREATE TABLE IF NOT EXISTS atendimentos (
        nr INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER NOT NULL,
        motivo INTEGER NOT NULL,
        atendido TEXT NOT NULL
    );
    """
    conn.execute(sql)
    conn.commit()

def inserir_solicitacoes(conn:sqlite3.Connection,
                        id:int,
                        motivo:int,
                        atendido:str):
    """Insere uma nova advertencia

    Args:
        conn (sqlite3.Connection): conexão com o banco
        id (int): id do usuário que solicitou
        motivo (int): index relacionado com a solicitacao
        atendido (str): inserir caso a solicitação tenha sido atendida
    """    
    
    sql = """
    INSERT INTO atendimentos (id, motivo, atendido)
    VALUES (?, ?, ?);
    """
    conn.execute(sql, (id, motivo, atendido))
    conn.commit()

def consultar_atendimento(conn:sqlite3.Connection, user_id:int):
    """Consulta as advertencias do usuario

    Args:
        conn (sqlite3.Connection): Conexão com banco
        user_id (int): id do usuario

    Returns:
        list: retorna uma lista com o numero da advertencia, id do user, e motivo da advertencia
    """
    sql = "SELECT * FROM atendimentos WHERE id = ?;"
    cursor = conn.execute(sql, (user_id,))
    return cursor.fetchall()

def consultar_todos(cnn:sqlite3.Connection):
    sql = "SELECT * FROM atendimentos"
    cursor = cnn.execute(sql)
    return cursor.fetchall()

def atualizar_user(conn:sqlite3.Connection,
                   nr:int,
                   user_id= None,
                   motivo= None,
                   atendido= None):
    """Atualiza os dados de um usuário específico na tabela."""
    sql = "UPDATE atendimentos SET "
    params = []
    
    if user_id:
        sql += "id = ?, "
        params.append(user_id)
    if motivo:
        sql += "motivo = ?, "
        params.append(motivo)
    if atendido:
        sql += "atendido = ?"
        params.append(atendido)
        
    sql = sql.rstrip(', ')
    
    sql += " WHERE nr = ?;"
    params.append(nr)
    
    conn.execute(sql, params)
    conn.commit()

def deletar_advertencia(conn, numero_advertencia):
    """Deleta um usuário específico na tabela."""
    sql = "DELETE FROM advertencia WHERE nr = ?;"
    conn.execute(sql, (numero_advertencia,))
    conn.commit()

