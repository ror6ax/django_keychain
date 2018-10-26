from botocore.stub import Stubber
import botocore.session

from datetime import datetime
from django.test import SimpleTestCase
from django_keychain import DjangoKeychain


class KeychainTestCase(SimpleTestCase):

    def setUp(self):
        client = botocore.session.get_session().create_client('secretsmanager',
                                                              'eu-west-1')
        stubber = Stubber(client)

        response = {
            'Name': 'TESTSECRET2',
            'SecretString': '{"TESTKEY1": "testvalue"}',
            'VersionStages': [
                '1',
            ],
            'CreatedDate': datetime(2015, 1, 1)
        }

        expected_params = {'SecretId': 'TESTSECRET2'}

        stubber.add_response('get_secret_value', response, expected_params)
        stubber.activate()

        self.keychain = DjangoKeychain("eu-west-1")
        self.keychain.get_client = client

    def test_read_existing_plaintext_secret(self):
        key = self.keychain.get_secret("TESTSECRET2", "TESTKEY1")
        self.assertEquals(key, 'testvalue')
