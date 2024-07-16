from django.shortcuts import render

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from loja.models import Peca, Cliente, Orcamento, Pedido, Fornecedor, PecaFornecedor, Cotacao, Usuario, CondicaoPagamento, Notificar
from loja.models import Transportadora, PedidoCompra, Estoque, Pack

from loja.serializer import PecaSerializer, ClienteSerializer, OrcamentoSerializer,ClienteOrcamentoSerializer, PedidoSerializer, PedidoPecaSerializer
from loja.serializer import ListaPedidoOrcamentoSerializer, FornecedorSerializer, PecaFornecedorSerializerV2, PecaFornecedorSerializer
from loja.serializer import CotacaoSerializer, CotacaoSerializerV2, UsuarioSerializer, CondicaoPagamentoSerializer, NotificarSerializer
from loja.serializer import TransportadoraSerializer, PedidoCompraSerializer, PedidoCompraAllSerializer, EstoqueSerializer, EstoquePecaSerializer, PackSerializer

import pandas as pd
import os, django

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
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['codigoPeca__id']
    
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

def addPecas(arquivo):
    tabela = pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

    l = len(tabela)
    for i in range(l):
        p = Peca(codigo = tabela['codigo'][i], descricao = tabela['descricao'][i], precoVenda = tabela['precoVenda'][i],
                precoExportacao = tabela['precoExportacao'][i], precoNacional = tabela['precoNacional'][i], ret = tabela['ret'][i],
                cc = tabela['cc'][i], peso  = tabela['peso'][i], comprimento = tabela['comprimento'][i],
                largura = tabela['largura'][i], altura = tabela['altura'][i], ncm = tabela['ncm'][i], gde  = tabela['gde'][i])
    p.save()
    return "peças adicionadas"

class AddPecasView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        arquivo = 'arquivosCsv/' + self.kwargs['arquivo']
        result = addPecas(arquivo)
        return Response(data={result})
    
def addPrecosFornecedor(arquivo, fonecedorId):
    tabela = pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

    l = len(tabela)
    fornecedorO = Fornecedor.objects.filter(id = fonecedorId).first()
    pecasNaoEncontradas = []
    pecasEncontradas = []
    for i in range(l):
        pecaO = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
        pecaFornecedor = PecaFornecedor.objects.filter(fornecedor = fornecedorO).all()
        pecaFornecedor = pecaFornecedor.filter(peca = pecaO ).first()
        if (pecaO is None):
            pecasNaoEncontradas.append(tabela['codigo'][i])
        else:
            pecasEncontradas.append(tabela['codigo'][i])
            if (pecaFornecedor is None):
                pf = PecaFornecedor(           
                        codigo = 12,
                        peca = pecaO,
                        preco = tabela['preco\r'][i],
                        fornecedor = fornecedorO
                        )
                pf.save()
            else:
                pecaFornecedor.preco = tabela['preco\r'][i]
                pecaFornecedor.save()

    return ("Peças adicionadas ao fornecedor : " + str(pecasEncontradas) + "Peças não encontradas : " + str(pecasNaoEncontradas))

class AddPecasFornecedorView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        arquivo = 'arquivosCsv/' + self.kwargs['arquivo']
        result = addPrecosFornecedor(arquivo, self.kwargs['fornecedorId'])
        return Response(data={result})
    
def addPedidosOrcamento(arquivo, clienteId, orcamentoId):
    tabela = pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

    l = len(tabela)
    pedido = Pedido.objects.last()
    codigoP = pedido.codigoPedido + 1
    cliente = Cliente.objects.filter(id = clienteId).first()
    orcamento = Orcamento.objects.filter(id = orcamentoId).first()
    pecasEncontradas = []
    pecasNaoEncontradas = []

    for i in range(l):
            peca = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
            if (peca is None):
                    pecasNaoEncontradas.append(tabela['codigo'][i])
            else:
                    pecasEncontradas.append(tabela['codigo'][i])
                    p = Pedido(           
                            codigoPedido = codigoP,
                            codigoPeca = peca,
                            codigoOrcamento = orcamento,
                            codigoCliente = cliente,
                            dataEntrega = '2024-05-10',
                            quantidade =  tabela['qtd'][i],
                            pesoBruto = 10,
                            volume = 0,
                            volumeBruto = 10
                            )
                    p.save()

    return ("Peças adicionadas : " + str(pecasEncontradas) + "Peças não encontradas : "  + str(pecasNaoEncontradas))

class addPedidosOrcamentoView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        arquivo = 'arquivosCsv/' + self.kwargs['arquivo']
        result = addPedidosOrcamento(arquivo, self.kwargs['clienteId'], self.kwargs['orcamentoId'])
        return Response(data={result})
    
def gerarCotacao(orcamentoId):
    pedidos = Pedido.objects.all().filter(codigoOrcamento = orcamentoId)
    pecasAdicionadas = []
    pecasNaoAdicionadas = []
    for pedido in pedidos:
            pecas = pedido.codigoPeca
            pecaFornecedor = PecaFornecedor.objects.filter(peca = pecas).order_by('-preco').last()
            if pecaFornecedor is None:
                pecasNaoAdicionadas.append(pecas.codigo)
            else:
                cotacao = Cotacao(
                        codigo = 1,
                        codigoPedido = pedido,
                        codigoPecaFornecedor = pecaFornecedor
                )
                cotacao.save()
                pecasAdicionadas.append(pecas.codigo + ' - Fonecedor: ' + pecaFornecedor.fornecedor.nomeFornecedor)
    return 'peças adicionadas: ' + str(pecasAdicionadas) + ' pecas não encontradas: ' + str(pecasNaoAdicionadas)
    
            
class gerarCotacaoView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = gerarCotacao(self.kwargs['orcamentoId'])
        return Response(data={result})