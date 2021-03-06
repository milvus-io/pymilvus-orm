======
Future
======


SearchFuture
------------------

Constructor
~~~~~~~~~~~

+----------------------------------------------------------------------+------------------------------------------------------------------------+
| Constructor                                                          | Description                                                            |
+======================================================================+========================================================================+
| `SearchFuture() <#pymilvus_orm.SearchFuture>`_                       | Search future.                                                         |
+----------------------------------------------------------------------+------------------------------------------------------------------------+

Attributes
~~~~~~~~~~

+----------------------------------------------------------------------+------------------------------------------------------------------------+
| API                                                                  | Description                                                            |
+======================================================================+========================================================================+
| `result() <#pymilvus_orm.SearchFuture.result>`_                      | Return the search result.                                              |
+----------------------------------------------------------------------+------------------------------------------------------------------------+
| `cancel() <#pymilvus_orm.SearchFuture.cancel>`_                      | Cancel the search request.                                             |
+----------------------------------------------------------------------+------------------------------------------------------------------------+
| `done() <#pymilvus_orm.SearchFuture.done>`_                          | Wait for search request done.                                          |
+----------------------------------------------------------------------+------------------------------------------------------------------------+


APIs References
~~~~~~~~~~~~~~~


.. autoclass:: pymilvus_orm.SearchFuture
   :member-order: bysource
   :members: result, cancel, done


MutationFuture
--------------

Constructor
~~~~~~~~~~~

+----------------------------------------------------------------------+------------------------------------------------------------------------+
| Constructor                                                          | Description                                                            |
+======================================================================+========================================================================+
| `MutationFuture() <#pymilvus_orm.MutationFuture>`_                   | Mutationfuture.                                                        |
+----------------------------------------------------------------------+------------------------------------------------------------------------+

Attributes
~~~~~~~~~~

+----------------------------------------------------------------------+------------------------------------------------------------------------+
| API                                                                  | Description                                                            |
+======================================================================+========================================================================+
| `result() <#pymilvus_orm.MutationFuture.result>`_                    | Return the insert result.                                              |
+----------------------------------------------------------------------+------------------------------------------------------------------------+
| `cancel() <#pymilvus_orm.MutationFuture.cancel>`_                    | Cancel the insert request.                                             |
+----------------------------------------------------------------------+------------------------------------------------------------------------+
| `done() <#pymilvus_orm.MutationFuture.done>`_                        | Wait for insert request done.                                          |
+----------------------------------------------------------------------+------------------------------------------------------------------------+


APIs References
~~~~~~~~~~~~~~~


.. autoclass:: pymilvus_orm.MutationFuture
   :member-order: bysource
   :members: result, cancel, done
