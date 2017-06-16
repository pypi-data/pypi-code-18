from pymongo.errors import PyMongoError

from core.logger.base.corebaselogger import CoreBaseLogger
from pymongo import MongoClient

from core.utils.coreutils import CoreUtils


class CoreLoggerMongo(CoreBaseLogger):
    def __init__(self, db, collection, host=None, port=None, max_pool_size=100):
        super(CoreLoggerMongo, self).__init__()
        try:
            self.mongo = MongoClient(host, port, max_pool_size)
            self.database = self.mongo[db]
            self.collection = self.database[collection]
        except PyMongoError as error:
            print error

    def addLogEntry(self, message):
        if self.mongo:
            self.collection.insert({"_id": CoreUtils.timeStamp(), "value": self.createEntryFrom(message)})
