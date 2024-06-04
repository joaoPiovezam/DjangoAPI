import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Fornecedor, Peca, PecaFornecedor


tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\testePecaFornecedor.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

l = len(tabela)
fornecedorO = Fornecedor.objects.filter(id = 1).first()
for i in range(l):
    pecaO = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
    pecaFornecedor = PecaFornecedor.objects.filter(fonecedor = fornecedorO).all()
    pecaFornecedor = pecaFornecedor.filter(peca = pecaO ).first()
    if (pecaFornecedor is None):
        pf = PecaFornecedor(           
                codigo = 12,
                peca = pecaO,
                preco = tabela['preco\r'][i],
                fonecedor = fornecedorO
                )
        pf.save()
    else:
        pecaFornecedor.preco = tabela['preco\r'][i]
        pecaFornecedor.save()