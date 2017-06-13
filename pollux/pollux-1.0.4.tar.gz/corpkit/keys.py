"""corpkit: simple keyworder"""

from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION
import pandas as pd
import math

def log_likelihood_measure(word_in_ref, word_in_target, ref_sum, target_sum):
    """
    Calculate log likelihood keyness"""
    neg = (word_in_target / float(target_sum)) < (word_in_ref / float(ref_sum))
    E1 = float(ref_sum)*((float(word_in_ref)+float(word_in_target)) / \
        (float(ref_sum)+float(target_sum)))
    E2 = float(target_sum)*((float(word_in_ref)+float(word_in_target)) / \
        (float(ref_sum)+float(target_sum)))
    
    if word_in_ref == 0:
        logaE1 = 0
    else:
        logaE1 = math.log(word_in_ref/E1)
    if word_in_target == 0:
        logaE2 = 0
    else:
        logaE2 = math.log(word_in_target/E2)
    score = float(2* ((word_in_ref*logaE1)+(word_in_target*logaE2)))
    if neg:
        score = -score
    return score

def perc_diff_measure(word_in_ref, word_in_target, ref_sum, target_sum):
    """calculate using perc diff measure"""
    norm_target = float(word_in_target) / target_sum
    norm_ref = float(word_in_ref) / ref_sum
    # Gabrielatos and Marchi (2012) do it this way!
    if norm_ref == 0:
        norm_ref = 0.00000000000000000000000001
    return ((norm_target - norm_ref) * 100.0) / norm_ref

def calc_keywords(row, df, selfdrop=True, measure_func=False, calc_all=False, threshold=False):
    """
    get keywords in target corpus compared to reference corpus
    this should probably become some kind of row-wise df.apply method
    """
    if selfdrop:
        df = df.drop(row.name)

    ref_ser = df.sum()
    ref_sum = ref_ser.sum()
    target_sum = row.sum()

    if not calc_all:
        good_words = list(row.index)

    vals = row.to_frame('target')
    vals['ref'] = ref_ser
    if not calc_all:
        vals = vals.dropna(subset='target')
    else:
        vals = vals.fillna(0)

    if threshold is not False:
        if isinstance(threshold, int):
            vals = vals[vals['target'] >= threshold]
        elif isinstance(threshold, float):
            vals = vals[vals['target'] * 100.0 / target_sum >= threshold]
        elif threshold is True:
            vals = vals[vals['target'] * 100.0 / target_sum >= 0.05]

    fnc = lambda a: measure_func(a[1], a[0], ref_sum, target_sum)
    done = vals.apply(fnc, axis=1, raw=True)
    return done

def keywords(target_corpus,
             subcorpora='default',
             show='w',
             reference_corpus=False,
             threshold=False,
             selfdrop=True,
             calc_all=True,
             measure='ll',
             sort_by=False,
             print_info=False,
             **kwargs):
    """
    Feed this function some target_corpus and get its keywords
    """
    from corpkit.interrogation import Results
    from corpkit.corpus import Corpus, LoadedCorpus

    make_table = False

    if isinstance(reference_corpus, bool):
        reference_corpus = target_corpus

    if isinstance(target_corpus, (LoadedCorpus, Results)):
        target_corpus = target_corpus.table(subcorpora, show)

    if isinstance(reference_corpus, (LoadedCorpus, Results)):
        reference_corpus = reference_corpus.table(subcorpora, show)

    # figure out which measure we're using
    if measure == 'll':
        measure_func = log_likelihood_measure
    elif measure == 'pd':
        measure_func = perc_diff_measure
    else:
        raise NotImplementedError("Only 'll' and 'pd' measures defined so far.")

    done = target_corpus.apply(calc_keywords,
                                df=reference_corpus,
                                selfdrop=selfdrop,
                                measure_func=measure_func,
                                calc_all=calc_all,
                                threshold=threshold,
                                axis=1)

    return done.sort(sort_by if sort_by else 'turbulent')
