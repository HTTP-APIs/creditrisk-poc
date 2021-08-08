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
    return apidoc, API_NAME


def generate_borrowers(apidoc: HydraDoc, API_NAME: str):
    """
    Generates 100 Borrowers with no loans & no collateral
    """
    for borrower in range(1000):
        dummy_object = gen_dummy_object("Borrower", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/Borrower/".format(api_name=API_NAME), json=dummy_object)


def generate_private_borrowers(apidoc: HydraDoc, API_NAME: str):
    """
    Generates 100 Borrowers with no loans & no collateral
    """
    for borrower in range(1000):
        dummy_object = gen_dummy_object("PrivateBorrower", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/PrivateBorrower/".format(api_name=API_NAME),
                                   json=dummy_object)


def generate_residential_mortgage(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 Borrowers with loan & no collateral
    """
    for mortgage in range(100):
        # Creating ResidentialMortgage Object
        mortgage_dummy_object = gen_dummy_object("ResidentialMortgage", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/ResidentialMortgage/".format(api_name=API_NAME),
                                   json=mortgage_dummy_object)

def generate_collateral(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 collateral objects
    """
    for collateral in range(100):
        # Creating ResidentialMortgage Object
        mortgage_dummy_object = gen_dummy_object("Collateral", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/Collateral/".format(api_name=API_NAME),
                                   json=mortgage_dummy_object)



if __name__ == "__main__":
    doc, api_name = get_api_doc()
    generate_borrowers(doc, api_name)
    generate_private_borrowers(doc, api_name)
    generate_residential_mortgage(doc, api_name)
    generate_collateral(doc, api_name)
