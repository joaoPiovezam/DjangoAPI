from django.contrib import admin
from django.urls import path, include,  re_path
from rest_framework import routers
from loja.views import PecasViewSet, PecaList, ClientesViewSet, OrcamentoViewSet, PedidoViewSet, PedidoOrcamentoViewSet, FornecedorList, FornecedoresViewSet, PecasFornecedoresViewSet, PecaFornecedorList, CotacaoViewSet

router = routers.DefaultRouter()
router.register('pecas', PecasViewSet, basename='Pecas')
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('orcamentos', OrcamentoViewSet, basename='Orcamentos')
router.register('pedidos', PedidoViewSet, basename='Pedidos')
router.register('fornecedores', FornecedoresViewSet, basename='Fornecedores')
router.register('pecasFornecedores', PecasFornecedoresViewSet, basename='PecasFornecedores')
router.register('cotacoes', CotacaoViewSet, basename='Cotacoes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('orcamento/<int:pk>/pedidos/',PedidoOrcamentoViewSet.as_view()),
    path('peca/', PecaList.as_view()),
    path('fornecedor/', FornecedorList.as_view()),
    path('pecaFornecedor/', PecaFornecedorList.as_view())
]
