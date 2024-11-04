import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import pandas as pd
from loja.models import Fornecedor, Peca, PecaFornecedor

def extrair_float_split(texto):
    for palavra in texto.split():
        try:
            return float(palavra)
        except ValueError:
            pass
    return 0


tabela = pd.read_csv(r'C:\Users\TARS\OneDrive\Documentos\testeUnimaq.csv', on_bad_lines='skip', encoding='latin-1', lineterminator='\n', sep = ';')

l = len(tabela)
fornecedorO = Fornecedor.objects.filter(id = 1).first()
pecasNaoEncontradas = []
pecasEncontradas = []
for i in range(l):
    pecas  = tabela['Reference Original'][i].split(' / ')
    for peca in pecas:
        pecaO = Peca.objects.filter(codigo =  peca).first()
        pecaFornecedor = PecaFornecedor.objects.filter(fornecedor = fornecedorO).all()
        pecaFornecedor = pecaFornecedor.filter(peca = pecaO ).first()
        if (pecaO is None):
            pecasNaoEncontradas.append(peca)
        else:
            pecasEncontradas.append(peca)
            if (pecaFornecedor is None):
                pf = PecaFornecedor(           
                        codigo = 12,
                        peca = pecaO,
                        preco = extrair_float_split(tabela['UNIMAQ\r'][i]),
                        fornecedor = fornecedorO
                        )
                pf.save()
            else:
                pecaFornecedor.preco = extrair_float_split(tabela['UNIMAQ\r'][i])
                pecaFornecedor.save()

print("Peças adicionadas : " + '\n' + str(pecasEncontradas) + "\nPeças não encontradas : " + '\n' + str(pecasNaoEncontradas))