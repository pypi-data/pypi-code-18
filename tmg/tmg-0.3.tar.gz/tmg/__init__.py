import sys
sys.path.append('/Users/rocco/tensorflow/lib/python2.7/site-packages')

import numpy as np
from preprocess import Pre
from dynamics import Dynamics
from sklearn.datasets import fetch_20newsgroups
n_samples = 2000
from time import time

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.tolist()):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in np.array(topic).argsort()[:-n_top_words - 1:-1]]))
    print()

def load_20ng():
    print("Loading dataset...")
    t0 = time()
    dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
    data_samples = dataset.data[:n_samples]
    print("done in %0.3fs." % (time() - t0))
    return data_samples

class tmg():
    def __init__(self, n_top_words = 25, max_df=0.95,min_df=2,max_features = 1000, language = 'english'):
        self.name = 'tmg'
        self.n_top_words = n_top_words
        self.max_df = max_df
        self.min_df= min_df
        self.max_features=max_features
        self.language=language

    def model(self,texts):
        Prep = Pre(self.max_df, self.min_df, self.max_features, self.language)
        [self.tfidf_vectorizer, self.tfidf] = Prep.get_tfidf(texts)
        Game_dyn = Dynamics()
        [self.topics,self.graph,self.p_iterations] = Game_dyn.games(self.tfidf)
        self.tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()

    def example(self):
        texts = load_20ng()
        model = self.model(texts)
        return model
        #print("\nTopics in GTG model:")
        #print_top_words(model.topics, model.tfidf_feature_names, self.n_top_words)
