# vocab_generator

`vocab_genrator.py` generates `NonPerformingLoan.jsonld` vocabulary from the owl ontology.

It is located inside the `npl_vocab` directory.
```python
npl_vocab
|
|___ vocab_generator.py
```
vocab_generator uses [rdflib](https://github.com/RDFLib/rdflib-jsonld) and [pyld](https://github.com/digitalbazaar/pyld) libaries to parse & serialize owl ontology 
to jsonld with the `@context.`

To generate JSON-LD voabulary:
```python
python npl_vocab/vocab_generator.py
```
