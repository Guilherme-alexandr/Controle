document.addEventListener('DOMContentLoaded', function () {
  const adicionarForm = document.getElementById('adicionarForm');
  const atualizarForm = document.getElementById('atualizarForm');
  const mostrarAdicionarFormBtn = document.getElementById('mostrarAdicionarFormBtn');
  const cancelarAdicionarBtn = document.getElementById('cancelarAdicionarBtn');
  const cancelarAtualizarBtn = document.getElementById('cancelarAtualizarBtn');

  mostrarAdicionarFormBtn.addEventListener('click', function () {
    adicionarForm.style.display = 'block';
    atualizarForm.style.display = 'none';
  });
  cancelarAdicionarBtn.addEventListener('click', function () {
    adicionarForm.style.display = 'none';
    adicionarForm.reset();
  });
  cancelarAtualizarBtn.addEventListener('click', function () {
    atualizarForm.style.display = 'none';
    atualizarForm.reset();
  });


  function listarProdutos() {
    fetch('/produtos', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        const tbody = document.querySelector('#produtosTable tbody');
        tbody.innerHTML = '';
        data.produtos.forEach(produto => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${produto.id}</td>
            <td>${produto.nome}</td>
            <td>${produto.valor}</td>
            <td>${produto.tipo}</td>
            <td>${produto.descricao}</td>
            <td>
              <button onclick="mostrarFormularioAtualizar(${produto.id}, '${produto.nome}', '${produto.valor}', '${produto.tipo}', '${produto.descricao}')">Editar</button>
              <button onclick="deletarProduto(${produto.id})">Deletar</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      })
      .catch(error => console.error('Erro ao listar produtos:', error));
  }


  window.mostrarFormularioAtualizar = function (id, nome, valor, tipo, descricao) {
    adicionarForm.style.display = 'none';
    atualizarForm.style.display = 'block';

    document.getElementById('produtoIdAtualizar').value = id;
    document.getElementById('nomeAtualizar').value = nome;
    document.getElementById('valorAtualizar').value = valor;
    document.getElementById('tipoAtualizar').value = tipo;
    document.getElementById('descricaoAtualizar').value = descricao;
  }


  window.deletarProduto = function (id) {
    if (confirm(`Tem certeza que deseja deletar este produto?`)) {
      fetch(`/produto/${id}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Produto deletado com sucesso!');
            listarProdutos();
          } else {
            alert('Erro ao deletar produto: ' + data.error);
          }
        })
        .catch(error => console.error('Erro ao deletar produto:', error));
    }
  }


  document.querySelector('#adicionarForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const nome = document.querySelector('#nome').value;
    const valor = document.querySelector('#valor').value;
    const tipo = document.querySelector('#tipo').value;
    const descricao = document.querySelector('#descricao').value;

    const produto = { nome, valor, tipo, descricao };

    fetch('/produtos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(produto)
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          alert(data.message);
          listarProdutos();
          adicionarForm.reset();
          adicionarForm.style.display = 'none';
        } else {
          alert('Erro ao adicionar produto');
        }
      })
      .catch(error => console.error('Erro ao adicionar produto:', error));
  });


  document.querySelector('#atualizarForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const id = document.getElementById('produtoIdAtualizar').value;
    const nome = document.getElementById('nomeAtualizar').value;
    const valor = document.getElementById('valorAtualizar').value;
    const tipo = document.getElementById('tipoAtualizar').value;
    const descricao = document.getElementById('descricaoAtualizar').value;

    const produtoAtualizado = { nome, valor, tipo, descricao };

    fetch(`/produtos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(produtoAtualizado)
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.message) {
          alert(data.message);
          listarProdutos();
          atualizarForm.style.display = 'none';
        } else {
          alert('Erro ao atualizar produto: ' + (data.error || 'Erro desconhecido'));
        }
      })
      .catch(error => {
        console.error('Erro ao atualizar produto:', error);
        alert('Erro ao atualizar produto: ' + error.message);
      });
  });
  listarProdutos();
});
