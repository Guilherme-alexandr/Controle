from flask import Blueprint, render_template, request, jsonify, session
from database import SessionLocal
from models import Produto, Pedido, PedidoProduto

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
def cliente():
    return render_template('cliente.html')

@cliente_bp.route('/carrinho')
def ver_carrinho():
    return render_template('carrinho.html')

@cliente_bp.route('/pedidos')
def ver_pedidos():
    return render_template('pedidos.html')

# realizar pedido
@cliente_bp.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401

        data = request.json
        produtos = data.get('produtos')
        nome_pedido = data.get('nomePedido')

        if not produtos or len(produtos) == 0:
            return jsonify({'success': False, 'error': 'Nenhum produto enviado.'}), 400

        session_db = SessionLocal()

        novo_pedido = Pedido(usuario_id=cliente_id, status='pendente', nome_pedido=nome_pedido)
        session_db.add(novo_pedido)
        session_db.commit()
        for produto_id in produtos:
            produto = session_db.query(Produto).filter(Produto.id == produto_id).first()
            if produto:
                pedido_produto = PedidoProduto(pedido_id=novo_pedido.id, produto_id=produto.id)
                session_db.add(pedido_produto)
            else:
                return jsonify({'success': False, 'error': f'Produto com ID {produto_id} não encontrado.'}), 404

        session_db.commit()
        session_db.close()

        return jsonify({'success': True, 'message': 'Pedido realizado com sucesso!'}), 201

    except Exception as e:
        session_db.rollback()
        session_db.close()
        return jsonify({'success': False, 'error': str(e)}), 500


# Listar
@cliente_bp.route('/pedidos/listar', methods=['GET'])
def listar_pedidos():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401

        session_db = SessionLocal()
        pedidos = session_db.query(Pedido).filter(Pedido.usuario_id == cliente_id).all()
        
        pedidos_lista = []
        for pedido in pedidos:
            pedidos_lista.append({
                'id': pedido.id,
                'nome_pedido': pedido.nome_pedido,
                'status': pedido.status,
                'produtos': [produto.id for produto in pedido.produtos]
            })

        session_db.close()

        return jsonify({'success': True, 'pedidos': pedidos_lista}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Realizar pagamento 
@cliente_bp.route('/realizar-pagamento/<int:pedido_id>', methods=['POST'])
def realizar_pagamento(pedido_id):
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401

    session_db = SessionLocal()
    pedido = session_db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == cliente_id).first()

    if not pedido:
        return jsonify({'success': False, 'error': 'Pedido não encontrado.'}), 404

    if pedido.status != 'pendente':
        return jsonify({'success': False, 'error': 'Este pedido já foi pago ou cancelado.'}), 400

    pedido.status = 'pago'
    session_db.commit()
    session_db.close()

    return jsonify({'success': True, 'message': 'Pagamento realizado com sucesso.'})

#atualizar nome do pedido
@cliente_bp.route('/atualizar-nome-pedido/<int:pedido_id>', methods=['POST'])
def atualizar_nome_pedido(pedido_id):
    novo_nome = request.json.get('nome_pedido')
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401

    session_db = SessionLocal()
    pedido = session_db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == cliente_id).first()

    if not pedido:
        return jsonify({'success': False, 'error': 'Pedido não encontrado.'}), 404

    pedido.nome_pedido = novo_nome
    session_db.commit()
    session_db.close()

    return jsonify({'success': True, 'message': 'Nome do pedido atualizado com sucesso.'})

#Cancelar pedido 
@cliente_bp.route('/cancelar-pedido/<int:pedido_id>', methods=['POST'])
def cancelar_pedido(pedido_id):
    cliente_id = session.get('cliente_id')

    if not cliente_id:
        return jsonify({'success': False, 'error': 'Cliente não autenticado.'}), 401

    session_db = SessionLocal()
    pedido = session_db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == cliente_id).first()

    if not pedido:
        return jsonify({'success': False, 'error': 'Pedido não encontrado.'}), 404

    if pedido.status != 'pendente':
        return jsonify({'success': False, 'error': 'Este pedido já foi pago ou cancelado.'}), 400

    pedido.status = 'cancelado'
    session_db.commit()
    session_db.close()

    return jsonify({'success': True, 'message': 'Pedido cancelado com sucesso.'})
