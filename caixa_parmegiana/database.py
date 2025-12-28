import sqlite3

def conectar():
    return sqlite3.connect("caixa.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            tipo TEXT,
            proteina TEXT,
            refrigerante INTEGER,
            entrega INTEGER,
            origem TEXT,
            pagamento TEXT,
            valor REAL,
            data_hora TEXT
        )
    """)
    conn.commit()
    conn.close()
