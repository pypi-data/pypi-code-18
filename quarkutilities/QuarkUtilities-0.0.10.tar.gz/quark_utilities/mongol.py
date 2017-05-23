from bson import ObjectId
from flasky.errors import FlaskyTornError

__all__ = ["maybe_object_id", "Repository", "create_id"]


class RecordNotExistsError(FlaskyTornError):
    def __init__(self, record_type, record_id):
        super().__init__(status_code=400)


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

        await self.collection.insert_one(data)
        return data

    async def update(self, _id, data):
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
        return await self.collection.find_one({"_id": maybe_object_id(_id)})
