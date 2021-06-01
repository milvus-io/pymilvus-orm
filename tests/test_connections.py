import copy
import logging
import pytest
import milvus
from unittest import mock

from pymilvus_orm import connections, Connections
from pymilvus_orm.default_config import DefaultConfig

LOGGER = logging.getLogger(__name__)


class TestConnections:
    @pytest.fixture(scope="function")
    def c(self):
        return copy.deepcopy(Connections())

    @pytest.fixture(scope="function")
    def configure_params(self):
        params = {
            "test": {"host": "localhost", "port": "19530"},
            "dev": {"host": "localhost", "port": "19530"},
        }
        return params

    @pytest.fixture(scope="function")
    def host(self):
        return "localhost"

    @pytest.fixture(scope="function")
    def port(self):
        return "19530"

    @pytest.fixture(scope="function")
    def params(self, host, port):
        d = {
            "host": host,
            "port": port,
        }
        return d

    def test_constructor(self, c):
        LOGGER.info(type(c))

    def test_configure(self, c, configure_params):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            c.configure(**configure_params)

            for key, _ in configure_params.items():
                c.create_connection(key)

                conn = c.get_connection(key)

                assert isinstance(conn, milvus.Milvus)

                c.pop(key)

    def test_remove_connection_without_no_connections(self, c):
        with pytest.raises(Exception):
            c.remove_connection("remove")

    def test_remove_connection(self, c, host, port):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            alias = "default"

            c.create_connection(alias, host=host, port=port)
            c.remove_connection(alias)

            assert c.get_connection(alias) is None

            c.pop(alias)

    def test_create_collection_without_param(self, c):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            alias = "default"
            c.create_connection(alias)
            conn_got = c.get_connection(alias)
            assert isinstance(conn_got, milvus.Milvus)
            c.pop(alias)

    def test_create_collection(self, c, params):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            alias = "default"
            c.create_connection(alias, **params)
            conn_got = c.get_connection(alias)
            assert isinstance(conn_got, milvus.Milvus)
            c.pop(alias)

    def test_get_collection_without_no_connections(self, c):
        assert c.get_connection("get") is None

    def test_get_collection(self, c, host, port):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            alias = "default"

            c.create_connection(alias, host=host, port=port)

            conn_got = c.get_connection(alias)
            assert isinstance(conn_got, milvus.Milvus)

            c.pop(alias)

    def test_get_collection_without_alias(self, c, host, port):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            alias = DefaultConfig.DEFAULT_USING

            c.create_connection(alias, host=host, port=port)

            conn_got = c.get_connection()
            assert isinstance(conn_got, milvus.Milvus)

            c.pop(alias)

    def test_get_collection_with_configure_without_add(self, c, configure_params):
        with mock.patch("milvus.Milvus.__init__", return_value=None):
            c.configure(**configure_params)
            for key, _ in configure_params.items():
                c.create_connection(key)
                conn = c.get_connection(key)
                assert isinstance(conn, milvus.Milvus)
                c.pop(key)

    def test_get_connection_addr(self, c, host, port):
        alias = DefaultConfig.DEFAULT_USING

        c.create_connection(alias, host=host, port=port)

        connection_addr = c.get_connection_addr(alias)

        assert connection_addr["host"] == host
        assert connection_addr["port"] == port
        c.pop(alias)

    def test_list_connections(self, c, host, port):
        alias = DefaultConfig.DEFAULT_USING

        c.create_connection(alias, host=host, port=port)

        conns = c.items()

        assert len(conns) == 1
        c.pop(alias)
