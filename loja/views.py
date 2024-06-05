from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework import status
from rest_framework.decorators import api_view

from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, PecaFornecedor, Cotacao, Usuario, CondicaoPagamento, Notificar
from loja.models import Transportadora, PedidoCompra, Estoque, Pack

from loja.serializer import PecaSerializer, ClienteSerializer, OrcamentoSerializer,ClienteOrcamentoSerializer, PedidoSerializer, PedidoPecaSerializer
from loja.serializer import ListaPedidoOrcamentoSerializer, FornecedorSerializer, PecaFornecedorSerializerV2, PecaFornecedorSerializer
from loja.serializer import CotacaoSerializer, CotacaoSerializerV2, UsuarioSerializer, CondicaoPagamentoSerializer, NotificarSerializer
from loja.serializer import TransportadoraSerializer, PedidoCompraSerializer, PedidoCompraAllSerializer, EstoqueSerializer, EstoquePecaSerializer, PackSerializer

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
    search_fields = ('cpfCnpj', 'nomeFornecedor')
    
class PecaFornecedorList(generics.ListAPIView):
    """Exibindo lista de todas pecas dos fornecedores"""
    def get_queryset(self):
        queryset = PecaFornecedor.objects.all()
        if self.kwargs['peca'] != 0:
            queryset = queryset.filter(peca__id = self.kwargs['peca'])
        if self.kwargs['fornecedor'] != 0:
            queryset = queryset.filter(fornecedor__id = self.kwargs['fornecedor'])
        return queryset
    serializer_class = PecaFornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['peca__codigo', 'fornecedor__nomeFornecedor']
    
class PecaFornecedorView(viewsets.ModelViewSet):
    """Exibindo lista de todas pecas dos fornecedores"""
    queryset = PecaFornecedor.objects.all()
    serializer_class = PecaFornecedorSerializerV2
    
class PecasFornecedoresView(generics.ListAPIView):
    """Exibindo peça de um fornecedor"""
    
    def get_queryset(self):
        queryset = PecaFornecedor.objects.filter(peca = self.kwargs['pecaId'])
        queryset = queryset.filter(id = self.kwargs['fornecedorId'])
        return queryset
    serializer_class = PecaFornecedorSerializer
    
class OrcamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os orçamentos"""
    queryset = Orcamento.objects.all()
    def get_serializer_class(self):
        return ClienteOrcamentoSerializer #OrcamentoSerializer
    
class PedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos"""
    queryset = Pedido.objects.all()
    def get_serializer_class(self):
        return PedidoSerializer

class PedidoView(generics.ListAPIView):
    """Exibindo todos os pedidos"""
    queryset = Pedido.objects.all()
    def get_serializer_class(self):
        return PedidoPecaSerializer
    
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

class CotacaoOrcamentoViewSet(generics.ListAPIView):
    """Exibindo todas as cotações"""
    def get_queryset(self):
        queryset = Cotacao.objects.filter(codigoPedido__codigoOrcamento = self.kwargs['pk'])
        return queryset
    serializer_class = CotacaoSerializer

class Cotacao2ViewSet(viewsets.ModelViewSet):
    """Exibindo todas as cotações"""
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializerV2
    
class UsuarioViewSet(viewsets.ModelViewSet):
    """Exibindo todos os usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class CondicaoPagamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todas as condicoes"""
    queryset = CondicaoPagamento.objects.all()
    serializer_class = CondicaoPagamentoSerializer

class CondicaoPagamentoView(generics.ListAPIView):
    """Exibindo todas as condicoes"""
    def get_queryset(self):
        queryset = CondicaoPagamento.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
    serializer_class = CondicaoPagamentoSerializer

class NotificarViewSet(viewsets.ModelViewSet):
    """Exibindo todas as notificacoes"""
    queryset = Notificar.objects.all()
    serializer_class = NotificarSerializer

class NotificarView(generics.ListAPIView):
    """Exibindo todas as notificacoes"""
    def get_queryset(self):
        queryset = Notificar.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
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
        queryset = PedidoCompra.objects.filter(cotacao__codigoPedido__codigoOrcamento = self.kwargs['pkOrcamento'])
        queryset = queryset.filter(cotacao__codigoPecaFornecedor__fornecedor = self.kwargs['pkFornecedor'])
        return queryset
    serializer_class = PedidoCompraAllSerializer
    
class EstoqueViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos de compras"""
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer

class EstoqueView(generics.ListAPIView):
    """Exibindo todos os pedidos de compras"""
    queryset = Estoque.objects.all()
    serializer_class = EstoquePecaSerializer
    
class PackViewSet(viewsets.ModelViewSet):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer

class PackView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Pack.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
    serializer_class = PackSerializer