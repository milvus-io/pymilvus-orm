from . import connections
from .collection import Collection

class Index(object):

    def __init__(self, collection, name, field_name, index_params, **kwargs):
        """
        Create index on a specified column according to the index parameters.

        :param collection: The collection of index
        :type  collection: Collection

        :param name: The name of index
        :type  name: str

        :param field_name: The name of the field to create an index for.
        :type  field_name: str

        :param index_params: Indexing parameters.
        :type  index_params: dict
            There are examples of supported indexes:

            IVF_FLAT:
                ` {
                    "metric_type":"L2",
                    "index_type": "IVF_FLAT",
                    "params":{"nlist": 1024}
                }`

            IVF_PQ:
                `{
                    "metric_type": "L2",
                    "index_type": "IVF_PQ",
                    "params": {"nlist": 1024, "m": 8, "nbits": 8}
                }`

            IVF_SQ8:
                `{
                    "metric_type": "L2",
                    "index_type": "IVF_SQ8",
                    "params": {"nlist": 1024}
                }`

            BIN_IVF_FLAT:
                `{
                    "metric_type": "JACCARD",
                    "index_type": "BIN_IVF_FLAT",
                    "params": {"nlist": 1024}
                }`

            HNSW:
                `{
                    "metric_type": "L2",
                    "index_type": "HNSW",
                    "params": {"M": 48, "efConstruction": 50}
                }`

            RHNSW_FLAT:
                `{
                    "metric_type": "L2",
                    "index_type": "RHNSW_FLAT",
                    "params": {"M": 48, "efConstruction": 50}
                }`

            RHNSW_PQ:
                `{
                    "metric_type": "L2",
                    "index_type": "RHNSW_PQ",
                    "params": {"M": 48, "efConstruction": 50, "PQM": 8}
                }`

            RHNSW_SQ:
                `{
                    "metric_type": "L2",
                    "index_type": "RHNSW_SQ",
                    "params": {"M": 48, "efConstruction": 50}
                }`

            ANNOY:
                `{
                    "metric_type": "L2",
                    "index_type": "ANNOY",
                    "params": {"n_trees": 8}
                }`

        :param kwargs:
            * *_async* (``bool``) --
              Indicate if invoke asynchronously. When value is true, method returns a IndexFuture object;
              otherwise, method returns results from server.
            * *_callback* (``function``) --
              The callback function which is invoked after server response successfully. It only take
              effect when _async is set to True.

        :return: None
        :rtype: NoneType

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        self._collection = collection
        self._name = name
        self._field_name = field_name
        self._index_params = index_params
        self._kwargs = kwargs

    @property
    def name(self):
        """
        Return the index name.

        :param None
        :type  NoneType

        :return: The name of index
        :rtype:  str
        """
        pass

    @name.setter
    def name(self, value):
        pass

    @property
    def params(self):
        """
        Return the index params.

        :param None
        :type  NoneType

        :return: Index parameters
        :rtype:  dict
        """
        pass

    @params.setter
    def params(self, value):
        pass

    # read-only
    @property
    def collection_name(self):
        """
        Return corresponding collection name.

        :param None
        :type  NoneType

        :return: Corresponding collection name.
        :rtype:  str
        """
        pass

    @property
    def field_name(self):
        """
        Return corresponding column name.

        :param: None
        :type:  NoneType

        :return: Corresponding column name.
        :rtype:  str
        """
        pass

    def drop(self, **kwargs):
        """
        Drop index and its corresponding index files.

        :param: None
        :type:  NoneType

        :return: None
        :rtype: NoneType

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass
