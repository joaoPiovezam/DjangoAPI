from django.contrib import admin
from django.urls import path, include,  re_path
from rest_framework import routers
from loja.views import PecasViewSet, PecaList, ClientesViewSet, TransportadoraViewSet, OrcamentoViewSet, PedidoViewSet
from loja.views import PedidoOrcamentoViewSet, FornecedorList, FornecedoresViewSet, PecasFornecedoresViewSet, PecaFornecedorView
from loja.views import PecaFornecedorList,PecasFornecedoresView, CotacaoViewSet, CondicaoPagamentoView, CotacaoOrcamentoViewSet
from loja.views import Cotacao2ViewSet, UsuarioViewSet, NotificarViewSet, NotificarView, CondicaoPagamentoViewSet, PedidoCompraViewSet
from loja.views import PedidoCompraAllViewSet, EstoqueViewSet, EstoqueView, PedidoView

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
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
    path('pedidoPeca/', PedidoView.as_view())
]
