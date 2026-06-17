import sqlite3

def init():
    conn = sqlite3.connect('agentes_cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache_mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT,
            conteudo TEXT,
            status TEXT DEFAULT 'pendente',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("SQLite pronto!")

if __name__ == '__main__':
    init()
