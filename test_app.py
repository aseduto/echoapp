import unittest
import json
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_json(self):
        payload = {"message": "Hello, World!"}
        response = self.app.post('/',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['body_content'], json.dumps(payload))

    def test_invalid_json_missing_field(self):
        payload = {"msg": "Hello, World!"} # "msg" instead of "message"
        response = self.app.post('/',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', response_data)
        self.assertIn('validation error', response_data['error'])

    def test_malformed_json(self):
        payload = '{"message": "Hello, World!"' # Malformed JSON
        response = self.app.post('/',
                                 data=payload,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid JSON format')

    def test_non_json_content_type(self):
        payload = '<message>Hello, World!</message>'
        response = self.app.post('/',
                                 data=payload,
                                 content_type='application/xml')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['body_content'], payload)

if __name__ == '__main__':
    unittest.main()
