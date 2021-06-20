import pytest
import random
import string
import json
import uuid
import os
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import DocUrl, HydraLink
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from hydrus.app_factory import app_factory
from hydrus.data import crud, doc_parse
from hydrus.data.db_models import Base, create_database_tables
from hydrus.utils import set_api_name, set_doc, set_page_size, set_session, get_api_name, get_session
from hydrus.extensions.socketio_factory import create_socket

def get_doc_classes_and_properties(doc):
    """
    Extract classes and properties from a given HydraDoc object
    :param doc: HydraDoc object whose classes and properties have to extracted
    :type doc: HydraDoc
    :return: classes and properties in the HydraDoc object in a tuple
    :rtype: tuple(list, set)
    """
    test_classes = doc_parse.get_classes(doc)
    test_properties = doc_parse.get_all_properties(test_classes)
    return test_classes, test_properties


def gen_dummy_object(class_title, doc):
    """
    Create a dummy object based on the definitions in the API Doc.
    :param class_title: Title of the class whose object is being created.
    :param doc: ApiDoc.
    :return: A dummy object of class `class_title`.
    """
    object_ = {
        "@type": class_title
    }
    expanded_base_url = DocUrl.doc_url
    for class_path in doc.collections:
        if class_title == doc.collections[class_path]["collection"].name:
            members = list()
            manages_class_titles = list()
            collection_manages = doc.collections[class_title]["collection"].manages
            if type(collection_manages) is dict:
                # only one manages block
                manages_class = collection_manages['object'].split(expanded_base_url)[1]
                manages_class_titles.append(manages_class)
            elif type(collection_manages) is list:
                # multiple manages block
                for manages_block in collection_manages:
                    manages_class = collection_manages['object'].split(expanded_base_url)[1]
                    manages_class_titles.append(manages_class)
            for _ in range(3):
                member_class = random.choice(manages_class_titles)
                member = gen_dummy_object(member_class, doc)
                member_id = crud.insert(object_=member,
                                        session=get_session(),
                                        collection=False)
                from hydrus.data.helpers import get_path_from_type
                member_class_path = get_path_from_type(member_class)
                member_api_path = f'/{get_api_name()}/{member_class_path}/{member_id}'
                members.append({
                    "@id": member_api_path,
                    "@type": member_class,
                })
            object_['members'] = members
            return object_
    for class_path in doc.parsed_classes:
        if class_title == doc.parsed_classes[class_path]["class"].title:
            for prop in doc.parsed_classes[class_path]["class"].supportedProperty:
                if prop.write is False:
                    continue
                if isinstance(prop.prop, HydraLink):
                    object_[prop.title] = ''.join(random.choice(
                        string.ascii_uppercase + string.digits) for _ in range(6))
                    pass
                elif expanded_base_url in prop.prop:
                    prop_class = prop.prop.split(expanded_base_url)[1]
                    object_[prop.title] = gen_dummy_object(prop_class, doc)
                else:
                    object_[prop.title] = ''.join(random.choice(
                        string.ascii_uppercase + string.digits) for _ in range(6))
            return object_

@pytest.fixture(scope='module')
def constants():
    """
    Constant values to be used in all tests
    """
    return {
        'API_NAME': 'creditrisk_api',
        'HYDRUS_SERVER_URL': "http://localhost:8080/",
        'PAGE_SIZE': 1
    }


@pytest.fixture(scope='module', name='doc')
def test_doc(constants):
    """
    Generate a test HydraDoc object from a Api Documentation
    """
    HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
    API_NAME = constants['API_NAME']
    API_DOC_PATH = os.path.relpath("tests/ApiDoc.jsonld")
    print(API_DOC_PATH)
    doc_file = open(API_DOC_PATH, "r")
    doc = json.load(doc_file)

    doc = doc_maker.create_doc(doc,
                               HYDRUS_SERVER_URL,
                               API_NAME)
    return doc


@pytest.fixture(scope='module')
def session(engine):
    """
    Initialize a flask scoped session binded with a database
    """
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()


@pytest.fixture(scope='module')
def engine():
    """
    Initialize a sqlalchemy engine binded with a database
    """
    DB_URL = 'sqlite:///:memory:'
    engine = create_engine(DB_URL)
    return engine


@pytest.fixture(scope='module')
def app(constants):
    """
    Get a test flask app for testing in test
    """
    API_NAME = constants['API_NAME']
    app = app_factory(API_NAME)
    return app


@pytest.fixture(scope='module', name='test_app_client')
def test_client(app, session, constants, doc):
    API_NAME = constants['API_NAME']
    PAGE_SIZE = constants['PAGE_SIZE']
    with set_api_name(app, API_NAME):
        with set_session(app, session):
            with set_doc(app, doc):
                with set_page_size(app, PAGE_SIZE):
                    testing_client = app.test_client()
                    # Establish an application context before running the tests.
                    ctx = app.app_context()
                    ctx.push()
                    yield testing_client
                    ctx.pop()


@pytest.fixture()
def init_db_for_functionality_tests(doc, constants, session, add_doc_classes_and_properties_to_db):
    """
    Initalze the database for testing app in
    tests/functional/test_app.py.
    """
    for class_ in doc.parsed_classes:
        class_title = doc.parsed_classes[class_]['class'].title
        dummy_obj = gen_dummy_object(class_title, doc)
        crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)
        # If it's a collection class then add an extra object so
        # we can test pagination thoroughly.
        if class_ in doc.collections:
            crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)


@pytest.fixture(scope='module')
def add_doc_classes_and_properties_to_db(doc, session, engine):
    """
    Add the doc classes and properties to database
    for testing in /functional/test_app.py and
    /functional/test_socket.py
    """
    test_classes, test_properties = get_doc_classes_and_properties(doc)
    # temporarily add manages block explicitly to collection-classes
    # until appropriate changes take place in hydra-python-core library
    manages = {
        "object": "vocab:dummyClass",
        "property": "rdf:type"
    }
    for class_ in test_classes:
        if "Collection" in class_['@id']:
            class_['manages'] = manages

    try:
        create_database_tables(test_classes)
    except Exception:
        # catch error when the tables have been already defined.
        # happens when /test_socket.py is run after /test_app.py
        # in the same session
        # in that case, no need to create the tables again on the
        # same sqlalchemy.ext.declarative.declarative_base instance
        pass
    Base.metadata.create_all(engine)


@pytest.fixture(scope='module')
def socketio(app, session):
    socket = create_socket(app, session)
    return socket


@pytest.fixture(scope='module')
def socketio_client(app, session, constants, doc, socketio):
    API_NAME = constants['API_NAME']
    PAGE_SIZE = constants['PAGE_SIZE']
    with set_api_name(app, API_NAME):
        with set_session(app, session):
            with set_doc(app, doc):
                with set_page_size(app, PAGE_SIZE):
                    socketio_client = socketio.test_client(app, namespace='/sync')
                    return socketio_client