from . import connections

class Collection(object):
    """This is a class coresponding to collection in milvus.
    """

    def __init__(self, name, schema, **kwargs):
        """Construct a collection by the name, schema and other parameters.
        Connection information is contained in kwargs.

        :param name: the name of collection
        :type name: str
        :param schema: the schema of collection
        :type schema: class `schema.CollectionSchema`
        """
        self._name = name
        self._kwargs = kwargs
        self._schema = schema

    def _get_using(self):
        return self._kwargs.get("_using", "default")

    def _get_connection(self):
        return connections.get_connection(self._get_using())

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        pass

    @property
    def description(self):
        pass

    @description.setter
    def description(self, value):
        pass

    @property
    def name(self):
        pass

    @name.setter
    def name(self, value):
        pass

    # read-only
    @property
    def is_empty(self):
        pass

    # read-only
    @property
    def num_entities(self):
        pass

    def drop(self, **kwargs):
        pass

    def load(self, field_names=None, index_names=None, partition_names=None, **kwargs):
        pass

    def release(self, **kwargs):
        pass

    def insert(self, data, **kwargs):
        pass

    def search(self, data, params, limit, expr="", partition_names=None, fields=None, **kwargs):
        pass

    @property
    def partitions(self):
        """
        Return all partitions of the collection.

        :param None
        :type NoneType

        :return: List of Partition object, return when operation is successful
        :rtype: list[Partition]

        :raises:
            RpcError: If gRPC encounter an error
            BaseException: If the return result from server is not ok
        """
        pass

    def partition(self, partition_name):
        """
        Return the partition corresponding to name. Create a new one if not existed.

        :param partition_name: The name of the partition to create.
        :type  partition_name: str

        :return:Partition object corresponding to partition_name
        :rtype: Partition

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass

    def has_partition(self, partition_name):
        """
        Checks if a specified partition exists.

        :param partition_name: The name of the partition to check
        :type  partition_name: str

        :param timeout: An optional duration of time in seconds to allow for the RPC. When timeout
                        is set to None, client waits until server response or error occur.
        :type  timeout: float

        :return: Whether a specified partition exists.
        :rtype: bool

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass

    def drop_partition(self, partition_name, **kwargs):
        """
        Drop the partition and its corresponding index files.

        :param partition_name: The name of the partition to drop.
        :type  partition_name: str

        :param kwargs

        :return: None
        :rtype: NoneType

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass

    @property
    def indexes(self):
        """
        Return all indexes of the collection..

        :param None
        :type NoneType

        :return: List of Index object, return when operation is successful
        :rtype: list[Index]

        :raises:
            RpcError: If gRPC encounter an error
            BaseException: If the return result from server is not ok
        """
        pass

    def index(self, index_name):
        """
        Return the index corresponding to name.

        :param index_name: The name of the index to create.
        :type  index_name: str

        :return:Index object corresponding to index_name
        :rtype: Index

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass

    def create_index(self, field_name, index_name, index_params, **kwargs):
        """
        Create index on a specified column according to the index parameters. Return Index Object.

        :param field_name: The name of the field to create an index for.
        :type  field_name: str

        :param index_name: The name of the index to create.
        :type  index_name: str

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
        pass

    def has_index(self, index_name):
        """
        Checks whether a specified index exists.

        :param index_name: The name of the index to check.
        :type  index_name: str

        :return: If specified index exists
        :rtype: bool

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass

    def drop_index(self, index_name, **kwargs):
        """
        Drop index and its corresponding index files.

        :param index_name: The name of the partition to drop.
        :type  index_name: str

        :param kwargs

        :return: None
        :rtype: NoneType

        :raises:
            RpcError: If gRPC encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        pass
