# Petstore API Autotests

Automated API tests for Petstore service (https://petstore.swagger.io)

## Tech Stack
- Python 3.8+
- Pytest
- Requests
- Pydantic
- Allure Reporting

## Project Structure
```
petstore-api-tests/
├── tests/          # Test cases
├── src/            # Source code
│   ├── api/        # API client
│   └── models/     # Data models
└── config/         # Configuration
```

## Installation
```bash
pip install -r requirements.txt
```

## Running Tests
```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=report.html

# Run with Allure
pytest --alluredir=allure-results
allure serve allure-results
