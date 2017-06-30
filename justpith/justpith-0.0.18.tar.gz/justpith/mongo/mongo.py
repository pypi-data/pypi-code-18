from pymongo import MongoClient
from time import time

class Mongo:

    ##### GENERAL #####
    def __init__(self, host, port, db):
        self.host       = host
        self.port       = port
        self.db         = db

        self.client     = None
        self.connection = None
        self.connect()

    def connect(self):
        self.client     = MongoClient(self.host, self.port)
        self.connection = self.client[self.db]


    ##### JUSTPITH SERVER #####
    def insert_news(self, news):
        selected_collection = self.connection['News']
        result = selected_collection.insert(news)

    def update_news_report(self, id_news, queue_name, queue_op):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$push': {'report': {'queue_name': queue_name, 'queue_op': queue_op, 'timestamp': str(time())}}}, upsert=True)

    def update_news_after_parsing(self, id_news, ttl, article, article_cleaned, queue_name):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$set': {'TTL': ttl, 'article': article, 'article_cleaned': article_cleaned}, '$push': {'report': {'queue_name': queue_name, 'queue_op': 'IN', 'timestamp': str(time())}}}, upsert=True)

    def update_news_after_similarity(self, id_news, doc_sim, topic_sim):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'doc_sims': doc_sim, 'topic_sims': topic_sim}})


    ##### JUSTPITH WEB SERVICE TEXT ANALYSIS #####
    def get_docs_to_build_model(self, category):
        selected_collection = self.connection['News']
        result = selected_collection.find({'category_title': category})
        # docs = []
        # for doc in result:
        #     docs.append(doc['article'])
        # return docs
        return result

    def update_news_id_for_model(self, id_news, id_news_corpus):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'id_corpus': id_news_corpus}})


    def insert_index(self, data):
        selected_collection = self.connection['Indexes']
        result = selected_collection.insert(data)

    def update_active_index(self, id_index, active):
        result = self.connection['Indexes'].find_one_and_update({'_id': id_index}, {'active': active})

    def set_in_model(self):
        selected_connection = self.connection["News"]
        result = selected_connection.update_many({ "article_cleaned": { "$gt": [] } }, {"$set": {"in_model": 1}})