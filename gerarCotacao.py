import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Pedido, Cotacao, PecaFornecedor



pedidos = Pedido.objects.all().filter(codigoOrcamento = 1)
for pedido in pedidos:
        pecas = pedido.codigoPeca
        pecaFornecedor = PecaFornecedor.objects.filter(peca = pecas).order_by('-preco').last()
        cotacao = Cotacao(
                codigo = 1,
                codigoPedido = pedido,
                codigoPecaFornecedor = pecaFornecedor
        )
        cotacao.save()

