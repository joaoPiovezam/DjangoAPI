from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework import status
from rest_framework.decorators import api_view
from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, PecaFornecedor, Cotacao, Usuario, CondicaoPagamento, Notificar, Transportadora, PedidoCompra, Estoque
from loja.serializer import PecaSerializer, ClienteSerializer, OrcamentoSerializer, PedidoSerializer, ListaPedidoOrcamentoSerializer, FornecedorSerializer, PecaFornecedorSerializer, CotacaoSerializer, UsuarioSerializer, CondicaoPagamentoSerializer, NotificarSerializer, TransportadoraSerializer, PedidoCompraSerializer, PedidoCompraAllSerializer, EstoqueSerializer
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
    """Exibindo todas as cotações"""
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer
    
class UsuarioViewSet(viewsets.ModelViewSet):
    """Exibindo todos os usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class CondicaoPagamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todas as condicoes"""
    queryset = CondicaoPagamento.objects.all()
    serializer_class = CondicaoPagamentoSerializer

class NotificarViewSet(viewsets.ModelViewSet):
    """Exibindo todas as notificacoes"""
    queryset = Notificar.objects.all()
    serializer_class = NotificarSerializer
    
class TransportadoraViewSet(viewsets.ModelViewSet):
    """Exibindo todas as tranportadoras"""
    queryset = Transportadora.objects.all()
    serializer_class = TransportadoraSerializer

class PedidoCompraViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos de compras"""
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializer
    
class PedidoCompraAllViewSet(generics.ListAPIView):
    """Exibindo todos pedidos de um orcamento de um fornecedor"""
    def get_queryset(self):
        queryset = PedidoCompra.objects.filter(cotacao__codigoPedido__codigoOrcamento = self.kwargs['pk'])
        return queryset
    serializer_class = PedidoCompraAllSerializer
    
class EstoqueViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos de compras"""
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer