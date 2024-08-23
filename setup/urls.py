from django.contrib import admin
from django.urls import path, include,  re_path
from rest_framework import routers
from loja.views import (PecasViewSet, PecaList, ClientesViewSet, TransportadoraViewSet, OrcamentoViewSet, PedidoViewSet,
 PedidoOrcamentoViewSet, FornecedorList, FornecedoresViewSet, PecasFornecedoresViewSet, PecaFornecedorView,
 PecaFornecedorList,PecasFornecedoresView, CotacaoViewSet, CondicaoPagamentoView, CotacaoOrcamentoViewSet,
 Cotacao2ViewSet, UsuarioViewSet, NotificarViewSet, NotificarView, CondicaoPagamentoViewSet, PedidoCompraViewSet,
 PedidoCompraAllViewSet, EstoqueViewSet, EstoqueView, PedidoView, PackViewSet, PackView, AddPecasView, AddPecasFornecedorView,
 addPedidosOrcamentoView, gerarCotacaoView, OrcamentoListView, OrcamentoClienteViewSet)
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
router.register('cotacoes', CotacaoViewSet, basename = 'Cotacoes')
router.register('cotacao', Cotacao2ViewSet, basename = 'Cotacoes')
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
    path('orcamento/<int:pk>/pedidos/',PedidoOrcamentoViewSet.as_view()),
    path('peca/', PecaList.as_view()),
    path('fornecedor/', FornecedorList.as_view()),
    path('pecaFornecedor/<int:peca>/<int:fornecedor>/', PecaFornecedorList.as_view()),
    path('cotacaoOrcamento/<int:pk>/',CotacaoOrcamentoViewSet.as_view()),
    path('condicao/<int:pkOrcamento>/', CondicaoPagamentoView.as_view()),
    path('notificacao/<int:pkOrcamento>/', NotificarView.as_view()),
    path('pedidoCompra/<int:pkOrcamento>/<int:pkFornecedor>', PedidoCompraAllViewSet.as_view()),
    path('peca/<int:pecaId>/fornecedor/<int:fornecedorId>', PecasFornecedoresView.as_view()),
    path('estoquePecas/', EstoqueView.as_view()),
    path('pedidoPeca/', PedidoView.as_view()),
    path('packOrcamento/<int:pkOrcamento>', PackView.as_view()),
    path('addPecas/<str:arquivo>', AddPecasView.as_view()),
    path('addPecasFornecedor/<str:arquivo>/<int:fornecedorId>', AddPecasFornecedorView.as_view()),
    path('addPedidosOrcamento/<str:arquivo>/<int:clienteId>/<int:orcamentoId>', addPedidosOrcamentoView.as_view()),
    path('gerarCotacao/<int:orcamentoId>', gerarCotacaoView.as_view())
]
