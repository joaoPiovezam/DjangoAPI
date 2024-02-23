from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from diagnostico.views import NodeViewSet

router = routers.DefaultRouter()
router.register('nodes', NodeViewSet, basename='Nodes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('questionario/', include('diagnostico.urls', namespace='diagnostico')),
    #path('node/<str:noPai>/', NodeViewSet.as_view(), name='node'),
]
