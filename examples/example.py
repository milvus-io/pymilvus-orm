from pymilvus_orm import *
from milvus import DataType
from pprint import pprint
import random

# configure milvus hostname and port
# TODO(wxyu): add configure statement

# List all collection names
pprint(list_collections())

# Create a collection named 'demo_film_tutorial'
collection = Collection(name='demo_film_tutorial', data=None, schema={
    "fields": [
        {
            "name": "release_year",
            "type": DataType.INT32
        },
        {
            "name": "embedding",
            "type": DataType.FLOAT_VECTOR,
            "params": {"dim": 8}
        },
    ],
    "segment_row_limit": 4096,
    "auto_id": False
})

# List all collection names
pprint(list_collections())

pprint(collection.name)
pprint(collection.schema)
pprint(collection.description)

# List all partition names in demo collection
pprint(collection.partitions)

# Create a partition named 'American'
partition = collection.partition(partition_name='American')

# List all partition names in demo collection
pprint(collection.partitions)

# Construct some entities
The_Lord_of_the_Rings = [
    {
        "id": 1,
        "title": "The_Fellowship_of_the_Ring",
        "release_year": 2001,
        "embedding": [random.random() for _ in range(8)]
    },
    {
        "id": 2,
        "title": "The_Two_Towers",
        "release_year": 2002,
        "embedding": [random.random() for _ in range(8)]
    },
    {
        "id": 3,
        "title": "The_Return_of_the_King",
        "release_year": 2003,
        "embedding": [random.random() for _ in range(8)]
    }
]

# Transform
ids = [k.get("id") for k in The_Lord_of_the_Rings]
release_years = [k.get("release_year") for k in The_Lord_of_the_Rings]
embeddings = [k.get("embedding") for k in The_Lord_of_the_Rings]

data = [
    # Milvus doesn't support string type yet,
    # so we cannot insert "title".
    {
        "name": "release_year",
        "values": release_years,
        "type": DataType.INT32
    },
    {
        "name": "embedding",
        "values": embeddings,
        "type": DataType.FLOAT_VECTOR
    },
]

# Insert into milvus
partition.insert(data)

# Count entities
pprint(collection.num_entities)

# TODO(wxyu): search
# collection.search()

# Drop a partition
partition.drop()

# List all partition names in demo collection
pprint(collection.partitions)

# Drop a collection
collection.drop()

# List all collection names
pprint(list_collections())
