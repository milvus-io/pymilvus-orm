import logging

try:
    from pymilvus_orm import connections
except ImportError:
    from os.path import dirname, abspath
    import sys

    sys.path.append(dirname(dirname(abspath(__file__))))

    from pymilvus_orm import connections

LOGGER = logging.getLogger(__name__)

conn = connections.create_connection()
LOGGER.info(conn.list_collections())
