# Copyright (C) 2019-2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

import copy
import json
from typing import List
import pandas
from pandas.api.types import is_list_like

from pymilvus_orm.constants import VECTOR_COMMON_TYPE_PARAMS
from pymilvus_orm.types import DataType, map_numpy_dtype_to_datatype, infer_dtype_bydata
from pymilvus_orm.exceptions import (
    CannotInferSchemaException,
    DataTypeNotSupport,
    ParamError,
    PrimaryKeyException,
)


class CollectionSchema:
    def __init__(self, fields, description="", **kwargs):
        if not isinstance(fields, list):
            raise ParamError("The fields of schema must be type list.")
        self._fields = [copy.deepcopy(field) for field in fields]
        primary_field = kwargs.get("primary_field", None)
        for field in self._fields:
            if not isinstance(field, FieldSchema):
                raise ParamError("The field of schema type must be FieldSchema.")
            if primary_field == field.name:
                field.is_primary = True
        self._primary_field = None
        for field in self._fields:
            if field.is_primary:
                if primary_field is not None and primary_field != field.name:
                    raise PrimaryKeyException(0, "Primary key field can only be one.")
                self._primary_field = field

        if self._primary_field is None:
            raise PrimaryKeyException(0, "Must be have a primary key field.")

        if self._primary_field.dtype not in [DataType.INT64]:
            raise PrimaryKeyException(0, "Primary key type must be DataType.INT64.")

        self._auto_id = kwargs.get("auto_id", None)
        if self._auto_id is not None:
            if not isinstance(self._auto_id, bool):
                raise ParamError("Param auto_id must be bool type.")
            if self._primary_field.auto_id is not None and self._primary_field.auto_id != self._auto_id:
                raise ParamError("The auto_id of the collection is inconsistent "
                                 "with the auto_id of the primary key field.")
        else:
            if self._primary_field.auto_id is None:
                self._primary_field.auto_id = False
            self._auto_id = self._primary_field.auto_id

        self._description = description
        self._kwargs = copy.deepcopy(kwargs)

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return str(json.dumps(self.to_dict()))

    def __len__(self):
        return len(self.fields)

    def __eq__(self, other):
        """
        The order of the fields of schema must be consistent.
        """
        return self.to_dict() == other.to_dict()

    @classmethod
    def construct_from_dict(cls, raw):
        fields = [FieldSchema.construct_from_dict(field_raw) for field_raw in raw['fields']]
        return CollectionSchema(fields, raw.get('description', ""))

    @property
    # TODO:
    def primary_field(self):
        return self._primary_field

    @property
    def fields(self):
        """
        Returns the fields about the CollectionSchema.

        :return list:
            List of FieldSchema, return when operation is successful.

        :example:
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema("int64", DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field])
        >>> schema.fields
        """
        return self._fields

    @property
    def description(self):
        """
        Returns a text description of the CollectionSchema.

        :return str:
            CollectionSchema description text, return when operation is successful.

        :example:
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema("int64", DataType.INT64, descrition="int64", is_parimary=False)
        >>> schema = CollectionSchema(fields=[field], description="test get description")
        >>> schema.description
        """
        return self._description

    @property
    def auto_id(self):
        """
        Whether the primary keys are automatically generated.

        :return bool:
            * True: If the primary keys are automatically generated,
            * False: Otherwise.

        :example:
        >>> from pymilvus_orm.schema import FieldSchema, CollectionSchema
        >>> from pymilvus_orm.types import DataType
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema("int64", DataType.INT64, descrition="int64", is_primary=False)
        >>> schema = CollectionSchema(fields=[field])
        >>> schema.auto_id
        """
        return self._auto_id


    def to_dict(self):
        _dict = {
            "auto_id": self.auto_id,
            "description": self._description,
            "fields": [f.to_dict() for f in self._fields]
        }
        return _dict


class FieldSchema:
    def __init__(self, name, dtype, description="", **kwargs):
        self.name = name
        try:
            DataType(dtype)
        except ValueError:
            raise DataTypeNotSupport(0, "Field type must be of DataType") from None
        if dtype == DataType.UNKNOWN:
            raise DataTypeNotSupport(0, "Field type must be of DataType")
        self._dtype = dtype
        self._description = description
        self._type_params = {}
        self._kwargs = copy.deepcopy(kwargs)
        if not isinstance(kwargs.get("is_primary", False), bool):
            raise ParamError("Param is_primary must be bool type.")
        self.is_primary = kwargs.get("is_primary", False)
        self.auto_id = kwargs.get("auto_id", None)
        if self.auto_id is not None:
            if not isinstance(kwargs.get("auto_id"), bool):
                raise ParamError("Param auto_id must be bool type.")
            if not self.is_primary and self.auto_id:
                raise PrimaryKeyException(0, "auto_id can only be specified on the primary key field")

        self._parse_type_params()

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        return self.construct_from_dict(self.to_dict())

    def _parse_type_params(self):
        # update self._type_params according to self._kwargs
        if self._dtype not in (DataType.BINARY_VECTOR, DataType.FLOAT_VECTOR):
            return
        if not self._kwargs:
            return
        # currently only support ndim
        if self._kwargs:
            for k in VECTOR_COMMON_TYPE_PARAMS:
                if k in self._kwargs:
                    if self._type_params is None:
                        self._type_params = {}
                    self._type_params[k] = self._kwargs[k]

    @classmethod
    def construct_from_dict(cls, raw):
        kwargs = {}
        kwargs.update(raw.get("params", {}))
        kwargs['is_primary'] = raw.get("is_primary", False)
        if raw.get("auto_id", None) is not None:
            kwargs['auto_id'] = raw.get("auto_id", None)
        return FieldSchema(raw['name'], raw['type'], raw['description'], **kwargs)

    def to_dict(self):
        _dict = dict()
        _dict["name"] = self.name
        _dict["description"] = self._description
        _dict["type"] = self.dtype
        if self._type_params:
            _dict["params"] = copy.deepcopy(self.params)
        if self.is_primary:
            _dict["is_primary"] = True
        if self.auto_id is not None:
            _dict["auto_id"] = self.auto_id
        return _dict

    def __getattr__(self, item):
        if self._type_params and item in self._type_params:
            return self._type_params[item]
        return None

    def __eq__(self, other):
        if not isinstance(other, FieldSchema):
            return False
        return self.to_dict() == other.to_dict()

    @property
    def description(self):
        """
        Returns the text description of the FieldSchema.

        :return str:
            FieldSchema description text, returned when the operation is successful.

        :example:
        >>> from pymilvus_orm.schema import FieldSchema
        >>> from pymilvus_orm.types import DataType
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema("int64", DataType.INT64, descrition="int64", is_parimary=False)
        >>> field.description
        """
        return self._description

    @property
    def params(self):
        """
        Returns the parameters of the field.

        :return list:
            List of the parameter.

        :example:
        >>> from pymilvus_orm.schema import FieldSchema
        >>> from pymilvus_orm.types import DataType
        >>> from pymilvus_orm import connections
        >>> connections.create_connection(alias="default")
        <milvus.client.stub.Milvus object at 0x7f9a190ca898>
        >>> field = FieldSchema("int64", DataType.INT64, descrition="int64", is_parimary=False)
        >>> field.params
        """
        return self._type_params

    @property
    def dtype(self):
        return self._dtype


def parse_fields_from_data(datas):
    if isinstance(datas, pandas.DataFrame):
        return parse_fields_from_dataframe(datas)
    fields = []
    if not isinstance(datas, list):
        raise DataTypeNotSupport(0, "Datas must be list")
    for d in datas:
        if not is_list_like(d):
            raise DataTypeNotSupport(0, "Data type must like list")
        d_type = infer_dtype_bydata(d[0])
        fields.append(FieldSchema("", d_type))
    return fields



def parse_fields_from_dataframe(dataframe) -> List[FieldSchema]:
    if not isinstance(dataframe, pandas.DataFrame):
        return None
    d_types = list(dataframe.dtypes)
    data_types = list(map(map_numpy_dtype_to_datatype, d_types))
    col_names = list(dataframe.columns)

    column_params_map = {}

    if DataType.UNKNOWN in data_types:
        if len(dataframe) == 0:
            raise CannotInferSchemaException(0, "Cannot infer schema from empty dataframe")
        values = dataframe.head(1).values[0]
        for i, dtype in enumerate(data_types):
            if dtype == DataType.UNKNOWN:
                new_dtype = infer_dtype_bydata(values[i])
                if new_dtype in (DataType.BINARY_VECTOR, DataType.FLOAT_VECTOR):
                    vector_type_params = {}
                    if new_dtype == DataType.BINARY_VECTOR:
                        vector_type_params['dim'] = len(values[i]) * 8
                    else:
                        vector_type_params['dim'] = len(values[i])
                    column_params_map[col_names[i]] = vector_type_params
                data_types[i] = new_dtype

    if DataType.UNKNOWN in data_types:
        raise CannotInferSchemaException(0, "Cannot infer schema from dataframe")

    fields = []
    for name, dtype in zip(col_names, data_types):
        type_params = column_params_map.get(name, {})
        field_schema = FieldSchema(name, dtype, **type_params)
        fields.append(field_schema)

    return fields
