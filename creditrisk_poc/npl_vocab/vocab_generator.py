"""
This script will generate the NonPerformingLoan.jsonld from the owl ontology.
"""
import json
import rdflib
from os.path import abspath, dirname
from pathlib import Path


def context() -> dict:
    """
    Returns @context of the jsonld.
    :return:
    """
    context = {
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
        "xsd": "https://www.w3.org/TR/xmlschema-2/#",
        "defines": {
            "@reverse": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
        },
        "propertyOf": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "propertyOn": {
            "@id": "rdfs:range",
            "@type": "@id"
        }
    }
    return context


def generate_jsonld(file_path: str, export_file_name: str):
    """
    Returns jsonld converted vocabulary from the owl ontology.
    """
    ontology = rdflib.Graph()
    # loading ontology in XML format
    ontology.parse(file_path)
    # Converting to jsonld using Context function
    npl_jsonld = ontology.serialize(format='json-ld', context=context(), indent=4)
    # converting binary string to json object
    npl_jsonld = json.loads(npl_jsonld)
    # Writing json sting to file
    export_file = open(export_file_name, "w")
    npl_jsonld = json.dumps(npl_jsonld, indent=4)
    export_file.write(npl_jsonld)


if __name__ == '__main__':
    ontology_file = "NonPerformingLoan.owl"
    export_file = "NonPerformingLoan.jsonld"
    cwd_path = Path(dirname(dirname(abspath(__file__))))
    ontology_file_path = cwd_path / "npl_vocab" / ontology_file
    export_file_path = cwd_path / "npl_vocab" / export_file
    generate_jsonld(str(ontology_file_path), str(export_file_path))
