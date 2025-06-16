#!/usr/bin/env python
"""
Simple test runner script for Django API
Usage: python run_tests.py [options]
"""

import os
import sys
import subprocess
import argparse


def run_command(command, description=""):
    """Run a shell command and return the result"""
    if description:
        print(f"\n🔄 {description}")
    
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Failed")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
    
    return result.returncode == 0


def run_all_tests():
    """Run all tests"""
    return run_command(
        "python manage.py test tests --verbosity=2",
        "Running all unit tests"
    )


def run_models_tests():
    """Run model tests only"""
    return run_command(
        "python manage.py test tests.test_models --verbosity=2",
        "Running model tests"
    )


def run_api_tests():
    """Run API tests only"""
    return run_command(
        "python manage.py test tests.test_api --verbosity=2",
        "Running API tests"
    )


def run_auth_tests():
    """Run authentication tests only"""
    return run_command(
        "python manage.py test tests.test_authentication --verbosity=2",
        "Running authentication tests"
    )


def run_error_tests():
    """Run error handling tests only"""
    return run_command(
        "python manage.py test tests.test_error_handling --verbosity=2",
        "Running error handling tests"
    )


def run_coverage_tests():
    """Run tests with coverage report"""
    print("\n🔄 Running tests with coverage analysis")
    
    # Install coverage if not available
    subprocess.run("pip install coverage", shell=True, capture_output=True)
    
    commands = [
        "coverage erase",
        "coverage run --source='.' manage.py test tests",
        "coverage report -m",
        "coverage html"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    print("\n📊 Coverage report generated in 'htmlcov' directory")
    return True


def run_specific_test(test_path):
    """Run a specific test"""
    return run_command(
        f"python manage.py test {test_path} --verbosity=2",
        f"Running specific test: {test_path}"
    )


def check_test_setup():
    """Check if test environment is properly set up"""
    print("\n🔍 Checking test environment setup")
    
    # Check if Django is available
    try:
        import django
        print(f"✅ Django {django.get_version()} is available")
    except ImportError:
        print("❌ Django is not installed")
        return False
    
    # Check if required packages are available
    required_packages = ['rest_framework', 'loja']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is not available")
            return False
    
    # Check if test database can be created
    result = run_command(
        "python manage.py check",
        "Checking Django configuration"
    )
    
    return result


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Django API Test Runner')
    parser.add_argument(
        'test_type',
        nargs='?',
        choices=['all', 'models', 'api', 'auth', 'errors', 'coverage', 'check'],
        default='all',
        help='Type of tests to run (default: all)'
    )
    parser.add_argument(
        '--specific',
        help='Run a specific test (e.g., tests.test_models.PecaModelTest)'
    )
    parser.add_argument(
        '--setup-check',
        action='store_true',
        help='Check if test environment is properly set up'
    )
    
    args = parser.parse_args()
    
    print("🧪 Django API Test Runner")
    print("=" * 50)
    
    # Check setup if requested
    if args.setup_check:
        success = check_test_setup()
        sys.exit(0 if success else 1)
    
    # Run specific test if provided
    if args.specific:
        success = run_specific_test(args.specific)
        sys.exit(0 if success else 1)
    
    # Run tests based on type
    success = False
    
    if args.test_type == 'all':
        success = run_all_tests()
    elif args.test_type == 'models':
        success = run_models_tests()
    elif args.test_type == 'api':
        success = run_api_tests()
    elif args.test_type == 'auth':
        success = run_auth_tests()
    elif args.test_type == 'errors':
        success = run_error_tests()
    elif args.test_type == 'coverage':
        success = run_coverage_tests()
    elif args.test_type == 'check':
        success = check_test_setup()
    
    # Print summary
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        print("\n📋 Test Summary:")
        print("✅ All test cases passed")
        print("✅ No errors detected")
        if args.test_type == 'coverage':
            print("✅ Coverage report generated")
    else:
        print("💥 Some tests failed!")
        print("\n📋 Test Summary:")
        print("❌ One or more test cases failed")
        print("❌ Please review the output above")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
