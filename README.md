# creditrisk-poc

Creditrisk-poc is a Hydra powered API which serves loan portfolio data using EBA NPL Template.

## Features
creditrisk-poc consist following features:
* Loan & Borrower classes.
* Borrower class collection.
* Loan & Borrower class are linked using a foreign key ("CounterpartyId").
* Loan class can perform all the CRUD operations ( GET, PUT, POST, DELETE).
* Borrower can perform all the CRUD operations.
* Borrower class collection can perform all the CRUD operations.

## API_DOC
API_Doc is generated through hydra-python-core module doc_writer.

API_Doc & doc_writer file can be found here :
```
api_doc
|
|___ ApiDoc.jsonld
|___ api_docwriter.py
```
`ApiDoc` is a JSON serialized object, It can be accessed as follows:
```python
import json

ApiDoc_file = open("creditrisk_poc/api_doc/ApiDoc.json","r")
doc = json.load(ApiDoc_file)
```
you will get the doc in `python dict` format.

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
