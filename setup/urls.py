from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from loja.views import PecasViewSet, ClientesViewSet, OrcamentoViewSet, PedidoViewSet, PedidoOrcamentoViewSet

router = routers.DefaultRouter()
router.register('pecas', PecasViewSet, basename='Pecas')
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('orcamentos', OrcamentoViewSet, basename='Orcamentos')
router.register('pedidos', PedidoViewSet, basename='Pedidos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('orcamento/<int:pk>/pedidos/',PedidoOrcamentoViewSet.as_view()),
]
