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

from pymilvus_orm.collection import Collection
from pymilvus_orm.connections import connections
from pymilvus_orm.schema import FieldSchema, CollectionSchema
from pymilvus_orm.types import DataType
import random
from sklearn import preprocessing
import string

default_dim = 128
default_nb = 3000
default_float_vec_field_name = "float_vector"
default_segment_row_limit = 1000


def gen_default_fields(auto_id=True):
    default_fields = [
        FieldSchema(name="int64", dtype=DataType.INT64, is_primary=False),
        FieldSchema(name="float", dtype=DataType.FLOAT),
        FieldSchema(name=default_float_vec_field_name, dtype=DataType.FLOAT_VECTOR, dim=default_dim)
    ]
    default_schema = CollectionSchema(fields=default_fields, description="test collection",
                                      segment_row_limit=default_segment_row_limit, auto_id=True)
    return default_schema


def gen_vectors(num, dim, is_normal=True):
    vectors = [[random.random() for _ in range(dim)] for _ in range(num)]
    vectors = preprocessing.normalize(vectors, axis=1, norm='l2')
    return vectors.tolist()


def gen_data(nb, is_normal=False):
    vectors = gen_vectors(nb, default_dim, is_normal)
    entities = [
        [i for i in range(nb)],
        [float(i) for i in range(nb)],
        vectors
    ]
    return entities


def gen_unique_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return "collection_" + prefix if str_value is None else str_value + "_" + prefix


connections.create_connection(alias="default")


def test_create_collection():
    collection = Collection(name=gen_unique_str(), schema=gen_default_fields())
    print(collection.name)
    print(collection.description)
    collection.drop()


def test_collection_only_name():
    name = gen_unique_str()
    collection_temp = Collection(name=name, schema=gen_default_fields())
    collection = Collection(name=name)
    data = gen_data(default_nb)
    collection.insert(data)
    collection.load()
    assert collection.is_empty is False
    assert collection.num_entities == default_nb
    collection.drop()


def test_collection_with_data():
    data = gen_data(default_nb)
    collection = Collection(name=gen_unique_str(), data=data, schema=gen_default_fields())
    collection.load()
    assert collection.is_empty is False
    assert collection.num_entities == default_nb
    collection.drop()


test_create_collection()
test_collection_only_name()
test_collection_with_data()
