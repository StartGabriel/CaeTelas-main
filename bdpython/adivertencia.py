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
    CREATE TABLE IF NOT EXISTS advertencia (
        nr INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER NOT NULL,
        motivo INTEGER NOT NULL
    );
    """
    conn.execute(sql)
    conn.commit()

def inserir_advertencia(conn:sqlite3.Connection,
                        id:int,
                        motivo:int):
    """Insere uma nova advertencia

    Args:
        conn (sqlite3.Connection): conexão com o banco
        id (int): id do usuário que ira levar a advertencia
        motivo (int): index relacionado com a advertencia
    """    
    
    sql = """
    INSERT INTO advertencia (id, motivo)
    VALUES (?, ?);
    """
    conn.execute(sql, (id, motivo))
    conn.commit()

def consultar_adivertencia(conn:sqlite3.Connection, user_id:int):
    """Consulta as advertencias do usuario

    Args:
        conn (sqlite3.Connection): Conexão com banco
        user_id (int): id do usuario

    Returns:
        list: retorna uma lista com o numero da advertencia, id do user, e motivo da advertencia
    """
    sql = "SELECT * FROM advertencia WHERE nr = ?;"
    cursor = conn.execute(sql, (user_id,))
    return cursor.fetchall()

def atualizar_user(conn:sqlite3.Connection,
                   nr_advertencia:int,
                   user_id= None,
                   motivo= None):
    """Atualiza os dados de um usuário específico na tabela."""
    sql = "UPDATE advertencia SET "
    params = []
    
    if user_id:
        sql += "id = ?, "
        params.append(user_id)
    if motivo:
        sql += "motivo = ?, "
        params.append(motivo)
        
    sql = sql.rstrip(', ')
    
    sql += " WHERE nr = ?;"
    params.append(nr_advertencia)
    
    conn.execute(sql, params)
    conn.commit()

def deletar_advertencia(conn, numero_advertencia):
    """Deleta um usuário específico na tabela."""
    sql = "DELETE FROM advertencia WHERE nr = ?;"
    conn.execute(sql, (numero_advertencia,))
    conn.commit()

