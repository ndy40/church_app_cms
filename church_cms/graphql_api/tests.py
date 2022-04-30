from django.test import TestCase, Client
from django.shortcuts import reverse

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
        resp = self.factory.get('/graphql/', data={'query': payload},)
        assert resp.status_code == 200