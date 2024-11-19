from flask import Flask, request, jsonify, render_template, Blueprint
import pyodbc

produtos_bp = Blueprint('produtos', __name__)
app = Flask(__name__)



def get_db_connection():
    database = 'CONTROLE'
    username = 'sa'
    password = 'impacta1'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=DESKTOP-075BAM7\\SQLEXPRESS;DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn


@produtos_bp.route('/')
def index():
    return render_template('produtos.html')

@produtos_bp.route('/', methods=['POST'])
def adicionar_produto():
    try:
        data = request.json
        nome = data['nome']
        valor = data['valor']
        tipo = data['tipo']
        descricao = data['descricao']
        quantidade = data['quantidade']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Produtos (Nome, Valor, Tipo, Descricao, Quantidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, valor, tipo, descricao, quantidade))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Produto adicionado com sucesso!'}), 201
    except pyodbc.Error as e:
        return jsonify({'error': 'Erro ao conectar ao banco de dados.', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar produto.', 'details': str(e)}), 500


@produtos_bp.route('/listar', methods=['GET'])
def listar_produtos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Produtos')
        produtos = cursor.fetchall()

        produtos_lista = []
        for produto in produtos:
            produtos_lista.append({
                'id': produto[0],
                'nome': produto[1],
                'valor': produto[2],
                'tipo': produto[3],
                'descricao': produto[4],
                'quantidade': produto[5]
            })
        conn.close()
        return jsonify({'produtos': produtos_lista})
    except Exception as e:
        return jsonify({'error': 'Erro ao listar produtos.', 'details': str(e)}), 500


@produtos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        data = request.json
        nome = data['nome']
        valor = data['valor']
        tipo = data['tipo']
        descricao = data['descricao']
        quantidade = data['quantidade']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Produtos
            SET Nome = ?, Valor = ?, Tipo = ?, Descricao = ?, Quantidade = ?
            WHERE Id = ?
        ''', (nome, valor, tipo, descricao, quantidade, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Produto atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@produtos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Produtos WHERE Id = ?", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Produto não encontrado."}), 404

        return jsonify({"message": f"Produto {id} deletado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
