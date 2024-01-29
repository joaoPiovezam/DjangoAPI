import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
import pypyodbc as odbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from loja.models import Peca



tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\precos.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n')

l = len(tabela)
for i in range(l):
    p = Peca(codigo = tabela['codigo'][i], descricao = tabela['descricao'][i], precoVenda = tabela['precoVenda'][i],
             precoExportacao = tabela['precoExportacao'][i], precoNacional = tabela['precoNacional'][i], ret = tabela['ret'][i],
             cc = tabela['cc'][i], peso  = tabela['peso'][i], comprimento = tabela['comprimento'][i],
             largura = tabela['largura'][i], altura = tabela['altura'][i], ncm = tabela['ncm'][i], gde  = tabela['gde'][i])
    p.save()