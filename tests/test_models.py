"""
Unit tests for Django API models
Tests model creation, validation, and methods
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from loja.models import (
    Peca, Cliente, Usuario, Fornecedor, Orcamento, 
    Pedido, CondicaoPagamento, Cotacao, PecaFornecedor,
    Transportadora, PedidoCompra, Estoque, Notificar, Pack
)


class PecaModelTest(TestCase):
    """Test cases for Peca model"""
    
    def setUp(self):
        """Set up test data"""
        self.peca_data = {
            'codigo': 'TEST001',
            'descricao': 'Test Piece',
            'marca': 'Test Brand',
            'preco_venda': Decimal('100.000'),
            'preco_exportacao': Decimal('90.000'),
            'preco_nacional': Decimal('110.000'),
            'ret': 'R',
            'cc': 123,
            'peso': Decimal('1.500'),
            'comprimento': Decimal('10.000'),
            'largura': Decimal('5.000'),
            'altura': Decimal('2.000'),
            'ncm': 12345678,
            'gde': 1
        }
    
    def test_create_peca(self):
        """Test creating a new Peca"""
        peca = Peca.objects.create(**self.peca_data)
        self.assertEqual(peca.codigo, 'TEST001')
        self.assertEqual(peca.descricao, 'Test Piece')
        self.assertEqual(peca.preco_venda, Decimal('100.000'))
        self.assertTrue(peca.id)
    
    def test_peca_str_method(self):
        """Test Peca string representation"""
        peca = Peca.objects.create(**self.peca_data)
        expected_str = f"{peca.codigo} - {peca.descricao}"
        self.assertEqual(str(peca), expected_str)
    
    def test_volume_peca_property(self):
        """Test volumePeca calculated property"""
        peca = Peca.objects.create(**self.peca_data)
        expected_volume = Decimal('10.000') * Decimal('5.000') * Decimal('2.000')
        self.assertEqual(peca.volumePeca, expected_volume)
    
    def test_codigo_interno_auto_increment(self):
        """Test that codigo_interno auto-increments"""
        peca1 = Peca.objects.create(**self.peca_data)
        peca2_data = self.peca_data.copy()
        peca2_data['codigo'] = 'TEST002'
        peca2 = Peca.objects.create(**peca2_data)
        
        self.assertGreater(peca2.codigo_interno, peca1.codigo_interno)
        self.assertEqual(peca2.codigo_interno - peca1.codigo_interno, 10)


class ClienteModelTest(TestCase):
    """Test cases for Cliente model"""
    
    def setUp(self):
        """Set up test data"""
        self.cliente_data = {
            'tipo_pessoa': 'j',
            'nome_cliente': 'Test Company',
            'cpfcnpj': '12345678901234',
            'endereco': 'Test Address 123',
            'cep': '12345678',
            'cidade': 'Test City',
            'pais': 'Brazil',
            'telefone': '11999999999',
            'site': 'www.testcompany.com',
            'email': 'test@testcompany.com',
            'detalhe': 'Test company details'
        }
    
    def test_create_cliente(self):
        """Test creating a new Cliente"""
        cliente = Cliente.objects.create(**self.cliente_data)
        self.assertEqual(cliente.nome_cliente, 'Test Company')
        self.assertEqual(cliente.tipo_pessoa, 'j')
        self.assertEqual(cliente.email, 'test@testcompany.com')
    
    def test_cliente_str_method(self):
        """Test Cliente string representation"""
        cliente = Cliente.objects.create(**self.cliente_data)
        self.assertEqual(str(cliente), 'Test Company')
    
    def test_cliente_pessoa_fisica(self):
        """Test creating Cliente as pessoa física"""
        self.cliente_data['tipo_pessoa'] = 'f'
        cliente = Cliente.objects.create(**self.cliente_data)
        self.assertEqual(cliente.tipo_pessoa, 'f')


class UsuarioModelTest(TestCase):
    """Test cases for Usuario model"""
    
    def setUp(self):
        """Set up test data"""
        self.usuario_data = {
            'nome': 'Test User',
            'empresa': 'Test Company',
            'email': 'testuser@company.com',
            'cpfcnpj': '12345678901',
            'endereco': 'Test Address 456',
            'cep': '87654321',
            'cidade': 'Test City',
            'pais': 'Brazil',
            'telefone': '11888888888'
        }
    
    def test_create_usuario(self):
        """Test creating a new Usuario"""
        usuario = Usuario.objects.create(**self.usuario_data)
        self.assertEqual(usuario.nome, 'Test User')
        self.assertEqual(usuario.email, 'testuser@company.com')
    
    def test_usuario_str_method(self):
        """Test Usuario string representation"""
        usuario = Usuario.objects.create(**self.usuario_data)
        self.assertEqual(str(usuario), 'Test User')


class FornecedorModelTest(TestCase):
    """Test cases for Fornecedor model"""
    
    def setUp(self):
        """Set up test data"""
        self.fornecedor_data = {
            'tipo_pessoa': 'j',
            'nome_fornecedor': 'Test Supplier',
            'cpfcnpj': '98765432109876',
            'endereco': 'Supplier Address 789',
            'cep': '11223344',
            'cidade': 'Supplier City',
            'pais': 'Brazil',
            'telefone': '11777777777',
            'site': 'www.testsupplier.com',
            'email': 'contact@testsupplier.com',
            'detalhe': 'Test supplier details'
        }
    
    def test_create_fornecedor(self):
        """Test creating a new Fornecedor"""
        fornecedor = Fornecedor.objects.create(**self.fornecedor_data)
        self.assertEqual(fornecedor.nome_fornecedor, 'Test Supplier')
        self.assertEqual(fornecedor.email, 'contact@testsupplier.com')
    
    def test_fornecedor_str_method(self):
        """Test Fornecedor string representation"""
        fornecedor = Fornecedor.objects.create(**self.fornecedor_data)
        self.assertEqual(str(fornecedor), 'Test Supplier')


class OrcamentoModelTest(TestCase):
    """Test cases for Orcamento model"""
    
    def setUp(self):
        """Set up test data"""
        self.cliente = Cliente.objects.create(
            nome_cliente='Test Client',
            cpfcnpj='12345678901234',
            endereco='Client Address',
            cep='12345678',
            cidade='Client City',
            pais='Brazil',
            telefone='11999999999',
            site='www.client.com',
            email='client@test.com',
            detalhe='Test client'
        )
        
        self.orcamento_data = {
            'data_emissao': date.today(),
            'data_validade': date.today() + timedelta(days=30),
            'tipo_entrega': '4',  # FOB
            'responsavel': 'Test Manager',
            'frete': Decimal('500.000'),
            'cliente': self.cliente,
            'marcas_embarque': 'Test Marks',
            'nome_entrega': 'Delivery Name',
            'cnpj_entrega': '12345678901234',
            'endereco_entrega': 'Delivery Address',
            'cidade_entrega': 'Delivery City',
            'pais_entrega': 'Brazil',
            'status_oramento': '1'
        }
    
    def test_create_orcamento(self):
        """Test creating a new Orcamento"""
        orcamento = Orcamento.objects.create(**self.orcamento_data)
        self.assertEqual(orcamento.responsavel, 'Test Manager')
        self.assertEqual(orcamento.cliente, self.cliente)
        self.assertEqual(orcamento.status_oramento, '1')
    
    def test_orcamento_str_method(self):
        """Test Orcamento string representation"""
        orcamento = Orcamento.objects.create(**self.orcamento_data)
        self.assertEqual(str(orcamento), str(orcamento.codigo))
    
    def test_orcamento_codigo_auto_increment(self):
        """Test that codigo auto-increments"""
        orcamento1 = Orcamento.objects.create(**self.orcamento_data)
        orcamento2 = Orcamento.objects.create(**self.orcamento_data)
        
        self.assertGreater(orcamento2.codigo, orcamento1.codigo)
        self.assertEqual(orcamento2.codigo - orcamento1.codigo, 10)


class PedidoModelTest(TestCase):
    """Test cases for Pedido model"""
    
    def setUp(self):
        """Set up test data"""
        # Create dependencies
        self.cliente = Cliente.objects.create(
            nome_cliente='Test Client',
            cpfcnpj='12345678901234',
            endereco='Client Address',
            cep='12345678',
            cidade='Client City',
            pais='Brazil',
            telefone='11999999999',
            site='www.client.com',
            email='client@test.com',
            detalhe='Test client'
        )
        
        self.peca = Peca.objects.create(
            codigo='TEST001',
            descricao='Test Piece',
            marca='Test Brand',
            preco_venda=Decimal('100.000'),
            preco_exportacao=Decimal('90.000'),
            preco_nacional=Decimal('110.000'),
            ret='R',
            cc=123,
            peso=Decimal('1.500'),
            comprimento=Decimal('10.000'),
            largura=Decimal('5.000'),
            altura=Decimal('2.000'),
            ncm=12345678,
            gde=1
        )
        
        self.orcamento = Orcamento.objects.create(
            data_emissao=date.today(),
            data_validade=date.today() + timedelta(days=30),
            tipo_entrega='4',
            responsavel='Test Manager',
            frete=Decimal('500.000'),
            cliente=self.cliente,
            marcas_embarque='Test Marks',
            nome_entrega='Delivery Name',
            cnpj_entrega='12345678901234',
            endereco_entrega='Delivery Address',
            cidade_entrega='Delivery City',
            pais_entrega='Brazil',
            status_oramento='1'
        )
        
        self.pedido_data = {
            'codigo_pedido': 1001,
            'peca': self.peca,
            'orcamento': self.orcamento,
            'cliente': self.cliente,
            'data_entrega': date.today() + timedelta(days=15),
            'quantidade': 10,
            'peso_bruto': Decimal('15.000'),
            'volume_bruto': Decimal('100.000'),
            'unidade': 'PCS',
            'pacote': 'Box',
            'volume': 5,
            'descricao': 'Test order description',
            'desconto': Decimal('5.00')
        }
    
    def test_create_pedido(self):
        """Test creating a new Pedido"""
        pedido = Pedido.objects.create(**self.pedido_data)
        self.assertEqual(pedido.codigo_pedido, 1001)
        self.assertEqual(pedido.quantidade, 10)
        self.assertEqual(pedido.peca, self.peca)
        self.assertEqual(pedido.orcamento, self.orcamento)
    
    def test_pedido_str_method(self):
        """Test Pedido string representation"""
        pedido = Pedido.objects.create(**self.pedido_data)
        expected_str = str(pedido.codigo_pedido) + pedido.peca.codigo
        self.assertEqual(str(pedido), expected_str)
