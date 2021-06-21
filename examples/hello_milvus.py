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


# import package
from pymilvus_orm import *


def hello_milvus():
    # create connection
    connections.connect()

    print(f"\nList collections...")
    print(list_collections())

    # create collection
    dim = 128
    default_fields = [
        schema.FieldSchema(name="count", dtype=DataType.INT64, is_primary=True),
        schema.FieldSchema(name="score", dtype=DataType.DOUBLE),
        schema.FieldSchema(name="float_vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    default_schema = schema.CollectionSchema(fields=default_fields, description="test collection")

    print(f"\nCreate collection...")
    collection = Collection(name="hello_milvus", data=None, schema=default_schema)

    print(f"\nList collections...")
    print(list_collections())

    #  insert data
    import random
    nb = 3000
    vectors = [[random.random() for _ in range(dim)] for _ in range(nb)]
    collection.insert([[i for i in range(nb)], [float(i) for i in range(nb)], vectors])

    print(f"\nGet collection entities...")
    print(collection.num_entities)

    # create index and load table
    default_index = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"}
    print(f"\nCreate index...")
    collection.create_index(field_name="float_vector", index_params=default_index)
    print(f"\nload collection...")
    collection.load()

    # load and search
    topK = 5
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    import time
    start_time = time.time()
    print(f"\nSearch...")
    res = collection.search(vectors[-2:], "float_vector", search_params, topK, "count > 100")
    end_time = time.time()

    # show result
    for hits in res:
        for hit in hits:
            print(hit)
    print("search latency = %.4fs" % (end_time - start_time))
    
    # drop collection
    collection.drop()


hello_milvus()
