#!/usr/bin/env python3
"""
Security Test Script for Django API

This script performs basic security checks on the Django configuration
to verify that security fixes have been properly implemented.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment for testing"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
    django.setup()

def test_debug_setting():
    """Test that DEBUG is properly configured"""
    print("🔍 Testing DEBUG setting...")
    debug_value = getattr(settings, 'DEBUG', None)
    
    if debug_value is False:
        print("✅ DEBUG is properly set to False")
        return True
    elif debug_value is True:
        print("⚠️  WARNING: DEBUG is set to True (should be False in production)")
        return False
    else:
        print(f"❌ DEBUG setting is invalid: {debug_value}")
        return False

def test_secret_key():
    """Test that SECRET_KEY is not using default insecure value"""
    print("\n🔍 Testing SECRET_KEY...")
    secret_key = getattr(settings, 'SECRET_KEY', '')
    
    insecure_patterns = [
        'change-me',
        'django-insecure',
        'your-secret-key',
        'secret-key-here'
    ]
    
    if any(pattern in secret_key.lower() for pattern in insecure_patterns):
        print("⚠️  WARNING: SECRET_KEY appears to be using default/insecure value")
        print("   Please generate a new secret key for production")
        return False
    elif len(secret_key) < 50:
        print("⚠️  WARNING: SECRET_KEY is too short (should be at least 50 characters)")
        return False
    else:
        print("✅ SECRET_KEY appears to be properly configured")
        return True

def test_cors_settings():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS settings...")
    cors_allow_all = getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', None)
    cors_allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
    
    if cors_allow_all is True:
        print("❌ CORS_ORIGIN_ALLOW_ALL is set to True (security risk)")
        return False
    elif cors_allow_all is False:
        print("✅ CORS_ORIGIN_ALLOW_ALL is properly set to False")
        if cors_allowed_origins:
            print(f"✅ CORS_ALLOWED_ORIGINS configured with {len(cors_allowed_origins)} origins")
            return True
        else:
            print("⚠️  WARNING: No CORS_ALLOWED_ORIGINS configured")
            return False
    else:
        print("⚠️  WARNING: CORS_ORIGIN_ALLOW_ALL not configured")
        return False

def test_security_headers():
    """Test security headers configuration"""
    print("\n🔍 Testing security headers...")
    security_settings = [
        ('SECURE_BROWSER_XSS_FILTER', True),
        ('SECURE_CONTENT_TYPE_NOSNIFF', True),
        ('X_FRAME_OPTIONS', 'DENY'),
    ]
    
    all_good = True
    for setting_name, expected_value in security_settings:
        actual_value = getattr(settings, setting_name, None)
        if actual_value == expected_value:
            print(f"✅ {setting_name} is properly configured")
        else:
            print(f"❌ {setting_name} is not properly configured (expected: {expected_value}, got: {actual_value})")
            all_good = False
    
    return all_good

def test_database_config():
    """Test database configuration"""
    print("\n🔍 Testing database configuration...")
    databases = getattr(settings, 'DATABASES', {})
    default_db = databases.get('default', {})
    
    # Check if password is from environment variable
    password = default_db.get('PASSWORD', '')
    if 'Shippou.2003' in password:
        print("❌ Database password is hardcoded (security risk)")
        return False
    
    # Check SSL configuration
    options = default_db.get('OPTIONS', {})
    if 'sslmode' in options:
        print("✅ Database SSL configuration found")
        return True
    else:
        print("⚠️  WARNING: Database SSL not configured")
        return False

def test_jwt_config():
    """Test JWT configuration"""
    print("\n🔍 Testing JWT configuration...")
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    
    if not jwt_settings:
        print("❌ SIMPLE_JWT settings not found")
        return False
    
    access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME')
    if access_lifetime:
        # Convert to minutes for comparison
        minutes = access_lifetime.total_seconds() / 60
        if minutes <= 60:  # 1 hour or less
            print(f"✅ JWT access token lifetime is reasonable ({minutes} minutes)")
        else:
            print(f"⚠️  WARNING: JWT access token lifetime is too long ({minutes} minutes)")
            return False
    
    if jwt_settings.get('ROTATE_REFRESH_TOKENS'):
        print("✅ JWT refresh token rotation is enabled")
    else:
        print("⚠️  WARNING: JWT refresh token rotation is not enabled")
        return False
    
    return True

def test_authentication_config():
    """Test REST framework authentication configuration"""
    print("\n🔍 Testing authentication configuration...")
    rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
    
    auth_classes = rest_framework.get('DEFAULT_AUTHENTICATION_CLASSES', [])
    if auth_classes:
        print(f"✅ Authentication classes configured: {len(auth_classes)} classes")
        
        # Check for the typo fix
        if 'DEAFAULT_AUTHENTICATION_CLASSES' in rest_framework:
            print("❌ Found typo: DEAFAULT_AUTHENTICATION_CLASSES (should be DEFAULT)")
            return False
        
        return True
    else:
        print("❌ No default authentication classes configured")
        return False

def run_all_tests():
    """Run all security tests"""
    print("🔒 Django API Security Test Suite")
    print("=" * 50)
    
    try:
        setup_django()
    except Exception as e:
        print(f"❌ Failed to setup Django: {e}")
        return False
    
    tests = [
        test_debug_setting,
        test_secret_key,
        test_cors_settings,
        test_security_headers,
        test_database_config,
        test_jwt_config,
        test_authentication_config,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🔒 Security Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All security tests passed!")
        return True
    else:
        print("⚠️  Some security issues need attention")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
