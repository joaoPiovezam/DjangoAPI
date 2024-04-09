from rest_framework import serializers
from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, Transportadora, PecaFornecedor, Cotacao, Notificar, Usuario, CondicaoPagamento, PedidoCompra, Estoque

class PecaSerializer(serializers.ModelSerializer):
    volume = serializers.ReadOnlyField(source='volumePeca')
    class Meta:
        model = Peca
        fields = '__all__'
        extra_fields = ['volume']
        filter_fields = ('codigo',)

    '''def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        codigo = self.context['request'].query_params.get('codigo')
        if codigo:
            queryset = queryset.filter(codigo__icontains=codigo)
        return queryset'''
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class TransportadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportadora
        fields = '__all__'
        
class PecaFornecedorSerializer(serializers.ModelSerializer):
    peca = PecaSerializer()
    menor  = serializers.ReadOnlyField(source = 'menorPrecoPeca')
    class Meta:
        model = PecaFornecedor
        fields = '__all__'
        extra_fields = ['peca','menor']
        

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        
class NotificarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificar
        fields = '__all__'
        
class CondicaoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicaoPagamento
        fields = '__all__'             
         
class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'    
        
class ClienteOrcamentoSerializer(serializers.ModelSerializer):
    client = ClienteSerializer(source = 'cliente')
    class Meta:
        model = Orcamento
        fields = ['client']
            
class PedidoSerializer(serializers.ModelSerializer):
    #peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields  = '__all__'#['peca','quantidade']
                        
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteOrcamentoSerializer(source = 'codigoOrcamento')
    orcamento = OrcamentoSerializer(source = 'codigoOrcamento')
    peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields = ['peca','quantidade','dataEntrega','codigoCliente','orcamento','cliente']
        
class CotacaoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(source = 'codigoPedido')
    pecaFornecedor  = PecaFornecedorSerializer(source = 'codigoPecaFornecedor')
    class Meta:
        model = Cotacao
        fields = '__all__'
        extra_fields = ['pedido','pecaFornecedor']
        
class PedidoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCompra
        fields = '__all__'

class PedidoCompraAllSerializer(serializers.ModelSerializer):
    cotacao = CotacaoSerializer()
    transportadora = TransportadoraSerializer()
    class Meta:
        model = PedidoCompra
        fields = '__all__'
        extra_fields = ['cotacao', 'transportadora']
        
class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'