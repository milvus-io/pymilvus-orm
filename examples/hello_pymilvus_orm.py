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
default_topK = 5
default_float_vec_field_name = "float_vector"
default_index = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"}
default_search_params = {}
default_search_expr = ""


def gen_default_schema():
    default_fields = [
        FieldSchema(name="int64", dtype=DataType.INT64, is_primary=False),
        FieldSchema(name="float", dtype=DataType.FLOAT),
        FieldSchema(name=default_float_vec_field_name, dtype=DataType.FLOAT_VECTOR, dim=default_dim)
    ]
    default_schema = CollectionSchema(fields=default_fields, description="test collection")
    return default_schema


def gen_unique_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return "collection_" + prefix if str_value is None else str_value + "_" + prefix


def gen_float_vectors(num, dim):
    vectors = [[random.random() for _ in range(dim)] for _ in range(num)]
    vectors = preprocessing.normalize(vectors, axis=1, norm='l2')
    return vectors.tolist()


def gen_float_data(nb):
    vectors = gen_float_vectors(nb, default_dim)
    entities = [
        [i for i in range(nb)],
        [float(i) for i in range(nb)],
        vectors
    ]
    return entities


def hello_milvus():
    connections.create_connection(alias="default")
    collection = Collection(name=gen_unique_str(), schema=gen_default_schema())
    data = gen_float_data(default_nb)
    collection.insert(data=data)
    collection.create_index(field_name=default_float_vec_field_name, index_params=default_index, index_name="")
    collection.load()
    search_result = collection.search(data=data[-5:], params=default_search_params, limit=default_topK, expr=default_search_expr)
    print(search_result)
