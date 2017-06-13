import os
import sys
import codecs

# python 2/3 coompatibility
PYTHON_VERSION = sys.version_info.major
STRINGTYPE = str if PYTHON_VERSION == 3 else basestring
INPUTFUNC = input if PYTHON_VERSION == 3 else raw_input
OPENER = open if PYTHON_VERSION == 3 else codecs.open

# quicker access to search, exclude, show types
from itertools import product
_starts = ['M', 'N', 'B', 'G', 'D', 'H', 'R', 'O', 'A', 'Q']
_ends = ['W', 'L', 'I', 'S', 'P', 'X', 'R', 'F', 'N']
_others = ['A', 'ANY', 'ANYWORD', 'C', 'SELF', 'V', 'K', 'T']
_prod = list(product(_starts, _ends))
_prod = [''.join(i) for i in _prod]
_letters = sorted(_prod + _starts + _ends + _others)

_adjacent_start = ['A{}'.format(i) for i in range(1, 9)] + \
                   ['Z{}'.format(i) for i in range(1, 9)]

_adjacent = [''.join(i) for i in list(product(_adjacent_start, _prod))]

LETTERS = sorted(_letters + _adjacent)

# translating search values intro words
transshow = {'f': 'Function',
             'l': 'Lemma',
             'a': 'Distance from root',
             'w': 'Word',
             't': 'Trees',
             'i': 'Index',
             'n': 'NER',
             'p': 'POS',
             'c': 'Count',
             '+': 'Next',
             '-': 'Previous',
             'x': 'XPOS',
             's': 'Sentence index'}

transobjs = {'g': 'Governor',
             'd': 'Dependent',
             'm': 'Match',
             'h': 'Head'}

# for untokenising results
nospace_before = ["'s", "n't", "'re", "--", "''", "'", "'ve", 
                  "'d", "'ll", "'m", '-RCB-', '-RRB-', '-RSB-']

nospace_after = ['``', "`", "--", '-LCB-', '-LRB-', '-LSB-']

tok_trans = {'-LCB-': '{',
             '-RCB-': '}',
             '-LRB-': '(',
             '-RRB-': ')',
             '-LSB-': '[',
             '-RSB-': ']'}

# below are the column names for the conll-u formatted data
# corpkit's format is slightly different, but largely compatible.

# Key differences:
#
#     1. 'e' is used for NER, rather than lang specific POS
#     2. 'd' gives a comma-sep list of dependents, rather than head-deprel pairs
#        this is done for processing speed.
#     3. 'c' is used for corefs, not 'misc comment'. it has an artibrary number 
#        representing a dependency chain. head of a mention is marked with an asterisk.

# 'm' does not have anything in it in corpkit, but denotes morphological features

# default: index, word, lem, pos, ner, morph, gov, func, deps, coref
CONLL_COLUMNS = ['i', 'w', 'l', 'p', 'n', 'm', 'g', 'f', 'd', 'c']
# UD 2.0
CONLL_COLUMNS_V2 = ['i', 'w', 'l', 'x', 'p', 'm', 'g', 'f', 'e', 'o']

# we can also load and display governor features
GOV_ATTRS = ['gw', 'gl', 'gp', 'gf']

# what the longest possible speaker ID is. this prevents huge lines with colons
# from getting matched unintentionally
MAX_SPEAKERNAME_SIZE = 40

# parsing sometimes fails with a java error. if corpus.parse(restart=True), this will try
# parsing n times before giving up
REPEAT_PARSE_ATTEMPTS = 3

CORENLP_VERSION = '3.7.0'
CORENLP_URL  = 'http://nlp.stanford.edu/software/stanford-corenlp-full-2016-10-31.zip'
CORENLP_DIRNAME = os.path.splitext(os.path.basename(CORENLP_URL))[0]
_langs = ['english', 'german', 'chinese', 'arabic', 'spanish', 'french', 'english-kpb']
CORENLP_MODEL_URLS = {lang: 'http://nlp.stanford.edu/software/stanford-%s-corenlp-2016-10-31-models.jar' % lang for lang in _langs}

CORENLP_PATH = os.path.join(os.path.expanduser("~"), 'corenlp')
# it can be very slow to load a bunch of unused metadata categories
MAX_METADATA_FIELDS = 99
MAX_METADATA_VALUES = 99

STATS_FIELDS = ['Characters', 'Clauses', 'Closed class', 'Interrogative',
               'Modalised declarative', 'Open class', 'Open interrogative', 'Passives',
               'Punctuation', 'Tokens', 'Unmodalised declarative', 'Words']

import numpy as np
DTYPES = {'i': np.int32,
                  's': np.int64,
                  'w': "category",
                  'l': "category",
                  'p': "category",
                  'x': "category",
                  'g': np.int64,
                  'parse': object,
                  'f': "category",
                  'm': str,
                  'o': str,
                  'n': "category",
                  'gender': "category",
                  'speaker': "category",
                  'year': np.int64, # 'datetime64',
                  'date': "category", # 'datetime64',
                  'month': "category", # 'datetime64',
                  'postgroup': np.float64,
                  'totalposts': np.float64,
                  'postnum': np.float64}

CORENLP_COREF_CATS = ['PronType',
                      'Gender',
                      'VerbForm',
                      'NumType',
                      'Animacy',
                      'Mood',
                      'Poss',
                      'Number',
                      'Tense',
                      'Reflex',
                      'Case',
                      'Aspect',
                      'Foreign',
                      'Definite',
                      'Voice',
                      'Abbr',
                      'Degree',
                      'Evident',
                      'Polarity',
                      'Person',
                      'Polite']

CONC_CONTEXT = 20