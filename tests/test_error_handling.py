"""
Unit tests for error handling and edge cases
Tests validation errors, 404s, and other error scenarios
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


class ErrorHandlingAPITest(TestCase):
    """Test cases for API error handling"""
    
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
        """Create minimal test data"""
        self.cliente = Cliente.objects.create(
            nome_cliente='Test Company',
            cpfcnpj='12345678901234',
            endereco='Test Address',
            cep='12345678',
            cidade='Test City',
            pais='Brazil',
            telefone='11999999999',
            site='www.test.com',
            email='test@company.com',
            detalhe='Test details'
        )
    
    def test_get_nonexistent_peca(self):
        """Test GET request for non-existent peca"""
        url = reverse('Pecas-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_peca(self):
        """Test PUT request for non-existent peca"""
        url = reverse('Pecas-detail', kwargs={'pk': 99999})
        data = {
            'codigo': 'TEST001',
            'descricao': 'Test Piece',
            'marca': 'Test Brand',
            'preco_venda': '100.000',
            'preco_exportacao': '90.000',
            'preco_nacional': '110.000',
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
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_peca(self):
        """Test DELETE request for non-existent peca"""
        url = reverse('Pecas-detail', kwargs={'pk': 99999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_peca_invalid_data(self):
        """Test POST request with invalid data"""
        url = reverse('Pecas-list')
        data = {
            'codigo': '',  # Empty required field
            'descricao': 'Test Piece',
            'preco_venda': 'invalid_decimal',  # Invalid decimal
            'ret': 'INVALID',  # Invalid choice
            'cc': 'not_an_integer',  # Invalid integer
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('codigo', response.data)
    
    def test_create_peca_missing_required_fields(self):
        """Test POST request with missing required fields"""
        url = reverse('Pecas-list')
        data = {
            'codigo': 'TEST001'
            # Missing many required fields
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_cliente_invalid_email(self):
        """Test POST request with invalid email"""
        url = reverse('Clientes-list')
        data = {
            'nome_cliente': 'Test Company',
            'cpfcnpj': '12345678901234',
            'endereco': 'Test Address',
            'cep': '12345678',
            'cidade': 'Test City',
            'pais': 'Brazil',
            'telefone': '11999999999',
            'site': 'www.test.com',
            'email': 'invalid-email',  # Invalid email format
            'detalhe': 'Test details'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_create_orcamento_invalid_foreign_key(self):
        """Test POST request with invalid foreign key"""
        url = reverse('Orcamentos-list')
        data = {
            'data_emissao': date.today().isoformat(),
            'data_validade': (date.today() + timedelta(days=30)).isoformat(),
            'tipo_entrega': '4',
            'responsavel': 'Test Manager',
            'frete': '500.000',
            'cliente': 99999,  # Non-existent cliente
            'marcas_embarque': 'Test Marks',
            'nome_entrega': 'Delivery Name',
            'cnpj_entrega': '12345678901234',
            'endereco_entrega': 'Delivery Address',
            'cidade_entrega': 'Delivery City',
            'pais_entrega': 'Brazil',
            'status_oramento': '1'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cliente', response.data)
    
    def test_create_orcamento_invalid_date_format(self):
        """Test POST request with invalid date format"""
        url = reverse('Orcamentos-list')
        data = {
            'data_emissao': 'invalid-date',  # Invalid date format
            'data_validade': (date.today() + timedelta(days=30)).isoformat(),
            'tipo_entrega': '4',
            'responsavel': 'Test Manager',
            'frete': '500.000',
            'cliente': self.cliente.id,
            'marcas_embarque': 'Test Marks',
            'nome_entrega': 'Delivery Name',
            'cnpj_entrega': '12345678901234',
            'endereco_entrega': 'Delivery Address',
            'cidade_entrega': 'Delivery City',
            'pais_entrega': 'Brazil',
            'status_oramento': '1'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_emissao', response.data)
    
    def test_partial_update_with_invalid_data(self):
        """Test PATCH request with invalid data"""
        # First create a valid peca
        peca = Peca.objects.create(
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
        
        url = reverse('Pecas-detail', kwargs={'pk': peca.id})
        data = {
            'preco_venda': 'invalid_decimal',  # Invalid decimal
            'ret': 'INVALID_CHOICE'  # Invalid choice
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_method_not_allowed(self):
        """Test unsupported HTTP method"""
        url = reverse('Pecas-list')
        
        # Try to use PATCH on list endpoint (not allowed)
        response = self.client.patch(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_large_page_size_request(self):
        """Test request with very large page size"""
        # Create multiple pecas
        for i in range(10):
            Peca.objects.create(
                codigo=f'TEST{i:03d}',
                descricao=f'Test Piece {i}',
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
        
        url = reverse('Pecas-list')
        response = self.client.get(url, {'page_size': 10000})  # Very large page size
        
        # Should still return 200 but with limited results due to pagination settings
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_search_parameters(self):
        """Test search with invalid parameters"""
        url = reverse('Pecas-list')
        response = self.client.get(url, {'invalid_param': 'value'})
        
        # Should ignore invalid parameters and return 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_concurrent_update_conflict(self):
        """Test potential race condition in updates"""
        # Create a peca
        peca = Peca.objects.create(
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
        
        url = reverse('Pecas-detail', kwargs={'pk': peca.id})
        
        # Simulate two concurrent updates
        data1 = {'descricao': 'Updated Description 1'}
        data2 = {'descricao': 'Updated Description 2'}
        
        response1 = self.client.patch(url, data1, format='json')
        response2 = self.client.patch(url, data2, format='json')
        
        # Both should succeed (last one wins)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Verify final state
        peca.refresh_from_db()
        self.assertEqual(peca.descricao, 'Updated Description 2')


class RateLimitingTest(TestCase):
    """Test cases for rate limiting (if implemented)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create authentication token
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_anonymous_rate_limiting(self):
        """Test rate limiting for anonymous users"""
        # Remove authentication
        self.client.credentials()
        
        url = reverse('login')
        
        # Make multiple requests rapidly
        responses = []
        for i in range(5):
            response = self.client.post(url, {
                'username': 'testuser',
                'password': 'wrongpassword'
            }, format='json')
            responses.append(response)
        
        # All should be processed (rate limiting may not be strict in tests)
        for response in responses:
            self.assertIn(response.status_code, [
                status.HTTP_401_UNAUTHORIZED,  # Invalid credentials
                status.HTTP_429_TOO_MANY_REQUESTS  # Rate limited
            ])
