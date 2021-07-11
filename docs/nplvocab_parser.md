# nplvocab_parser

`nplvocab_parser` parses all the classes & properties from `NonPerformingLoan.jsonld` and convert them to HydraClass & HydraClassProp.

nplvocab_parser is located in `api_doc` directory
```python
api_doc
|
|___ nplvocab_parser.py
```
It can be used by importing as a python module:
```python
import NPLVocab_parse as parser

npl_vocab = parser.get_npl_vocab()
classes = parser.get_all_classes(npl_vocab)
hydra_classes = parser.create_hydra_classes(classes)
```
nplvocab_parser provide following functions:
* `get_all_classes()` -> Return all the classes from the given Vocabulary.
* `create_hydra_classes()` -> Return list of HydraClass objects.
* `get_class_properties()` -> Return all the properties of the given class.
* `create_hydra_properties()` -> Return list of HydraclasProps from the list of properties.
* `get_class_id()` -> Returns the class id of given class.
* `add_operations_to_class()` -> Return list of hydra properties of given class.


 
