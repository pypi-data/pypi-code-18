import pymongo
from bson import ObjectId
from flasky.errors import FlaskyTornError
from pymongo.errors import DuplicateKeyError

__all__ = ["maybe_object_id", "Repository", "create_id"]


class RecordNotExistsError(FlaskyTornError):
    def __init__(self, record_type, record_id):
        super().__init__(status_code=404, err_code="errors.resourceNotFound")
        self.record_type = record_type
        self.record_id = record_id

class IDMismatchError(FlaskyTornError):
    def __init__(self, given_id, data_id):
        super().__init__(message="errors.idMismatchError", err_code="errors.idMismatchError", status_code=400)
        self.given_id = given_id
        self.data_id = data_id

class FlaskyDuplicateKeyError(FlaskyTornError):
    def __init__(self, collection_name, key, pymongo_exc):
        super().__init__(status_code=409,
                         message="There is already existing record at <{}> collection"
                                 "with given <{}>key ".format(collection_name, key),
                         err_code="errors.resourceAlreadyExists",
                         reason=pymongo_exc)
        self.collection_name = collection_name
        self.key = key


def maybe_object_id(maybe_id):
    if isinstance(maybe_id, ObjectId):
        return maybe_id
    elif not ObjectId.is_valid(maybe_id):
        return maybe_id
    else:
        return ObjectId(maybe_id)

def create_id():
    return ObjectId()

class Repository(object):

    def __init__(self, collection):
        self.collection = collection

    @property
    def collection_name(self):
        return self.collection.name

    async def query(self, select=None, where=None,
                    sort=None, skip=None, limit=None):
        cur = self.collection.find(where, select)

        if skip:
            cur.skip(skip)

        if sort:
            cur.sort(sort)

        if limit:
            cur.limit(limit)

        records = await cur.to_list(length=None)
        return [record
                for record in records
                if not record.get("is_deleted", False)]

    async def save(self, data):
        if not data.get("_id", None):
            # ~append id if it not exists
            data["_id"] = ObjectId()

        try:
            await self.collection.insert_one(data)
            return data
        except DuplicateKeyError as e:
            raise FlaskyDuplicateKeyError(
                collection_name=self.collection_name,
                key=data.get("_id"),
                pymongo_exc=e
            )

    async def update(self, _id, data):
        #: Data object should not have id field in it
        #: if it has it should be the same id with given
        #: id
        if "_id" in data:
            if str(_id) != str(data["_id"]):
                raise IDMismatchError(_id, data["_id"])

            data["_id"] = maybe_object_id(data["_id"])

        await self.collection.replace_one({
            "_id": maybe_object_id(_id)
        }, data)

        return data

    async def delete(self, _id):
        record = await self.find(_id=_id)
        if not record:
            raise RecordNotExistsError(self.collection.name, _id)
        await self.collection.remove(record["_id"], record)

    async def find(self, _id=None):
        document = await self.collection.find_one({"_id": maybe_object_id(_id)})
        if not document:
            raise RecordNotExistsError(self.collection_name, _id)
        return document

