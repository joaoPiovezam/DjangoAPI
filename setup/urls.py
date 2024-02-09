from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from diagnostico.views import Questionario

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('questionario/', include('diagnostico.urls', namespace='diagnostico'))
]
