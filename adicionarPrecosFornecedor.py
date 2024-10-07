import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Fornecedor, Peca, PecaFornecedor


tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\testePecaFornecedor.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

l = len(tabela)
fornecedorO = Fornecedor.objects.filter(id = 1).first()
pecasNaoEncontradas = []
pecasEncontradas = []
for i in range(l):
    pecaO = Peca.objects.filter(codigo =  tabela['codigo'][i]).first()
    pecaFornecedor = PecaFornecedor.objects.filter(fornecedor = fornecedorO).all()
    pecaFornecedor = pecaFornecedor.filter(peca = pecaO ).first()
    if (pecaO is None):
        pecasNaoEncontradas.append(tabela['codigo'][i])
    else:
        pecasEncontradas.append(tabela['codigo'][i])
        if (pecaFornecedor is None):
            pf = PecaFornecedor(           
                    codigo = 12,
                    peca = pecaO,
                    preco = tabela['preco\r'][i],
                    fornecedor = fornecedorO
                    )
            pf.save()
        else:
            pecaFornecedor.preco = tabela['preco\r'][i]
            pecaFornecedor.save()

print("Peças adicionadas : " + '\n' + str(pecasEncontradas) + "\nPeças não encontradas : " + '\n' + str(pecasNaoEncontradas))