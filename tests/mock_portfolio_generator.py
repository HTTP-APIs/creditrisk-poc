"""
Generates the mock portfolio data with all the FR key relations to the database.
"""
from conftest import gen_dummy_object
import json
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import HydraDoc
import requests
import os
from os.path import join, dirname


def get_api_doc(apidoc_file_path: str = "ApiDoc.jsonld") -> HydraDoc:
    """
    Returns HydraDoc object from API Documentation
    """
    path = join(dirname(__file__), apidoc_file_path)
    doc_file = open(path, "r")
    API_NAME = os.environ["API_NAME"] if "API_NAME" in dict(os.environ).keys() else "creditrisk_api"
    apidoc = json.load(doc_file)
    apidoc = doc_maker.create_doc(apidoc, "http://localhost:8080/", API_NAME)
    return apidoc


def generate_borrowers(apidoc: HydraDoc):
    """
    Generates 100 Borrowers with no loans & no collateral
    """
    for borrower in range(1000):
        dummy_object = gen_dummy_object("Borrower", apidoc)
        put_request = requests.put("http://localhost:8080/creditrisk_api/Borrower/", json=dummy_object)


def generate_private_borrowers(apidoc: HydraDoc):
    """
    Generates 100 Borrowers with no loans & no collateral
    """
    for borrower in range(1000):
        dummy_object = gen_dummy_object("PrivateBorrower", apidoc)
        put_request = requests.put("http://localhost:8080/creditrisk_api/PrivateBorrower/", json=dummy_object)
        print(put_request.text)


def generate_residential_mortgage(apidoc: HydraDoc):
    """
    Generate 1000 Borrowers with loan & no collateral
    """
    for mortgage in range(100):
        # Creating ResidentialMortgage Object
        mortgage_dummy_object = gen_dummy_object("ResidentialMortgage", apidoc)
        put_request = requests.put("http://localhost:8080/creditrisk_api/ResidentialMortgage/", json=mortgage_dummy_object)

def generate_collateral(apidoc: HydraDoc):
    """
    Generate 1000 collateral objects
    """
    for collateral in range(100):
        # Creating ResidentialMortgage Object
        mortgage_dummy_object = gen_dummy_object("Collateral", apidoc)
        put_request = requests.put("http://localhost:8080/creditrisk_api/Collateral/", json=mortgage_dummy_object)



if __name__ == "__main__":
    doc = get_api_doc()
    generate_borrowers(doc)
    generate_private_borrowers(doc)
    generate_residential_mortgage(doc)
    generate_collateral(doc)
