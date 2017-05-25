from bson.objectid import ObjectId
import pymongo
from pymongo import ReturnDocument


class Mongo(object):
    def __init__(self, uri, db, cl):
        self.co = pymongo.MongoClient(uri)
        self.db = self.co[db]
        self.cl = self.co[cl]

    def O2S(self, doc):
        if doc:
            doc.update({"_id": str(doc.get("_id"))})
        return doc

    def S2O(self, _id):
        return dict(_id=ObjectId(_id))

    def AddOne(self, doc):
        self.cl.insert_one(doc)
        return doc

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

