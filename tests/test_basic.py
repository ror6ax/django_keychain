import boto3
from django.test import SimpleTestCase
from django_keychain import DjangoKeychain


class KeychainTestCase(SimpleTestCase):

    def setUp(self):
        client = boto3.client('secretsmanager', region_name="eu-west-1")
        client.create_secret(
            Name='TESTSECRET2',
            SecretString='testvalue')

        self.keychain = DjangoKeychain("eu-west-1")

    def test_read_existing_plaintext_secret(self):
        key = self.keychain.get_secret("TESTSECRET2")
        self.assertEquals(key, 'testvalue')

    def test_read_unexisting_secret(self):
        key = self.keychain.get_secret("TESTSECRET3", "TESTKEY1")
        self.assertIsNone(key)


