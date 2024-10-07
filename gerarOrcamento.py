import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Pedido, Peca, Orcamento, Cliente


tabela = pd.read_csv(r'C:\Users\TARS\Downloads\Cotação teste.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

l = len(tabela)
pedido = Pedido.objects.last()
codigoP = pedido.codigoPedido + 1
cliente = Cliente.objects.first()
orcamento = Orcamento.objects.filter(codigo = 1).first()
pecasEncontradas = []
pecasNaoEncontradas = []

for i in range(l):
        peca = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
        if (peca is None):
                pecasNaoEncontradas.append(tabela['codigo'][i])
        else:
                pecasEncontradas.append(tabela['codigo'][i])
                p = Pedido(           
                        codigoPedido = codigoP,
                        codigoPeca = peca,
                        codigoOrcamento = orcamento,
                        codigoCliente = cliente,
                        dataEntrega = '2024-05-10',
                        quantidade =  tabela['qtd'][i],
                        pesoBruto = 10,
                        volume = 0,
                        volumeBruto = 10
                        )
                p.save()

print("Peças adicionadas : " + '\n' + str(pecasEncontradas) + "\nPeças não encontradas : " + '\n' + str(pecasNaoEncontradas))