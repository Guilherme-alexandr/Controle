document.addEventListener('DOMContentLoaded', function () {
    listarCarrinho();
    document.querySelector('#finalizarCompraBtn').addEventListener('click', finalizarCompra);
    document.getElementById('voltar').addEventListener('click', voltarPaginaCliente);
});

function listarCarrinho() {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    const tabela = document.querySelector('#carrinhoTabela tbody');
    const totalCarrinhoSpan = document.querySelector('#totalCarrinho');

    if (carrinho.length === 0) {
        tabela.innerHTML = '<tr><td colspan="5">Seu carrinho está vazio.</td></tr>';
        totalCarrinhoSpan.textContent = '0.00';
        return;
    }

    tabela.innerHTML = '';
    let totalCarrinho = 0;

    carrinho.forEach((produto, index) => {
        const valorProduto = produto.valor ? parseFloat(produto.valor) : 0;
        const valorTotal = valorProduto * produto.quantidade;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${produto.nome}</td>
            <td>${valorProduto.toFixed(2)}</td>
            <td><input type="number" class="quantidadeInput" value="${produto.quantidade}" min="1" data-index="${index}"></td>
            <td>${valorTotal.toFixed(2)}</td>
            <td><button class="btn-remove" onclick="removerProduto(${index})">Remover</button></td>
        `;
        tabela.appendChild(tr);
        totalCarrinho += valorTotal;
    });

    totalCarrinhoSpan.textContent = totalCarrinho.toFixed(2);
    localStorage.setItem('carrinho', JSON.stringify(carrinho));

    document.querySelectorAll('.quantidadeInput').forEach(input => {
        input.addEventListener('change', function () {
            const index = parseInt(this.getAttribute('data-index'));
            atualizarQuantidade(index, parseInt(this.value));
        });
    });
}

function atualizarQuantidade(index, novaQuantidade) {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

    if (novaQuantidade < 1) {
        alert('A quantidade mínima é 1');
        novaQuantidade = 1;
    }
    carrinho[index].quantidade = novaQuantidade;
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    listarCarrinho();
}

function removerProduto(index) {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    carrinho.splice(index, 1);
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    listarCarrinho();
}

function finalizarCompra() {
    alert('Compra finalizada com sucesso!');
    localStorage.removeItem('carrinho');
    window.location.href = '/cliente';
}

function voltarPaginaCliente() {
    sessionStorage.clear();
    window.location.href = '/cliente/';
}
