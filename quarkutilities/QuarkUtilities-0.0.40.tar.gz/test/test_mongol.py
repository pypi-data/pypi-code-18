
import pytest

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from quark_utilities import mongol
from quark_utilities.mongol import Repository

test_collection_name = "test_col"


test_data = [
    {
        "_id": ObjectId(),
        "field_1": "value_1",
        "field_2": "value_2",
        "field_3": "value_3",
        "field_4": "value_4"
    },
    {
        "_id": ObjectId(),
        "field_1": "value_5",
        "field_2": "value_6",
        "field_3": "value_7",
        "field_4": "value_8"
    }
]


@pytest.mark.asyncio
async def test_maybe_object_id_should_return_object_id():
    object_id = ObjectId()
    string_id = str(ObjectId())
    not_object_id = "23124354657"

    assert object_id == mongol.maybe_object_id(object_id)
    assert string_id == str(mongol.maybe_object_id(string_id))
    assert not_object_id == mongol.maybe_object_id(not_object_id)


@pytest.mark.asyncio
async def resource_test():
    collection = AsyncIOMotorClient("localhost").test[test_collection_name]
    test_repo = Repository(collection)

    for data in test_data:
        await test_repo.create(data)

    #: Test Searchs
    assert await test_repo.find()["_id"] is not None, "Find one"
    assert len(await test_repo.query()) == 2, "Query without param"
    assert await test_repo.find(test_data[0]["_id"]) is not None, "Find by ID"

    #: Test update
    test_record_id = test_data[0]["_id"]
    founded = await test_repo.find(test_record_id)
    founded["updated_field"] = True
    await test_repo.update(test_record_id, founded)
    assert await test_repo.find(test_record_id)["updated_field"] is True

    #: Test Delete
    await test_repo.delete(test_record_id)
    founded = await test_repo.find(test_record_id, include_deleted=True)
    assert founded["is_deleted"] is True
    assert await test_repo.find(test_record_id) is None

    await test_repo.collection.drop()


async def load_test_data(collection):
    for data in test_data:
        await collection.create(data)


def get_db():
    return AsyncIOMotorClient("localhost").test
