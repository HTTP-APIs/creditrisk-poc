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


def generate_propertycollateral(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 collateral objects
    """
    for collateral in range(100):
        # Creating ResidentialMortgage Object
        collateral_dummy_object = gen_dummy_object("PropertyCollateral", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/PropertyCollateral/".format(api_name=API_NAME),
                                   json=collateral_dummy_object)


def generate_forbearance(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 collateral objects
    """
    for forbearance in range(100):
        # Creating ResidentialMortgage Object
        forbearance_dummy_object = gen_dummy_object("Forbearance", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/Forbearance/".format(api_name=API_NAME),
                                   json=forbearance_dummy_object)


def generate_externalcollection(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 collateral objects
    """
    for externalcollection in range(100):
        # Creating ResidentialMortgage Object
        externalcollection_dummy_object = gen_dummy_object("ExternalCollection", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/ExternalCollection/".format(api_name=API_NAME),
                                   json=externalcollection_dummy_object)


def generate_enforcement(apidoc: HydraDoc, API_NAME: str):
    """
    Generate 1000 collateral objects
    """
    for enforcement in range(100):
        # Creating ResidentialMortgage Object
        enforcement_dummy_object = gen_dummy_object("Enforcement", apidoc)
        put_request = requests.put("http://localhost:8080/{api_name}/Enforcement/".format(api_name=API_NAME),
                                   json=enforcement_dummy_object)
        print(put_request.text)


if __name__ == "__main__":
    doc, api_name = get_api_doc()
    generate_private_borrowers(doc, api_name)
    generate_residential_mortgage(doc, api_name)
    generate_propertycollateral(doc, api_name)
    generate_forbearance(doc, api_name)
    generate_externalcollection(doc, api_name)
    generate_enforcement(doc, api_name)
