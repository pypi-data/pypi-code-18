# -*- coding: utf-8 -*-
import math
from pymongo import MongoClient

class PMI(object):
    """docstring for PMI"""
    def __init__(self, uri=None):
        self.client = MongoClient(uri)
        self.db = self.client['nlp']
        self.Collect = self.db['pmi']
        self.frequency = {}

    def checkHasPMI(self, keyword):
        result = self.Collect.find({'key':keyword}, {'freq':1, 'value':1, '_id':False}).limit(1)
        if result.count() == 0:
            return False
        return True

    def getWordFreqItems(self):
        # result all frequency of word in type of dict.
        self.frequency = {}
        frequency_of_total_keyword = 0
        for i in self.db['kcm'].find():
            keyword = i['key']
            for correlationTermsArr in i['value']:
                corTermCount = correlationTermsArr[1]
                frequency_of_total_keyword += corTermCount
                # accumulate keyword's frequency.
                self.frequency[keyword] = self.frequency.setdefault(keyword, 0) + corTermCount

        return frequency_of_total_keyword, self.frequency.items()

    def build(self):
        import pymongo
        self.Collect.remove({})
        frequency_of_total_keyword, WordFreqItems = self.getWordFreqItems()
        print('frequency of total keyword:'+str(frequency_of_total_keyword))
        # read all frequency from KCM and build all PMI of KCM in MongoDB. 
        # with format {key:'中興大學', freq:100, value:[(keyword, PMI-value), (keyword, PMI-value)...]}
        result = []
        for keyword, keyword_freq in WordFreqItems:
            pmiResult = []

            for kcm_pair in list(self.db['kcm'].find({'key':keyword}, {'value':1, '_id':False}).limit(1))[0]['value']:
                kcmKeyword, kcmCount = kcm_pair[0], kcm_pair[1]

                # PMI = log2(p(x, y)/p(x)*p(y)) 
                # p(x, y) = frequency of (x, y) / frequency of total keyword.
                # p(x) = frequency of x / frequency of total keyword.
                value=(math.log10( int(kcmCount) * frequency_of_total_keyword  /(float(keyword_freq) * int(self.frequency[kcmKeyword])  )) / math.log10(2))

                # this equation is contributed by 陳聖軒. 
                # contact him with facebook: https://www.facebook.com/henrymayday
                value*=(math.log10(int(self.frequency[kcmKeyword]))/math.log10(2))

                pmiResult.append((kcmKeyword, value))

            pmiResult = sorted(pmiResult, key = lambda x: -x[1])
            result.append({'key':keyword, 'freq':keyword_freq, 'value':pmiResult})

        self.Collect.insert(result)
        self.Collect.create_index([("key", pymongo.HASHED)])

    def get(self, keyword, amount):
        # return PMI value of this keyword
        # if doesn't exist in MongoDB, then return [].

        if self.checkHasPMI(keyword):
            return list(self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1))[0]['value'][:amount]
        return []