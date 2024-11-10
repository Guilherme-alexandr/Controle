
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
          `;
          tbody.appendChild(tr);
        });
      })
      .catch(error => console.error('Erro ao listar produtos:', error));
  }
  
function listarProdutos() {
  fetch('/produtos', { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.produtos) {
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
          `;
          tbody.appendChild(tr);
        });
      } else {
        console.error('Erro ao carregar produtos: ', data.error);
      }
    })
    .catch(error => console.error('Erro ao listar produtos:', error));
}
window.onload = listarProdutos;
