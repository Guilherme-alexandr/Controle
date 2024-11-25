document.addEventListener('DOMContentLoaded', function () {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    const tabela = document.querySelector('#carrinhoTabela tbody');
    const totalCarrinhoSpan = document.querySelector('#totalCarrinho');

    function atualizarCarrinho() {
        tabela.innerHTML = '';
        let totalCarrinho = 0;

        carrinho.forEach((produto, index) => {
            const row = document.createElement('tr');

            const nomeCell = document.createElement('td');
            nomeCell.textContent = produto.nome;
            row.appendChild(nomeCell);

            const valorUnitarioCell = document.createElement('td');
            const valorProduto = produto.valor ? parseFloat(produto.valor) : 0;
            valorUnitarioCell.textContent = valorProduto.toFixed(2);
            row.appendChild(valorUnitarioCell);

            const quantidadeCell = document.createElement('td');
            const quantidadeInput = document.createElement('input');
            quantidadeInput.type = 'number';
            quantidadeInput.value = produto.quantidade;
            quantidadeInput.min = 1;
            quantidadeInput.addEventListener('change', function () {
                produto.quantidade = parseInt(quantidadeInput.value);
                atualizarCarrinho();
            });
            quantidadeCell.appendChild(quantidadeInput);
            row.appendChild(quantidadeCell);

            const valorTotalCell = document.createElement('td');
            const valorTotal = valorProduto * produto.quantidade;
            valorTotalCell.textContent = valorTotal.toFixed(2);
            row.appendChild(valorTotalCell);

            const acaoCell = document.createElement('td');
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remover';
            removeButton.addEventListener('click', function () {
                carrinho.splice(index, 1);
                atualizarCarrinho();
            });
            acaoCell.appendChild(removeButton);
            row.appendChild(acaoCell);

            tabela.appendChild(row);
            totalCarrinho += valorTotal;
        });

        totalCarrinhoSpan.textContent = totalCarrinho.toFixed(2);
        localStorage.setItem('carrinho', JSON.stringify(carrinho));
    }

    atualizarCarrinho();

    document.querySelector('#finalizarCompraBtn').addEventListener('click', function () {
        alert('Compra finalizada com sucesso!');
        localStorage.removeItem('carrinho');
        window.location.href = '/cliente';
    });
});

document.getElementById('voltar').addEventListener('click', function() {

    sessionStorage.clear();
    window.location.href = '/cliente/';
});