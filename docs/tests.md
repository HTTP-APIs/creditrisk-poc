# tests for creditrisk-poc

tests for creditrisk-poc are written with [pytest](https://docs.pytest.org/en/6.2.x/) testing framework.

## tests directory contains folloing files :

```
tests
├── conftest.py
├── __init__.py
├── integration
│   ├── test_agent.py
│   └── test_app.py
└── test_examples
    └── test_ApiDoc.jsonld
```

`integration` contains all the integration tests for creditrisk-poc.

`test_ApiDoc.jsonld` is the ApiDoc used for testing & data generation.

## To run tests enter the following command in the terminal :

```python
pytest tests/
```

## Current status:

All tests are passing successfully with the latest changes.

![Screenshot from 2021-07-12 16-43-15](https://user-images.githubusercontent.com/90337323/156911921-6a1c6ca1-4798-4cad-a2c7-33e0dae79172.png)
