# creditrisk-poc

Creditrisk-poc is a Hydra powered API which serves loan portfolio data using EBA NPL Template.

## Features
creditrisk-poc consist following features:
* Loan ,Borrower & Collateral classes.
* Borrower class collection.
* Loan, Borrower & Collateral classes are linked using `foreign keys`.
* Loan class can perform all the CRUD operations ( GET, PUT, POST, DELETE).
* Borrower can perform all the CRUD operations.
* Borrower class collection can perform all the CRUD operations.

## Classes are linked in the following manner:

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
```
NonPerformingLoan.owl --> ( vocab_generator.py ) NonPerformingLoan.jsonld --> ( nplvocab_parser.py) ApiDoc.jsonld 
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
python main.py
```
The hydrus should be up & running on `http://localhost:8080/creditrisk_api/`
