# -*- coding: utf-8 -*-
import logging

import itertools
import re

from gensim.models.doc2vec import TaggedDocument

from pynlple.data.corpus import StackingSource, FilteringSource, JsonFieldSource, MappingSource, SplittingSource
from pynlple.data.filesource import FilePathSource
from pynlple.data.datasource import TsvDataframeSource, JsonDataframeSource
from pynlple.data.jsonsource import FileJsonDataSource
from pynlple.processing.preprocessor import DefaultPreprocessorStack, RegexReplacerAdapter
from pynlple.module import abs_path, append_paths
from gensim import models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

replacers_stack = DefaultPreprocessorStack()

# mentions_path = 'F:/data/youscan/2017.04.28/100894_mentions_rus.json'
mentions_path = 'E:\\Projects\\YouScan\\data-science-lab\\data\\youscan\\2017-04-26\\100894_mentions.json'
mentions_source = FileJsonDataSource(mentions_path)
text_source = JsonFieldSource(mentions_source, 'text')
notnan_text_source = FilteringSource(text_source, lambda t: t is not None and type(t) is str)
# line_source = SplittingSource(text_source, lambda t: re.split(r'[\r\n]+', t))
line_source = notnan_text_source
line_token_source = MappingSource(line_source, lambda t: {'text': t, 'tokens': replacers_stack.preprocess(t).split()})

n = 3
long_sentences_source = FilteringSource(line_token_source, lambda s: len(s['tokens']) >= n)

entries_source = MappingSource(long_sentences_source, lambda d: dict(d, **{'doctag': [str(hash(' '.join(d['tokens']))),]}))

published_source = JsonFieldSource(mentions_source, 'published')
entries = [dict(entry, **{'published': published, 'text': text}) for entry, published, text in zip(entries_source, published_source, line_source)]
out_ = FileJsonDataSource('E:\\Projects\\YouScan\\data-science-lab\\data\\youscan\\2017-04-26\\100894_mentions_doctag.json').set_data(entries)

source = MappingSource(entries_source, lambda s: TaggedDocument(s['tokens'], s['doctag']))
key = '100894' + '_texts_min_tokens=' + str(n)
pars = dict(
    size=200,
    window=8,
    dm=0,
    dbow_words=1,
    seed=13,
    min_count=2,
    iter=10,
    workers=3
)
params = '_'.join(repr(key) + '=' + repr(pars[key]) for key in sorted(pars.keys()))
vocab_name = 'gensim_doc2vec_' + key + '_' + params + '.voc'
vocab_path = append_paths(abs_path('model/'), vocab_name)
model_name = 'gensim_doc2vec_' + key + '_' + params + '.tst'
model_path = append_paths(abs_path('model/'), model_name)

model = models.Doc2Vec(None, **pars)
model.scan_vocab(source, progress_per=5000, trim_rule=None, update=False)
model.save(vocab_path)
print('Vocabulary building step finished. Vocabulary saved.')
# print('Loading vocabulary.')
# model = models.Doc2Vec.load(vocab_path)

model.scale_vocab(keep_raw_vocab=False, trim_rule=None, update=False)
model.finalize_vocab(update=False)
model.train(source)
model.save(model_path)
print('First training step finished.')

# model = models.Doc2Vec.load(model_path)
# print ('Model ' + model_name + ' was successfully loaded.')