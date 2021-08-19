# creditrisk-poc

Creditrisk-poc is a Hydra powered API which serves loan portfolio data using EBA NPL Template.

<div  align="center">
  
  ![Creditrisk-poc](https://user-images.githubusercontent.com/49719371/130111451-5c06ce06-012e-44df-986c-b736bb21b191.png)
  </div>

## Working Project
API is live @ **http://34.145.188.116:8080/**



## Features
creditrisk-poc consist following features:
* ResidentialMortgage, PrivateBorrower, Collateral, Portfolio & manymore classes.
* Portfolio class collection.
* classes are linked with each other using `foreign keys`.
* All the classes can perform all the CRUD operations ( GET, PUT, POST, DELETE).
* Portfolio class collection can perform all the CRUD operations.

## Classes are linked in the following manner:
[Here's](https://drive.google.com/file/d/1HWd72JVtf13P7DdTF3Er2870FVx7c9BM/view) the Database schema for the classes.

## NonPerformingLoan.jsonld
The `NonPerformingLoan.jsonld` is a subset vocabulary for NonPerformingLoan portfolios,
vocabulary is generated automatically using `vocab_generator.py` from `NonperformingLoan.owl` ontology.
```bash
python npl_vocab/vocab_generator.py
```
It will generate the JSON-LD vocabulary which can be used to create ApiDoc.

## API_DOC
API_Doc is generated through hydra-python-core module `doc_writer` and `nplvoac_parse.py` which automates the creation
of classes and properties from JSON-LD vocabulary.

API_Doc, doc_writer & `nplvocab_parser.py` files can be found here :
```
api_doc
|
|___ ApiDoc.jsonld
|___ api_docwriter.py
|___ nplvocab_parser.py
```
**nplvocab_parser** parse all the classes & properties from `NonPerformingLoan.jsonld` and provide functions for converting
them to HydraClass & HydraClassProp.

`ApiDoc` is a JSON serialized object, It can be accessed as follows:
```python
import json

ApiDoc_file = open("creditrisk_poc/api_doc/ApiDoc.json","r")
doc = json.load(ApiDoc_file)
```
you will get the doc in `python dict` format.

### ApiDoc is generated with this flow:
![Automation_structure](https://user-images.githubusercontent.com/49719371/130113828-f4241ac7-08fb-4a14-aa64-a2c85b549d37.png)

## Repository Structure
```python
creditrisk_poc
|
|____api_doc
|    |
|    |_____api_docwriter.py
|    |_____ApiDoc.jsonld
|    |_____nplvocab_generator.py
|
|____npl_vocab
|    |
|    |____NonPerformingLoan.jsonld
|    |____NonPerformingLoan.owl
|    |____nplo.jsonld
|    |____vocab_generator.py
|
|____"__main.py__"
```


## Demo
To run hydra powered creditrisk-poc API, just do the following:
1) Clone creditrisk-poc
```bash
git clone https://github.com/HTTP-APIs/creditrisk-poc.git
cd creditrisk-poc
```
2. Install a [*Python virtual environment*](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) using:
```bash
python3.7 -m venv .venv
```
or:
```bash
virtualenv -p python3.7 .venv
```

3. Install requirements:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
3) Run hydrus server 
```bash
cd creditrisk_poc
python __main__.py
```
The hydrus should be up & running on `http://localhost:8080/creditrisk_api/`

### API can be tested using Mock_portfolio_generator
```bash
cd tests
python mock_portfolio_generator.py
```
> Mock_portfolio_generator is a mock client which can populate the database with the more realistic data, It automatically creates the object of the classes on the basis of ApiDocumentation. 
