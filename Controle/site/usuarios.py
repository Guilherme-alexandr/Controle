from flask import Flask, request, jsonify, render_template
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_db_connection():
    database = 'CONTROLE'
    username = 'sa'
    password = 'impacta1'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=DESKTOP-075BAM7\\SQLEXPRESS;DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/')
def usuarios():
    return render_template('login.html')

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        data = request.json
        nome = data['nome']
        email = data['email']
        senha = data['senha']
        
        senha_hash = generate_password_hash(senha)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO Usuarios (Nome, Email, Senha) 
            VALUES (?, ?, ?)
        ''', (nome, email, senha_hash))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao cadastrar usuário.', 'details': str(e)}), 500

@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        data = request.json
        email = data['email']
        senha = data['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Email = ?', (email,))
        usuario = cursor.fetchone()
        
        if usuario and check_password_hash(usuario[3], senha):
            return jsonify({'message': 'Login bem-sucedido!'})
        else:
            return jsonify({'error': 'Credenciais inválidas.'}), 401

    except Exception as e:
        return jsonify({'error': 'Erro ao realizar login.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)