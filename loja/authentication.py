import os
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get token from Authorization header (Bearer token)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            # Fallback to cookie-based token
            token = request.COOKIES.get('auth_token')
        else:
            token = auth_header.split(' ')[1]

        if not token:
            return None  # Let other authentication methods handle it

        try:
            # SECURITY FIX: Use environment variable for JWT secret
            secret_key = os.getenv('JWT_SECRET_KEY', settings.SECRET_KEY)
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')
        except Exception:
            raise AuthenticationFailed('Erro na autenticação')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Usuário não encontrado')

        return (user, token)
