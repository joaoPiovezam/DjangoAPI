# Generated by Django 4.1 on 2024-10-16 18:05

from django.db import migrations, models
import django.db.models.deletion
import loja.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipopessoa', models.CharField(choices=[('f', 'Pessoa Fisica'), ('j', 'Pessoa Juridica')], default='j', max_length=1)),
                ('nomecliente', models.CharField(max_length=250)),
                ('cpfcnpj', models.CharField(max_length=14)),
                ('endereco', models.CharField(max_length=250)),
                ('cep', models.CharField(max_length=250)),
                ('cidade', models.CharField(max_length=250)),
                ('pais', models.CharField(max_length=250)),
                ('telefone', models.CharField(max_length=250)),
                ('site', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('detalhe', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipopessoa', models.CharField(choices=[('f', 'Pessoa Fisica'), ('j', 'Pessoa Juridica')], default='j', max_length=1)),
                ('nomefornecedor', models.CharField(max_length=50)),
                ('cpfcnpj', models.CharField(max_length=14)),
                ('endereco', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=60)),
                ('pais', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=20)),
                ('site', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=30)),
                ('detalhe', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(default=loja.models.add_dez)),
                ('dataemissao', models.DateField()),
                ('datavalidade', models.DateField()),
                ('tipoentrega', models.CharField(choices=[('1', 'EXW'), ('2', 'FCA'), ('3', 'FAS'), ('4', 'FOB'), ('5', 'CIF'), ('6', 'CFR'), ('7', 'CTP'), ('8', 'CIP'), ('9', 'DAT'), ('10', 'DAP'), ('11', 'DDP')], default='3', max_length=5)),
                ('responsavel', models.CharField(max_length=50)),
                ('frete', models.DecimalField(decimal_places=3, max_digits=15)),
                ('marcasembarque', models.CharField(max_length=250)),
                ('nomeentrega', models.CharField(max_length=250)),
                ('cnpjentrega', models.CharField(max_length=250)),
                ('enderecoentrega', models.CharField(max_length=250)),
                ('cidadeentrega', models.CharField(max_length=250)),
                ('paisentrega', models.CharField(max_length=250)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Peca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30)),
                ('codigointerno', models.IntegerField(default=loja.models.add_ten)),
                ('descricao', models.CharField(max_length=30)),
                ('marca', models.CharField(max_length=50)),
                ('precovenda', models.DecimalField(decimal_places=3, max_digits=15)),
                ('precoexportacao', models.DecimalField(decimal_places=3, max_digits=15)),
                ('preconacional', models.DecimalField(decimal_places=3, max_digits=15)),
                ('ret', models.CharField(choices=[('R', 'R'), ('N', 'N'), ('D', 'D')], default='R', max_length=1)),
                ('cc', models.IntegerField()),
                ('peso', models.DecimalField(decimal_places=3, max_digits=15)),
                ('comprimento', models.DecimalField(decimal_places=3, max_digits=15)),
                ('largura', models.DecimalField(decimal_places=3, max_digits=15)),
                ('altura', models.DecimalField(decimal_places=3, max_digits=15)),
                ('ncm', models.IntegerField()),
                ('gde', models.IntegerField()),
            ],
        ),
           
        migrations.CreateModel(
            name='Transportadora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=255)),
                ('endereco', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=60)),
                ('pais', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=20)),
                ('site', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=30)),
                ('detalhe', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=250)),
                ('empresa', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('cpfcnpj', models.CharField(max_length=14)),
                ('endereco', models.CharField(max_length=250)),
                ('cep', models.CharField(max_length=250)),
                ('cidade', models.CharField(max_length=250)),
                ('pais', models.CharField(max_length=250)),
                ('telefone', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataemicao', models.DateField(auto_now_add=True)),
                ('operacaofiscal', models.CharField(max_length=255)),
                ('vencimento', models.CharField(choices=[('1', '28'), ('2', '30'), ('3', '30/60/90'), ('4', '28/56/84'), ('5', '30/60'), ('6', '28/56'), ('7', '30/45/60')], max_length=50)),
                ('comprador', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('observacoes', models.TextField()),
                ('frete', models.CharField(max_length=255)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.fornecedor')),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento')),
                ('transportadora', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.transportadora')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_pedido', models.IntegerField()),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('data_entrega', models.DateField()),
                ('quantidade', models.IntegerField()),
                ('peso_bruto', models.DecimalField(decimal_places=3, max_digits=15)),
                ('volume_bruto', models.DecimalField(decimal_places=3, max_digits=15)),
                ('unidade', models.CharField(max_length=255)),
                ('pacote', models.CharField(max_length=255)),
                ('volume', models.IntegerField()),
                ('codigo_cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.cliente')),
                ('codigo_orcamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento')),
                ('codigo_peca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.peca')),
            ],
        ),
        migrations.CreateModel(
            name='PecaFornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30)),
                ('preco', models.DecimalField(decimal_places=3, max_digits=15)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.fornecedor')),
                ('peca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.peca')),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.IntegerField()),
                ('pacote', models.CharField(max_length=255)),
                ('comprimento', models.DecimalField(decimal_places=3, max_digits=15)),
                ('largura', models.DecimalField(decimal_places=3, max_digits=15)),
                ('altura', models.DecimalField(decimal_places=3, max_digits=15)),
                ('peso', models.DecimalField(decimal_places=3, max_digits=15)),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento')),
            ],
        ),
        migrations.CreateModel(
            name='Notificar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento')),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataentrada', models.DateField()),
                ('datasaida', models.DateField()),
                ('estado', models.CharField(choices=[('1', 'fora de estoque'), ('2', 'em estoque'), ('3', 'entregue ao cliente')], max_length=50)),
                ('codigopedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_peca_fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.pecafornecedor')),
                ('codigo_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='CondicaoPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Não Pago'), ('2', 'Pago')], default='1', max_length=1)),
                ('cota', models.CharField(max_length=255)),
                ('porcentagem', models.DecimalField(decimal_places=3, max_digits=15)),
                ('data', models.DateField()),
                ('total', models.DecimalField(decimal_places=3, max_digits=15)),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento')),
            ],
        ),
    ]
