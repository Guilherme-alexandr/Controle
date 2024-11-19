from flask import Flask, request, jsonify, render_template, Blueprint, redirect, url_for, session, flash
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

cliente_bp = Blueprint('cliente', __name__)
usuarios_bp = Blueprint('usuarios', __name__)
app = Flask(__name__)

app.secret_key = 'cyber_key_segurity'

def get_db_connection():
    database = 'CONTROLE'
    username = 'sa'
    password = 'impacta1'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=DESKTOP-075BAM7\\SQLEXPRESS;DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn

@usuarios_bp.route('/')
def index():
    return render_template('login.html')

@usuarios_bp.route('/', methods=['POST'])
def cadastrar_usuario():
    try:
        data = request.json
        nome = data['nome']
        email = data['email']
        senha = data['senha']
        tipo = data.get('tipo', 'cli')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Email = ?', (email,))
        usuario_existente = cursor.fetchone()
        if usuario_existente:
            conn.close()
            return jsonify({'error': 'Este e-mail já está cadastrado.'}), 400
                
        senha_hash = generate_password_hash(senha)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Usuarios (Nome, Email, Senha, Tipo)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, senha_hash, tipo))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuário cadastrado com sucesso!', 'success': True}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao cadastrar usuário.', 'details': str(e)}), 500


@usuarios_bp.route('/login', methods=['POST'])
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
            cliente_id = usuario[0]
            tipo_usuario = usuario[4]
            session['cliente_id'] = cliente_id
            print(f"Cliente ID: {cliente_id}")

            if tipo_usuario == 'admin':
                return jsonify({'redirect_url': '/produtos'})
            elif tipo_usuario == 'cliente':
                return jsonify({'redirect_url': '/cliente'})
            else:
                return jsonify({'error': 'Tipo de usuário desconhecido.'}), 400
        else:
            return jsonify({'error': 'Credenciais inválidas.'}), 401

    except Exception as e:
        return jsonify({'error': 'Erro ao realizar login.', 'details': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)