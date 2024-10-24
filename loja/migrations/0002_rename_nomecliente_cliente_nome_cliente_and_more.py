# Generated by Django 4.1 on 2024-10-21 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='nomecliente',
            new_name='nome_cliente',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='tipopessoa',
            new_name='tipo_pessoa',
        ),
        migrations.RenameField(
            model_name='cotacao',
            old_name='codigo_peca_fornecedor',
            new_name='pecafornecedor',
        ),
        migrations.RenameField(
            model_name='cotacao',
            old_name='codigo_pedido',
            new_name='pedido',
        ),
        migrations.RenameField(
            model_name='estoque',
            old_name='dataentrada',
            new_name='data_entrada',
        ),
        migrations.RenameField(
            model_name='estoque',
            old_name='datasaida',
            new_name='data_saida',
        ),
        migrations.RenameField(
            model_name='estoque',
            old_name='codigopedido',
            new_name='pedido',
        ),
        migrations.RenameField(
            model_name='fornecedor',
            old_name='nomefornecedor',
            new_name='nome_fornecedor',
        ),
        migrations.RenameField(
            model_name='fornecedor',
            old_name='tipopessoa',
            new_name='tipo_pessoa',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='cidadeentrega',
            new_name='cidade_entrega',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='cnpjentrega',
            new_name='cnpj_entrega',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='dataemissao',
            new_name='data_emissao',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='datavalidade',
            new_name='data_validade',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='enderecoentrega',
            new_name='endereco_entrega',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='marcasembarque',
            new_name='marcas_embarque',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='nomeentrega',
            new_name='nome_entrega',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='paisentrega',
            new_name='pais_entrega',
        ),
        migrations.RenameField(
            model_name='orcamento',
            old_name='tipoentrega',
            new_name='tipo_entrega',
        ),
        migrations.RenameField(
            model_name='peca',
            old_name='codigointerno',
            new_name='codigo_interno',
        ),
        migrations.RenameField(
            model_name='peca',
            old_name='precoexportacao',
            new_name='preco_exportacao',
        ),
        migrations.RenameField(
            model_name='peca',
            old_name='preconacional',
            new_name='preco_nacional',
        ),
        migrations.RenameField(
            model_name='peca',
            old_name='precovenda',
            new_name='preco_venda',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='codigo_cliente',
            new_name='cliente',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='codigo_orcamento',
            new_name='orcamento',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='codigo_peca',
            new_name='peca',
        ),
        migrations.RenameField(
            model_name='pedidocompra',
            old_name='dataemicao',
            new_name='data_emissao',
        ),
        migrations.RenameField(
            model_name='pedidocompra',
            old_name='operacaofiscal',
            new_name='operacao_fiscal',
        ),
    ]