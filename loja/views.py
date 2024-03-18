from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework import status
from rest_framework.decorators import api_view
from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor
from loja.serializer import PecaSerializer, ClienteSerializer, OrcamentoSerializer, PedidoSerializer, ListaPedidoOrcamentoSerializer, FornecedorSerializer
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

class PecasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as peças"""
    queryset = Peca.objects.all()
    def get_serializer_class(self):
        return PecaSerializer
    serializer_class = PecaSerializer

    
class PecaList(generics.ListAPIView):
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('codigo', 'descricao')
    
    
class ClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os clientes"""
    queryset = Cliente.objects.all()
    def get_serializer_class(self):
        return ClienteSerializer
 

    
class FornecedoresViewSet(viewsets.ModelViewSet):
    """Exibindo todos os fornecedores"""
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    http_method_names = ['get', 'post', 'put', 'path']
    
class FornecedorList(generics.ListAPIView):
    """Exibindo lista de todos os fornecedores"""
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('codigo', 'nomeFornecedor')
    
class OrcamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os orçamentos"""
    queryset = Orcamento.objects.all()
    def get_serializer_class(self):
        return OrcamentoSerializer
    
class PedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos"""
    queryset = Pedido.objects.all()
    def get_serializer_class(self):
        return PedidoSerializer
    
class PedidoOrcamentoViewSet(generics.ListAPIView):
    """Exibindo todos os pedidos de um orcamento"""
    
    def get_queryset(self):
        queryset = Pedido.objects.filter(codigoOrcamento = self.kwargs['pk'])
        return queryset
    serializer_class = ListaPedidoOrcamentoSerializer