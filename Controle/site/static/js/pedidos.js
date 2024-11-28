document.addEventListener('DOMContentLoaded', function () {
    listarPedidos();

    document.querySelector('#voltar').addEventListener('click', function () {
        window.location.href = '/cliente/';
    });
});

function listarPedidos() {
    fetch('/cliente/pedidos/listar')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const pedidos = data.pedidos;
                const tabela = document.querySelector('#pedidosTabela tbody');

                if (pedidos.length === 0) {
                    tabela.innerHTML = '<tr><td colspan="4">Você ainda não fez nenhum pedido.</td></tr>';
                    return;
                }

                tabela.innerHTML = '';

                pedidos.forEach((pedido) => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${pedido.nome_pedido || 'Sem nome'}</td>
                        <td>${pedido.status}</td>
                        <td>
                            ${
                                pedido.status === 'pendente' 
                                ? `<button class="btn-pagar" onclick="realizarPagamento(${pedido.id})">Pagar</button>
                                   <button class="btn-cancelar" onclick="cancelarPedido(${pedido.id})">Cancelar</button>`
                                : 'Pedido pago ou cancelado'
                            }
                        </td>
                        <td><button onclick="verProdutos(${pedido.id})">Ver Produtos</button></td>
                    `;
                    tabela.appendChild(tr);
                });
            } else {
                alert('Erro ao carregar pedidos.');
            }
        })
        .catch(error => {
            console.error('Erro ao listar pedidos:', error);
            alert('Erro inesperado ao listar pedidos.');
        });
}

function realizarPagamento(pedidoId) {
    fetch(`/cliente/pedidos/pagar/${pedidoId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido pago com sucesso!');
                listarPedidos();
            } else {
                alert('Erro ao pagar o pedido.');
            }
        })
        .catch(error => {
            console.error('Erro ao realizar o pagamento:', error);
            alert('Erro inesperado ao realizar pagamento.');
        });
}

function cancelarPedido(pedidoId) {
    fetch(`/cliente/pedidos/cancelar/${pedidoId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido cancelado com sucesso!');
                listarPedidos();
            } else {
                alert('Erro ao cancelar o pedido.');
            }
        })
        .catch(error => {
            console.error('Erro ao cancelar o pedido:', error);
            alert('Erro inesperado ao cancelar pedido.');
        });
}

function verProdutos(pedidoId) {
    fetch(`/cliente/pedidos/produtos/${pedidoId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const produtos = data.produtos;
                alert(`Produtos do pedido:\n${produtos.map(p => p.nome).join(', ')}`);
            } else {
                alert('Erro ao visualizar produtos.');
            }
        })
        .catch(error => {
            console.error('Erro ao visualizar produtos:', error);
            alert('Erro inesperado ao visualizar produtos.');
        });
}
