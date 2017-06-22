from __future__ import division
from __future__ import print_function

import topiceval.preprocessing.params as params
# from topiceval.preprocessing.textcleaning import get_shorter_lem_word

from gensim import corpora
import numpy as np

from collections import defaultdict
import re
import logging


def prune_word_frequency(texts, least_freq):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] >= least_freq] for text in texts]
    return texts


def remove_threads(text):
    text = re.sub(r'^From: .*', ' ', text, flags=re.MULTILINE | re.DOTALL)
    return text


def remove_signature(text):
    signatures = ["regards", "best", "thanking you", "thanks", "sincerely", "warm regards", "best regards"]
    for signature in signatures:
        text = re.sub(r'^%s[^a-z]*?$.*?(<meta>){0, 1}' % signature, ' ', text,
                      flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    # for name in names:
    #     text = re.sub(r'^%s.*' % name, ' ', text, flags=re.IGNORECASE)
    return text


def make_doc2bow(df, dirname):
    texts = [[word for word in document.split()] for document in df['CleanBody']]
    texts = prune_word_frequency(texts=texts, least_freq=params.word_least_corpus_frequency)
    id2word_dict = corpora.Dictionary(texts)
    # Prune 10 most frequent words
    id2word_dict.filter_n_most_frequent(params.filter_n_most_frequent)
    # Remove words in <5 docs, in more than 50% of docs, and keep vocab size to max 3000
    id2word_dict.filter_extremes(no_below=params.word_least_document_frequency,
                                 no_above=params.word_highest_document_fraction, keep_n=params.max_vocab)
    logging.info("vocabulary size: %d" % len(id2word_dict))
    # Making corpus
    corpus = [id2word_dict.doc2bow(text) for text in texts]
    # Truncate corpus by removing docs of length < 10
    doc_indices_to_keep = truncate_corpus(corpus, min_len_doc=params.document_min_length)
    logging.info("Number of emails retained: %d (of %d)" % (len(doc_indices_to_keep), len(corpus)))
    trunc_corpus = [corpus[i] for i in doc_indices_to_keep]
    logging.info("Saving id2word_dict and corpus...")
    id2word_dict.save(dirname + 'id2word_dict.pickle')
    np.save(dirname + "corpus.npy", trunc_corpus)
    np.save(dirname + "dfindices_in_corpus.npy", doc_indices_to_keep)
    return id2word_dict, trunc_corpus


def len_doc(list_of_tups):
    length_doc = 0
    for tup in list_of_tups:
        length_doc += tup[1]
    return length_doc


def truncate_corpus(corpus, min_len_doc=10):
    good_indices = []
    for i, doc in enumerate(corpus):
        if len_doc(doc) >= min_len_doc:
            good_indices.append(i)
    return good_indices


def replace_names(text, names):
    for name in names:
        try:
            text = re.sub(r'%s' % name, '<name>', text)
        except:
            continue
    return text
