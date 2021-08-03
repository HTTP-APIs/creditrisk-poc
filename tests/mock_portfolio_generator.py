"""
Generates the mock portfolio data with all the FR key relations to the database.
"""
from conftest import gen_dummy_object
import json
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import HydraDoc
import requests
import ast


def get_api_doc(apidoc_file_path: str = "ApiDoc.jsonld") -> HydraDoc:
    """
    Returns HydraDoc object from API Documentation
    """
    doc_file = open(apidoc_file_path, "r")
    apidoc = json.load(doc_file)
    apidoc = doc_maker.create_doc(apidoc, "http://localhost:8080/", "creditrisk_api")
    return apidoc


def borrowers_with_no_loan(apidoc: HydraDoc):
    """
    Generates 100 Borrowers with no loans & no collateral
    """
    for borrower in range(1000):
        dummy_object = gen_dummy_object("Borrower", apidoc)
        put_request = requests.put("http://localhost:8080/creditrisk_api/Borrower/", json=dummy_object)


def borrower_with_loan(apidoc: HydraDoc):
    """
    Generate 1000 Borrowers with loan & no collateral
    """
    for borrower in range(100):
        # Creating Counterparty Object
        borrower_dummy_object = gen_dummy_object("Borrower", apidoc)
        # Loan object using Borrower foreign key
        loan_dummy_object = gen_dummy_object("Loan", apidoc)
        loan_dummy_object['has_borrower'] = borrower_dummy_object
        put_request = requests.put("http://localhost:8080/creditrisk_api/Loan/", json=loan_dummy_object)



if __name__ == "__main__":
    doc = get_api_doc()
    borrowers_with_no_loan(doc)
    borrower_with_loan(doc)