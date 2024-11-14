from django.shortcuts import render

from setup import settings

from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext
import jwt
from django.contrib.auth import authenticate

from loja.models import (Peca, Usuario, Cliente, Orcamento, Pedido, Fornecedor, PecaFornecedor, Cotacao, Usuario, CondicaoPagamento, Notificar,
 Transportadora, PedidoCompra, Estoque, Pack)

from loja.serializer import (UserSerializer, PecaSerializer, UsuarioSerializer, ClienteSerializer, OrcamentoSerializer,ClienteOrcamentoSerializer, PedidoSerializer, PedidoPecaSerializer,
 ListaPedidoOrcamentoSerializer, FornecedorSerializer, PecaFornecedorSerializerV2, PecaFornecedorSerializer,
 CotacaoSerializer, CotacaoSerializerV2, UsuarioSerializer, CondicaoPagamentoSerializer, NotificarSerializer,
 TransportadoraSerializer, PedidoCompraSerializer, PedidoCompraAllSerializer,PedidoCompra2Serializer, EstoqueSerializer, EstoquePecaSerializer, PackSerializer)

import pandas as pd
import re
import json
import os, django

from django.http import HttpResponse

@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    user = authenticate(username=request.data['username'], password=request.data['password'])
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    usuario = Usuario.objects.filter(email = user.email).first()
    usuarioS = UsuarioSerializer(usuario)
    #cliente = Cliente.objects.filter(email = user.email)
    if usuario is None:
        tipo = "cliente"
    else:
        tipo = "usuario"
        print (usuario.cpfcnpj)
    return Response({'token': token.key, 'user': serializer.data,'tipo': tipo})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
def test_token(request):
    return Response("passed!")

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PecasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as peças"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Peca.objects.all()
    def get_serializer_class(self):
        return PecaSerializer
    serializer_class = PecaSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class PecaList(generics.ListAPIView):
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Peca.objects.all()
        if self.kwargs['codigo'] != 0: 
            queryset = queryset.filter(codigo = self.kwargs['codigo'])
        return queryset
    serializer_class = PecaSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('codigo', 'descricao')
       
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class ClientesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os clientes"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Cliente.objects.all()
    def get_serializer_class(self):
        return ClienteSerializer
 
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])   
class PecasFornecedoresViewSet(viewsets.ModelViewSet):
    """Exibindo todos os fornecedores"""
    #permission_classes = (permissions.AllowAny, )
    serializer_class = PecaFornecedorSerializer
    def get_queryset(self):
        queryset = PecaFornecedor.objects.all()
        peca = self.request.query_params.get('peca')
        if peca is not None:
            queryset = queryset.filter(peca__codigo=peca)
        return queryset

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])    
class FornecedoresViewSet(viewsets.ModelViewSet):
    """Exibindo todos os fornecedores"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class FornecedorList(generics.ListAPIView):
    """Exibindo lista de todos os fornecedores"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('cpfcnpj', 'nome_fornecedor')
 
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class PecaFornecedorList(generics.ListAPIView):
    """Exibindo lista de todas pecas dos fornecedores"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = PecaFornecedor.objects.all()
        if self.kwargs['peca'] != 0:
            queryset = queryset.filter(peca__id = self.kwargs['peca'])
        if self.kwargs['fornecedor'] != 0:
            queryset = queryset.filter(fornecedor__id = self.kwargs['fornecedor'])
        return queryset
    serializer_class = PecaFornecedorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['peca__codigo', 'fornecedor__nome_fornecedor']

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class PecaFornecedorView(viewsets.ModelViewSet):
    """Exibindo lista de todas pecas dos fornecedores"""
    #permission_classes = (permissions.AllowAny, )
    queryset = PecaFornecedor.objects.all()
    serializer_class = PecaFornecedorSerializerV2
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class PecasFornecedoresView(generics.ListAPIView):
    """Exibindo peça de um fornecedor"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = PecaFornecedor.objects.all()
        queryset = queryset.filter(peca__id = self.kwargs['pecaId'])
        queryset = queryset.filter(fornecedor__id  = self.kwargs['fornecedorId'])
        return queryset
    serializer_class = PecaFornecedorSerializer
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def OrcamentoView(request):
    session_key = request.COOKIES.get('sessionid')
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    #email = request.COOKIES.get('email')
    email = user.email
    orcamentos = Orcamento.objects.filter(cliente__email = email)
    serializer = OrcamentoSerializer(orcamentos, many=True)
    return Response(serializer.data)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])    
class OrcamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os orçamentos"""
    queryset = Orcamento.objects.all()
    def get_serializer_class(self):
        return ClienteOrcamentoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])    
class OrcamentoClienteViewSet(generics.ListAPIView):
    """Exibindo todos os orçamentos"""
    def get_queryset(self):
        queryset = Orcamento.objects.filter(cliente__email = self.kwargs['email'])
        return queryset
    
    def get_serializer_class(self):
        return ClienteOrcamentoSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])   
class OrcamentoListView(generics.ListAPIView):
    """Exibindo todos os orçamentos"""
    queryset = Orcamento.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = OrcamentoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_200_OK) 
    def get_serializer_class(self):
        return OrcamentoSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class PedidoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Pedido.objects.all()
    def get_serializer_class(self):
        return PedidoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PedidoView(generics.ListAPIView):
    """Exibindo todos os pedidos"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Pedido.objects.all()
    def get_serializer_class(self):
        return PedidoPecaSerializer
   
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PedidoOrcamentoViewSet(generics.ListAPIView):
    """Exibindo todos os pedidos de um orcamento"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Pedido.objects.filter(orcamento = self.kwargs['pk'])
        if self.kwargs['volume'] != 0:
            queryset = queryset.filter(volume = self.kwargs['volume'])
        if self.kwargs['peca'] != 0:
            queryset = queryset.filter(peca__id = self.kwargs['peca'])
        return queryset
        
    serializer_class = ListaPedidoOrcamentoSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    #search_fields = ['codigoPeca__id']
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class CotacaoViewSet(viewsets.ModelViewSet):
    """Exibindo todas as cotações"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class CotacaoOrcamentoViewSet(generics.ListAPIView):
    """Exibindo todas as cotações"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Cotacao.objects.filter(pedido__orcamento = self.kwargs['pk'])
        return queryset
    serializer_class = CotacaoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class Cotacao2ViewSet(generics.ListAPIView):
    """Exibindo todas as cotações"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Cotacao.objects.all()
        return queryset
    def post(self, request, *args, **kwargs):
        serializer = CotacaoSerializerV2(data = request.data)
        cotacao = Cotacao.objects.filter(pedido = request.data['pedido']).first()
        if cotacao is not None:
            return Response({"pedido já cotado"}, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_200_OK)
    serializer_class = CotacaoSerializerV2
  
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class UsuarioViewSet(viewsets.ModelViewSet):
    """Exibindo todos os usuarios"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class CondicaoPagamentoViewSet(viewsets.ModelViewSet):
    """Exibindo todas as condicoes"""
    #permission_classes = (permissions.AllowAny, )
    queryset = CondicaoPagamento.objects.all()
    serializer_class = CondicaoPagamentoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class CondicaoPagamentoView(generics.ListAPIView):
    """Exibindo todas as condicoes"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = CondicaoPagamento.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
    serializer_class = CondicaoPagamentoSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class NotificarViewSet(viewsets.ModelViewSet):
    """Exibindo todas as notificacoes"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Notificar.objects.all()
    serializer_class = NotificarSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class NotificarView(generics.ListAPIView):
    """Exibindo todas as notificacoes"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Notificar.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
    serializer_class = NotificarSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class TransportadoraViewSet(viewsets.ModelViewSet):
    """Exibindo todas as tranportadoras"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Transportadora.objects.all()
    serializer_class = TransportadoraSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PedidoCompraViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos de compras"""
    #permission_classes = (permissions.AllowAny, )
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializer

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PedidoCompraOrcamentoViewSet(generics.ListAPIView):
    """Exibindo todos os pedidos de compras"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = PedidoCompra.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        queryset = queryset.filter(fornecedor = self.kwargs['pkFornecedor'])
        return queryset
    serializer_class = PedidoCompra2Serializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PedidoCompraAllViewSet(generics.ListAPIView):
    """Exibindo todos pedidos de um orcamento de um fornecedor"""
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Cotacao.objects.filter(pedido__orcamento = self.kwargs['pkOrcamento'])
        queryset = queryset.filter(pecafornecedor__fornecedor = self.kwargs['pkFornecedor'])
        return queryset
    serializer_class = PedidoCompraAllSerializer
        
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class EstoqueViewSet(viewsets.ModelViewSet):
    """Exibindo todos os pedidos de compras"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
 
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
class EstoqueView(generics.ListAPIView):
    """Exibindo todos os pedidos de compras"""
    #permission_classes = (permissions.AllowAny, )
    queryset = Estoque.objects.all()
    serializer_class = EstoquePecaSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PackViewSet(viewsets.ModelViewSet):
    #permission_classes = (permissions.AllowAny, )
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class PackView(generics.ListAPIView):
    #permission_classes = (permissions.AllowAny, )
    def get_queryset(self):
        queryset = Pack.objects.filter(orcamento = self.kwargs['pkOrcamento'])
        return queryset
    serializer_class = PackSerializer

def addPecas(arquivo):
    tabela = pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

    l = len(tabela)
    for i in range(l):
        p = Peca(codigo = tabela['codigo'][i], descricao = tabela['descricao'][i], preco_venda = tabela['precoVenda'][i],
                preco_exportacao = tabela['precoExportacao'][i], preco_nacional = tabela['precoNacional'][i], ret = tabela['ret'][i],
                cc = tabela['cc'][i], peso  = tabela['peso'][i], comprimento = tabela['comprimento'][i],
                largura = tabela['largura'][i], altura = tabela['altura'][i], ncm = tabela['ncm'][i], gde  = tabela['gde'][i])
    p.save()
    return "peças adicionadas"

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class AddPecasView(APIView):
    #permission_classes = (permissions.AllowAny, )
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

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class AddPecasFornecedorView(APIView):
    #permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        arquivo = 'arquivosCsv/' + self.kwargs['arquivo']
        result = addPrecosFornecedor(arquivo, self.kwargs['fornecedorId'])
        return Response(data={result})
    
def addPedidosOrcamento(arquivo, clienteId, orcamentoId):
    tabela = pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

    l = len(tabela)
    pedido = Pedido.objects.last()
    codigoP = pedido.codigo_pedido + 1
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
                            codigo_pedido = codigoP,
                            peca = peca,
                            orcamento = orcamento,
                            cliente = cliente,
                            data_entrega = '2024-05-10',
                            quantidade =  tabela['qtd'][i],
                            peso_bruto = 10,
                            volume = 0,
                            volume_bruto = 10
                            )
                    p.save()

    return ("Peças adicionadas : " + str(pecasEncontradas) + "Peças não encontradas : "  + str(pecasNaoEncontradas))

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class addPedidosOrcamentoView(APIView):
    #permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        arquivo = 'arquivosCsv/' + self.kwargs['arquivo']
        result = addPedidosOrcamento(arquivo, self.kwargs['clienteId'], self.kwargs['orcamentoId'])
        return Response(data={result})
    
def gerarCotacao(orcamentoId):
    pedidos = Pedido.objects.all().filter(orcamento = orcamentoId)
    pecasAdicionadas = []
    pecasNaoAdicionadas = []
    for pedido in pedidos:
            pecas = pedido.peca
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
                pecasAdicionadas.append(pecas.codigo + ' - Fonecedor: ' + pecaFornecedor.fornecedor.nome_fornecedor)
    return 'peças adicionadas: ' + str(pecasAdicionadas) + ' pecas não encontradas: ' + str(pecasNaoAdicionadas)
                
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class gerarCotacaoView(APIView):
    #permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = gerarCotacao(self.kwargs['orcamentoId'])
        return Response(data={result})
    
def negativarEstoque(orcamentoId):
    pedidos = Pedido.objects.all().filter(orcamento = orcamentoId)
    pecasAdicionadas = []
    for pedido in pedidos:
        print(pedido)
        peca = Estoque.objects.filter(pedido = pedido).first()
        if peca is None:
            estoque = Estoque(
                    dataEntrada = '2024-01-01',
                    dataSaida = '2024-01-01',
                    estado = '1',
                    pedido = pedido
            )
            estoque.save()
            pecasAdicionadas.append(pedido.peca)
    return 'peças adicionadas: ' + str(pecasAdicionadas)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class addEstoqueView(APIView):
    #permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = negativarEstoque(self.kwargs['orcamentoId'])
        return Response(data={result})
    
def positivarEstoque(pedidoCompraId):
    pedidoCompra = PedidoCompra.objects.filter(id = pedidoCompraId).first()
    
    cotacoes = Cotacao.objects.filter(pedido__orcamento = pedidoCompra.orcamento)
    cotacoes = cotacoes.filter(pecafornecedor__fornecedor = pedidoCompra.fornecedor)

    pedidos = []
    
    for cotacao in cotacoes:
        pedido = Pedido.objects.all().filter(id = cotacao.pedido.id).first()
        pedidos.append(pedido)
        
    pecasAdicionadas = []
    for pedido in pedidos:
        print(pedido)
        peca = Estoque.objects.filter(pedido = pedido).first()
        if peca is not None:
            estoque = Estoque(
                    data_entrada = '2024-01-01',
                    data_saida = '2024-01-01',
                    estado = '2',
                    pedido = pedido
            )
            estoque.save()
            pecasAdicionadas.append(pedido.peca)
    return 'peças adicionadas: ' + str(pecasAdicionadas)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
class AdicionarEstoqueView(APIView):
    #permission_classes = (permissions.AllowAny, )
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = positivarEstoque(self.kwargs['pedidoCompraId'])
        return Response(data={result})
 
 
def AddPedidoOrcamento(arquivo, clienteId, orcamentoId):
    qtdv = arquivo.count(";")
    partes = arquivo.split(";")
    codigos = []
    quantidades = []
    descricao = []
    for parte in partes:
        pecas =  parte.split(",")
        codigos.append(pecas[0])
        quantidades.append(pecas[1])
        descricao.append(pecas[2])
    
    #tabela = json.loads(arquivo)

    l = len(codigos)
    pedido = Pedido.objects.last()
    codigoP = pedido.codigo_pedido + 1
    cliente = Cliente.objects.filter(id = clienteId).first()
    orcamento = Orcamento.objects.filter(id = orcamentoId).first()
    pecasEncontradas = []
    pecasNaoEncontradas = []
    pecasJaAdicionadas = []
    for i in range(l):
        peca = Peca.objects.filter(codigo =  codigos[i]).first()
        pedido = Pedido.objects.filter(orcamento__id = orcamentoId)
        pedido = pedido.filter(peca__codigo = codigos[i]).first()
        print(peca)
        if pedido is None:
            
            if (peca is None):
                pecasNaoEncontradas.append(codigos[i])
            else:
                pecasEncontradas.append(codigos[i])
                p = Pedido(           
                    codigo_pedido = codigoP,
                    peca = peca,
                    orcamento = orcamento,
                    cliente = cliente,
                    data_entrega = '2024-05-10',
                    quantidade =  quantidades[i],
                    peso_bruto = 10,
                    volume = 0,
                    volume_bruto = 10,
                    descricao = descricao[i]
                    )
                p.save()
        else:
            pedido.quantidade = quantidades[i]
            pedido.descricao = descricao[i]
            pedido.save()
            pecasJaAdicionadas.append(codigos[i])

    return ("Peças adicionadas : " + str(pecasEncontradas) +
            "Peças não encontradas : "  + str(pecasNaoEncontradas) +
            "Pecas que ja tinham sido adicionadas : " + str(pecasJaAdicionadas))
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddPedidoOrcamentoView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = AddPedidoOrcamento(self.kwargs['arquivo'], self.kwargs['clienteId'], self.kwargs['orcamentoId'])
        return Response(data={result})

def AddPeca(arquivo):
    partes = arquivo.split(";")
    codigos = []
    descricaos = []
    precoVendas = []
    precoExportacaos = []
    precoNacionals = []
    rets = []
    ccs = []
    pesos = []
    comprimentos = []
    larguras = []
    alturas = []
    ncms = []
    gdes = []
    partes.pop(0)
    for parte in partes:
        pecas =  parte.split(",")
        codigos.append(pecas[0])
        descricaos.append(pecas[1])
        precoV = re.findall(r'-?\d+\.?\d*', pecas[2])
        precoVendas.append(precoV[0])
        precoE = re.findall(r'-?\d+\.?\d*',pecas[3])
        precoExportacaos.append(precoE[0])
        precoN = re.findall(r'-?\d+\.?\d*',pecas[4])
        precoNacionals.append(precoN[0])
        rets.append(pecas[5])
        ccs.append(pecas[6])
        pesos.append(pecas[7])
        comprimentos.append(pecas[8])
        larguras.append(pecas[9])
        alturas.append(pecas[10])
        ncms.append(pecas[11])
        gdes.append(pecas[12])
    
    pecasAdicionadas = []
    pecasAtualizadas = []

    l = len(codigos)
    for i in range(l-1):
        pecas = Peca.objects.filter(codigo = codigos[i+1]).first()
        if pecas is None:
            peca = Peca(
                codigo = codigos[i+1],
                descricao = descricaos[i+1],
                marca = "john deere",
                preco_venda = precoVendas[i+1],
                preco_exportacao = precoExportacaos[i+1],
                preco_nacional = precoNacionals[i+1],
                ret = rets[i+1],
                cc = ccs[i+1],
                peso = pesos[i+1],
                comprimento = comprimentos[i+1],
                largura = larguras[i+1],
                altura = alturas[i+1],
                ncm = ncms[i+1],
                gde = gdes[i+1]
            )
            peca.save()
            pecasAdicionadas.append(peca.codigo)
        else:
            pecas.preco_exportacao = precoExportacaos[i+1]
            pecas.preco_venda = precoVendas[i+1]
            pecas.preco_nacional = precoNacionals[i+1]
            pecas.save()
            pecasAtualizadas.append(pecas)
        

    return ("Peças adicionadas : " + str(pecasAdicionadas) + " - Pecas atualizadas : " + str(pecasAtualizadas))
    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddPecaView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = AddPeca(self.kwargs['arquivo'])
        return Response(data={result})
    
def AddPecaFornecedor(arquivo, fornecedorId):
    partes = arquivo.split(";")
    codigos = []
    pecas = []
    precos = []
    fornecedorObj = Fornecedor.objects.filter(id = fornecedorId).first()
    partes.pop(0)
    for parte in partes:
        linha =  parte.split(",")
        codigos.append(linha[0])
        peca = Peca.objects.filter(codigo = linha[1]).first()
        pecas.append(peca)
        precos.append(linha[2])
    
    pecasAdicionadas = []
    pecasAtualizadas = []

    l = len(codigos)
    for i in range(l-1):
        pecasFornecedor = PecaFornecedor.objects.filter(peca = pecas[i+1]).first()
        if pecasFornecedor is None:
            pecaFornecedor = PecaFornecedor(
                codigo = codigos[i+1],
                peca = pecas[i+1],
                preco = precos[i+1],
                fornecedor = fornecedorObj
            )
            pecaFornecedor.save()
            pecasAdicionadas.append(pecas[i+1])
        else:
            pecasFornecedor.preco = precos[i+1]
            pecasFornecedor.save()
            pecasAtualizadas.append(pecas[i+1])
        

    return ("Peças adicionadas : " + str(pecasAdicionadas) + "Peças atualizadas: " + str(pecasAtualizadas) )

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddPecaFornecedorView(APIView):
    http_method_names = ['get', 'head']
    def get(self, request, *args, **kwargs):
        result = AddPecaFornecedor(self.kwargs['arquivo'], self.kwargs['fornecedor'])
        return Response(data={result})