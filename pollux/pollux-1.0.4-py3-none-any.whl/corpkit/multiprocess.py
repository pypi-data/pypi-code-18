"""
corpkit: multiprocessing of searching
"""

from __future__ import print_function

def pmultiquery(corpus, 
                target=False,
                query=False,
                searchmode='all',
                multiprocess='default', 
                print_info=True,
                subcorpora=False,
                mainpath=False,
                countmode=False,
                **kwargs):
    """
    - Parallel process multiple queries or corpora.
    - This function is used by corpkit.interrogator.interrogator()
    - for multiprocessing.
    - There's no reason to call this function yourself.
    """
    import os
    import pandas as pd
    import collections
    from collections import namedtuple, OrderedDict
    from time import strftime, localtime
    from corpkit.interrogator import interrogator
    from corpkit.interrogation import Results
    from corpkit.process import canpickle, partition
    from corpkit.corpus import Corpus, File
    try:
        from joblib import Parallel, delayed
    except ImportError:
        pass
    import multiprocessing

    #if isinstance(corpus, Datalist):
    #    corpus = Corpus(corpus, level='d', print_info=False)

    locs = locals()
    for k, v in kwargs.items():
        locs[k] = v
    in_notebook = locs.get('in_notebook')
    #cname = kwargs.pop('cname')

    if not isinstance(multiprocess, int):
        multiprocess = multiprocessing.cpu_count()

    if getattr(corpus, 'files', False):
        files = corpus.files
    else:
        files = corpus

    num_files = len(files)

    chunks = partition(files, multiprocess)

    if len(chunks) < multiprocess:
        multiprocess = len(chunks)

    search = {target: query}

    # make a list of dicts to pass to interrogator,
    # with the iterable unique in every one
    basic_multi_dict = {'target': target,
                        'query': query,
                        'searchmode': searchmode,
                        #'just_metadata' = just_metadata,
                        'printstatus': False,
                        'multiprocess': False,
                        'mp': True,
                        'countmode': countmode,
                        'corpus_name': kwargs.get('corpus_name')}

    # make a new dict for every iteration
    ds = [dict(**basic_multi_dict) for i in range(multiprocess)]

    for index, (d, bit) in enumerate(zip(ds, chunks)):
        if not isinstance(bit, pd.DataFrame) and isinstance(bit[0], File):
            bit = [i.path for i in bit]
        d['paralleling'] = -index
        d['corpus'] = list(bit) if not isinstance(bit, pd.DataFrame) else bit

    print('\n')
    print('\n' * len(ds))

    res = Parallel(n_jobs=multiprocess)(delayed(interrogator)(**x) for x in ds)

    subc = subcorpora if kwargs.get('subcorpora') else 'default'

    # make our final big df
    res = [i for i in res if i is not None]
    df = [x for x, y in res]
    results = [y for x, y in res]
    df = pd.concat(df) if len(df) > 1 else df[0]
    results = pd.concat(results) if len(results) > 1 else results[0]

    if isinstance(df, pd.DataFrame):
        df = df.copy()
        df['_n'] = range(len(df))
        results = results.copy()
        results['_n'] = df._n

    interro = Results(matches=results, path=mainpath, reference=df)

    return interro
