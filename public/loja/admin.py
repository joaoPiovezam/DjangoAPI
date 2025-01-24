from django.contrib import admin

from loja.models import Peca, Cliente, Orcamento, Pedido

class Pecas(admin.ModelAdmin):
    list_display = ('id','descricao', 'codigo', 'preco_venda')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20
    
admin.site.register(Peca, Pecas)

class Clientes(admin.ModelAdmin):
    list_display = ('id','nome_cliente', 'cpfcnpj')
    list_display_links = ('id','nome_cliente')
    search_fields = ('nome_cliete', 'cpfcnpj',)
    list_per_page = 20
    
admin.site.register(Cliente, Clientes)

class Orcamentos(admin.ModelAdmin):
    list_display = ('id','codigo', 'cliente', 'tipo_entrega')
    list_display_links = ('id','codigo', 'cliente', 'tipo_entrega')
    search_fields = ('id','codigo', 'cliente', 'tipo_entrega',)
    list_per_page = 20
    
admin.site.register(Orcamento, Orcamentos)

class Pedidos(admin.ModelAdmin):
    list_display = ('codigo_pedido', 'peca', 'orcamento')
    list_display_links = ('codigo_pedido', 'peca', 'orcamento')
    search_fields = ('codigo_pedido', 'peca', 'orcamento',)
    list_per_page = 20
    
admin.site.register(Pedido, Pedidos)