#### pymilvus.utility

---



##### Checking job states

| Methods                                                      | Description                                                  | 参数                                                         | 返回值                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------- |
| utility.loading_progress(collection_name, partition_name="") | Show # loaded entities vs. # total entities                  | collection_name 类型是string<br />partition_name 类型是 string | (int, int)            |
| utility.wait_for_loading_complete(collection_name, partition_name="", timeout=None) | Block until loading is done or Raise Exception after timeout. | collection_name 类型是 string<br />partition_name 类型是 string | None或Raise Exception |
| utility.index_building_progress(collection_name, index_name="") | Show # indexed entities vs. # total entities                 | collection_name 类型是 string<br />index_name 类型是 string   | (int, int)            |
| utility.wait_for_index_building_complete(collection_name, index_name, timeout = None) | Block until building is done or Raise Exception after timeout. | collection_name 类型是string<br />partition_name 类型是 string<br />timeout 类型是 int (秒) | None或Raise Exception |
| utility.has_collection(collection_name)                      | Checks whether a specified collection exists.                | collection_name 类型是string                                 | boolean               |
| utility.has_partition(collecton_name, partition_name)        | Checks if a specified partition exists in a collection.      | collection_name 类型是string<br />partition_name 类型是 string | boolean               |

