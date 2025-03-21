import mysql.connector
import hashlib

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'megaleilao'
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def validate_user(username, password):
    hashed_password = hash_password(password)
    
    # Verificações para depuração
    print(f"Username: {username} ({type(username)})")
    print(f"Hashed Password: {hashed_password} ({type(hashed_password)})")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Garantir que os valores sejam strings
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (str(username), str(hashed_password)))
    
    user = cursor.fetchone()
    conn.close()
    return user


def register_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    conn.close()
