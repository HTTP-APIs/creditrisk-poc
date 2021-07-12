# tests for creditrisk-poc

tests for creditrisk-poc are written with [pytest](https://docs.pytest.org/en/6.2.x/) testing framework.

## tests directory contains folloing files :
```
tests
|
|__ conftest.py
|__ mock_portfolio_generator.py
|__ test_01_ApiDoc.jsonld
|__ test_functional.py
```

`test_functional.py` contains all the functional tests for creditrisk-poc.

`mock_portfolio_generator.py` is a mock client which can populate the database with realistic portfolio data.

`test_01_ApiDoc.jsonld` is the ApiDoc used for testing & data generation.

## To run tests enter the following command in the terminal :
```python
pytest tests/
```
## Current status:
All tests are passing successfully with the latest changes.

![Screenshot from 2021-07-12 16-43-15](https://user-images.githubusercontent.com/49719371/125278454-648f9980-e330-11eb-911f-26a3d744e830.png)
