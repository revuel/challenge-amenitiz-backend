""" Unit test module for presentation.rest.setup module"""
from tests.unit.presentation.base_rest_test import BaseRestTest


class Test(BaseRestTest):
    """ Unit Test class for App Root"""

    def test_root(self):
        """
        Checks that rest API runs properly
        Returns: None

        """
        response = self.rest_client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'message': 'Welcome!'}, response.json())
