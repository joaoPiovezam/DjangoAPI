from rest_framework import serializers
from .models import Questionario, Resposta, Pergunta

class QuestionarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Questionario
        fields = [
            'titulo',
            'categoria',
        ]
        
class RespostaSerializer(serializers.ModelSerializer):

    class Meta:       
        model = Resposta
        fields = [
            'id',
            'resposta_texto',
        ]

class RandomPerguntaSerializer(serializers.ModelSerializer):

    resposta = RespostaSerializer(many=True, read_only=True)

    class Meta: 
        model = Pergunta
        fields = [
            'titulo','resposta',
        ]


class PerguntaSerializer(serializers.ModelSerializer):

    resposta = RespostaSerializer(many=True, read_only=True)
    questionario = QuestionarioSerializer(read_only=True)

    class Meta:
    
        model = Pergunta
        fields = [
            'questionario','titulo','resposta',
        ]