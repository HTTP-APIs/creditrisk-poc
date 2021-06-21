"""Creating API Doc for credit-risk POC"""
import json
from hydra_python_core.doc_writer import (HydraDoc, HydraClass,
                                          HydraClassProp, HydraClassOp, HydraStatus, HydraCollection)

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

# Creating Loan class
loan_class_title = "Loan"
loan_class_description = "This class contains the information regarding Loan"
loan_class = HydraClass(loan_class_title, loan_class_description, endpoint=True)
# Adding properties to load class
loan_property1_uri = "NPL:TotalBalance"
loan_property1_title = "TotalBalance"
Total_balance_prop = HydraClassProp(loan_property1_uri, loan_property1_title,
                                    required=True, read=True, write=True)
loan_property2_uri = "NPL:ChannelOfOrigination"
loan_property2_title = "ChannelOfOrigination"
Origination_prop = HydraClassProp(loan_property2_uri, loan_property2_title,
                                  required=True, read=True, write=True)
loan_property3_uri = "https://schema.org/identifier"
loan_property3_title = "CounterpartyId"
CounterpartyId_prop = HydraClassProp(loan_property3_uri, loan_property3_title,
                                     required=True, read=True, write=True)
# Creating borrower class
borrower_class_title = "Borrower"
borrower_class_description = "This class contains the information regarding Loan"
borrower_class = HydraClass(borrower_class_title, borrower_class_description, endpoint=True)
# Adding properties to Borrower class
borrower_property1_uri = "NPL:LegalEntityIdentifier"
borrower_property1_title = "LegalEntityIdentifier"
LegalEntityIdentifier_prop = HydraClassProp(borrower_property1_uri, borrower_property1_title,
                                            required=True, read=True, write=True)
borrower_property2_uri = "NPL:TotalAssets"
borrower_property2_title = "TotalAssets"
TotalAssets_prop = HydraClassProp(borrower_property2_uri, borrower_property2_title,
                                  required=True, read=True, write=True)
borrower_property3_uri = "NPL:DateOfIncorporation"
borrower_property3_title = "DateOfIncorporation"
DateOfIncorporation_prop = HydraClassProp(borrower_property3_uri, borrower_property3_title,
                                          required=True, read=True, write=True)
# Creating Borrower Collection
borrower_collection_name = "Borrowers"
borrower_collection_title = "Borrower class collection"
borrower_collection_description = "Collection for Borrower class"
borrower_collection_managed_by = {
    "property": "rdf:type",
    "object": borrower_class.id_,
}
borrower_collection = HydraCollection(collection_name=borrower_collection_name,
                                      collection_description=borrower_collection_description,
                                      manages=borrower_collection_managed_by,
                                      get=True,
                                      post=True,
                                      put=True,
                                      delete=True)
# Creating Collateral class
collateral_class_title = "Collateral"
collateral_class_description = "This class contains the information regarding Collateral"
collateral_class = HydraClass(collateral_class_title, collateral_class_description, endpoint=True)
# Adding properties to Collateral class
collateral_property1_uri = "NPL:CollateralType"
collateral_property1_title = "CollateralType"
CollateralType_prop = HydraClassProp(collateral_property1_uri, collateral_property1_title,
                                     required=True, read=True, write=True)
collateral_property2_uri = "NPL:LatestValuationAmount"
collateral_property2_title = "LatestValuationAmount"
LatestValuationAmount_prop = HydraClassProp(collateral_property2_uri, collateral_property2_title,
                                            required=True, read=True, write=True)
collateral_property3_uri = "NPL:ConcernLoan"
collateral_property3_title = "ConcernLoan"
ConcernLoan_prop = HydraClassProp(collateral_property3_uri, collateral_property3_title,
                                  required=True, read=True, write=True)

# Loan class operations
update_loan_operation = "UpdateLoan"
update_loan_operation_method = "POST"
update_loan_operation_expects = loan_class.id_
update_loan_operation_returns = None
update_loan_operation_returns_header = ["Content-Type", "Content-Length"]
update_loan_operation_expects_header = []
# status code
update_loan_operation_status = [HydraStatus(code=200, desc="Loan class updated.")]

add_loan_operation = "AddLoan"
add_loan_operation_method = "PUT"
add_loan_operation_expects = loan_class.id_
add_loan_operation_returns = None
add_loan_operation_returns_header = []
add_loan_operation_expects_header = []
# status code
add_loan_operation_status = [HydraStatus(code=200, desc="Loan class updated.")]

get_loan_operation = "GetLoan"
get_loan_operation_method = "GET"
get_loan_operation_expects = None
get_loan_operation_returns = loan_class.id_
get_loan_operation_returns_header = []
get_loan_operation_expects_header = []
# Status code
get_loan_operation_status = [HydraStatus(code=200, desc="Loan class returned.")]

delete_loan_operation = "DeleteLoan"
delete_loan_operation_method = "DELETE"
delete_loan_operation_expects = None
delete_loan_operation_returns = None
delete_loan_operation_returns_header = []
delete_loan_operation_expects_header = []
# Status code
delete_loan_operation_status = [HydraStatus(code=200, desc="Loan class deleted.")]

loan_post = HydraClassOp(update_loan_operation,
                         update_loan_operation_method,
                         update_loan_operation_expects,
                         update_loan_operation_returns,
                         update_loan_operation_expects_header,
                         update_loan_operation_returns_header,
                         update_loan_operation_status)

loan_add = HydraClassOp(add_loan_operation,
                        add_loan_operation_method,
                        add_loan_operation_expects,
                        add_loan_operation_returns,
                        add_loan_operation_expects_header,
                        add_loan_operation_returns_header,
                        add_loan_operation_status)

loan_get = HydraClassOp(get_loan_operation,
                        get_loan_operation_method,
                        get_loan_operation_expects,
                        get_loan_operation_returns,
                        get_loan_operation_expects_header,
                        get_loan_operation_returns_header,
                        get_loan_operation_status)

loan_delete = HydraClassOp(delete_loan_operation,
                           delete_loan_operation_method,
                           delete_loan_operation_expects,
                           delete_loan_operation_returns,
                           delete_loan_operation_expects_header,
                           delete_loan_operation_returns_header,
                           delete_loan_operation_status)
# operations for borrower class
update_borrower_operation = "UpdateBorrower"
update_borrower_operation_method = "POST"
update_borrower_operation_expects = borrower_class.id_
update_borrower_operation_returns = None
update_borrower_operation_returns_header = []
update_borrower_operation_expects_header = []
# status code
update_borrower_operation_status = [HydraStatus(code=200, desc="Borrower class updated.")]

add_borrower_operation = "AddBorrower"
add_borrower_operation_method = "PUT"
add_borrower_operation_expects = borrower_class.id_
add_borrower_operation_returns = None
add_borrower_operation_returns_header = []
add_borrower_operation_expects_header = []
# status code
add_borrower_operation_status = [HydraStatus(code=200, desc="Borrower class updated.")]

get_borrower_operation = "GetBorrower"
get_borrower_operation_method = "GET"
get_borrower_operation_expects = None
get_borrower_operation_returns = borrower_class.id_
get_borrower_operation_returns_header = []
get_borrower_operation_expects_header = []
# Status code
get_borrower_operation_status = [HydraStatus(code=200, desc="Borrower class returned.")]

delete_borrower_operation = "DeleteBorrower"
delete_borrower_operation_method = "DELETE"
delete_borrower_operation_expects = None
delete_borrower_operation_returns = None
delete_borrower_operation_returns_header = []
delete_borrower_operation_expects_header = []
# Status code
delete_borrower_operation_status = [HydraStatus(code=200, desc="Borrower class deleted.")]

borrower_post = HydraClassOp(update_borrower_operation,
                             update_borrower_operation_method,
                             update_borrower_operation_expects,
                             update_borrower_operation_returns,
                             update_borrower_operation_expects_header,
                             update_borrower_operation_returns_header,
                             update_borrower_operation_status)

borrower_add = HydraClassOp(add_borrower_operation,
                            add_borrower_operation_method,
                            add_borrower_operation_expects,
                            add_borrower_operation_returns,
                            add_borrower_operation_expects_header,
                            add_borrower_operation_returns_header,
                            add_borrower_operation_status)

borrower_get = HydraClassOp(get_borrower_operation,
                            get_borrower_operation_method,
                            get_borrower_operation_expects,
                            get_borrower_operation_returns,
                            get_borrower_operation_expects_header,
                            get_borrower_operation_returns_header,
                            get_borrower_operation_status)

borrower_delete = HydraClassOp(delete_borrower_operation,
                               delete_borrower_operation_method,
                               delete_borrower_operation_expects,
                               delete_borrower_operation_returns,
                               delete_borrower_operation_expects_header,
                               delete_borrower_operation_returns_header,
                               delete_borrower_operation_status)
# operations for Collateral class
update_collateral_operation = "UpdateCollateral"
update_collateral_operation_method = "POST"
update_collateral_operation_expects = collateral_class.id_
update_collateral_operation_returns = None
update_collateral_operation_returns_header = []
update_collateral_operation_expects_header = []
# status code
update_collateral_operation_status = [HydraStatus(code=200, desc="Collateral class updated.")]

add_collateral_operation = "AddCollateral"
add_collateral_operation_method = "PUT"
add_collateral_operation_expects = collateral_class.id_
add_collateral_operation_returns = None
add_collateral_operation_returns_header = []
add_collateral_operation_expects_header = []
# status code
add_collateral_operation_status = [HydraStatus(code=200, desc="Collateral class updated.")]

get_collateral_operation = "GetCollateral"
get_collateral_operation_method = "GET"
get_collateral_operation_expects = None
get_collateral_operation_returns = collateral_class.id_
get_collateral_operation_returns_header = []
get_collateral_operation_expects_header = []
# Status code
get_collateral_operation_status = [HydraStatus(code=200, desc="Collateral class returned.")]

delete_collateral_operation = "DeleteCollateral"
delete_collateral_operation_method = "DELETE"
delete_collateral_operation_expects = None
delete_collateral_operation_returns = None
delete_collateral_operation_returns_header = []
delete_collateral_operation_expects_header = []
# Status code
delete_collateral_operation_status = [HydraStatus(code=200, desc="Collateral class deleted.")]

collateral_post = HydraClassOp(update_collateral_operation,
                               update_collateral_operation_method,
                               update_collateral_operation_expects,
                               update_collateral_operation_returns,
                               update_collateral_operation_expects_header,
                               update_collateral_operation_returns_header,
                               update_collateral_operation_status)

collateral_add = HydraClassOp(add_collateral_operation,
                              add_collateral_operation_method,
                              add_collateral_operation_expects,
                              add_collateral_operation_returns,
                              add_collateral_operation_expects_header,
                              add_collateral_operation_returns_header,
                              add_collateral_operation_status)

collateral_get = HydraClassOp(get_collateral_operation,
                              get_collateral_operation_method,
                              get_collateral_operation_expects,
                              get_collateral_operation_returns,
                              get_collateral_operation_expects_header,
                              get_collateral_operation_returns_header,
                              get_collateral_operation_status)

collateral_delete = HydraClassOp(delete_collateral_operation,
                                 delete_collateral_operation_method,
                                 delete_collateral_operation_expects,
                                 delete_collateral_operation_returns,
                                 delete_collateral_operation_expects_header,
                                 delete_collateral_operation_returns_header,
                                 add_collateral_operation_status)

# adding property & operation to Loan classes
loan_class.add_supported_prop(Total_balance_prop)
loan_class.add_supported_prop(Origination_prop)
loan_class.add_supported_prop(CounterpartyId_prop)
loan_class.add_supported_op(loan_get)
loan_class.add_supported_op(loan_post)
loan_class.add_supported_op(loan_add)
loan_class.add_supported_op(loan_delete)

# adding property & operation to Borrower classes
borrower_class.add_supported_prop(LegalEntityIdentifier_prop)
borrower_class.add_supported_prop(TotalAssets_prop)
borrower_class.add_supported_prop(DateOfIncorporation_prop)
borrower_class.add_supported_op(borrower_get)
borrower_class.add_supported_op(borrower_post)
borrower_class.add_supported_op(borrower_add)
borrower_class.add_supported_op(borrower_delete)

# adding borrower collection
api_doc.add_supported_collection(borrower_collection)

# adding property & operation to Collateral class
collateral_class.add_supported_prop(CollateralType_prop)
collateral_class.add_supported_prop(LatestValuationAmount_prop)
collateral_class.add_supported_prop(ConcernLoan_prop)
collateral_class.add_supported_op(collateral_get)
collateral_class.add_supported_op(collateral_add)
collateral_class.add_supported_op(collateral_post)
collateral_class.add_supported_op(collateral_delete)

# adding classes to api_doc
api_doc.add_supported_class(loan_class)
api_doc.add_supported_class(borrower_class)
api_doc.add_supported_class(collateral_class)

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
    except Exception as error:
        print(error, "Occurred while saving API_Doc")
