# Django API Unit Tests

This directory contains comprehensive unit tests for the Django API, covering all main functions with GET, PUT, DELETE, and POST operations.

## Test Structure

```
tests/
├── __init__.py                 # Package initialization
├── test_models.py             # Model tests (creation, validation, methods)
├── test_api.py                # API endpoint tests (CRUD operations)
├── test_authentication.py     # Authentication and authorization tests
├── test_error_handling.py     # Error handling and edge cases
├── test_runner.py             # Test runner utilities
└── README.md                  # This documentation
```

## Test Coverage

### Models Tested
- **Peca** - Product/part model with all fields and properties
- **Cliente** - Customer model with validation
- **Usuario** - User model with business logic
- **Fornecedor** - Supplier model
- **Orcamento** - Quote/budget model with relationships
- **Pedido** - Order model with complex relationships

### API Endpoints Tested
- **GET** operations (list and detail views)
- **POST** operations (create new resources)
- **PUT** operations (full updates)
- **PATCH** operations (partial updates)
- **DELETE** operations (resource deletion)

### Authentication Tests
- Login endpoint with valid/invalid credentials
- Signup endpoint with validation
- Token authentication
- Permission checks
- User type detection (cliente vs usuario)

### Error Handling Tests
- 404 errors for non-existent resources
- 400 errors for invalid data
- 401 errors for unauthorized access
- 405 errors for unsupported methods
- Validation errors
- Foreign key constraint errors

## Running Tests

### Prerequisites

1. **Install test dependencies**:
   ```bash
   pip install coverage
   ```

2. **Set up test database**:
   The tests use Django's test database which is created automatically.

### Basic Test Execution

1. **Run all tests**:
   ```bash
   python manage.py test tests
   ```

2. **Run specific test module**:
   ```bash
   python manage.py test tests.test_models
   python manage.py test tests.test_api
   python manage.py test tests.test_authentication
   ```

3. **Run specific test class**:
   ```bash
   python manage.py test tests.test_api.PecasAPITest
   python manage.py test tests.test_models.PecaModelTest
   ```

4. **Run specific test method**:
   ```bash
   python manage.py test tests.test_api.PecasAPITest.test_get_pecas_list
   ```

### Using the Test Runner

The custom test runner provides additional functionality:

1. **Run all tests**:
   ```bash
   python tests/test_runner.py all
   ```

2. **Run tests with coverage report**:
   ```bash
   python tests/test_runner.py coverage
   ```

3. **Run performance tests**:
   ```bash
   python tests/test_runner.py performance
   ```

4. **Run specific test module**:
   ```bash
   python tests/test_runner.py tests.test_models
   ```

### Verbose Output

For detailed test output:
```bash
python manage.py test tests --verbosity=2
```

## Test Data

### Test Database
- Tests use a separate test database
- Database is created and destroyed for each test run
- No impact on development or production data

### Test Fixtures
- Tests create their own test data in `setUp()` methods
- Data is isolated between test methods
- Automatic cleanup after each test

### Authentication
- Test users are created automatically
- Authentication tokens are generated for API tests
- Different permission levels are tested

## Test Examples

### Model Tests
```python
def test_create_peca(self):
    """Test creating a new Peca"""
    peca = Peca.objects.create(**self.peca_data)
    self.assertEqual(peca.codigo, 'TEST001')
    self.assertTrue(peca.id)
```

### API Tests
```python
def test_get_pecas_list(self):
    """Test GET /pecas/ - List all pecas"""
    url = reverse('Pecas-list')
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 1)
```

### Authentication Tests
```python
def test_login_success(self):
    """Test successful login"""
    url = reverse('login')
    data = {'username': 'testuser', 'password': 'testpass123'}
    
    response = self.client.post(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('token', response.data)
```

## Coverage Report

After running tests with coverage:

1. **Console report** shows coverage percentages
2. **HTML report** is generated in `htmlcov/` directory
3. **Coverage data** is saved in `.coverage` file

### Viewing HTML Coverage Report
```bash
# After running: python tests/test_runner.py coverage
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Best Practices

### Writing New Tests

1. **Follow naming conventions**:
   - Test files: `test_*.py`
   - Test classes: `*Test`
   - Test methods: `test_*`

2. **Use descriptive test names**:
   ```python
   def test_create_peca_with_valid_data(self):
   def test_get_nonexistent_peca_returns_404(self):
   ```

3. **Structure tests with AAA pattern**:
   - **Arrange**: Set up test data
   - **Act**: Execute the operation
   - **Assert**: Verify the results

4. **Use setUp() for common test data**:
   ```python
   def setUp(self):
       self.user = User.objects.create_user(...)
       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   ```

### Test Data Management

1. **Create minimal test data**
2. **Use factories for complex objects**
3. **Clean up in tearDown() if needed**
4. **Avoid dependencies between tests**

### API Testing

1. **Test all HTTP methods** (GET, POST, PUT, PATCH, DELETE)
2. **Test both success and error cases**
3. **Verify response status codes**
4. **Check response data structure**
5. **Test authentication and permissions**

## Continuous Integration

### GitHub Actions Example
```yaml
name: Django Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test tests
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure Django settings are properly configured
2. **Database errors**: Check test database permissions
3. **Authentication errors**: Verify token creation in setUp()
4. **Timeout errors**: Increase test timeout for slow operations

### Debug Mode

Run tests with debug output:
```bash
python manage.py test tests --debug-mode --verbosity=2
```

### Test Database Issues

If test database creation fails:
```bash
python manage.py migrate --run-syncdb
python manage.py test tests --keepdb
```

## Performance Considerations

- Tests should run quickly (< 1 second per test)
- Use `setUpClass()` for expensive setup operations
- Mock external services and APIs
- Use database transactions for faster cleanup

## Security Testing

The test suite includes security-focused tests:
- Authentication bypass attempts
- Authorization checks
- Input validation
- SQL injection prevention
- XSS protection

## Maintenance

### Regular Tasks

1. **Update tests** when adding new features
2. **Review coverage reports** to identify gaps
3. **Refactor tests** to reduce duplication
4. **Update test data** when models change
5. **Monitor test performance** and optimize slow tests

### Test Review Checklist

- [ ] All CRUD operations tested
- [ ] Authentication and permissions tested
- [ ] Error cases covered
- [ ] Edge cases identified and tested
- [ ] Performance acceptable
- [ ] Coverage targets met
