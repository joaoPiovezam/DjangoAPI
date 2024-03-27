const urlAPI = "http://127.0.0.1:8000/orcamento/2/pedidos/?format=json";

var  precoTotal = 0.0;
var pesoTotal = 0.0;
var volumeTotal = 0.0;
async function carregarDados() {
        const resposta = await fetch(urlAPI);
        const dadosJSON = await resposta.json();
    
        popularTabelaCliente1(dadosJSON);
        popularTabelaCliente2(dadosJSON);
        popularTabelaCliente3(dadosJSON);
        popularTabelaCliente4(dadosJSON);
        popularTabelaPedidos(dadosJSON);
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
    
function popularTabelaCliente1(dados){
    const tabela = document.getElementById("tabela-cliente");

    const orcamento = dados.results[0].orcamento;

    const linha = document.createElement("tr");
    const colunaDataEmissao = document.createElement("td");
    const colunaDataValidade = document.createElement("td");
    const colunaTipoEntrega = document.createElement("td");
    const colunaResponsavel = document.createElement("td");
    const colunaCodigo = document.createElement("td");
   
    colunaDataEmissao.textContent = "DATA DE EMISSÃO";
    colunaDataValidade.textContent = "DATA VALIDADE";
    colunaTipoEntrega.textContent = "INCOTERM";
    colunaResponsavel.textContent = "RESPONSÁVEL";
    colunaCodigo.textContent = "ORÇAMENTO";

    linha.appendChild(colunaDataEmissao);
    linha.appendChild(colunaDataValidade);
    linha.appendChild(colunaTipoEntrega);
    linha.appendChild(colunaResponsavel);
    linha.appendChild(colunaCodigo);

    tabela.appendChild(linha);
    
    const linha1 = document.createElement("tr");
    const colunaDataEmissao1 = document.createElement("td");
    const colunaDataValidade1 = document.createElement("td");
    const colunaTipoEntrega1 = document.createElement("td");
    const colunaResponsavel1 = document.createElement("td");
    const colunaCodigo1 = document.createElement("td");

    colunaDataEmissao1.textContent = formatarData(orcamento.dataEmissao);
    colunaDataValidade1.textContent = formatarData(orcamento.dataValidade);
    colunaTipoEntrega1.textContent = orcamento.tipoEntrega;
    colunaResponsavel1.textContent = orcamento.responsavel;
    colunaCodigo1.textContent = orcamento.codigo;

    linha1.appendChild(colunaDataEmissao1);
    linha1.appendChild(colunaDataValidade1);
    linha1.appendChild(colunaTipoEntrega1);
    linha1.appendChild(colunaResponsavel1);
    linha1.appendChild(colunaCodigo1);

    tabela.appendChild(linha1);
}

function popularTabelaCliente2(dados){
    const tabela = document.getElementById("tabela-cliente");

    const cliente = dados.results[0].cliente.client;

    const linha = document.createElement("tr");
    const colunaNome = document.createElement("td");
    colunaNome.setAttribute('colspan', '5');
    
    colunaNome.textContent = "NOME CLINETE";

    linha.appendChild(colunaNome);

    tabela.appendChild(linha);
    
    const linha1 = document.createElement("tr");
    const colunaNome1 = document.createElement("td");
    colunaNome1.setAttribute('colspan', '5');

    colunaNome1.textContent = cliente.nomeCliente;

    linha1.appendChild(colunaNome1);

    tabela.appendChild(linha1);
}

function popularTabelaCliente3(dados){
    const tabela = document.getElementById("tabela-cliente");

    const cliente = dados.results[0].cliente.client;

    const linha = document.createElement("tr");
    const colunaEndereco = document.createElement("td");
    const colunaCEP = document.createElement("td");
    const colunaCidade = document.createElement("td");
    const colunaPais = document.createElement("td");
    colunaEndereco.setAttribute('colspan', '2');
    
    colunaEndereco.textContent = "ENDERECO";
    colunaCEP.textContent = "POSTAL CODE";
    colunaCidade.textContent = "CIDADE";
    colunaPais.textContent = "PAÍS";

    linha.appendChild(colunaEndereco);
    linha.appendChild(colunaCEP);
    linha.appendChild(colunaCidade);
    linha.appendChild(colunaPais);

    tabela.appendChild(linha);
    
    const linha1 = document.createElement("tr");
    const colunaEndereco1 = document.createElement("td");
    const colunaCEP1 = document.createElement("td");
    const colunaCidade1 = document.createElement("td");
    const colunaPais1 = document.createElement("td");
    colunaEndereco1.setAttribute('colspan', '2');

    colunaEndereco1.textContent = cliente.endereco;
    colunaCEP1.textContent = cliente.cep;
    colunaCidade1.textContent = cliente.cidade;
    colunaPais1.textContent = cliente.pais;

    linha1.appendChild(colunaEndereco1);
    linha1.appendChild(colunaCEP1);
    linha1.appendChild(colunaCidade1);
    linha1.appendChild(colunaPais1);

    tabela.appendChild(linha1);
}

function popularTabelaCliente4(dados){
    const tabela = document.getElementById("tabela-cliente");

    const cliente = dados.results[0].cliente.client;

    const linha = document.createElement("tr");
    const colunaTelefone = document.createElement("td");
    const colunaEmail = document.createElement("td");
    colunaEmail.setAttribute('colspan', '4');

    colunaTelefone.textContent = "TELEFONE";
    colunaEmail.textContent = "EMAIL";

    linha.appendChild(colunaTelefone);
    linha.appendChild(colunaEmail);

    tabela.appendChild(linha);
    
    const linha1 = document.createElement("tr");
    const colunaTelefone1 = document.createElement("td");
    const colunaEmail1 = document.createElement("td");
    colunaEmail1.setAttribute('colspan', '4');

    colunaTelefone1.textContent = cliente.telefone;
    colunaEmail1.textContent = cliente.email;

    linha1.appendChild(colunaTelefone1);
    linha1.appendChild(colunaEmail1);

    tabela.appendChild(linha1);
}

function popularTabelaPedidos(dados){
    const tabela = document.getElementById("tabela-pedidos");
    
    const linha = document.createElement("tr");
    const colunaItem = document.createElement("td");
    const colunaCodigo = document.createElement("td");
    const colunaDescricao = document.createElement("td");
    const colunaQuantidade = document.createElement("td");
    const colunaDataEntrega = document.createElement("td");
    const colulaPrecoUnit = document.createElement("td");
    const colunaPreco = document.createElement("td");
    const colunaNcm = document.createElement("td");
    const colunaVolume = document.createElement("td");
    const colunaPeso = document.createElement("td");
    colunaDescricao.setAttribute('width', '188px');
    

    colunaItem.textContent = "ITEM";
    colunaCodigo.textContent = "CODIGO";
    colunaDescricao.textContent = "PRODUTOS";
    colunaQuantidade.textContent = "QTDE.";
    colunaDataEntrega.textContent = "ENTREGA";
    colulaPrecoUnit.textContent = "PREÇO UN.";
    colunaPreco.textContent = 'PREÇO';
    colunaVolume.textContent = 'VOLUME';
    colunaPeso.textContent = 'PESO';
    colunaNcm.textContent = 'NCM';

    linha.appendChild(colunaItem);
    linha.appendChild(colunaCodigo);
    linha.appendChild(colunaDescricao);
    linha.appendChild(colunaDataEntrega);
    linha.appendChild(colunaNcm);
    linha.appendChild(colunaQuantidade);
    linha.appendChild(colulaPrecoUnit);
    linha.appendChild(colunaPreco);
    linha.appendChild(colunaVolume);
    linha.appendChild(colunaPeso);

    tabela.appendChild(linha);

    var i = 1
    for (const item of dados.results) {
        const linha = document.createElement("tr");
        const colunaItem = document.createElement("td");
        const colunaCodigo = document.createElement("td");
        const colunaDescricao = document.createElement("td");
        const colunaQuantidade = document.createElement("td");
        const colunaDataEntrega = document.createElement("td");
        const colulaPrecoUnit = document.createElement("td");
        const colunaPreco = document.createElement("td");
        const colunaNcm = document.createElement("td");
        const colunaVolume = document.createElement("td");
        const colunaPeso = document.createElement("td");

        colunaItem.textContent = i.toString();
        colunaCodigo.textContent = item.peca.codigo;
        colunaDescricao.textContent = item.peca.descricao;
        colunaQuantidade.textContent = item.quantidade;
        colunaDataEntrega.textContent = formatarData(item.dataEntrega);
        colulaPrecoUnit.textContent = formatarPreco(item.peca.precoVenda * 1.2);
        colunaPreco.textContent = formatarPreco(item.peca.precoVenda * item.quantidade * 1.2);
        colunaNcm.textContent = item.peca.ncm;
        colunaVolume.textContent = item.peca.volume;
        colunaPeso.textContent = item.peca.peso

        precoTotal  += item.peca.precoVenda * item.quantidade;
        volumeTotal += item.peca.volume     * item.quantidade;
        pesoTotal   += item.peca.peso       * item.quantidade;        

        linha.appendChild(colunaItem);
        linha.appendChild(colunaCodigo);
        linha.appendChild(colunaDescricao);
        linha.appendChild(colunaDataEntrega);
        linha.appendChild(colunaNcm);
        linha.appendChild(colunaQuantidade);
        linha.appendChild(colulaPrecoUnit);
        linha.appendChild(colunaPreco);
        linha.appendChild(colunaVolume);
        linha.appendChild(colunaPeso);

        tabela.appendChild(linha);

        i++;
      }
      const totalOrcado = document.getElementById("total-orcado");
      const totalPeso = document.getElementById("total-peso");
      const totalVolume = document.getElementById("total-volume");
      
      totalOrcado.append('PREÇO TOTAL  = ');
      totalOrcado.append(formatarPreco(precoTotal));

      totalVolume.append('VOLUME TOTAL = ');
      totalVolume.append(formatarPreco(volumeTotal));

      totalPeso.append('PESO TOTAL     = ');
      totalPeso.append(formatarPreco(pesoTotal));

}