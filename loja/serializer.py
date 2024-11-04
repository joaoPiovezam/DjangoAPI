from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, Transportadora, PecaFornecedor, Cotacao, Notificar, Usuario
from loja.models import CondicaoPagamento, PedidoCompra, Estoque, Pack
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']
        
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
        

        
class PecaFornecedorSerializerV2(serializers.ModelSerializer):
    menor  = serializers.ReadOnlyField(source = 'menorPrecoPeca')
    class Meta:
        model = PecaFornecedor
        fields = '__all__'
        extra_fields = ['menor']

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        
class PecaFornecedorSerializer(serializers.ModelSerializer):
    peca = PecaSerializer()
    fornecedor = FornecedorSerializer()
    menor  = serializers.ReadOnlyField(source = 'menorPrecoPeca')
    class Meta:
        model = PecaFornecedor
        fields = '__all__'
        extra_fields = ['peca','menor', 'fornecedor']
        
class NotificarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificar
        fields = '__all__'
        
class CondicaoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicaoPagamento
        fields = '__all__'             
         
class OrcamentoSerializer(ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'    
        
class ClienteOrcamentoSerializer(serializers.ModelSerializer):
    client = ClienteSerializer(source = 'cliente')
    class Meta:
        model = Orcamento
        fields = '__all__'
        extra_fields = ['client']
            
class PedidoSerializer(serializers.ModelSerializer):
    #peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields  = '__all__'#['peca','quantidade']
        #extra_fields = ['peca']

class PedidoPecaSerializer(serializers.ModelSerializer):
    peca = PecaSerializer(source = 'peca')
    orcamento = ClienteOrcamentoSerializer(source = 'orcamento')
    class Meta:
        model = Pedido
        fields  = '__all__'#['peca','quantidade']
        extra_fields = ['peca','orcamento']
                        
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteOrcamentoSerializer(source = 'orcamento')
    orcamento = OrcamentoSerializer(source = 'orcamento')
    peca = PecaSerializer(source = 'peca')
    class Meta:
        model = Pedido
        fields = '__all__'#['id','peca','quantidade','dataEntrega','codigoCliente','orcamento','cliente','unidade']
        extra_fields = ['cliente','orcamento','peca']
        
class CotacaoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(source = 'pedido')
    pecasFornecedor  = PecaFornecedorSerializer(source = 'pecafornecedor')
    class Meta:
        model = Cotacao
        fields = '__all__'
        extra_fields = ['pedido','pecasFornecedor']

class CotacaoSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = '__all__'
        
class PedidoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCompra
        fields = '__all__'

class PedidoCompra2Serializer(serializers.ModelSerializer):
    vencimento = serializers.CharField(source='get_vencimento_display')
    transportadora = TransportadoraSerializer()
    class Meta:
        model = PedidoCompra
        fields = '__all__'
        extra_fields = ['vencimento', 'transportadora']

class PedidoCompraAllSerializer(serializers.ModelSerializer):
    pedido = PedidoPecaSerializer(source = 'pedido') 
    pecasFornecedor  = PecaFornecedorSerializer(source = 'pecafornecedor')
    class Meta:
        model = Cotacao
        fields = '__all__' 
        extra_fields = ['pedido', 'pecasFornecedor']
        
class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'

class EstoquePecaSerializer(serializers.ModelSerializer):
    pedido = PedidoPecaSerializer(source = 'pedido')
    class Meta:
        model = Estoque
        fields = '__all__'
        extra_fields = ['pedido', 'orcamento']

class PackSerializer(serializers.ModelSerializer):
    volumePack = serializers.ReadOnlyField(source='volumePacote')
    class Meta:
        model = Pack
        fields = '__all__'
        extra_fields = ['volumePack']