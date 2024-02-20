from rest_framework import serializers
from loja.models import Peca, Cliente, Orcamento, Pedido

class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = '__all__'
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
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
    peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields  = ['peca','quantidade']
                        
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteOrcamentoSerializer(source = 'codigoOrcamento')
    orcamento = OrcamentoSerializer(source = 'codigoOrcamento')
    peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields = ['peca','quantidade','dataEntrega','codigoCliente','orcamento','cliente']