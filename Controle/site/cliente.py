from flask import Blueprint, render_template, request, jsonify, session
from database import SessionLocal
from models import Produto, Pedido

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
def cliente():
    return render_template('cliente.html')

@cliente_bp.route('/carrinho')
def ver_carrinho():
    return render_template('carrinho.html')


@cliente_bp.route('/finalizar-pedido', methods=['POST'])
def finalizar_pedido():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401
        
        data = request.json
        produtos = data['produtos']

        session_db = SessionLocal()
        novo_pedido = Pedido(cliente_id=cliente_id, status='pendente')
        session_db.add(novo_pedido)
        session_db.commit()

        for produto_id in produtos:
            produto = session_db.query(Produto).filter(Produto.id == produto_id).first()
            if produto:
                # Aqui você deve adicionar a lógica para associar os produtos ao pedido
                # Supondo que você tenha uma tabela intermediária, por exemplo, PedidoProduto, você deve adicionar
                # esse produto ao pedido aqui, mas falta o código para isso.
                pass

        session_db.commit()
        session_db.close()

        return jsonify({'success': True, 'message': 'Pedido finalizado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500