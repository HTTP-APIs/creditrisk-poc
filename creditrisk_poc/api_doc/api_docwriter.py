"""Creating API Doc for credit-risk POC"""
import json
from hydra_python_core.doc_writer import (HydraDoc, HydraClass,
                                          HydraClassProp, HydraClassOp, HydraStatus, HydraCollection)
import logging
import nplvocab_parser as parser

logging.basicConfig(filename="docwriter_log.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

API_NAME = "creditrisk_api"
BASE_URL = "http://localhost:8080/"

# Creating APIDoc Object
api_doc = HydraDoc(API_NAME,
                   "Hdyra powered Credit-risk api",
                   "This API is a POC for creditrisk management",
                   API_NAME,
                   BASE_URL,
                   "vocab")

# Adding NPL jsonld vocabulary to api_doc context
api_doc.add_to_context("NPL",
                       "https://raw.githubusercontent.com/Purvanshsingh/creditrisk-poc/main/NonPerformingLoan.jsonld#")

npl_vocab = parser.get_npl_vocab()
classes = parser.get_all_classes(npl_vocab)
hydra_classes = parser.create_hydra_classes(classes)
classes = {class_.title: class_ for class_ in hydra_classes}

loan_foriegnkey_uri = classes['GeneralCounterparty'].id_
loan_foriegnkey_title = "CounterpartyId"
CounterpartyId_prop = HydraClassProp(loan_foriegnkey_uri, loan_foriegnkey_title,
                                     required=True, read=True, write=True)
classes['Loan'].add_supported_prop(CounterpartyId_prop)

Loan_operations = parser.add_operations_to_class(hydra_classes, "Loan", ["GET", "PUT", "POST", "DELETE"])
Counterparty_operations = parser.add_operations_to_class(hydra_classes, "Counterparty",
                                                         ["GET", "PUT", "POST", "DELETE"])
Collateral_operations = parser.add_operations_to_class(hydra_classes, "Collateral", ["GET", "PUT", "POST", "DELETE"])

for class_ in hydra_classes:
    class_name = class_.title
    class_properties = parser.get_class_properties(class_name, npl_vocab)
    for property_ in class_properties:
        prop = parser.create_hydra_properties(property_, classes)
        class_.add_supported_prop(prop)
    try:
        class_operations = eval(class_name + "_operations")
    except NameError:
        class_operations = None
    if class_operations:
        for operation in class_operations:
            class_.add_supported_op(operation)
    api_doc.add_supported_class(class_)




# Creating Borrower Collection
counterparty_collection_name = "CounterParty_collection"
counterparty_collection_title = "CounterParty class collection"
counterparty_collection_description = "Collection for Borrower class"
counterparty_collection_managed_by = {
    "property": "rdf:type",
    "object": parser.get_class_id("GeneralCounterparty", hydra_classes),
}
counterparty_collection = HydraCollection(collection_name=counterparty_collection_name,
                                          collection_description=counterparty_collection_description,
                                          manages=counterparty_collection_managed_by,
                                          get=True,
                                          post=True,
                                          put=True,
                                          delete=True)
api_doc.add_supported_collection(counterparty_collection)

api_doc.add_baseResource()
api_doc.add_baseCollection()
# creating Entrypoint
api_doc.gen_EntryPoint()
# generating api_doc
doc = api_doc.generate()

# saving the api_doc
if __name__ == "__main__":
    try:
        # Serialized Json object
        json_doc = json.dumps(doc, indent=4, sort_keys=True)
        # saving to json file
        with open("ApiDoc.jsonld", "w") as doc_file:
            doc_file.write(json_doc)
            print("Your API_Doc has be successfully created.")
            logger.info("Your API_Doc has be successfully created.")
    except Exception as error:
        logger.debug(error, "Occurred while saving API_Doc")
