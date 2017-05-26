from bson.objectid import ObjectId
import pymongo
from jsonschema import validate
from pymongo import ReturnDocument
from .error import Http400


class MongoC(object):
    def __init__(self, uri):
        self.co = pymongo.MongoClient(uri)

    def me(self):
        return self.co


class Mongo(object):
    def __init__(self, co, db, cl):
        self.co = co.me()
        self.db = self.co[db]
        self.cl = self.db[cl]
        self.schema = []

    def O2S(self, doc):
        if doc:
            doc.update({"_id": str(doc.get("_id"))})
        return doc

    def S2O(self, _id):
        return dict(_id=ObjectId(_id))

    def Validate(self, doc):
        try:
            if self.schema:
                validate(doc, self.schema)
        except Exception as e:
            Http400(e.message)

    def AddOne(self, doc):
        self.Validate(doc)
        self.cl.insert_one(doc)
        return self.O2S(doc)

    def GetAll(self, qry):
        return list(map(lambda i: self.O2S(i), self.cl.find(qry)))

    def GetOne(self, _id):
        return self.O2S(self.cl.find_one(self.S2O(_id)))

    def SetOne(self, _id, doc):
        return self.O2S(self.cl.find_one_and_update(self.S2O(_id),
                                                    {'$set': doc},
                                                    return_document=ReturnDocument.AFTER))

    def DelOne(self, _id):
        return self.O2S(self.cl.find_one_and_delete(self.S2O(_id)))

