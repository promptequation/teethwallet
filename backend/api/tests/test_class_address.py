from django.test import Client
from django.test import TestCase


class Test_GraphQL_Clinic_All(TestCase):
    def setUp(self):
        self.url = '/graphql'

    def test_post(self):
        cl = Client()
        body = 'query { allClinics { id name vat hasAgreement owner { id name } hasInvoiceAddress isTheSameAddress address invoiceAddress} }'

        response = cl.generic('POST', self.url, body, 'application/json')
        self.assertEqual(response, 1)
