import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Peca
import re


tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\precos3.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ',')
print(tabela)
l = len(tabela)
for i in range(l):
    if tabela['codigo'][i] == 'CQ08134':
        break
    if type(tabela['gde\r'][i]) is not int:
        gden = tabela['gde\r'][i].replace("\r","")
        gde = gden.replace("O",'0')
    else:
        gde = tabela['gde\r'][i]
    p = Peca(codigo = tabela['codigo'][i], descricao = tabela['descricao'][i], preco_venda = tabela['precoVenda'][i],
             preco_exportacao = tabela['precoExportacao'][i], preco_nacional = tabela['precoNacional'][i], ret = tabela['ret'][i],
             cc = tabela['cc'][i], peso  = tabela['peso'][i], comprimento = tabela['comprimento'][i],
             largura = tabela['largura'][i], altura = tabela['altura'][i], ncm = tabela['ncm'][i], gde = gde)
    p.save()