"""
Test runner script for Django API tests
Provides utilities for running tests and generating reports
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line


def setup_django():
    """Setup Django environment for testing"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
    django.setup()


def run_all_tests():
    """Run all tests in the tests package"""
    setup_django()
    
    # Use Django's test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run tests
    failures = test_runner.run_tests(['tests'])
    
    if failures:
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


def run_specific_test(test_path):
    """Run a specific test or test module"""
    setup_django()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    failures = test_runner.run_tests([test_path])
    
    if failures:
        sys.exit(1)
    else:
        print(f"Test {test_path} passed!")
        sys.exit(0)


def run_tests_with_coverage():
    """Run tests with coverage report"""
    try:
        import coverage
    except ImportError:
        print("Coverage package not installed. Install with: pip install coverage")
        sys.exit(1)
    
    # Start coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Setup Django
    setup_django()
    
    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory='htmlcov')
    print("HTML coverage report generated in 'htmlcov' directory")
    
    if failures:
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


def run_performance_tests():
    """Run performance-focused tests"""
    setup_django()
    
    # Run only tests that measure performance
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # You can add specific performance test patterns here
    failures = test_runner.run_tests(['tests.test_api'])
    
    if failures:
        sys.exit(1)
    else:
        print("Performance tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'all':
            run_all_tests()
        elif command == 'coverage':
            run_tests_with_coverage()
        elif command == 'performance':
            run_performance_tests()
        elif command.startswith('tests.'):
            run_specific_test(command)
        else:
            print("Usage:")
            print("  python test_runner.py all                    # Run all tests")
            print("  python test_runner.py coverage               # Run tests with coverage")
            print("  python test_runner.py performance            # Run performance tests")
            print("  python test_runner.py tests.test_models      # Run specific test module")
            print("  python test_runner.py tests.test_api.PecasAPITest  # Run specific test class")
    else:
        run_all_tests()
