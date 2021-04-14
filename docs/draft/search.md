| Methods                                                      | Descriptions               | 参数                                                         | 返回值                        |
| ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------ | ----------------------------- |
| Search(collection, data, params, limit, expr=None, partition_names=None, fields=None, **kwargs) | Construct a Search object. | collection类型是 Collection<br />data是 list-like(list, tuple, numpy.ndarray)<br /><br />params 类型是 dict<br /><br />limit 类型是 int <br />expr 类型是string<br />partitions_names类型是 list(string)<br />fields类型是list(string) | Search对象或者Raise Exception |
| Search.execute(sync=True, **kwargs)                          | Return the search result.  | sync 类型是boolean，是否同步等待查询结果<br />kwargs 的可以是 callback=function | SearchResult对象              |


| Methods                     | Descriptions                                                 | 参数                     | 返回值                  |
| --------------------------- | ------------------------------------------------------------ | ------------------------ | ----------------------- |
| SearchResult(grpc_response) | Construct a Search Result from response.                     | 内部构造函数，用户用不到 | SearchResult对象        |
| SearchResult.__iter__()     | Iterate the Search Result. Every iteration returns a `Hits` coresponding to a query. | /                        | python generator        |
| SearchResult[n]             | Return the `Hits` coresponding to the nth query.             | int                      | Hits对象                |
| SearchResult.__len__()      | Return the number of query of Search Result.                 | /                        | int                     |
| SearchResult.done()         | 同步等待结果，幂等操作                                       | /                        | None或者Raise Exception |


| Methods          | Descriptions                                                 | 参数           | 返回值                            |
| ---------------- | ------------------------------------------------------------ | -------------- | --------------------------------- |
| Hits(raw_data)   | Construct a Hits object from response.                       |                | Hits对象                          |
| Hits.__iter__()  | Iterate the `Hits` object. Every iteration returns a `Hit` which represent a record coresponding to the query. |                | python迭代器，每次迭代返回Hit对象 |
| Hits[k]          | Return the kth `Hit` coresponding to the query.              | 参数k 类型 int | Hit对象                           |
| Hits.__len__()   | Return the number of hit record.                             | /              | int                               |
| Hits.ids       | Return the ids of all hit record.                            | /              | list(int)或者list(string)         |
| Hits.distances | Return the distances of all hit record.                      | /              | list(float)                       |


| Methods        | Descriptions                                                 | 参数 | 返回值      |
| -------------- | ------------------------------------------------------------ | ---- | ----------- |
| Hit(raw_data)  | Construct a Hit object from response. A hit represent a record coresponding to the query. |      | Hit对象     |
| Hit.id       | Return the id of the hit record.                             | /    | int /string |
| Hit.distance | Return the distance between the hit record and the query.    | /    | float       |
| Hit.score    | Return the calculated score of the hit record, now the score is equal to distance. | /    | float       |



