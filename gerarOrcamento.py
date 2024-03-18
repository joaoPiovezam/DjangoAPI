import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Pedido, Peca, Orcamento, Cliente


tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\teste.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

l = len(tabela)
pedido = Pedido.objects.last()
codigoP = pedido.codigoPedido + 1
cliente = Cliente.objects.first()
orcamento = Orcamento.objects.filter(codigo = 1).first()

for i in range(l):
    peca = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
    p = Pedido(           
            codigoPedido = codigoP,
            codigoPeca = peca,
            codigoOrcamento = orcamento,
            codigoCliente = cliente,
            dataEntrega = '2024-05-10',
            quantidade =  tabela['qtd\r'][i]
            )
    p.save()

