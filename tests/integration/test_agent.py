import pytest
from hydra_agent.agent import Agent
from hydra_agent.helpers import expand_template
from urllib.parse import urlparse


@pytest.mark.usefixtures("setup_agent_for_tests")
class TestAgent:
    """TestCase for Agent Class"""

    @pytest.fixture(autouse=True)
    def init_agent(self, constants):
        """Setting up Agent object"""

        def init_agent_():
            try:
                print(constants["ENTRYPOINT_URL"])
                self.agent = Agent(constants["ENTRYPOINT_URL"])
            except (SyntaxError, ConnectionResetError) as e:
                init_agent_()

        init_agent_()

    def test_get_url(self, get_session_mock, portfolio_object):
        """Tests get method from the Agent with URL"""
        get_session_mock.return_value.status_code = 200
        get_session_mock.return_value.json.return_value = portfolio_object
        response = self.agent.get(self.entrypoint_url + "/Borrower/1")
        assert response == portfolio_object


    def test_get_collection(
        self, get_session_mock, put_session_mock, borrower_object, simplified_collection
    ):
        """Tests get method from the Agent when fetching collections"""

        collection_url = self.entrypoint_url + "/Borrower_collection/"
        new_collection_url = collection_url + "1"

        put_session_mock.return_value.status_code = 201
        put_session_mock.return_value.json.return_value = borrower_object
        put_session_mock.return_value.headers = {"Location": new_collection_url}

        get_session_mock.return_value.json.return_value = simplified_collection
        get_session_mock.return_value.status_code = 200
        response, new_object_url = self.agent.put(collection_url, borrower_object)
        get_collection_url = self.agent.get(collection_url)
        assert type(get_collection_url) == dict
        # get_collection_cached = self.agent.get(resource_type="Borrower",
        #                                     cached_limit=0)
        # self.assertEqual(get_collection_cached[-1]["@id"],
        #                 get_collection_url['members'][-1]["@id"])

    def test_put(
        self,
        mocker,
        get_session_mock,
        put_session_mock,
        new_object,
        portfolio_object,
        borrower_res,
    ):
        """Tests put method from the Agent"""

        class_url = self.entrypoint_url + "/Borrower/"
        new_object_url = class_url + "1"

        put_session_mock.return_value.status_code = 201
        put_session_mock.return_value.json.return_value = new_object
        put_session_mock.return_value.headers = {"Location": new_object_url}

        fake_responses = [mocker.Mock(), mocker.Mock(), mocker.Mock(), mocker.Mock()]
        fake_responses[0].json.return_value = borrower_res
        fake_responses[0].status_code = 200
        fake_responses[1].json.return_value = borrower_res
        fake_responses[1].status_code = 200
        fake_responses[2].json.return_value = borrower_res
        fake_responses[2].status_code = 200
        fake_responses[3].json.return_value = portfolio_object
        fake_responses[3].status_code = 200
        # Mocking an object to be used for a property that has an embedded link
        get_session_mock.return_value.status_code = 200
        get_session_mock.side_effect = fake_responses
        response, new_object_url = self.agent.put(new_object_url, new_object)

        # Assert if object was inserted queried and inserted successfully
        get_new_object_url = self.agent.get(new_object_url)
        assert get_new_object_url == borrower_res

        get_new_object_type = self.agent.get(
            new_object_url, filters={"has_cutoff_date": "2020-03-20T14:28:23.382748"}
        )
        assert get_new_object_url == get_new_object_type

    def test_post(
        self,
        put_session_mock,
        post_session_mock,
        get_session_mock,
        new_object,
        portfolio_object,
        borrower_res,
        mocker,
    ):
        """Tests post method from the Agent"""
        class_url = self.entrypoint_url + "/Borrower/"
        new_object_url = class_url + "2"

        put_session_mock.return_value.status_code = 201
        put_session_mock.return_value.json.return_value = new_object
        put_session_mock.return_value.headers = {"Location": new_object_url}

        fake_responses = [mocker.Mock(), mocker.Mock()]
        fake_responses[0].json.return_value = borrower_res
        fake_responses[0].status_code = 200
        fake_responses[1].json.return_value = portfolio_object
        fake_responses[1].status_code = 200
        # Mocking an object to be used for a property that has an embedded link
        get_session_mock.return_value.status_code = 200
        get_session_mock.side_effect = fake_responses

        response, new_object_url = self.agent.put(new_object_url, new_object)

        post_session_mock.return_value.status_code = 200
        post_session_mock.return_value.json.return_value = {"msg": "success"}
        new_object["borrower_is_part_of_portfolio"][
            "@id"
        ] = f"/{self.entrypoint_url}/Portfolio/1"
        new_object["has_cutoff_date"] = "2022-06-20T14:28:23.382748"
        # Mocking an object to be used for a property that has an embedded link
        response = self.agent.post(new_object_url, new_object)
        # Assert if object was updated successfully as intended
        fake_responses[1].json.return_value = new_object
        fake_responses[1].status_code = 200
        get_new_object = self.agent.get(new_object_url)

        assert get_new_object == new_object

    def test_delete(
        self,
        put_session_mock,
        delete_session_mock,
        get_session_mock,
        mocker,
        new_object,
        borrower_res,
    ):
        """Tests post method from the Agent"""

        class_url = self.entrypoint_url + "/Borrower/"
        new_object_url = class_url + "3"

        put_session_mock.return_value.status_code = 201
        put_session_mock.return_value.json.return_value = new_object
        put_session_mock.return_value.headers = {"Location": new_object_url}
        fake_responses = [mocker.Mock(), mocker.Mock()]
        fake_responses[0].json.return_value = borrower_res
        fake_responses[0].status_code = 200
        fake_responses[1].text = {"msg": "resource doesn't exist"}
        # Mocking an object to be used for a property that has an embedded link
        get_session_mock.return_value.status_code = 200
        get_session_mock.side_effect = fake_responses

        response, new_object_url = self.agent.put(new_object_url, new_object)

        delete_session_mock.return_value.status_code = 200
        delete_session_mock.return_value.json.return_value = {"msg": "success"}
        response = self.agent.delete(new_object_url)
        get_new_object = self.agent.get(new_object_url)

        # Assert if nothing different was returned by Redis
        assert get_new_object == {"msg": "resource doesn't exist"}

    def test_basic_iri_templates(self, simplified_collection):
        """Tests the URI constructed on the basis of Basic Representation"""
        sample_mapping_object = {
            "borrower_is_part_of_portfolio[has_cutoff_date]": "2020-03-20T14:28:23.382748",
            "pageIndex": "1",
            "limit": "10",
            "offset": "1",
        }
        url = urlparse(
            expand_template(
                "http://localhost:8080/serverapi/BorrowerCollection",
                simplified_collection,
                sample_mapping_object,
            )
        )
        url_should_be = urlparse(
            "http://localhost:8080/creditrisk_api/Borrower_collection?borrower_is_part_of_portfolio%5Bhas_cutoff_date%5D=2020-03-20T14%3A28%3A23.382748&pageIndex=1&limit=10&offset=1"
        )

        assert sorted(url.query) == sorted(url_should_be.query)
