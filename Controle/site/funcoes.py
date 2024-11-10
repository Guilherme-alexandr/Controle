from flask import Flask, request, jsonify, render_template
import pyodbc

app = Flask(__name__)

def get_db_connection():
    database = 'CONTROLE'
    username = 'sa'
    password = 'impacta1'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=DESKTOP-075BAM7\\SQLEXPRESS;DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    try:
        data = request.json
        nome = data['nome']
        valor = data['valor']
        tipo = data['tipo']
        descricao = data['descricao']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Produtos (Nome, Valor, Tipo, Descricao)
            VALUES (?, ?, ?, ?)
        ''', (nome, valor, tipo, descricao))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Produto adicionado com sucesso!'}), 201
    except pyodbc.Error as e:
        return jsonify({'error': 'Erro ao conectar ao banco de dados.', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar produto.', 'details': str(e)}), 500


@app.route('/produtos', methods=['GET'])
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
                'descricao': produto[4]
            })
        
        return jsonify({'produtos': produtos_lista})
    except Exception as e:
        return jsonify({'error': 'Erro ao listar produtos.', 'details': str(e)}), 500


@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.json
    nome = data['nome']
    valor = data['valor']
    tipo = data['tipo']
    descricao = data['descricao']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Produtos
        SET Nome = ?, Valor = ?, Tipo = ?, Descricao = ?
        WHERE Id = ?
    ''', (nome, valor, tipo, descricao, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Produto atualizado com sucesso!'})

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produtos WHERE Id = ?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Produto não encontrado."}), 404

    return jsonify({"message": f"Produto {id} deletado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
