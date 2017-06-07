from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords as stopset
import string

stopset = set(stopset.words('english')+[p for p in string.punctuation])

class Pre():
    def __init__(self, max_df, min_df, max_features, language ):
        self.max_df = max_df
        self.tfidf_vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, max_features=max_features, stop_words=language)

    def get_tfidf(self,texts):
        tfidf = self.tfidf_vectorizer.fit_transform(texts)
        return [self.tfidf_vectorizer, tfidf]

