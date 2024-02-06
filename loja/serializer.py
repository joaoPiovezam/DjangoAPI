from rest_framework import serializers
from loja.models import Peca, Cliente, Orcamento, Pedido

class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = '__all__'
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'
        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        
'''class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    orcamento_entrega      = serializers.ReadOnlyField(source = 'orcamento.tipoEntrega')
    orcamento_codigo       = serializers.ReadOnlyField(source = 'orcamento.codigo')
    orcamento_dataEmicao   = serializers.ReadOnlyField(source = 'orcamento.dataEmissao')
    orcamento_dataValidade = serializers.ReadOnlyField(source = 'orcamento.dataValidade')
    orcamento_responsavel  = serializers.ReadOnlyField(source = 'orcamento.responsavel')
    orcamento_frete        = serializers.ReadOnlyField(source = 'orcamento.frete')
    
    cliente_nome           = serializers.ReadOnlyField(source = 'cliente.nomeCliente')
    cliente_cnpj           = serializers.ReadOnlyField(source = 'cliente.cpfCnpj')
    cliente_rg             = serializers.ReadOnlyField(source = 'cliente.rgIE')
    cliente_endereco       = serializers.ReadOnlyField(source = 'cliente.endereco')
    cliente_bairro         = serializers.ReadOnlyField(source = 'cliente.bairro')
    cliente_cep            = serializers.ReadOnlyField(source = 'cliente.cep')
    cliente_cidade         = serializers.ReadOnlyField(source = 'cliente.cidade')
    cliente_estado         = serializers.ReadOnlyField(source = 'cliente.estado')
    cliente_telefone       = serializers.ReadOnlyField(source = 'cliente.telefone')
    cliente_contato        = serializers.ReadOnlyField(source = 'cliente.contato')
    cliente_email          = serializers.ReadOnlyField(source = 'cliente.email')
    
    peca_codigo            = serializers.ReadOnlyField(source = 'peca.codigo')
    peca_descricao         = serializers.ReadOnlyField(source = 'peca.descricao')
    peca_precoVenda        = serializers.ReadOnlyField(source = 'peca.precoVenda')
    peca_precoExportacao   = serializers.ReadOnlyField(source = 'peca.precoExportacao')
    peca_precoNacional     = serializers.ReadOnlyField(source = 'peca.precoNacional')
    peca_ret               = serializers.ReadOnlyField(source = 'peca.ret')
    peca_cc                = serializers.ReadOnlyField(source = 'peca.cc')
    peca_peso              = serializers.ReadOnlyField(source = 'peca.peso')
    peca_comprimento       = serializers.ReadOnlyField(source = 'peca.comprimento')
    peca_largura           = serializers.ReadOnlyField(source = 'peca.largura')
    peca_altura            = serializers.ReadOnlyField(source = 'peca.altura')
    peca_ncm               = serializers.ReadOnlyField(source = 'peca.ncm')
    peca_gde               = serializers.ReadOnlyField(source = 'peca.gde')
    
    class Meta:
        model = Pedido
        fields = ['orcamento_entrega'
                    ,'orcamento_codigo'
                    ,'orcamento_dataEmicao'
                    ,'orcamento_dataValidade'
                    ,'orcamento_responsavel'
                    ,'orcamento_frete'
                    
                    ,'cliente_nome'
                    ,'cliente_cnpj'
                    ,'cliente_rg'
                    ,'cliente_endereco'
                    ,'cliente_bairro'
                    ,'cliente_cep'
                    ,'cliente_cidade'
                    ,'cliente_estado'
                    ,'cliente_telefone'
                    ,'cliente_contato'
                    ,'cliente_email'
                    
                    ,'peca_codigo'
                    ,'peca_descricao'
                    ,'peca_precoVenda'
                    ,'peca_precoExportacao'
                    ,'peca_precoNacional'
                    ,'peca_ret'
                    ,'peca_cc'
                    ,'peca_peso'
                    ,'peca_comprimento'
                    ,'peca_largura'
                    ,'peca_altura'
                    ,'peca_ncm'
                    ,'peca_gde']'''
                    
class ListaPedidoOrcamentoSerializer(serializers.ModelSerializer):
    pedido     = serializers.SerializerMethodField()
    class Meta:
        model = Orcamento
        fields = '__all__' #['orcamento']
    def get_pedido(self, obj):
        return obj.__str__()