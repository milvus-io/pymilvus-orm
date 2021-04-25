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
import numpy as np
from sklearn import preprocessing
import string

default_dim = 128
default_nb = 3000
default_float_vec_field_name = "float_vector"
default_binary_vec_field_name = "binary_vector"
default_segment_row_limit = 1000


all_index_types = [
    "FLAT",
    "IVF_FLAT",
    "IVF_SQ8",
    # "IVF_SQ8_HYBRID",
    "IVF_PQ",
    "HNSW",
    # "NSG",
    "ANNOY",
    "RHNSW_FLAT",
    "RHNSW_PQ",
    "RHNSW_SQ",
    "BIN_FLAT",
    "BIN_IVF_FLAT"
]

default_index_params = [
    {"nlist": 128},
    {"nlist": 128},
    {"nlist": 128},
    # {"nlist": 128},
    {"nlist": 128, "m": 16, "nbits": 8},
    {"M": 48, "efConstruction": 500},
    # {"search_length": 50, "out_degree": 40, "candidate_pool_size": 100, "knng": 50},
    {"n_trees": 50},
    {"M": 48, "efConstruction": 500},
    {"M": 48, "efConstruction": 500, "PQM": 64},
    {"M": 48, "efConstruction": 500},
    {"nlist": 128},
    {"nlist": 128}
]


default_index = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"}
default_binary_index = {"index_type": "BIN_FLAT", "params": {"nlist": 1024}, "metric_type": "JACCARD"}


def gen_default_fields():
    default_fields = [
        FieldSchema(name="int64", dtype=DataType.INT64, is_primary=False),
        FieldSchema(name="float", dtype=DataType.FLOAT),
        FieldSchema(name=default_float_vec_field_name, dtype=DataType.FLOAT_VECTOR, dim=default_dim)
    ]
    default_schema = CollectionSchema(fields=default_fields, description="test collection",
                                      segment_row_limit=default_segment_row_limit, auto_id=True)
    return default_schema


def gen_binary_schema():
    binary_fields = [
        FieldSchema(name="int64", dtype=DataType.INT64, is_primary=False),
        FieldSchema(name="float", dtype=DataType.FLOAT),
        FieldSchema(name=default_binary_vec_field_name, dtype=DataType.BINARY_VECTOR, dim=default_dim)
    ]
    default_schema = CollectionSchema(fields=binary_fields, description="test collection",
                                      segment_row_limit=default_segment_row_limit, auto_id=True)
    return default_schema


def gen_float_vectors(num, dim, is_normal=True):
    vectors = [[random.random() for _ in range(dim)] for _ in range(num)]
    vectors = preprocessing.normalize(vectors, axis=1, norm='l2')
    return vectors.tolist()


def gen_float_data(nb, is_normal=False):
    vectors = gen_float_vectors(nb, default_dim, is_normal)
    entities = [
        [i for i in range(nb)],
        [float(i) for i in range(nb)],
        vectors
    ]
    return entities


def gen_binary_vectors(num, dim):
    raw_vectors = []
    binary_vectors = []
    for i in range(num):
        raw_vector = [random.randint(0, 1) for i in range(dim)]
        raw_vectors.append(raw_vector)
        binary_vectors.append(bytes(np.packbits(raw_vector, axis=-1).tolist()))
    return raw_vectors, binary_vectors


def gen_binary_data(nb):
    raw_vectors, binary_vectors = gen_binary_vectors(nb, dim=default_dim)
    entities = [
        [i for i in range(nb)],
        [float(i) for i in range(nb)],
        binary_vectors
    ]
    return entities


def gen_unique_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return "collection_" + prefix if str_value is None else str_value + "_" + prefix


def binary_support():
    return ["BIN_FLAT", "BIN_IVF_FLAT"]


def gen_simple_index():
    index_params = []
    for i in range(len(all_index_types)):
        if all_index_types[i] in binary_support():
            continue
        dic = {"index_type": all_index_types[i], "metric_type": "L2"}
        dic.update({"params": default_index_params[i]})
        index_params.append(dic)
    return index_params


connections.create_connection(alias="default")


def test_create_collection():
    collection = Collection(name=gen_unique_str(), schema=gen_default_fields())
    assert collection.is_empty is True
    assert collection.num_entities == 0
    collection.drop()


def test_collection_only_name():
    name = gen_unique_str()
    collection_temp = Collection(name=name, schema=gen_default_fields())
    collection = Collection(name=name)
    data = gen_float_data(default_nb)
    collection.insert(data)
    collection.load()
    assert collection.is_empty is False
    assert collection.num_entities == default_nb
    collection.drop()


def test_collection_with_data():
    data = gen_float_data(default_nb)
    collection = Collection(name=gen_unique_str(), data=data, schema=gen_default_fields())
    collection.load()
    assert collection.is_empty is False
    assert collection.num_entities == default_nb
    collection.drop()


def test_create_index_float_vector():
    data = gen_float_data(default_nb)
    collection = Collection(name=gen_unique_str(), data=data, schema=gen_default_fields())
    for index_param in gen_simple_index():
        collection.create_index(field_name=default_float_vec_field_name, index_params=index_param)
    assert len(collection.indexes) != 0
    collection.drop()


def test_create_index_binary_vector():
    collection = Collection(name=gen_unique_str(), schema=gen_binary_schema())
    data = gen_binary_data(default_nb)
    collection.insert(data)
    collection.create_index(field_name=default_binary_vec_field_name, index_params=default_binary_index)
    assert len(collection.indexes) != 0
    collection.drop()


test_create_collection()
test_collection_only_name()
test_collection_with_data()
test_create_index_float_vector()
test_create_index_binary_vector()
