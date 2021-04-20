import unittest
from unittest.mock import MagicMock
import milvus
from utils import *


class MyTestCase(unittest.TestCase):
    def test_drop_collection(self):
        client = milvus.Milvus()
        client.drop_collection = MagicMock(return_value=True)
        assert client.drop_collection(gen_collection_name()) is True


if __name__ == '__main__':
    unittest.main()
