from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics
from .models import Questionario as QuestionarioModel, Node, Pergunta, Categoria
from .serializers import NodeSerializer, QuestionarioSerializer, RandomPerguntaSerializer, PerguntaSerializer
from rest_framework.views import APIView

class StartQuestionario(APIView):

    def get(self, request, **kwargs):
        questionario = QuestionarioModel.objects.filter(categoria__nome=kwargs['titulo'])
        serializer = QuestionarioSerializer(questionario, many=True)
        return Response(serializer.data)

class Questionario(generics.ListAPIView):
    
    serializer_class = QuestionarioSerializer
    queryset = QuestionarioModel.objects.all()
    
class RandomPergunta(APIView):

    def get(self, request, format=None, **kwargs):
        pergunta = Pergunta.objects.filter(questionario__titulo=kwargs['topico']).order_by('?')[:1]
        serializer = RandomPerguntaSerializer(pergunta, many=True)
        return Response(serializer.data)

class QuestionarioPergunta(APIView):

    def get(self, request, format=None, **kwargs):
        questionario = Pergunta.objects.filter(questionario__titulo=kwargs['topico'])
        serializer = PerguntaSerializer(questionario, many=True)
        return Response(serializer.data)
    
class NodeViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        queryset = Node.objects.all()#filter(noPai = self.kwargs['noPai'])
        return queryset
    serializer_class = NodeSerializer