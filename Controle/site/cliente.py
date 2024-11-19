from flask import Blueprint, render_template, request, jsonify, session
from usuarios import get_db_connection

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
def cliente():
    return render_template('cliente.html')

@cliente_bp.route('/carrinho')
def ver_carrinho():
    return render_template('carrinho.html')


@cliente_bp.route('/finalizar-pedido',methods=['POST'])
def finalizar_pedido():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401
        
        data = request.json
        produtos = data['produtos']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Pedidos (ClienteID, Status) VALUES (?, ?)
        ''', (cliente_id, 'pendente'))
        pedido_id = cursor.lastrowid
        
        for produto in produtos:
            cursor.execute('''
                INSERT INTO PedidoProdutos (PedidoID, ProdutoID) VALUES (?, ?)
            ''', (pedido_id, produto['id']))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Pedido finalizado com sucesso!'}), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
        