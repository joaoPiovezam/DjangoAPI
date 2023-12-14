from django.db import models

class Peca(models.Model):
    RET = (
        ('R', 'R'),
        ('N', 'N'),
        ('D', 'D')
    )
    codigo = models.CharField(max_length=30)
    decricao = models.CharField(max_length=30)
    precoVenda = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    precoExpotacao = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    precoNacional = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    ret = models.CharField(max_length=1, choices = RET, blank=False, null=False,default='R')
    cc = models.IntegerField(_(""))
    peso = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    comprimento = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    largura = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    altura = models.DecimalField(_(""), max_digits=15, decimal_places=3)
    ncm = models.IntegerField(_(""))
    gde = models.IntegerField(_(""))

    def __str__(self):
        return self.nome
