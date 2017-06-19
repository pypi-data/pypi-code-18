from __future__ import division
from __future__ import print_function

from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np

import re
import os


def get_shorter_lem_word(word, lemma=WordNetLemmatizer()):
    try:
        nword = lemma.lemmatize(word, 'n')
        if len(nword) < len(word):
            return nword
        vword = lemma.lemmatize(word, 'v')
        if len(vword) < len(word):
            return vword
        else:
            return word
    except Exception as e:
        print('Exception during lemmatization for word: %s' % word)
        print(e)
        return word


def clean_text(text):
    """ Return clean lemmatized text """
    lemma = WordNetLemmatizer()
    path = os.path.dirname(os.path.abspath(__file__))
    path = '/'.join(path.split("\\")[:-1])
    try:
        stop = np.append(np.load(path + "/data/stopwords.npy"), "<meta>")
    except FileNotFoundError:
        stop = np.append(np.load(path + "/topiceval/data/stopwords.npy"), "<meta>")
    text = text.lower()
    text = re.sub(r'[<>]', ' ', text)
    text = re.sub(r'(^to:.*)|(^from: .*)|(^cc:.*)|(^bcc:.*)|(^subject:.*)|(^sent:.*)|(^sent by:.*)', '<meta>', text,
                  flags=re.MULTILINE)
    text = re.sub(r'-{5}original .*?-{5}', ' ', text)
    # text = remove_signature(text)
    text = re.sub(r'[^@]+@[^@]+\.[^@]+', '<email>', text)
    text = re.sub(r'(http://[^ ]+)|([^ ]+\.com)|([^ ]+\.co\.in)', ' <url> ', text)
    text = re.sub(r'([^a-z]|^)(monday|mon|tuesday|tue|wednesday|wed|thursday|thu|friday|fri)([^a-z]|$)',
                  '\g<1><weekday>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([^a-z]|^)(saturday|sunday)([^a-z]|$)', '\g<1><weekend>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([^a-z]|^)(january|jan|february|feb|march|april|apr|june|jun|july|jul|august|aug|september|sept'
                  r'|october|oct|november|nov|december|dec)([^a-z]|$)', '\g<1><month>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([0-9]{1,2}:[0-9]{2}( ?)(am|pm|noon|afternoon|evening|morning|night)?)|(\d{1,2}( ?)'
                  r'(am|pm|noon|afternoon|evening|morning|night))', ' <time> ', text)
    text = re.sub(r'(dd/mm/yy)|(\d+/\d+/\d+)|(<month> \d{1,2}(st|nd|rd|th)?)', ' <date> ', text)
    text = re.sub(r'(\$|rs\.?)( ?)[0-9.]+', ' <money> ', text)
    text = re.sub(r'([^a-z]|^)[0-9]+([^a-z]|$)', '\g<1><number>\g<2> ', text)
    text = re.sub(r'[^a-zA-Z<>_\-]', ' ', text)
    text = re.sub(r'-{2,}|_{2,}', ' ', text)
    text = re.sub(r'-[^a-z<>]|[^a-z<>]-', ' ', text)
    words = text.split()
    words = [get_shorter_lem_word(w, lemma) for w in words if (len(w) > 1 and w not in stop and
                                                               lemma.lemmatize(w) not in stop and
                                                               lemma.lemmatize(w, 'v') not in stop)]
    return ' '.join(words)


def remove_signature(text):
    signatures = ["regards", "best", "thanking you", "thanks", "sincerely", "warm regards"]
    for signature in signatures:
        text = re.sub(r'^%s ?$.*' % signature, ' ', text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    # for name in names:
    #     text = re.sub(r'^%s.*' % name, ' ', text, flags=re.IGNORECASE)
    return text
