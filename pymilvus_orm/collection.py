from . import connections
from .schema import CollectionSchema, FieldSchema
import pandas


class Collection(object):
    """
    This is a class corresponding to collection in milvus.
    """

    def __init__(self, name, data=None, schema=None, **kwargs):
        """
        Construct a collection by the name, schema and other parameters.
        Connection information is contained in kwargs.

        :param name: the name of collection
        :type name: str

        :param schema: the schema of collection
        :type schema: class `schema.CollectionSchema`

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="collection description", auto_id=True)
        >>> collection = Collection(name="test_name", data=None, schema=schema)
        >>> collection.name
        'test_name'
        >>> collection.description
        'collection description'
        >>> collection.is_empty
        True
        >>> collection.num_entities
        0
        """
        self._name = name
        self._kwargs = kwargs
        conn = self._get_connection()
        has = conn.has_collection(self._name)
        if has:
            resp = conn.describe_collection(self._name)
            server_schema = CollectionSchema.construct_from_dict(resp.dict())
            if schema is None:
                self._schema = server_schema
                if data is not None:
                    self.insert(data=data)
            else:
                if len(schema.fields) != len(resp.fields):
                    raise Exception("The collection already exist, but the schema is not the same as the passed in.")
                for schema_field in schema.fields:
                    same_field = False
                    for field in resp.fields:
                        if field.name == schema_field.name and field.type == schema_field.dtype \
                                and field.is_primary_key == schema_field.is_primary:
                            same_field = True
                    if not same_field:
                        raise Exception("The collection already exist, but the schema is not the same as the passed in.")
                self._schema = schema
                if data is not None:
                    self.insert(data=data)

        else:
            if schema is None:
                if data is None:
                    raise Exception("Collection missing schema.")
                else:
                    if isinstance(data, pandas.DataFrame):
                        # TODO: construct schema by DataFrame
                        pass
                    else:
                        raise Exception("Data of not pandas.DataFrame type should be passed into the schema.")
            else:
                # create collection schema must be dict
                if isinstance(schema, CollectionSchema):
                    for i in range(len(schema.fields)):
                        if isinstance(schema.fields[i], FieldSchema):
                            schema.fields[i] = schema.fields[i].__dict__
                        else:
                            raise Exception("field type must be schema.FieldSchema.")
                    conn.create_collection(self._name, fields=schema.__dict__)
                    self._schema = schema
                    if isinstance(data, pandas.DataFrame):
                        # TODO: insert data by DataFrame
                        pass
                    else:
                        self.insert(data=data)
                else:
                    raise Exception("schema type must be schema.CollectionSchema.")

    def _get_using(self):
        return self._kwargs.get("_using", "default")

    def _get_connection(self):
        return connections.get_connection(self._get_using())

    def _check_schema(self):
        pass

    @property
    def schema(self):
        """
        Return the schema of collection.

        :return: Schema of collection
        :rtype: schema.CollectionSchema
        """
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        Set the schema of collection.

        :param value: the schema of collection
        :type value: class `schema.CollectionSchema`
        """
        pass

    @property
    def description(self):
        """
        Return the description text about the collection.

        :return:
            Collection description text, return when operation is successful

        :rtype: str

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test get description", auto_id=True)
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> collection.description
        'test get description'
        """

        return self._schema.description

    @property
    def name(self):
        """
        Return the collection name.

        :return: Collection name, return when operation is successful
        :rtype: str

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test get collection name", auto_id=True)
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> collection.name
        'test_collection'
        """
        return self._name

    # read-only
    @property
    def is_empty(self):
        """
        Return whether the collection is empty.

        :return: Whether the collection is empty
        :rtype: bool

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test collection is empty", auto_id=True)
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> collection.is_empty
        True
        """
        return self.num_entities == 0

    # read-only
    @property
    def num_entities(self):
        """
        Return the number of entities.

        :return: Number of entities in this collection
        :rtype: int

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="get collection entities num", auto_id=True)
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> collection.num_entities
        0
        TODO: add example for num_entities of collection after insert
        """
        conn = self._get_connection()
        status = conn.get_collection_stats(db_name="", collection_name=self._name)
        return status["row_count"]

    def drop(self, **kwargs):
        """
        Drop the collection, as well as its corresponding index files.

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="drop collection", auto_id=True)
        >>> collection = Collection(name="test_collection", schema=schema)
        TODO: add example for drop of collection
        # >>> collection.insert(data="")
        # >>> collection.index(index_name="")
        >>> collection.drop()
        >>> collection.num_entities
        0
        >>> collection.is_empty
        True

        """
        conn = self._get_connection()
        indexes = self.indexes
        for index in indexes:
            index.drop(**kwargs)
        conn.drop_collection(self._name, timeout=kwargs.get("timeout", None))

    def load(self, field_names=None, index_names=None, partition_names=None, **kwargs):
        """
        Load the collection from disk to memory.

        :param field_names: The specified fields to load.
        :type  field_names: list[str]

        :param index_names: The specified indexes to load.
        :type  index_names: list[str]

        :param partition_names: The specified partitions to load.
        :type partition_names: list[str]
        """
        conn = self._get_connection()
        conn.load_collection("", self._name, **kwargs)

    def release(self, **kwargs):
        """
        Release the collection from memory.
        """
        conn = self._get_connection()
        conn.release_collection("", self._name, kwargs)

    def insert(self, data, **kwargs):
        """
        Insert data into collection.

        :param data: The specified data to insert, the dimension of data needs to align with column number
        :type  data: list-like(list, tuple, numpy.ndarray) object or pandas.DataFrame
        """
        pass

    def search(self, data, params, limit, expr="", partition_names=None, fields=None, **kwargs):
        """
        Vector similarity search with an optional boolean expression as filters.

        :param data: Data to search, the dimension of data needs to align with column number
        :type  data: list-like(list, tuple, numpy.ndarray) object or pandas.DataFrame

        :param params: Search parameters
        :type  params: dict

        :param limit:
        :type  limit: int

        :param expr: Search expression
        :type  expr: str

        :param fields: The fields to return in the search result
        :type  fields: list[str]

        :return: A Search object, you can call its' `execute` method to get the search result
        :rtype: class `search.Search`
        """
        pass

    @property
    def partitions(self):
        """
        Return all partitions of the collection.

        :return: List of Partition object, return when operation is successful
        :rtype: list[Partition]
        """
        from .partition import Partition
        conn = self._get_connection()
        partition_strs = conn.list_partitions(self._name)
        partitions = []
        for partition in partition_strs:
            partitions.append(Partition(self, partition))
        return partitions

    def partition(self, partition_name):
        """
        Return the partition corresponding to name. Create a new one if not existed.

        :param partition_name: The name of the partition to create.
        :type  partition_name: str

        :return:Partition object corresponding to partition_name
        :rtype: Partition
        """
        from .partition import Partition
        conn = self._get_connection()
        return Partition(self, partition_name)

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
        conn = self._get_connection()
        return conn.has_partition(self._name, partition_name)

    def drop_partition(self, partition_name, **kwargs):
        """
        Drop the partition and its corresponding index files.

        :param partition_name: The name of the partition to drop.
        :type  partition_name: str
        """
        conn = self._get_connection()
        return conn.drop_partition(self._name, partition_name, timeout=kwargs.get("timeout", None))

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
        # TODO(yukun): Need field name, but provide index name
        from .index import Index
        conn = self._get_connection()
        tmp_index = conn.describe_index(self._name, "")
        return Index(self, index_name, "", tmp_index.params)

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
        # TODO(yukun): Add index_name
        conn = self._get_connection()
        return conn.create_index(self._name, field_name, index_params, timeout=kwargs.get("timeout", None),
                                 kwargs=kwargs)

    def has_index(self, index_name):
        """
        Checks whether a specified index exists.

        :param index_name: The name of the index to check.
        :type  index_name: str

        :return: If specified index exists
        :rtype: bool
        """
        conn = self._get_connection()
        # TODO(yukun): Need field name, but provide index name
        if conn.describe_index(self._name, "") == None:
            return False
        return True

    def drop_index(self, index_name, **kwargs):
        """
        Drop index and its corresponding index files.

        :param index_name: The name of the partition to drop.
        :type  index_name: str
        """
        # TODO(yukun): Need field name
        conn = self._get_connection()
        conn.drop_index(self._name, "", index_name, timeout=kwargs.get("timeout", None), kwargs=kwargs)
