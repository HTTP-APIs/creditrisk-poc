import json
from os.path import abspath, dirname
from hydra_python_core.doc_writer import HydraClass, HydraClassProp, HydraClassOp, HydraStatus
from pathlib import Path


def get_npl_vocab() -> dict:
    cwd_path = Path(dirname(dirname(abspath(__file__))))
    vocab_file_path = cwd_path / "npl_vocab" / "NonPerformingLoan.jsonld"
    npl_vocab_file = open(vocab_file_path)
    npl_vocab = json.load(npl_vocab_file)
    return npl_vocab


def get_all_classes(vocab: dict) -> list:
    """
    Get all the classes from the given Vocabulary.
    """
    classes = list()
    defines = vocab['@graph']
    for obj in defines:
        if obj['@type'] == 'owl:Class':
            classes.append(obj)
    return classes


def create_hydra_classes(vocab_classes: list) -> list:
    """
    Create hydra classes from list of vocab classes.
    """
    hydra_classes = list()
    for class_ in vocab_classes:
        class_name = (class_['rdfs:comment'].split('Class')[0]).replace(" ", "")
        if "class" in class_name:
            class_name = (class_['rdfs:comment'].split('class')[0]).replace(" ", "")
        hydra_class = HydraClass(class_name, class_['rdfs:comment'], endpoint=True)
        hydra_classes.append(hydra_class)
    return hydra_classes


def get_class_properties(class_name: str, vocab: dict) -> list:
    """
    Return all the properties of the given class.
    """
    properties = list()
    defines = vocab['@graph']
    for obj in defines:
        if obj.get('propertyOf'):
            propertyof = obj['propertyOf'].split('#')[1]
            if propertyof == class_name or obj['@type'] == 'owl:DataProperty' and obj['@type'] == 'owl:ObjectProperty':
                properties.append(obj)
    return properties


def create_hydra_properties(property_: dict, hydra_classes: dict) -> HydraClassProp:
    if property_['@type'] == 'owl:DatatypeProperty':
        try:
            prop_range = "xsd:" + property_['propertyOn'].split('#')[1]
        except Exception:
            prop_range = "xsd:" + property_['propertyOn']
        hydra_property = HydraClassProp(property_['@id'], property_['rdfs:label'], range=prop_range,
                                        required=True, read=True, write=True)
    elif 'owl:ObjectProperty' in property_['@type']:
        property_on_class = property_.get("propertyOn").split('#')[1]
        property_uri = hydra_classes[property_on_class].id_
        property_name = property_['@id'].split('#')[1]
        hydra_property = HydraClassProp(property_uri, property_name,
                                        required=True, read=True, write=True)

    return hydra_property


def get_class_id(class_name: str, hydra_classes: list):
    """
    Returns the class id of given class.
    """
    for class_ in hydra_classes:
        if class_.title == class_name:
            return class_.id_


def add_operations_to_class(hydra_classes: list, class_name: str, operations: list) -> list:
    """
    Return list of hydra properties of given class.
    """
    hydra_operations = []
    class_id = get_class_id(class_name, hydra_classes)
    if class_id:
        for operation in operations:
            if operation == "GET":
                get_operation_status = [HydraStatus(code=200, desc=class_name + " class returned.")]
                op = HydraClassOp(class_name + operation, operation, None, class_id, [], [], get_operation_status)
                hydra_operations.append(op)
            if operation == "PUT":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class Added.")]
                op = HydraClassOp(class_name + operation, operation, class_id, None, [], [], put_operation_status)
                hydra_operations.append(op)
            if operation == "POST":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class updated.")]
                op = HydraClassOp(class_name + operation, operation, class_id, None, [],
                                  ["Content-Type", "Content-Length"],
                                  put_operation_status)
                hydra_operations.append(op)
            if operation == "DELETE":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class Deleted.")]
                op = HydraClassOp(class_name + operation, operation, None, None, [], [],
                                  put_operation_status)
                hydra_operations.append(op)
    return hydra_operations
