from django.db import models

def add_ten():
    return 1 + 10

class Peca(models.Model):
    RET = (
        ('R', 'R'),
        ('N', 'N'),
        ('D', 'D')
    )
    codigo = models.CharField(max_length=30)
    codigoInterno = models.IntegerField(default=add_ten)
    descricao = models.CharField(max_length=30)
    marca = models.CharField(max_length = 50)
    precoVenda = models.DecimalField( max_digits=15, decimal_places=3)
    precoExportacao = models.DecimalField( max_digits=15, decimal_places=3)
    precoNacional = models.DecimalField( max_digits=15, decimal_places=3)
    ret = models.CharField(max_length=1, choices = RET, blank=False, null=False,default='R')
    cc = models.IntegerField()
    peso = models.DecimalField( max_digits=15, decimal_places=3)
    comprimento = models.DecimalField( max_digits=15, decimal_places=3)
    largura = models.DecimalField( max_digits=15, decimal_places=3)
    altura = models.DecimalField( max_digits=15, decimal_places=3)
    ncm = models.IntegerField()
    gde = models.IntegerField()

    @property
    def volumePeca(self):
        return self.comprimento * self.altura * self.largura

    def __str__(self):
        return self.descricao
    
class Usuario(models.Model):
    nome = models.CharField(max_length=250)
    empresa = models.CharField(max_length=250)
    email = models.EmailField(max_length=30)
    site = models.URLField( max_length=200)
    cpfCnpj = models.CharField(max_length=14)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=60)
    pais = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)

class Cliente(models.Model):
    Pessoa = (
        ('f', 'Pessoa Fisica'),
        ('j', 'Pessoa Juridica'),
    )
    tipoPessoa = models.CharField(choices = Pessoa, max_length=1, default = 'j')
    nomeCliente = models.CharField(max_length=50)
    cpfCnpj = models.CharField(max_length=14)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=60)
    pais = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    site = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    detalhe = models.TextField()
    
class Fornecedor(models.Model):
    Pessoa = (
        ('f', 'Pessoa Fisica'),
        ('j', 'Pessoa Juridica'),
    )
    tipoPessoa = models.CharField(choices = Pessoa, max_length=1, default = 'j')
    nomeFornecedor = models.CharField(max_length=50)
    cpfCnpj = models.CharField(max_length=14)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=60)
    pais = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    site = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    detalhe = models.TextField()
    
class PecaFornecedor(models.Model):
    codigo = models.CharField(max_length = 30)
    peca = models.ForeignKey(Peca, on_delete = models.DO_NOTHING)
    preco = models.DecimalField( max_digits=15, decimal_places=3)
    fonecedor = models.ForeignKey(Fornecedor, on_delete = models.DO_NOTHING)
  
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
    tipoEntrega = models.CharField(max_length=1, choices = entrega, blank=False, null=False,default='3') 
    responsavel = models.CharField(max_length=50)
    frete = models.DecimalField(max_digits=15, decimal_places=3)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    marcasEmbarque = models.CharField(max_length=250)
    nomeEntrega = models.CharField(max_length=250)
    cnpjEntrega = models.CharField(max_length=250)
    enderecoEntrega = models.CharField(max_length=250)
    cidadeEntrega = models.CharField(max_length=250)
    paisEntrega = models.CharField(max_length=250)

class Notificar(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

class Pedido(models.Model):
    status = (
        ('1', 'Orçado'),
        ('2', 'Comprado'),
        
    )
    codigoPedido = models.IntegerField()
    codigoPeca = models.ForeignKey(Peca, on_delete= models.DO_NOTHING)
    codigoOrcamento = models.ForeignKey(Orcamento, on_delete=models.DO_NOTHING)
    codigoCliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    dataCriacao = models.DateField(auto_now_add=True, editable=False)
    dataEntrega = models.DateField()
    quantidade = models.IntegerField()
    pesoBruto = models.DecimalField(max_digits=15, decimal_places=3)
    volumeBruto = models.DecimalField(max_digits=15, decimal_places=3)
    unidade = models.CharField(max_length = 255)
    pacote = models.CharField(max_length = 255)
    volume = models.IntegerField()
    
class CondicaoPagamento(models.Model):
    STATUS = (
        ('1', 'Não Pago'),
        ('2', 'Pago'),
    )
    status = models.CharField(choices = STATUS, default = '1', blank=False, max_length=1)
    cota = models.CharField(max_length = 255)
    porcentagem = models.DecimalField(max_digits=15, decimal_places=3)
    data = models.DateField()
    total = models.DecimalField(max_digits=15, decimal_places=3)
    orcamento = models.ForeignKey(Orcamento, on_delete = models.DO_NOTHING)
    
class Cotacao(models.Model):
    codigo = models.CharField(max_length = 30)
    codigoPedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    codigoPecaFornecedor = models.ForeignKey(PecaFornecedor, on_delete = models.DO_NOTHING)
    