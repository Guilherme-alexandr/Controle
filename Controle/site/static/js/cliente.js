document.addEventListener('DOMContentLoaded', function () {

    fetch('/produtos/listar')
        .then(response => response.json())
        .then(data => {
            const produtos = data.produtos;
            const tabela = document.querySelector('#produtosTabela tbody');

            produtos.forEach(produto => {
                const row = document.createElement('tr');

                const nomeCell = document.createElement('td');
                nomeCell.textContent = produto.nome;
                row.appendChild(nomeCell);

                const valorCell = document.createElement('td');
                valorCell.textContent = produto.valor;
                row.appendChild(valorCell);

                const descricaoCell = document.createElement('td');
                descricaoCell.textContent = produto.descricao;
                row.appendChild(descricaoCell);

                const quantidadeCell = document.createElement('td');
                const quantidadeInput = document.createElement('input');
                quantidadeInput.type = 'number';
                quantidadeInput.value = 1;
                quantidadeInput.min = 1;
                quantidadeCell.appendChild(quantidadeInput);
                row.appendChild(quantidadeCell);

                const acaoCell = document.createElement('td');
                const addButton = document.createElement('button');
                addButton.textContent = 'Adicionar ao Carrinho';
                addButton.addEventListener('click', function () {
                    adicionarAoCarrinho(produto, quantidadeInput.value);
                });
                acaoCell.appendChild(addButton);
                row.appendChild(acaoCell);

                tabela.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Erro ao listar produtos:', error);
        });
});

function adicionarAoCarrinho(produto, quantidade) {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

    const produtoExistente = carrinho.find(item => item.id === produto.id);
    if (produtoExistente) {
        produtoExistente.quantidade += parseInt(quantidade);
    } else {
        carrinho.push({
            id: produto.id,
            nome: produto.nome,
            valor: parseFloat(produto.valor),
            quantidade: parseInt(quantidade)
        });
    }

    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    alert('Produto adicionado ao carrinho com sucesso!');
}

document.getElementById('logoutBtn').addEventListener('click', function() {

    sessionStorage.clear();
    window.location.href = '/usuarios/';
});
