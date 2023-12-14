from django.contrib import admin
from loja.models import Peca

class Pecas(admin.ModelAdmin):
    list_display = ('id','descricao', 'codigo', 'precoVenda')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20
    
admin.site.register(Peca, Pecas)
