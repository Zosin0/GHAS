import os
import sqlite3
import hashlib
from flask import Flask, request, Response

app = Flask(__name__)

# --- PARTE 1: VAZAMENTO DE SEGREDOS (SECRET SCANNING) ---
# O Secret Scanning do GitHub irá identificar estes padrões como credenciais vazadas.

# Segredo Genérico 1: PostgreSQL Connection String
# GHAS irá classificar isso como um segredo exposto.
postgres_connection_string = "postgresql://user:password123@db.example.com:5432/mydatabase"

# Segredo Genérico 2: MongoDB Connection String
# Outro padrão comum que será detectado.
mongodb_connection_string = "mongodb+srv://admin:aSuperSecretPassword@cluster0.mongodb.net/testdb?retryWrites=true&w=majority"

# Segredo Genérico 3: MySQL Connection String
# Formato clássico de string de conexão.
mysql_connection_string = "mysql://dbuser:MyStrongP@ssw0rd!@192.168.1.100/app_db"


# --- PARTE 2: VULNERABILIDADES DE CÓDIGO (CODE SCANNING / CODEQL) ---

@app.route('/user_profile')
def get_user_profile():
    """
    Vulnerabilidade CRÍTICA: SQL Injection (CWE-89)
    A entrada do usuário (user_id) é concatenada diretamente em uma query SQL.
    Um atacante pode manipular o 'user_id' para executar queries maliciosas.
    Exemplo de ataque: /user_profile?user_id=1' OR '1'='1
    """
    user_id = request.args.get('user_id')
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    
    # A linha abaixo é a vulnerabilidade
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    
    try:
        cursor.execute(query)
        user_data = cursor.fetchone()
        return f"User data: {user_data}"
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        db.close()

@app.route('/hello')
def say_hello():
    """
    Vulnerabilidade MÉDIA: Cross-Site Scripting (XSS) Refletido (CWE-79)
    A entrada do usuário (name) é refletida diretamente na resposta HTML sem sanitização.
    Um atacante pode injetar scripts que serão executados no navegador de outra pessoa.
    Exemplo de ataque: /hello?name=<script>alert('XSS PoC')</script>
    """
    name = request.args.get('name', 'Guest')
    
    # A resposta abaixo é vulnerável a XSS
    html_response = f"<h1>Olá, {name}!</h1>"
    
    return Response(html_response, mimetype='text/html')

@app.route('/login', methods=['POST'])
def user_login():
    """
    Vulnerabilidade BAIXA/MÉDIA: Uso de Hash Fraco (CWE-327)
    O sistema usa MD5 para gerar o hash da senha do usuário. MD5 é considerado
    criptograficamente quebrado e suscetível a colisões e ataques de rainbow table.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    # O uso de MD5 é a vulnerabilidade
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    # Lógica de login (simulada)
    return f"Tentando login para {username} com o hash (MD5): {hashed_password}"

@app.route('/get_file')
def get_file_content():
    """
    Vulnerabilidade ALTA: Path Traversal (CWE-22)
    O nome do arquivo é pego diretamente da requisição e usado para ler um arquivo do sistema.
    Um atacante pode navegar pelo sistema de arquivos.
    Exemplo de ataque: /get_file?filename=../../../../etc/passwd
    """
    filename = request.args.get('filename')
    
    try:
        # A linha abaixo é a vulnerabilidade
        with open(f'/var/www/uploads/{filename}', 'r') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        return "Arquivo não encontrado.", 404

if __name__ == '__main__':
    # AVISO: O modo debug do Flask também é uma vulnerabilidade (CWE-117, CWE-215)
    # se exposto em produção, o que o CodeQL também pode apontar.
    app.run(debug=True)
