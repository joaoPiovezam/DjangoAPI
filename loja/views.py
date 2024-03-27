from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework import status
from rest_framework.decorators import api_view
from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, PecaFornecedor, Cotacao
from loja.serializer import PecaSerializer, ClienteSerializer, OrcamentoSerializer, PedidoSerializer, ListaPedidoOrcamentoSerializer, FornecedorSerializer, PecaFornecedorSerializer, CotacaoSerializer
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
 
 
class PecasFornecedoresViewSet(viewsets.ModelViewSet):
    """Exibindo todos os fornecedores"""
    
    serializer_class = PecaFornecedorSerializer
    def get_queryset(self):
        queryset = PecaFornecedor.objects.all()
        peca = self.request.query_params.get('peca')
        if peca is not None:
            queryset = queryset.filter(peca__codigo=peca)
        return queryset
  
class FornecedoresViewSet(viewsets.ModelViewSet):
    """Exibindo todos os fornecedores"""
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    
class FornecedorList(generics.ListAPIView):
    """Exibindo lista de todos os fornecedores"""
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('codigo', 'nomeFornecedor')
    
class PecaFornecedorList(generics.ListAPIView):
    """Exibindo lista de todas pecas dos fornecedores"""
    queryset = PecaFornecedor.objects.all()
    serializer_class = PecaFornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('peca__codigo', 'fornecedor')
    
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
    
class CotacaoViewSet(viewsets.ModelViewSet):
    """Exibindo todos as cotações"""
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer