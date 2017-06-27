from pymongo import MongoClient
from time import time

class Mongo:
    def __init__(self, host, port, db):
        self.host       = host
        self.port       = port
        self.db         = db

        self.client     = None
        self.connection = None

    def connect(self):
        self.client     = MongoClient(self.host, self.port)
        self.connection = self.client[self.db]

    def insert_news(self, news):
        selected_collection = self.connection['News']
        result = selected_collection.insert(news)

    def update_news_report(self, id_news, queue_name, queue_op):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$push': {'report': {'queue_name': queue_name, 'queue_op': queue_op, 'timestamp': str(time())}}}, upsert=True)

    def update_news_after_parsing(self, id_news, ttl, article_cleaned):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$set': {'TTL': ttl, 'article_cleaned': article_cleaned}}, upsert=True)

    def update_news_after_similarity(self, id_news, doc_sim, topic_sim):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'doc_sims': doc_sim, 'topic_sims': topic_sim}})

    def get_docs_to_build_lda(self, category_id):
        selected_collection = self.connection['News']
        result = selected_collection.find({'category_id': category_id})
        docs = []
        for doc in result:
            docs.append(doc['article_cleaned'])
        return docs
