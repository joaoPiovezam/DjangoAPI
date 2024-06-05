from django.db import models

def add_ten():
    return 1 + 10

class Peca(models.Model):
    RET = (
        ('R', 'R'),
        ('N', 'N'),
        ('D', 'D')
    )
    codigo = models.CharField(max_length = 30)
    codigoInterno = models.IntegerField(default = add_ten)
    descricao = models.CharField(max_length = 30)
    marca = models.CharField(max_length = 50)
    precoVenda = models.DecimalField( max_digits = 15, decimal_places = 3)
    precoExportacao = models.DecimalField( max_digits = 15, decimal_places = 3)
    precoNacional = models.DecimalField( max_digits = 15, decimal_places = 3)
    ret = models.CharField(max_length = 1, choices = RET, blank = False, null = False, default = 'R')
    cc = models.IntegerField()
    peso = models.DecimalField( max_digits = 15, decimal_places = 3)
    comprimento = models.DecimalField( max_digits = 15, decimal_places = 3)
    largura = models.DecimalField( max_digits = 15, decimal_places = 3)
    altura = models.DecimalField( max_digits = 15, decimal_places = 3)
    ncm = models.IntegerField()
    gde = models.IntegerField()

    @property
    def volumePeca(self):
        return self.comprimento * self.altura * self.largura

    def __str__(self):
        return self.codigo + ' - ' + self.descricao
    
class Usuario(models.Model):
    nome = models.CharField(max_length = 250)
    empresa = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 30)
    site = models.URLField( max_length = 200)
    cpfCnpj = models.CharField(max_length = 14)
    endereco = models.CharField(max_length = 50)
    cep = models.CharField(max_length = 8)
    cidade = models.CharField(max_length = 60)
    pais = models.CharField(max_length = 20)
    telefone = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    Pessoa = (
        ('f', 'Pessoa Fisica'),
        ('j', 'Pessoa Juridica'),
    )
    tipoPessoa = models.CharField(choices = Pessoa, max_length = 1, default = 'j')
    nomeCliente = models.CharField(max_length = 50)
    cpfCnpj = models.CharField(max_length = 14)
    endereco = models.CharField(max_length = 50)
    cep = models.CharField(max_length = 8)
    cidade = models.CharField(max_length = 60)
    pais = models.CharField(max_length = 20)
    telefone = models.CharField(max_length = 20)
    site = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 30)
    detalhe = models.TextField()
    
    def __str__(self):
        return self.nomeCliente
    
class Fornecedor(models.Model):
    Pessoa = (
        ('f', 'Pessoa Fisica'),
        ('j', 'Pessoa Juridica'),
    )
    tipoPessoa = models.CharField(choices = Pessoa, max_length = 1, default = 'j')
    nomeFornecedor = models.CharField(max_length = 50)
    cpfCnpj = models.CharField(max_length = 14)
    endereco = models.CharField(max_length = 50)
    cep = models.CharField(max_length = 8)
    cidade = models.CharField(max_length = 60)
    pais = models.CharField(max_length = 20)
    telefone = models.CharField(max_length = 20)
    site = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 30)
    detalhe = models.TextField()
    
class Transportadora(models.Model):
    nome = models.CharField(max_length = 255)
    cnpj = models.CharField(max_length = 255)
    endereco = models.CharField(max_length = 50)
    cep = models.CharField(max_length = 8)
    cidade = models.CharField(max_length = 60)
    pais = models.CharField(max_length = 20)
    telefone = models.CharField(max_length = 20)
    site = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 30)
    detalhe = models.TextField()
    
    def __str__(self):
        return self.nome
    
class PecaFornecedor(models.Model):
    codigo = models.CharField(max_length = 30)
    peca = models.ForeignKey(Peca, on_delete = models.DO_NOTHING)
    preco = models.DecimalField( max_digits = 15, decimal_places = 3)
    fornecedor = models.ForeignKey(Fornecedor, on_delete = models.DO_NOTHING)
  
class Orcamento(models.Model):
    entrega = (
        ('3', 'Transportadora'),
    )
    status = (
        ('1', 'Orçado'),
        ('2', 'Faturado'),
    )
    codigo = models.IntegerField()
    dataEmissao = models.DateField()
    dataValidade = models.DateField()
    tipoEntrega = models.CharField(max_length = 1, choices = entrega, blank = False, null = False, default = '3') 
    responsavel = models.CharField(max_length = 50)
    frete = models.DecimalField(max_digits = 15, decimal_places = 3)
    cliente = models.ForeignKey(Cliente, on_delete = models.DO_NOTHING)
    marcasEmbarque = models.CharField(max_length = 250)
    nomeEntrega = models.CharField(max_length = 250)
    cnpjEntrega = models.CharField(max_length = 250)
    enderecoEntrega = models.CharField(max_length = 250)
    cidadeEntrega = models.CharField(max_length = 250)
    paisEntrega = models.CharField(max_length = 250)
    
    def __str__(self):
        return str(self.codigo)

class Notificar(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    nome = models.CharField(max_length = 50)
    telefone = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100)

class Pedido(models.Model):
    status = (
        ('1', 'Orçado'),
        ('2', 'Comprado'),
        
    )
    codigoPedido = models.IntegerField()
    codigoPeca = models.ForeignKey(Peca, on_delete = models.DO_NOTHING)
    codigoOrcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    codigoCliente = models.ForeignKey(Cliente, on_delete = models.DO_NOTHING)
    dataCriacao = models.DateField(auto_now_add = True, editable = False)
    dataEntrega = models.DateField()
    quantidade = models.IntegerField()
    pesoBruto = models.DecimalField(max_digits = 15, decimal_places=3)
    volumeBruto = models.DecimalField(max_digits = 15, decimal_places=3)
    unidade = models.CharField(max_length = 255)
    pacote = models.CharField(max_length = 255)
    volume = models.IntegerField()
    
    def __str__(self):
        return str(self.codigoPedido) + self.codigoPeca.codigo
    
class CondicaoPagamento(models.Model):
    STATUS = (
        ('1', 'Não Pago'),
        ('2', 'Pago'),
    )
    status = models.CharField(choices = STATUS, default = '1', blank = False, max_length = 1)
    cota = models.CharField(max_length = 255)
    porcentagem = models.DecimalField(max_digits = 15, decimal_places = 3)
    data = models.DateField()
    total = models.DecimalField(max_digits = 15, decimal_places = 3)
    orcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    
class Cotacao(models.Model):
    codigo = models.CharField(max_length = 30)
    codigoPedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    codigoPecaFornecedor = models.ForeignKey(PecaFornecedor, on_delete = models.DO_NOTHING)

class PedidoCompra(models.Model):
    VENCIMENTOS = (
        ('1', '28'),
        ('2', '30'),
        ('3', '30/60/90'), 
        ('4', '28/56/84'),
        ('5', '30/60'),
        ('6', '28/56'),
        ('7', '30/45/60'),
    )
    cotacao = models.ForeignKey(Cotacao, on_delete = models.DO_NOTHING)
    transportadora = models.ForeignKey(Transportadora, on_delete = models.DO_NOTHING)
    dataEmicao = models.DateField(auto_now_add = True)
    operacaoFiscal = models.CharField(max_length = 255)
    vencimento = models.CharField(choices = VENCIMENTOS, max_length = 50)
    comprador = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    observacoes = models.TextField()
    frete = models.CharField(max_length = 255)
    
class Estoque(models.Model):
    STATUS = (
        ('1', 'a caminho do estoque'),
        ('2', 'em estoque'),
        ('3', 'em separação'),
        ('4', 'a caminho do cliente'),
        ('5', 'entregue ao cliente')
    )
    dataEntrada = models.DateField()
    dataSaida = models.DateField()
    codigoPedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    
class Pack(models.Model):
    volume = models.IntegerField()
    pacote = models.CharField(max_length = 255)
    comprimento = models.DecimalField( max_digits = 15, decimal_places = 3)
    largura = models.DecimalField( max_digits = 15, decimal_places = 3)
    altura = models.DecimalField( max_digits = 15, decimal_places = 3)
    peso = models.DecimalField( max_digits = 15, decimal_places = 3)
    orcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    
    @property
    def volumePacote(self):
        return self.comprimento * self.altura * self.largura