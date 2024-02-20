const urlAPI = "http://127.0.0.1:8000/orcamento/1/pedidos/?format=json";

async function carregarDados() {
        const resposta = await fetch(urlAPI);
        const dadosJSON = await resposta.json();
    
        popularTabela(dadosJSON);
    }
// Função para formatar data
function formatarData(data) {
    const dataFormatada = new Date(data);
    return `${dataFormatada.getDate()}/${dataFormatada.getMonth() + 1}/${dataFormatada.getFullYear()}`;
}

// Função para formatar preço
function formatarPreco(preco) {
    return ` ${preco.toFixed(2).replace(".", ",")}`;
}    
carregarDados();
    
function popularTabela(dados){
    const tabela = document.getElementById("tabela-pedidos");
    
    const linha = document.createElement("tr");
    const colunaItem = document.createElement("td");
    const colunaCodigo = document.createElement("td");
    const colunaDescricao = document.createElement("td");
    const colunaQuantidade = document.createElement("td");
    const colunaDataEntrega = document.createElement("td");
    const colunaPreco = document.createElement("td");
    const colunaNcm = document.createElement("td");

    colunaItem.textContent = "ITEM";
    colunaCodigo.textContent = "CODIGO";
    colunaDescricao.textContent = "PRODUTOS";
    colunaQuantidade.textContent = "QTDE.";
    colunaDataEntrega.textContent = "ENTREGA";
    colunaPreco.textContent = 'PREÇO';
    colunaNcm.textContent = 'NCM';

    linha.appendChild(colunaItem);
    linha.appendChild(colunaCodigo);
    linha.appendChild(colunaDescricao);
    linha.appendChild(colunaDataEntrega);
    linha.appendChild(colunaNcm);
    linha.appendChild(colunaQuantidade);
    linha.appendChild(colunaPreco);

    tabela.appendChild(linha);

    const i = 1
    for (const item of dados) {
        const linha = document.createElement("tr");
        const colunaItem = document.createElement("td");
        const colunaCodigo = document.createElement("td");
        const colunaDescricao = document.createElement("td");
        const colunaQuantidade = document.createElement("td");
        const colunaDataEntrega = document.createElement("td");
        const colunaPreco = document.createElement("td");
        const colunaNcm = document.createElement("td");

        colunaItem.textContent = i.toString();
        colunaCodigo.textContent = item.peca.codigo;
        colunaDescricao.textContent = item.peca.descricao;
        colunaQuantidade.textContent = item.quantidade;
        colunaDataEntrega.textContent = formatarData(item.dataEntrega);
        colunaPreco.textContent = formatarPreco(item.peca.precoVenda * item.quantidade);
        colunaNcm.textContent = item.peca.ncm;

        linha.appendChild(colunaItem);
        linha.appendChild(colunaCodigo);
        linha.appendChild(colunaDescricao);
        linha.appendChild(colunaDataEntrega);
        linha.appendChild(colunaNcm);
        linha.appendChild(colunaQuantidade);
        linha.appendChild(colunaPreco);

        tabela.appendChild(linha);

        i++;
      }
}