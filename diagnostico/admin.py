from django.contrib import admin
from . import models

@admin.register(models.Categoria)

class CatAdmin(admin.ModelAdmin):
	list_display = [
        'nome',
        ]

@admin.register(models.Questionario)

class QuizAdmin(admin.ModelAdmin):
	list_display = [
        'id', 
        'titulo',
        ]

class RespostaInlineModel(admin.TabularInline):
    model = models.Resposta
    fields = [
        'resposta_texto', 
        ]

@admin.register(models.Pergunta)

class PerguntaAdmin(admin.ModelAdmin):
    fields = [
        'titulo',
        'questionario',
        ]
    list_display = [
        'titulo', 
        'questionario',
        'data_atualizada'
        ]
    inlines = [
        RespostaInlineModel, 
        ] 

@admin.register(models.Resposta)

class RespostaAdmin(admin.ModelAdmin):
    list_display = [
        'resposta_texto', 
        'pergunta'
        ]
