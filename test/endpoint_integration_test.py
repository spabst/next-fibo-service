from flask_testing import TestCase
from src.main import app
import msgpack
import json


ENDPOINT = "/next_fibonacci"


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class IntegrationTest(BaseTestCase):
    def test_json_input_output(self):
        response = self.client.post(ENDPOINT, json={"n": 8})
        self.assert200(response)
        self.assertEqual(response.json, {
            'n': 13
        })
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response = self.client.post(ENDPOINT, json={"n": 34})
        self.assert200(response)
        self.assertEqual(response.json, {
            'n': 55
        })
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_msgpack_input_output(self):
        packed_data = msgpack.packb({"n": 8}, use_bin_type=True)
        response = self.client.post(
            ENDPOINT,
            data=packed_data,
            headers={"Content-Type": "application/msgpack"}
            )
        self.assert200(response)
        self.assertEqual(msgpack.unpackb(response.data, raw=False), {"n": 13})
        self.assertEqual(response.headers["Content-Type"], "application/msgpack")

        packed_data = msgpack.packb({"n": 34}, use_bin_type=True)
        response = self.client.post(
            ENDPOINT,
            data=packed_data,
            headers={"Content-Type": "application/msgpack"}
            )
        self.assert200(response)
        self.assertEqual(msgpack.unpackb(response.data, raw=False), {"n": 55})
        self.assertEqual(response.headers["Content-Type"], "application/msgpack")

    def test_wrong_content_type(self):
        response = self.client.post(ENDPOINT,
                                    json={"n": 8},
                                    headers={"Content-Type": "text/plain"})
        self.assert400(response)

    def test_wrong_data_key(self):
        response = self.client.post(ENDPOINT, json={"wrong_key": 8})
        self.assert400(response)
        expected_response = {'error': 'Input data must contain the key "n".'}
        self.assertEqual(json.loads(response.data), expected_response)

    def test_wrong_data_type(self):
        response = self.client.post(ENDPOINT,
                                    json="wrong_data_type",
                                    headers={"Content-Type": "application/json"})
        self.assert400(response)
        expected_response = {'error': 'Input data must be a JSON object or MessagePack.'}
        self.assertEqual(json.loads(response.data), expected_response)

    def test_wrong_data_value(self):
        response = self.client.post(ENDPOINT,
                                    json={'n': -1},
                                    headers={"Content-Type": "application/json"})
        self.assert400(response)
        expected_response = {'error': 'Input should be greater than 0'}
        self.assertEqual(json.loads(response.data), expected_response)

        response = self.client.post(ENDPOINT,
                                    json={'n': "wrong n type"},
                                    headers={"Content-Type": "application/json"})
        self.assert400(response)
        expected_message = "Input should be a valid integer, unable to parse string"
        assert expected_message in json.loads(response.data)["error"]
