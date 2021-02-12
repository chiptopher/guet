from unittest import TestCase
from unittest.mock import Mock

from guet.util import Proxy


class TestProxy(TestCase):

    def test_attempts_to_access_attribute_from_proxy(self):
        proxy_object = Mock()
        attribute = Mock()

        proxy_object.attribute = attribute

        proxy = Proxy(proxy_object)

        self.assertEqual(attribute, proxy.attribute)

    def test_loads_object_if_not_given(self):
        proxy_object = Mock()
        attribute = Mock()

        proxy_object.attribute = attribute

        loader = Mock()
        loader.return_value = proxy_object

        proxy = Proxy()
        proxy.loader = loader

        self.assertEqual(attribute, proxy.attribute)
