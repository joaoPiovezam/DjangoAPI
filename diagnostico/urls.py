from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Questionario, RandomPergunta, QuestionarioPergunta, StartQuestionario

app_name='diagnostico'

urlpatterns = [
    path('', Questionario.as_view(), name='questionario'),
    path('r/<str:topico>/', RandomPergunta.as_view(), name='random' ),
    path('q/<str:topico>/', QuestionarioPergunta.as_view(), name='perguntas' ),
    path('single/<str:titulo>/', StartQuestionario.as_view(), name='questionario'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)