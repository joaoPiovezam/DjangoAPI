from django.contrib import admin

from loja.models import Peca, Cliente, Orcamento, Pedido

class Pecas(admin.ModelAdmin):
    list_display = ('id','descricao', 'codigo', 'precoVenda')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20
    
admin.site.register(Peca, Pecas)

class Clientes(admin.ModelAdmin):
    list_display = ('id','nomeCliente', 'cpfCnpj')
    list_display_links = ('id','nomeCliente')
    search_fields = ('nomeCliete', 'cpfCnpj',)
    list_per_page = 20
    
admin.site.register(Cliente, Clientes)

class Orcamentos(admin.ModelAdmin):
    list_display = ('id','codigo', 'cliente', 'tipoEntrega')
    list_display_links = ('id','codigo', 'cliente', 'tipoEntrega')
    search_fields = ('id','codigo', 'cliente', 'tipoEntrega',)
    list_per_page = 20
    
admin.site.register(Orcamento, Orcamentos)

class Pedidos(admin.ModelAdmin):
    list_display = ('codigoPedido', 'codigoPeca', 'codigoOrcamento')
    list_display_links = ('codigoPedido', 'codigoPeca', 'codigoOrcamento')
    search_fields = ('codigoPedido', 'codigoPeca', 'codigoOrcamento',)
    list_per_page = 20
    
admin.site.register(Pedido, Pedidos)