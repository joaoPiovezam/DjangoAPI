from rest_framework import serializers
from loja.models import Peca, Cliente, Orcamento, Pedido

class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = ['id', 'codigo', 'descricao', 'precoVenda', 'precoExpotacao', 'precoNacional', 'ret', 'cc', 'peso', 'comprimento', 'largura', 'altura', 'ncm', 'gde']
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'
        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    orcamento = serializers.ReadOnlyField(source='orcamento.codigo')
    peca = serializers.ReadOnlyField(source='peca.descricao')
    class Meta:
        model = Pedido
        fields = '__all__'