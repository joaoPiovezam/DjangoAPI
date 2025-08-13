"""
Unit tests for Django API endpoints
Tests GET, POST, PUT, DELETE operations for main ViewSets
"""

import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from loja.models import (
    Peca, Cliente, Usuario, Fornecedor, Orcamento, 
    Pedido, CondicaoPagamento, Cotacao, PecaFornecedor,
    Transportadora, PedidoCompra, Estoque, Notificar, Pack
)


class BaseAPITestCase(TestCase):
    """Base test case with common setup for API tests"""
    
    def setUp(self):
        """Set up test data and authentication"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create authentication token
        self.token = Token.objects.create(user=self.user)
        
        # Set up API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create test data
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create test data for API tests"""
        # Create test Peca
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
        
        # Create test Cliente
        self.cliente = Cliente.objects.create(
            tipo_pessoa='j',
            nome_cliente='Test Company',
            cpfcnpj='12345678901234',
            endereco='Test Address 123',
            cep='12345678',
            cidade='Test City',
            pais='Brazil',
            telefone='11999999999',
            site='www.testcompany.com',
            email='test@testcompany.com',
            detalhe='Test company details'
        )
        
        # Create test Usuario
        self.usuario = Usuario.objects.create(
            nome='Test User',
            empresa='Test Company',
            email='testuser@company.com',
            cpfcnpj='12345678901',
            endereco='Test Address 456',
            cep='87654321',
            cidade='Test City',
            pais='Brazil',
            telefone='11888888888'
        )
        
        # Create test Fornecedor
        self.fornecedor = Fornecedor.objects.create(
            tipo_pessoa='j',
            nome_fornecedor='Test Supplier',
            cpfcnpj='98765432109876',
            endereco='Supplier Address 789',
            cep='11223344',
            cidade='Supplier City',
            pais='Brazil',
            telefone='11777777777',
            site='www.testsupplier.com',
            email='contact@testsupplier.com',
            detalhe='Test supplier details'
        )
        
        # Create test Orcamento
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


class PecasAPITest(BaseAPITestCase):
    """Test cases for Pecas API endpoints"""
    
    def test_get_pecas_list(self):
        """Test GET /pecas/ - List all pecas"""
        url = reverse('Pecas-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['codigo'], 'TEST001')
    
    def test_get_peca_detail(self):
        """Test GET /pecas/{id}/ - Get specific peca"""
        url = reverse('Pecas-detail', kwargs={'pk': self.peca.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo'], 'TEST001')
        self.assertEqual(response.data['descricao'], 'Test Piece')
    
    def test_post_create_peca(self):
        """Test POST /pecas/ - Create new peca"""
        url = reverse('Pecas-list')
        data = {
            'codigo': 'TEST002',
            'descricao': 'New Test Piece',
            'marca': 'New Brand',
            'preco_venda': '150.000',
            'preco_exportacao': '140.000',
            'preco_nacional': '160.000',
            'ret': 'N',
            'cc': 456,
            'peso': '2.500',
            'comprimento': '15.000',
            'largura': '8.000',
            'altura': '3.000',
            'ncm': 87654321,
            'gde': 2
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['codigo'], 'TEST002')
        self.assertEqual(Peca.objects.count(), 2)
    
    def test_put_update_peca(self):
        """Test PUT /pecas/{id}/ - Update peca"""
        url = reverse('Pecas-detail', kwargs={'pk': self.peca.id})
        data = {
            'codigo': 'TEST001',
            'descricao': 'Updated Test Piece',
            'marca': 'Updated Brand',
            'preco_venda': '120.000',
            'preco_exportacao': '110.000',
            'preco_nacional': '130.000',
            'ret': 'R',
            'cc': 123,
            'peso': '1.500',
            'comprimento': '10.000',
            'largura': '5.000',
            'altura': '2.000',
            'ncm': 12345678,
            'gde': 1
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descricao'], 'Updated Test Piece')
        
        # Verify database was updated
        updated_peca = Peca.objects.get(id=self.peca.id)
        self.assertEqual(updated_peca.descricao, 'Updated Test Piece')
    
    def test_patch_partial_update_peca(self):
        """Test PATCH /pecas/{id}/ - Partial update peca"""
        url = reverse('Pecas-detail', kwargs={'pk': self.peca.id})
        data = {
            'descricao': 'Partially Updated Piece',
            'preco_venda': '125.000'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descricao'], 'Partially Updated Piece')
        self.assertEqual(response.data['preco_venda'], '125.000')
        
        # Verify other fields remain unchanged
        updated_peca = Peca.objects.get(id=self.peca.id)
        self.assertEqual(updated_peca.codigo, 'TEST001')  # Should remain unchanged
    
    def test_delete_peca(self):
        """Test DELETE /pecas/{id}/ - Delete peca"""
        url = reverse('Pecas-detail', kwargs={'pk': self.peca.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Peca.objects.count(), 0)
    
    def test_unauthorized_access(self):
        """Test that unauthorized requests are rejected"""
        # Remove authentication
        self.client.credentials()
        
        url = reverse('Pecas-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ClientesAPITest(BaseAPITestCase):
    """Test cases for Clientes API endpoints"""
    
    def test_get_clientes_list(self):
        """Test GET /clientes/ - List all clientes"""
        url = reverse('Clientes-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nome_cliente'], 'Test Company')
    
    def test_get_cliente_detail(self):
        """Test GET /clientes/{id}/ - Get specific cliente"""
        url = reverse('Clientes-detail', kwargs={'pk': self.cliente.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_cliente'], 'Test Company')
        self.assertEqual(response.data['email'], 'test@testcompany.com')
    
    def test_post_create_cliente(self):
        """Test POST /clientes/ - Create new cliente"""
        url = reverse('Clientes-list')
        data = {
            'tipo_pessoa': 'f',
            'nome_cliente': 'New Test Client',
            'cpfcnpj': '98765432109',
            'endereco': 'New Address 456',
            'cep': '87654321',
            'cidade': 'New City',
            'pais': 'Brazil',
            'telefone': '11888888888',
            'site': 'www.newclient.com',
            'email': 'new@client.com',
            'detalhe': 'New client details'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome_cliente'], 'New Test Client')
        self.assertEqual(Cliente.objects.count(), 2)
    
    def test_put_update_cliente(self):
        """Test PUT /clientes/{id}/ - Update cliente"""
        url = reverse('Clientes-detail', kwargs={'pk': self.cliente.id})
        data = {
            'tipo_pessoa': 'j',
            'nome_cliente': 'Updated Test Company',
            'cpfcnpj': '12345678901234',
            'endereco': 'Updated Address 123',
            'cep': '12345678',
            'cidade': 'Updated City',
            'pais': 'Brazil',
            'telefone': '11999999999',
            'site': 'www.updatedcompany.com',
            'email': 'updated@testcompany.com',
            'detalhe': 'Updated company details'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_cliente'], 'Updated Test Company')
        self.assertEqual(response.data['email'], 'updated@testcompany.com')
    
    def test_delete_cliente(self):
        """Test DELETE /clientes/{id}/ - Delete cliente"""
        url = reverse('Clientes-detail', kwargs={'pk': self.cliente.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)


class OrcamentosAPITest(BaseAPITestCase):
    """Test cases for Orcamentos API endpoints"""
    
    def test_get_orcamentos_list(self):
        """Test GET /orcamentos/ - List all orcamentos"""
        url = reverse('Orcamentos-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['responsavel'], 'Test Manager')
    
    def test_get_orcamento_detail(self):
        """Test GET /orcamentos/{id}/ - Get specific orcamento"""
        url = reverse('Orcamentos-detail', kwargs={'pk': self.orcamento.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['responsavel'], 'Test Manager')
        self.assertEqual(response.data['status_oramento'], '1')
    
    def test_post_create_orcamento(self):
        """Test POST /orcamentos/ - Create new orcamento"""
        url = reverse('Orcamentos-list')
        data = {
            'data_emissao': date.today().isoformat(),
            'data_validade': (date.today() + timedelta(days=45)).isoformat(),
            'tipo_entrega': '5',  # CIF
            'responsavel': 'New Manager',
            'frete': '750.000',
            'cliente': self.cliente.id,
            'marcas_embarque': 'New Marks',
            'nome_entrega': 'New Delivery Name',
            'cnpj_entrega': '98765432109876',
            'endereco_entrega': 'New Delivery Address',
            'cidade_entrega': 'New Delivery City',
            'pais_entrega': 'Brazil',
            'status_oramento': '1'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['responsavel'], 'New Manager')
        self.assertEqual(Orcamento.objects.count(), 2)
    
    def test_put_update_orcamento(self):
        """Test PUT /orcamentos/{id}/ - Update orcamento"""
        url = reverse('Orcamentos-detail', kwargs={'pk': self.orcamento.id})
        data = {
            'data_emissao': self.orcamento.data_emissao.isoformat(),
            'data_validade': self.orcamento.data_validade.isoformat(),
            'tipo_entrega': '6',  # CFR
            'responsavel': 'Updated Manager',
            'frete': '600.000',
            'cliente': self.cliente.id,
            'marcas_embarque': 'Updated Marks',
            'nome_entrega': 'Updated Delivery Name',
            'cnpj_entrega': '12345678901234',
            'endereco_entrega': 'Updated Delivery Address',
            'cidade_entrega': 'Updated Delivery City',
            'pais_entrega': 'Brazil',
            'status_oramento': '2'  # Faturado
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['responsavel'], 'Updated Manager')
        self.assertEqual(response.data['status_oramento'], '2')
    
    def test_delete_orcamento(self):
        """Test DELETE /orcamentos/{id}/ - Delete orcamento"""
        url = reverse('Orcamentos-detail', kwargs={'pk': self.orcamento.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Orcamento.objects.count(), 0)


class PedidosAPITest(BaseAPITestCase):
    """Test cases for Pedidos API endpoints"""

    def setUp(self):
        """Set up additional test data for pedidos"""
        super().setUp()

        # Create test Pedido
        self.pedido = Pedido.objects.create(
            codigo_pedido=1001,
            peca=self.peca,
            orcamento=self.orcamento,
            cliente=self.cliente,
            data_entrega=date.today() + timedelta(days=15),
            quantidade=10,
            peso_bruto=Decimal('15.000'),
            volume_bruto=Decimal('100.000'),
            unidade='PCS',
            pacote='Box',
            volume=5,
            descricao='Test order description',
            desconto=Decimal('5.00')
        )

    def test_get_pedidos_list(self):
        """Test GET /pedidos/ - List all pedidos"""
        url = reverse('Pedidos-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['codigo_pedido'], 1001)

    def test_get_pedido_detail(self):
        """Test GET /pedidos/{id}/ - Get specific pedido"""
        url = reverse('Pedidos-detail', kwargs={'pk': self.pedido.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo_pedido'], 1001)
        self.assertEqual(response.data['quantidade'], 10)

    def test_post_create_pedido(self):
        """Test POST /pedidos/ - Create new pedido"""
        url = reverse('Pedidos-list')
        data = {
            'codigo_pedido': 1002,
            'peca': self.peca.id,
            'orcamento': self.orcamento.id,
            'cliente': self.cliente.id,
            'data_entrega': (date.today() + timedelta(days=20)).isoformat(),
            'quantidade': 15,
            'peso_bruto': '22.500',
            'volume_bruto': '150.000',
            'unidade': 'PCS',
            'pacote': 'Crate',
            'volume': 8,
            'descricao': 'New test order',
            'desconto': '7.50'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['codigo_pedido'], 1002)
        self.assertEqual(Pedido.objects.count(), 2)

    def test_put_update_pedido(self):
        """Test PUT /pedidos/{id}/ - Update pedido"""
        url = reverse('Pedidos-detail', kwargs={'pk': self.pedido.id})
        data = {
            'codigo_pedido': 1001,
            'peca': self.peca.id,
            'orcamento': self.orcamento.id,
            'cliente': self.cliente.id,
            'data_entrega': (date.today() + timedelta(days=25)).isoformat(),
            'quantidade': 20,
            'peso_bruto': '30.000',
            'volume_bruto': '200.000',
            'unidade': 'PCS',
            'pacote': 'Updated Box',
            'volume': 10,
            'descricao': 'Updated order description',
            'desconto': '10.00'
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantidade'], 20)
        self.assertEqual(response.data['descricao'], 'Updated order description')

    def test_delete_pedido(self):
        """Test DELETE /pedidos/{id}/ - Delete pedido"""
        url = reverse('Pedidos-detail', kwargs={'pk': self.pedido.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pedido.objects.count(), 0)


class UsuariosAPITest(BaseAPITestCase):
    """Test cases for Usuarios API endpoints"""

    def test_get_usuarios_list(self):
        """Test GET /usuarios/ - List all usuarios"""
        url = reverse('Usuarios-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nome'], 'Test User')

    def test_get_usuario_detail(self):
        """Test GET /usuarios/{id}/ - Get specific usuario"""
        url = reverse('Usuarios-detail', kwargs={'pk': self.usuario.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Test User')
        self.assertEqual(response.data['email'], 'testuser@company.com')

    def test_post_create_usuario(self):
        """Test POST /usuarios/ - Create new usuario"""
        url = reverse('Usuarios-list')
        data = {
            'nome': 'New Test User',
            'empresa': 'New Company',
            'email': 'newuser@company.com',
            'cpfcnpj': '98765432109',
            'endereco': 'New Address 789',
            'cep': '11223344',
            'cidade': 'New City',
            'pais': 'Brazil',
            'telefone': '11777777777'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'New Test User')
        self.assertEqual(Usuario.objects.count(), 2)

    def test_put_update_usuario(self):
        """Test PUT /usuarios/{id}/ - Update usuario"""
        url = reverse('Usuarios-detail', kwargs={'pk': self.usuario.id})
        data = {
            'nome': 'Updated Test User',
            'empresa': 'Updated Company',
            'email': 'updated@company.com',
            'cpfcnpj': '12345678901',
            'endereco': 'Updated Address 456',
            'cep': '87654321',
            'cidade': 'Updated City',
            'pais': 'Brazil',
            'telefone': '11888888888'
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Updated Test User')
        self.assertEqual(response.data['email'], 'updated@company.com')

    def test_delete_usuario(self):
        """Test DELETE /usuarios/{id}/ - Delete usuario"""
        url = reverse('Usuarios-detail', kwargs={'pk': self.usuario.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Usuario.objects.count(), 0)
