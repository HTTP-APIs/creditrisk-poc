"""Creating API Doc for credit-risk POC"""
from hydra_python_core.doc_writer import (HydraDoc, HydraClass,
                                          HydraClassProp, HydraClassOp, HydraStatus)

API_NAME = "creditrisk_api"
BASE_URL = "http://localhost:8080/"

# Creating APIDoc Object
api_doc = HydraDoc(API_NAME,
                   "Hdyra powered Credit-risk api",
                   "This API is a POC for creditrisk management",
                   API_NAME,
                   BASE_URL,
                   "vocab")

# Adding NPL jsonld vocabulary to API_Doc context
api_doc.add_to_context("NPL",
                       "https://raw.githubusercontent.com/Purvanshsingh/creditrisk-poc/main/NonPerformingLoan.jsonld#")

# Creating Loan & Borrower classes
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
# Adding borrower class
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
get_loan_operation_returns_header = ["Content-Type", "Content-Length"]
get_loan_operation_expects_header = []
# Status code
get_loan_operation_status = [HydraStatus(code=200, desc="Loan class returned.")]

post = HydraClassOp(update_loan_operation,
                    update_loan_operation_method,
                    update_loan_operation_expects,
                    update_loan_operation_returns,
                    update_loan_operation_expects_header,
                    update_loan_operation_returns_header,
                    update_loan_operation_status)

add = HydraClassOp(add_loan_operation,
                   add_loan_operation_method,
                   add_loan_operation_expects,
                   add_loan_operation_returns,
                   add_loan_operation_expects_header,
                   add_loan_operation_returns_header,
                   add_loan_operation_status)

get = HydraClassOp(get_loan_operation,
                   get_loan_operation_method,
                   get_loan_operation_expects,
                   get_loan_operation_returns,
                   get_loan_operation_expects_header,
                   get_loan_operation_returns_header,
                   get_loan_operation_status)

# adding property & operation to Loan classes
loan_class.add_supported_prop(Total_balance_prop)
loan_class.add_supported_prop(Origination_prop)
loan_class.add_supported_op(post)
loan_class.add_supported_op(get)
loan_class.add_supported_op(add)
borrower_class.add_supported_prop(LegalEntityIdentifier_prop)
borrower_class.add_supported_prop(TotalAssets_prop)
borrower_class.add_supported_prop(DateOfIncorporation_prop)

api_doc.add_supported_class(loan_class)
api_doc.add_supported_class(borrower_class)

api_doc.add_baseResource()
api_doc.add_baseCollection()
# creating Entrypoint
api_doc.gen_EntryPoint()
# generating API_Doc
doc = api_doc.generate()

# saving the API_Doc
if __name__ == "__main__":
    """Print the complete sample Doc in api_doc_output.py."""
    import json
    dump = json.dumps(doc, indent=4, sort_keys=True)
    doc = '''"""Generated API Documentation sample using doc_writer_sample.py."""
    \ndoc = {}\n'''.format(dump)
    # Python does not recognise null, true and false in JSON format, convert
    # them to string
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    with open("creditrisk_api_doc.py", "w") as f:
        f.write(doc)