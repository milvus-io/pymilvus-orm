# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under the License.

from . import connections
from .schema import CollectionSchema, FieldSchema
import pandas
from .prepare import Prepare


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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="collection description")
        >>> collection = Collection(name="test_collection", data=None, schema=schema, alias="default")
        >>> collection.name
        'test_collection'
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
            server_schema = CollectionSchema.construct_from_dict(resp)
            if schema is None:
                self._schema = server_schema
                if data is not None:
                    self.insert(data=data)
            else:
                if len(schema.fields) != len(resp["fields"]):
                    raise Exception("The collection already exist, but the schema is not the same as the passed in.")
                for schema_field in schema.fields:
                    same_field = False
                    for field in resp["fields"]:
                        if field["name"] == schema_field.name and field["type"] == schema_field.dtype:
                            # and field["is_primary_key"] == schema_field.is_primary:
                            same_field = True
                    if not same_field:
                        raise Exception(
                            "The collection already exist, but the schema is not the same as the passed in.")
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
                    conn.create_collection(self._name, fields=schema.to_dict())
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
    def schema(self) -> CollectionSchema:
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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test get description")
        >>> collection = Collection(name="test_collection", schema=schema, alias="default")
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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test get collection name")
        >>> collection = Collection(name="test_collection", schema=schema, alias="default")
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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test collection is empty")
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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="get collection entities num")
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
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema(name="int64", dtype=DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="drop collection")
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

        :param kwargs:
            * *timeout* (``float``) --
              An optional duration of time in seconds to allow for the RPC. When timeout
              is set to None, client waits until server response or error occur.

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> field = FieldSchema(name="int64", type="int64", is_primary=False, description="int64")
        >>> schema = CollectionSchema(fields=[field], auto_id=True, description="collection schema has a int64 field")
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> import pandas as pd
        >>> int64_series = pd.Series(data=list(range(10, 20)), index=list(range(10)))
        >>> data = pd.DataFrame(data={"int64" : int64_series})
        >>> collection.insert(data)
        >>> collection.load() # load collection to memory
        >>> assert not collection.is_empty
        >>> assert collection.num_entities == 10
        """
        conn = self._get_connection()
        conn.load_collection(self._name, timeout=kwargs.get("timeout", None))

    def release(self, **kwargs):
        """
        Release the collection from memory.

        :param kwargs:
            * *timeout* (``float``) --
              An optional duration of time in seconds to allow for the RPC. When timeout
              is set to None, client waits until server response or error occur.

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> field = FieldSchema(name="int64", type="int64", is_primary=False, description="int64")
        >>> schema = CollectionSchema(fields=[field], auto_id=True, description="collection schema has a int64 field")
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> import pandas as pd
        >>> int64_series = pd.Series(data=list(range(10, 20)), index=list(range(10)))
        >>> data = pd.DataFrame(data={"int64" : int64_series})
        >>> collection.insert(data)
        >>> collection.load()   # load collection to memory
        >>> assert not collection.is_empty
        >>> assert collection.num_entities == 10
        >>> collection.release()    # release the collection from memory
        >>> assert collection.is_empty
        >>> assert collection.num_entities == 0
        """
        conn = self._get_connection()
        # TODO(yukun): release_collection in pymilvus need db_name, but not field_name
        conn.release_collection(self._name, timeout=kwargs.get("timeout", None))

    def insert(self, data, partition_name=None, **kwargs):
        """
        Insert data into collection.

        :param data: The specified data to insert, the dimension of data needs to align with column number
        :type  data: list-like(list, tuple) object or pandas.DataFrame
        :param partition_name: The partition name which the data will be inserted to, if partition name is
                               not passed, then the data will be inserted to "_default" partition
        :type partition_name: str

        :param kwargs:
            * *timeout* (``float``) --
              An optional duration of time in seconds to allow for the RPC. When timeout
              is set to None, client waits until server response or error occur.

        :example:
        >>> from pymilvus_orm.collection import Collection
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> field = FieldSchema(name="int64", type="int64", is_primary=False, description="int64")
        >>> schema = CollectionSchema(fields=[field], auto_id=True, description="collection schema has a int64 field")
        >>> collection = Collection(name="test_collection", schema=schema)
        >>> import random
        >>> data = [[random.randint(1, 100) for _ in range(10)]]
        >>> collection.insert(data)
        >>> collection.load()
        >>> assert not collection.is_empty
        >>> assert collection.num_entities == 10
        """
        conn = self._get_connection()
        if isinstance(data, (list, tuple)):
            entities = Prepare.prepare_insert_data_for_list_or_tuple(data, self._schema)
            timeout = kwargs.pop("timeout", None)
            return conn.insert(self._name, entities, partition_tag=partition_name, timeout=timeout, **kwargs)

    def search(self, data, params, limit, expr="", partition_names=None, fields=None, **kwargs):
        """
        Vector similarity search with an optional boolean expression as filters.

        :param data: Data to search, the dimension of data needs to align with column number
        :type  data: list-like(list, tuple, numpy.ndarray) object or pandas.DataFrame

        :param params: Search parameters
        :type  params: dict

        :param limit: Search topk
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
    def partitions(self) -> list:
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

    from .partition import Partition

    def partition(self, partition_name) -> Partition:
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

    def has_partition(self, partition_name) -> bool:
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
        from .index import Index
        conn = self._get_connection()
        indexes = []
        for field in self._schema.fields:
            tmp_index = conn.describe_index(self._name, field.name)
            if tmp_index is not None:
                indexes.append(Index(self, field.name, tmp_index["params"]))
        return indexes

    def index(self, index_name=""):
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
        for field in self._schema.fields:
            tmp_index = conn.describe_index(self._name, field.name)
            if tmp_index is not None:
                return Index(self, field.name, tmp_index["params"])

    def create_index(self, field_name, index_params, index_name="", **kwargs):
        """
        Create index on a specified column according to the index parameters. Return Index Object.

        :param field_name: The name of the field to create an index for.
        :type  field_name: str

        :param index_params: Indexing parameters.
        :type  index_params: dict

        :param index_name: The name of the index to create.
        :type  index_name: str
        """
        # TODO(yukun): Add index_name
        conn = self._get_connection()
        return conn.create_index(self._name, field_name, index_params, timeout=kwargs.get("timeout", None),
                                 **kwargs)

    def has_index(self, index_name=""):
        """
        Checks whether a specified index exists.

        :param index_name: The name of the index to check.
        :type  index_name: str

        :return: If specified index exists
        :rtype: bool
        """
        conn = self._get_connection()
        # TODO(yukun): Need field name, but provide index name
        if conn.describe_index(self._name, "") is None:
            return False
        return True

    def drop_index(self, index_name="", **kwargs):
        """
        Drop index and its corresponding index files.

        :param index_name: The name of the partition to drop.
        :type  index_name: str
        """
        from .index import Index
        conn = self._get_connection()
        for field in self._schema.fields:
            tmp_index = conn.describe_index(self._name, field.name)
            if tmp_index is not None:
                index = Index(self, field.name, tmp_index["params"], index_name)
                index.drop()
