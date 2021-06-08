"""Generated API Documentation sample using doc_writer_sample.py."""
    
doc = {
    "@context": {
        "ApiDocumentation": "hydra:ApiDocumentation",
        "NPL": "https://raw.githubusercontent.com/Purvanshsingh/creditrisk-poc/main/NonPerformingLoan.json",
        "description": "hydra:description",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "entrypoint": {
            "@id": "hydra:entrypoint",
            "@type": "@id"
        },
        "expects": {
            "@id": "hydra:expects",
            "@type": "@id"
        },
        "expectsHeader": "hydra:expectsHeader",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "label": "rdfs:label",
        "manages": "hydra:manages",
        "method": "hydra:method",
        "object": {
            "@id": "hydra:object",
            "@type": "@id"
        },
        "possibleStatus": "hydra:possibleStatus",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "range": {
            "@id": "rdfs:range",
            "@type": "@id"
        },
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "readable": "hydra:readable",
        "required": "hydra:required",
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "returnsHeader": "hydra:returnsHeader",
        "search": "hydra:search",
        "statusCode": "hydra:statusCode",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "subject": {
            "@id": "hydra:subject",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "writeable": "hydra:writeable"
    },
    "@id": "http://localhost:8080/creditrisk_api/vocab",
    "@type": "ApiDocumentation",
    "description": "This API is a POC for creditrisk management",
    "entrypoint": "http://localhost:8080/creditrisk_api",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "http://localhost:8080/creditrisk_api/vocab?resource=Loan",
            "@type": "hydra:Class",
            "description": "This class contains the information regarding Loan",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://localhost:8080/creditrisk_api/vocab?resource=Loan",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://raw.githubusercontent.com/HydraCG/Specifications/master/spec/latest/core/core.jsonld",
                            "@type": "Status",
                            "description": "Loan class updated.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "UpdateLoan"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "@context": "https://raw.githubusercontent.com/HydraCG/Specifications/master/spec/latest/core/core.jsonld",
                            "@type": "Status",
                            "description": "Movie class returned.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/creditrisk_api/vocab?resource=Loan",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "GetLoan"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://localhost:8080/creditrisk_api/vocab?resource=Loan",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://raw.githubusercontent.com/HydraCG/Specifications/master/spec/latest/core/core.jsonld",
                            "@type": "Status",
                            "description": "Loan class updated.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "AddLoan"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "NPL:TotalBalance",
                    "readable": "true",
                    "required": "true",
                    "title": "TotalBalance",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "NPL:ChannelOfOrigination",
                    "readable": "true",
                    "required": "true",
                    "title": "ChannelOfOrigination",
                    "writeable": "true"
                }
            ],
            "title": "Loan"
        },
        {
            "@id": "http://localhost:8080/creditrisk_api/vocab?resource=Borrower",
            "@type": "hydra:Class",
            "description": "This class contains the information regarding Loan",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "NPL:LegalEntityIdentifier",
                    "readable": "true",
                    "required": "true",
                    "title": "LegalEntityIdentifier",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "NPL:TotalAssets",
                    "readable": "true",
                    "required": "true",
                    "title": "TotalAssets",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "NPL:DateOfIncorporation",
                    "readable": "true",
                    "required": "true",
                    "title": "DateOfIncorporation",
                    "writeable": "true"
                }
            ],
            "title": "Borrower"
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "Resource"
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Collection",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "null",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "Collection"
        },
        {
            "@id": "http://localhost:8080/creditrisk_api#EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "http://localhost:8080//creditrisk_api#EntryPoint",
                    "description": "The APIs main entry point.",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "null",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [],
            "title": "EntryPoint"
        }
    ],
    "title": "Hdyra powered Credit-risk api"
}
