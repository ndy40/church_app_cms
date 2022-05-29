import json

from django.test import TestCase, Client

# Create your tests here.


class GraphQlApiTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = Client()

    def test_graphiql_works(self):
        payload = """
            query {
              hello
            }
        """
        resp = self.factory.post('/', data={'query': payload}, )
        assert resp.status_code == 200

    def test_device_registration_mutation(self):
        payload = """
            mutation registerDevice($input: DeviceInput!) {
              registerDevice(input: $input) {
                device {
                  id
                  token
                  osVersion
                  manufacturer
                  model
                  consent {
                    pushBroadcast
                    appNotification
                    email
                  }
                }
              }
            }
        """

        variables = """
            {
                "input": {
                    "manufacturer": "Apple",
                    "osVersion": "15.01",
                    "model": "iPhone 11",
                    "token": "token123",
                    "appVersion": "v0.1.0",
                    "consent": {
                        "email": true,
                        "pushBroadcast": true,
                        "appNotification": true
                    }
                }
            }
        """

        expected_response = {
            'data': {
                'registerDevice': {
                    'device': {
                        'id': '1',
                        'token': 'token123',
                        'osVersion': '15.01',
                        'manufacturer': 'Apple',
                        'model': 'iPhone 11',
                        'consent': {
                            'pushBroadcast': True,
                            'appNotification': True,
                            'email': True
                        }
                    }
                }
            }
        }

        resp = self.factory.post('/', data={'query': payload, 'variables': variables})
        assert resp.status_code == 200
        assert expected_response == resp.json()

    def test_update_device_consent(self):
        payload = """
            mutation registerDevice($input: DeviceInput!) {
              registerDevice(input: $input) {
                device {
                  id
                  token
                  osVersion
                  manufacturer
                  model
                  consent {
                    pushBroadcast
                    appNotification
                    email
                  }
                }
              }
            }
        """

        variables = """
            {
                "input": {
                    "manufacturer": "Apple",
                    "osVersion": "15.01",
                    "model": "iPhone 11",
                    "token": "token123",
                    "appVersion": "v0.1.0",
                    "consent": {
                        "email": true,
                        "pushBroadcast": true,
                        "appNotification": true
                    }
                }
            }
        """

        resp = self.factory.post('/', data={'query': payload, 'variables': variables})
        device_id = resp.json()['data']['registerDevice']['device']['id']

        update_payload = """
            mutation updateDeviceConsent($id: ID!, $input: DeviceConsentInput!) {
                updateDeviceConsent(id: $id, input: $input) {
                    device {
                        id
                        consent {
                            email
                            pushBroadcast
                            appNotification
                        }
                    }
                }
            }
        """

        variables = """
            {
                "id": %s,
                "input": {
                    "email": true,
                    "pushBroadcast": false,
                    "appNotification": true
                }
            }
        """ % device_id

        expected_response = {
            'data': {
                'updateDeviceConsent': {
                    'device': {
                        'id': f'{device_id}',
                        'consent': {
                            'email': True,
                            'pushBroadcast': False,
                            'appNotification': True
                        }
                    }
                }
            }
        }

        resp = self.factory.post('/', data={'query': update_payload, 'variables': variables})
        print(resp.json())
        assert expected_response == resp.json()
