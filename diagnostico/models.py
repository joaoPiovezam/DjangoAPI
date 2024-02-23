from django.db import models
from django.utils.translation import gettext_lazy as _

class Categoria(models.Model):
    nome = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.nome

class Questionario(models.Model):
    class Meta:
        verbose_name = _("Questionário")
        verbose_name_plural = _("Questionários")
        ordering = ['id']
        
    titulo = models.CharField(max_length = 255, default = _(
        "Novo Questionário"), verbose_name = _("Título do Questionário"
    ))
    categoria = models.ForeignKey(
        Categoria, default = 1, on_delete = models.DO_NOTHING
    )
    data_criacao = models.DateTimeField(auto_now_add = True, verbose_name = _("Data de Criação"))
    
    def __str__(self):
        return self.titulo

class Atualizada(models.Model):
    data_atualizada = models.DateTimeField(
        verbose_name = _("Última Atualização"), auto_now = True
    )
    
    class Meta:
        abstract = True

class Node(models.Model):
    RESULTADO = (
        (0, _('Não')),
        (1, _('Sim')),
    )
    RESULTADO_PAI = (
        (0, _('Não')),
        (1, _('Sim')),
        (2, _('Nulo'))
    )
    questionario = models.ForeignKey(
        Questionario, related_name = 'node', on_delete = models.DO_NOTHING
    )
    resultado = models.IntegerField(choices = RESULTADO, default = 0, verbose_name = _("Resultado"))
    resultadoPai = models.IntegerField(choices = RESULTADO_PAI, default = 2, null = False, verbose_name = _("Resultado do nó Pai"))
    codigoNode = models.IntegerField(unique = True, null = False)
    noPai = models.IntegerField(null = True)
    questao = models.CharField(null = False, max_length = 255)
    
    
    
class Pergunta(Atualizada):
    
    class Meta:
        verbose_name = _("Pergunta")
        verbose_name_plural = _("Perguntas")
        ordering = ['id']
        
    Escala = (
        (0, _('Nulo')),
        (1, _('Muito Pouco')),
        (2, _('Pouco')),
        (3, _('Razoavel')),
        (4, _('Ok')),
        (5, _('Muito')),
    )
    
    Opcao = (
        (0, _('Nulo')),
        (1, _('Sim')),
        (2, _('Não')),
    )
    
    TIPO = (
        (0, _('Multipla Escolha')),
        (1, _('Dicotômica')),
    )
    
    questionario = models.ForeignKey(
        Questionario, related_name = 'pergunta', on_delete = models.DO_NOTHING
    )
    node = models.ForeignKey(
        Node, on_delete = models.DO_NOTHING
    )
    tecnica = models.IntegerField(choices = TIPO, default = 0, verbose_name = _("Tipo de Pergunta"))
    titulo = models.CharField(verbose_name = _("Titulo"), max_length=255)
    escala = models.IntegerField(choices = Escala, default = 0, verbose_name = _("Escala"))
    opcao = models.IntegerField(choices = Opcao, default = 0, verbose_name = _("Opção"))
    data_criacao = models.DateTimeField(auto_now_add = True, verbose_name = _("Data de Criação"))
    esta_ativo = models.BooleanField(default = True, verbose_name = _("Status de Ativação"))
    
    def __str__(self):
        return self.titulo

class Resposta(Atualizada):
    
    class Meta:
        verbose_name = _("Resposta")
        verbose_name_plural = _("Respostas")
        ordering = ['id']
    
    pergunta = models.ForeignKey(
        Pergunta, related_name = 'resposta', on_delete = models.DO_NOTHING
    )
    resposta_texto = models.CharField(max_length = 255, verbose_name = _("Resposta Texto"))