from pymongo import MongoClient
import pydantic
import abc
from time import time
from uuid import uuid4
from typing import Union, Optional



CONFIG = {
    "URI": "mongodb://localhost:27017/",
    "DB_NAME": "fintech",
}

class DBClient():
    def __init__(self, uri=None, dbname=None):
        self.uri = CONFIG["URI"] if uri is None else uri
        self.dbname = CONFIG["DB_NAME"] if dbname is None else dbname

    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.dbname]
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close() 


def get_time(seconds_precision=True):
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


class BaseField(pydantic.BaseModel):
    _id: Optional[str]
    created: Optional[Union[float, int]]
    updated: Optional[Union[float, int]]

    @pydantic.root_validator(pre=True)
    def _min_properties(cls, data):
        """At least one property is required"""
        if not data:
            raise ValueError("At least one property is required")
        return data

    def dict(self, include_nulls=True, **kwargs):
        """Override the super dict method by removing null keys from the dict, unless include_nulls=True"""
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)


class BaseCollection(metaclass=abc.ABCMeta):
    def __init__(self, db, name):
        self.name = name
        self.collection = db[name]
        self.fieldtype = None

    def list(self):
        cursor = self.collection.find()
        return [self.fieldtype(**document) for document in cursor]

    def create(self, field):
        document = field.dict()
        document["_id"] = get_uuid()
        document["created"] = document["updated"] = get_time()
        result = self.collection.insert_one(document)
        assert result.acknowledged
        return self.get(_id=document["_id"])
    
    def delete(self, **kargs):
        result = self.collection.delete_one(kargs)
        if not result.deleted_count:
            raise NotFoundException(self.name, **kargs)
    
    def get(self, **kargs):
        document = self.collection.find_one(kargs)
        if not document:
            raise NotFoundException(self.name, **kargs)
        return self.fieldtype(**document)

    def update(self, query, **kargs):
        kargs["updated"] = get_time()
        result = self.collection.update_one(query, {"$set": kargs})
        if not result.modified_count:
            raise NotFoundException(self.name, **query)


class NotFoundException(Exception):
    def __init__(self, name, **kargs) -> None:
        self.name = name
        self.dct = kargs

    def __str__(self):
        return f"Entry {self.dct} not found in collection: {self.name}"