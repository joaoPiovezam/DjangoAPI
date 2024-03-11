from django.db import models

class Peca(models.Model):
    RET = (
        ('R', 'R'),
        ('N', 'N'),
        ('D', 'D')
    )
    codigo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=30)
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

    def __str__(self):
        return self.descricao

class Cliente(models.Model):
    nomeCliente = models.CharField(max_length=50)
    cpfCnpj = models.CharField(max_length=14)
    rgIE = models.CharField(max_length=20)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=60)
    pais = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    contato = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    
class Fornecedor(models.Model):
    nomeFornecedor = models.CharField(max_length = 255)
    
    
   
class Orcamento(models.Model):
    entrega = (
        ('3', 'Transportadora'),
    )
    codigo = models.IntegerField()
    dataEmissao = models.DateField()
    dataValidade = models.DateField()
    tipoEntrega = models.CharField(max_length=1, choices = entrega, blank=False, null=False,default='3') 
    responsavel = models.CharField(max_length=50)
    frete = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Pedido(models.Model):
    codigoPedido = models.IntegerField()
    codigoPeca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    codigoOrcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
    codigoCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dataEntrega = models.DateField()
    quantidade = models.IntegerField()
    def __str__(self):
        return self.quantidade