import os
import sqlite3
import hashlib
import subprocess # NOVO: Módulo para injeção de comando
import logging   # NOVO: Módulo para logging inseguro
from flask import Flask, request, Response

app = Flask(__name__)

# --- PARTE 1: VAZAMENTO DE SEGREDOS (SECRET SCANNING) ---
# Adicionamos mais padrões claros para garantir a detecção.
# O Secret Scanning do GitHub irá identificar estes padrões como credenciais vazadas.

# Segredo 1: Chave de API da AWS (padrão de altíssima confiança para o scanner)
# NOVO: Adicionado para garantir a detecção pelo Secret Scanning.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE" 

# Segredo 2: PostgreSQL Connection String
postgres_connection_string = "postgresql://app_user:db_p4ssw0rd_Th4t_L00ks_R3al@prod-db.example.com:5432/production"

# Segredo 3: MySQL Connection String
mysql_connection_string = "mysql://root:s3cr3t_!n_Pl4in_T3xt@10.0.0.5/customer_data"

# Segredo 4: MongoDB Connection String
mongodb_connection_string = "mongodb+srv://admin:aSuperSecretPassword@cluster0.mongodb.net/testdb?retryWrites=true&w=majority"


# --- PARTE 2: VULNERABILIDADES DE CÓDIGO (CODE SCANNING / CODEQL) ---

# NOVO: VULNERABILIDADE CRÍTICA
@app.route('/run_command')
def run_command():
    """
    Vulnerabilidade CRÍTICA: OS Command Injection (CWE-78)
    Executa um comando no sistema operacional usando entrada do usuário sem sanitização.
    Isso permite a execução remota de código (RCE) no servidor.
    Exemplo de ataque: /run_command?cmd=ls -la /
    """
    command = request.args.get('cmd')
    
    # A linha abaixo é a vulnerabilidade crítica
    output = subprocess.check_output(command, shell=True, text=True)
    
    return f"Comando executado:\n<pre>{output}</pre>"

@app.route('/user_profile')
def get_user_profile():
    """
    Vulnerabilidade ALTA: SQL Injection (CWE-89)
    A entrada do usuário (user_id) é concatenada diretamente em uma query SQL.
    """
    user_id = request.args.get('user_id')
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = '" + user_id + "'" # Vulnerabilidade aqui
    try:
        cursor.execute(query)
        user_data = cursor.fetchone()
        return f"User data: {user_data}"
    except Exception as e:
        # A linha abaixo gera o alerta "Information exposure through an exception"
        return f"An error occurred: {e}"
    finally:
        db.close()

@app.route('/hello')
def say_hello():
    """
    Vulnerabilidade MÉDIA: Cross-Site Scripting (XSS) Refletido (CWE-79)
    A entrada do usuário (name) é refletida diretamente na resposta HTML.
    """
    name = request.args.get('name', 'Guest')
    html_response = f"<h1>Olá, {name}!</h1>" # Vulnerabilidade aqui
    return Response(html_response, mimetype='text/html')

# NOVO: VULNERABILIDADE BAIXA
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(message)s')
@app.route('/log_visit')
def log_user_visit():
    """
    Vulnerabilidade BAIXA: Log Injection / Unvalidated Log Entry (CWE-117)
    A entrada do usuário (username) é escrita diretamente em um arquivo de log.
    Um atacante pode injetar caracteres de nova linha (%0a) para forjar entradas de log.
    Exemplo: /log_visit?user=admin%0aINFO: User 'admin' logged out successfully.
    """
    user_identifier = request.args.get('user', 'anonymous')
    
    # A linha abaixo é a vulnerabilidade de log injection
    logging.info(f"User visited the page: {user_identifier}")
    
    return "Visita registrada com sucesso."

@app.route('/login', methods=['POST'])
def user_login():
    """
    Vulnerabilidade ALTA: Uso de Hash Fraco (CWE-327)
    (A criticidade pode ser High ou Medium dependendo da análise do CodeQL)
    """
    password = request.form.get('password')
    hashed_password = hashlib.md5(password.encode()).hexdigest() # Vulnerabilidade aqui
    return f"Hash (MD5): {hashed_password}"

if __name__ == '__main__':
    # A linha abaixo gera o alerta "Flask app is run in debug mode" (High)
    app.run(debug=True)
