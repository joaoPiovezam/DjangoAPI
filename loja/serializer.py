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
        
      
class PedidoSerializer(serializers.ModelSerializer):
    peca = PecaSerializer(source = 'codigoPeca')
    class Meta:
        model = Pedido
        fields  = ['peca','quantidade']
                        
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    orcamento = OrcamentoSerializer(source = 'codigoOrcamento')
    peca = PecaSerializer(source = 'codigoPeca')
    cliente = ClienteSerializer(source = 'codigoCliente')
    class Meta:
        model = Pedido
        fields = ['peca','quantidade','orcamento','cliente']