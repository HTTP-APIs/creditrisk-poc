"""
This file performs all the functionality test for the creditrisk-poc API.
All the CRUD operation with Classes & Collection can be tested by running
pytest tests/test_functional.py
"""

import pytest
import json
import re
import uuid
from tests.conftest import gen_dummy_object


@pytest.mark.usefixtures('init_db_for_functionality_tests')
class TestApp:
    def test_root_url(self, test_app_client, constants):
        """Test for the Index."""
        HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
        API_NAME = constants['API_NAME']
        response_get = test_app_client.get(f'/{API_NAME}')
        endpoints = json.loads(response_get.data.decode('utf-8'))
        response_post = test_app_client.post(f'/{API_NAME}', data=dict(foo='bar'))
        response_put = test_app_client.put(f'/{API_NAME}', data=dict(foo='bar'))
        response_delete = test_app_client.delete(f'/{API_NAME}')
        assert '@context' in endpoints
        assert endpoints['@id'] == f'{HYDRUS_SERVER_URL}{API_NAME}'
        assert endpoints['@type'] == 'EntryPoint'
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_put.status_code == 405
        assert response_delete.status_code == 405

    def test_Collections_GET(self, test_app_client, constants, doc, init_db_for_functionality_tests):
        """Test GET on collection endpoints."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            response_get = test_app_client.get(endpoint['@id'])
            assert response_get.status_code == 200
            response_get_data = json.loads(response_get.data.decode('utf-8'))
            assert '@context' in response_get_data
            assert '@id' in response_get_data
            assert '@type' in response_get_data
            assert 'members' in response_get_data
            # Check the item URI has the valid format, so it can be dereferenced
            if len(response_get_data['members']) > 0:
                for item in response_get_data['members']:
                    class_type = item['@type']
                    if class_type in doc.parsed_classes:
                        class_ = doc.parsed_classes[class_type]['class']
                        class_methods = [
                            x.method for x in class_.supportedOperation]
                        if 'GET' in class_methods:
                            item_response = test_app_client.get(
                                response_get_data['members'][0]['@id'])
                            assert item_response.status_code == 200

    def test_Collections_PUT(self, test_app_client, constants, doc):
        """Test insert data to the collection."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                assert good_response_put.json["iri"] == good_response_put.location

    def test_collection_object_GET(self, test_app_client, constants, doc):
        """Test GET of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                initial_put_response = test_app_client.put(
                    endpoint['@id'], data=json.dumps(dummy_object))
                assert initial_put_response.status_code == 201
                response = json.loads(initial_put_response.data.decode('utf-8'))
                regex = r'(.*)ID (.{36})* (.*)'
                matchObj = re.match(regex, response['description'])
                assert matchObj is not None
                id_ = matchObj.group(2)
                if 'GET' in collection_methods:
                    get_response = test_app_client.get(f'{endpoint["@id"]}/{id_}')
                    assert get_response.status_code == 200

    def test_collection_object_PUT(self, test_app_client, constants, doc):
        """Test PUT of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object_1 = gen_dummy_object(collection.name, doc)
                initial_put_response = test_app_client.put(
                    endpoint['@id'], data=json.dumps(dummy_object_1))
                assert initial_put_response.status_code == 201
                collection_id = initial_put_response.location
                dummy_object_2 = gen_dummy_object(collection.name, doc)
                second_put_response = test_app_client.put(
                    collection_id, data=json.dumps(dummy_object_2))
                assert second_put_response.status_code == 201
                assert second_put_response.location == collection_id
                assert second_put_response.json["iri"] == collection_id

    def test_collection_object_POST(self, test_app_client, constants, doc, socketio):
        """Test POST of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            initial_put_response = test_app_client.put(
                endpoint['@id'], data=json.dumps(dummy_object))
            assert initial_put_response.status_code == 201
            assert initial_put_response.json["iri"] == initial_put_response.location
            response = json.loads(initial_put_response.data.decode('utf-8'))
            regex = r'(.*)ID (.{36})* (.*)'
            matchObj = re.match(regex, response['description'])
            assert matchObj is not None
            id_ = matchObj.group(2)
            if 'POST' in collection_methods:
                # members attribute should be writeable for POSTs
                if collection.supportedProperty[0].write:
                    dummy_object = gen_dummy_object(collection.name, doc)
                    post_replace_response = test_app_client.post(f'{endpoint["@id"]}/{id_}',
                                                                 data=json.dumps(dummy_object))
                    assert post_replace_response.status_code == 200

    def test_collection_object_DELETE(self, test_app_client, constants, doc):
        """Test DELETE of a given collection object using ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(
                endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [
                x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            initial_put_response = test_app_client.put(endpoint["@id"],
                                                       data=json.dumps(dummy_object))
            assert initial_put_response.status_code == 201
            response = json.loads(initial_put_response.data.decode('utf-8'))
            regex = r'(.*)ID (.{36})* (.*)'
            matchObj = re.match(regex, response['description'])
            assert matchObj is not None
            id_ = matchObj.group(2)
            if 'DELETE' in collection_methods:
                delete_response = test_app_client.delete(
                    f'{endpoint["@id"]}/{id_}')
                assert delete_response.status_code == 200

    def test_object_PUT_at_id(self, test_app_client, constants, doc):
        """Create object in collection using PUT at specific ID."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(
                endpoint["@id"].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [
                x.method for x in collection.supportedOperation]
            dummy_object = gen_dummy_object(collection.name, doc)
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                put_response = test_app_client.put(f'{endpoint["@id"]}/{uuid.uuid4()}',
                                                   data=json.dumps(dummy_object))
                assert put_response.status_code == 201
                assert put_response.json["iri"] == put_response.location

    def test_object_PUT_at_ids(self, test_app_client, constants, doc):
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    data_ = {'data': list()}
                    objects = list()
                    ids = ''
                    for index in range(3):
                        objects.append(gen_dummy_object(class_.title, doc))
                        ids = f'{uuid.uuid4()},'
                    data_['data'] = objects
                    if 'PUT' in class_methods:
                        put_response = test_app_client.put(f'{endpoints[endpoint]}/add/{ids}',
                                                           data=json.dumps(data_))
                        assert put_response.status_code == 201
                        assert isinstance(put_response.json['iri'], list)

    def test_endpointClass_PUT(self, test_app_client, constants, doc):
        """Check non collection Class PUT."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        dummy_object = gen_dummy_object(class_.title, doc)
                        put_response = test_app_client.put(endpoints[endpoint],
                                                           data=json.dumps(dummy_object))
                        assert put_response.status_code == 201
                        assert put_response.json["iri"] == put_response.location

    def test_endpointClass_POST(self, test_app_client, constants, doc):
        """Check non collection Class POST."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        # first insert a object which we will update later
                        dummy_object = gen_dummy_object(class_.title, doc)
                        initial_put_response = test_app_client.put(endpoints[endpoint],
                                                                   data=json.dumps(dummy_object))
                        response = json.loads(
                            initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        id_ = matchObj.group(2)
                        if 'POST' in class_methods:
                            dummy_object = gen_dummy_object(class_.title, doc)
                            post_response = test_app_client.post(f'{endpoints[endpoint]}/{id_}',
                                                                 data=json.dumps(dummy_object))
                            assert post_response.status_code == 200

    def test_endpointClass_DELETE(self, test_app_client, constants, doc):
        """Check non collection Class DELETE."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(
                    endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'PUT' in class_methods:
                        # first insert a object which we will update later
                        dummy_object = gen_dummy_object(class_.title, doc)
                        initial_put_response = test_app_client.put(endpoints[endpoint],
                                                                   data=json.dumps(dummy_object))
                        response = json.loads(
                            initial_put_response.data.decode('utf-8'))
                        regex = r'(.*)ID (.{36})* (.*)'
                        matchObj = re.match(regex, response['description'])
                        id_ = matchObj.group(2)
                        if 'DELETE' in class_methods:
                            delete_response = test_app_client.delete(
                                f'{endpoints[endpoint]}/{id_}')
                            assert delete_response.status_code == 200

    def test_endpointClass_GET(self, test_app_client, constants, doc):
        """Check non collection Class GET."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ['@context', '@id', '@type', 'collections']:
                class_name = '/'.join(endpoints[endpoint].split(f'/{API_NAME}/')[1:])
                if class_name not in doc.collections:
                    class_ = doc.parsed_classes[class_name]['class']
                    class_methods = [x.method for x in class_.supportedOperation]
                    if 'GET' in class_methods:
                        response_get = test_app_client.get(endpoints[endpoint])
                        assert response_get.status_code == 405

    def test_Collections_member_GET(self, test_app_client, constants, doc):
        """Test endpoint to get member from a collection"""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                collection_endpoint = good_response_put.location
                if 'GET' in collection_methods:
                    for member in dummy_object['members']:
                        member_id = member['@id'].split('/')[-1]
                        get_response = test_app_client.get(f'{collection_endpoint}/{member_id}')
                        assert get_response.status_code == 200

    def test_Collections_member_DELETE(self, test_app_client, constants, doc):
        """Test endpoint to delete member from a collection."""
        API_NAME = constants['API_NAME']
        index = test_app_client.get(f'/{API_NAME}')
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints['collections']:
            collection_name = '/'.join(endpoint['@id'].split(f'/{API_NAME}/')[1:])
            collection = doc.collections[collection_name]['collection']
            collection_methods = [x.method for x in collection.supportedOperation]
            if 'PUT' in collection_methods:
                dummy_object = gen_dummy_object(collection.name, doc)
                good_response_put = test_app_client.put(endpoint['@id'],
                                                        data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201
                collection_endpoint = good_response_put.location
                if 'DELETE' in collection_methods:
                    for member in dummy_object['members']:
                        member_id = member['@id'].split('/')[-1]
                        full_endpoint = f'{collection_endpoint}/{member_id}'
                        delete_response = test_app_client.delete(full_endpoint)
                        assert delete_response.status_code == 200

