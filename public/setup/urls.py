from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,  re_path
from rest_framework import routers
from loja.views import (PecasViewSet, PecaList, ClientesViewSet, TransportadoraViewSet, OrcamentoViewSet, PedidoViewSet,
 PedidoOrcamentoViewSet, FornecedorList, FornecedoresViewSet, PecasFornecedoresViewSet, PecaFornecedorView,
 PecaFornecedorList,PecasFornecedoresView, CotacaoViewSet, CondicaoPagamentoView, CotacaoOrcamentoViewSet,
 Cotacao2ViewSet, UsuarioViewSet, NotificarViewSet, NotificarView, CondicaoPagamentoViewSet, PedidoCompraViewSet,PedidoCompraOrcamentoViewSet,
 PedidoCompraAllViewSet, EstoqueViewSet, EstoqueView, PedidoView, PackViewSet, PackView, AddPecasView, AddPecasFornecedorView,
 addPedidosOrcamentoView, gerarCotacaoView, OrcamentoListView, OrcamentoClienteViewSet, addEstoqueView, AdicionarEstoqueView, AddPedidoOrcamentoView,
 AddPecaView, AddPecaFornecedorView, OrcamentoNaoFaturadoViewSet, OrcamentoFaturadoViewSet)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from loja import views

router = routers.DefaultRouter()
router.register('pecas', PecasViewSet, basename = 'Pecas')
router.register('clientes', ClientesViewSet, basename = 'Clientes')
router.register('transportadora', TransportadoraViewSet, basename = 'Transportadora')
router.register('orcamentos', OrcamentoViewSet, basename = 'Orcamentos')
router.register('pedidos', PedidoViewSet, basename = 'Pedidos')
router.register('fornecedores', FornecedoresViewSet, basename = 'Fornecedores')
router.register('pecasFornecedores', PecasFornecedoresViewSet, basename = 'PecasFornecedores')
router.register('pecasFornecedor', PecaFornecedorView, basename = 'PecasFornecedores')
#router.register('cotacoes', CotacaoViewSet, basename = 'Cotacoes')
router.register('cotacao', CotacaoViewSet, basename = 'Cotacoes')
router.register('usuarios', UsuarioViewSet, basename = 'Usuarios')
router.register('notificar', NotificarViewSet, basename = 'Notificar')
router.register('condicoes', CondicaoPagamentoViewSet, basename = 'Condicoes')
router.register('pedidosCompra', PedidoCompraViewSet, basename = 'PedidoCompra')
router.register('estoque', EstoqueViewSet, basename = 'Estoque')
router.register('pack', PackViewSet, basename = 'Pack')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    path("orcamento/", OrcamentoListView.as_view()),
    path("orcamento/<str:email>/", OrcamentoClienteViewSet.as_view()),
    path("orc/", views.OrcamentoView),
    path('orcamento/<int:pk>/pedidos/<int:volume>/<int:peca>/',PedidoOrcamentoViewSet.as_view()),
    path('orcamentosNaoFaturados/',OrcamentoNaoFaturadoViewSet.as_view()),
    path('orcamentosFaturados/',OrcamentoFaturadoViewSet.as_view()),
    path('peca/', PecaList.as_view()),
    path('peca/<int:codigo>/', PecaList.as_view()),
    path('fornecedor/', FornecedorList.as_view()),
    path('pecaFornecedor/<int:peca>/<int:fornecedor>/', PecaFornecedorList.as_view()),
    path('cotacoes/', Cotacao2ViewSet.as_view()),
    path('cotacaoOrcamento/<int:pk>/',CotacaoOrcamentoViewSet.as_view()),
    path('condicao/<int:pkOrcamento>/', CondicaoPagamentoView.as_view()),
    path('notificacao/<int:pkOrcamento>/', NotificarView.as_view()),
    path('pedidoCompra/<int:pkOrcamento>/<int:pkFornecedor>', PedidoCompraAllViewSet.as_view()),
    path('pedidoCompraOrcamento/<int:pkOrcamento>/<int:pkFornecedor>', PedidoCompraOrcamentoViewSet.as_view()),
    path('peca/<int:pecaId>/fornecedor/<int:fornecedorId>', PecasFornecedoresView.as_view()),
    path('estoquePecas/', EstoqueView.as_view()),
    path('pedidoPeca/', PedidoView.as_view()),
    path('packOrcamento/<int:pkOrcamento>', PackView.as_view()),
    path('addPecas/<str:arquivo>', AddPecasView.as_view()),
    path('addPecasFornecedor/<str:arquivo>/<int:fornecedorId>', AddPecasFornecedorView.as_view()),
    path('addPedidosOrcamento/<str:arquivo>/<int:clienteId>/<int:orcamentoId>', addPedidosOrcamentoView.as_view()),
    path('gerarCotacao/<int:orcamentoId>', gerarCotacaoView.as_view()),
    path('addEstoque/<int:orcamentoId>',addEstoqueView().as_view()),
    path('adicionarEstoqueView/<int:pedidoCompraId>',AdicionarEstoqueView.as_view()),    
    path('AddPedidoOrcamentoView/<str:arquivo>/<int:clienteId>/<int:orcamentoId>/',AddPedidoOrcamentoView.as_view()),   
    path('AddPeca/<str:arquivo>/',AddPecaView.as_view()),
    path('addPecaFornecedor/<str:arquivo>/<int:fornecedor>/',AddPecaFornecedorView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )