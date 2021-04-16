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

        :return: List of Partition object, return when operation is successful
        :rtype: list[Partition]
        """
        pass

    def partition(self, partition_name):
        """
        Return the partition corresponding to name. Create a new one if not existed.

        :param partition_name: The name of the partition to create.
        :type  partition_name: str

        :return:Partition object corresponding to partition_name
        :rtype: Partition
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
        """
        pass

    def drop_partition(self, partition_name, **kwargs):
        """
        Drop the partition and its corresponding index files.

        :param partition_name: The name of the partition to drop.
        :type  partition_name: str
        """
        pass

    @property
    def indexes(self):
        """
        Return all indexes of the collection..

        :return: List of Index object, return when operation is successful
        :rtype: list[Index]
        """
        pass

    def index(self, index_name):
        """
        Return the index corresponding to name.

        :param index_name: The name of the index to create.
        :type  index_name: str

        :return:Index object corresponding to index_name
        :rtype: Index
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
        """
        pass

    def has_index(self, index_name):
        """
        Checks whether a specified index exists.

        :param index_name: The name of the index to check.
        :type  index_name: str

        :return: If specified index exists
        :rtype: bool
        """
        pass

    def drop_index(self, index_name, **kwargs):
        """
        Drop index and its corresponding index files.

        :param index_name: The name of the partition to drop.
        :type  index_name: str
        """
        pass
