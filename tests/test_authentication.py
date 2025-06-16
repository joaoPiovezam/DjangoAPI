"""
Unit tests for authentication endpoints
Tests login, signup, and token validation
"""

import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from loja.models import Usuario


class AuthenticationAPITest(TestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create corresponding Usuario
        self.usuario = Usuario.objects.create(
            nome='Test User',
            empresa='Test Company',
            email='test@example.com',
            cpfcnpj='12345678901',
            endereco='Test Address',
            cep='12345678',
            cidade='Test City',
            pais='Brazil',
            telefone='11999999999'
        )
    
    def test_login_success(self):
        """Test successful login"""
        url = reverse('login')  # Assuming you have a named URL for login
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertIn('tipo', response.data)
        self.assertEqual(response.data['tipo'], 'usuario')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_login_missing_username(self):
        """Test login with missing username"""
        url = reverse('login')
        data = {
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_login_missing_password(self):
        """Test login with missing password"""
        url = reverse('login')
        data = {
            'username': 'testuser'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_login_inactive_user(self):
        """Test login with inactive user"""
        # Deactivate user
        self.user.is_active = False
        self.user.save()
        
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_signup_success(self):
        """Test successful user signup"""
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_signup_missing_fields(self):
        """Test signup with missing required fields"""
        url = reverse('signup')
        data = {
            'username': 'newuser'
            # Missing email and password
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_signup_duplicate_username(self):
        """Test signup with existing username"""
        url = reverse('signup')
        data = {
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_signup_duplicate_email(self):
        """Test signup with existing email"""
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'test@example.com',  # Already exists
            'password': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_test_token_authenticated(self):
        """Test token validation with valid token"""
        # Create token for user
        token = Token.objects.create(user=self.user)
        
        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('authenticated', response.data)
        self.assertTrue(response.data['authenticated'])
    
    def test_test_token_unauthenticated(self):
        """Test token validation without authentication"""
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_test_token_invalid_token(self):
        """Test token validation with invalid token"""
        # Set invalid authentication header
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_cliente_type(self):
        """Test login returns 'cliente' type when no Usuario exists"""
        # Create user without corresponding Usuario
        user_without_usuario = User.objects.create_user(
            username='clienteuser',
            email='cliente@example.com',
            password='clientepass123'
        )
        
        url = reverse('login')
        data = {
            'username': 'clienteuser',
            'password': 'clientepass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], 'cliente')
    
    def test_login_usuario_type(self):
        """Test login returns 'usuario' type when Usuario exists"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], 'usuario')


class TokenAuthenticationTest(TestCase):
    """Test cases for token-based authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='tokenuser',
            email='token@example.com',
            password='tokenpass123'
        )
        
        # Create token
        self.token = Token.objects.create(user=self.user)
    
    def test_valid_token_authentication(self):
        """Test API access with valid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Try to access a protected endpoint
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_token_authentication(self):
        """Test API access with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_token_authentication(self):
        """Test API access without token"""
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_malformed_token_header(self):
        """Test API access with malformed token header"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)  # Wrong format
        
        url = reverse('test_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
