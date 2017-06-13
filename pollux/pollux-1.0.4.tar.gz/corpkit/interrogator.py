"""
corpkit: Interrogate a parsed corpus
"""

from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION, INPUTFUNC

def interrogator(corpus,
                 target='w',
                 query=False,
                 searchmode='all',
                 case_sensitive=False,
                 inverse=False,
                 just=False,
                 skip=False,
                 multiprocess=False,
                 regex_nonword_filter=r'[A-Za-z0-9]',
                 no_closed=False,
                 no_punct=False,
                 countmode=False,
                 coref=False,
                 low_memory=False,
                 no_store=False,
                 just_index=False,
                 df=False,
                 cols=None,
                 **kwargs):
    """
    Interrogate corpus, corpora, subcorpus and file objects.
    See `corpkit.corpus.Corpus.search` for docstring
    """

    import signal
    import os
    import re

    from time import localtime, strftime
    from traitlets import TraitError

    import pandas as pd
    from tqdm import tqdm, tqdm_notebook
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            tqdm = tqdm_notebook
    except:
        pass

    from corpkit.interrogation import Results
    from corpkit.corpus import File, Corpus, LoadedCorpus
    from corpkit.conll import pipeline, path_to_df
    from corpkit.query import preprocess_depgrep
    from corpkit.process import partition
    
    # for hdf5 corpora
    if isinstance(corpus, str):
        from corpkit.hdf5 import determine_corpus
        corpus = determine_corpus(corpus, search={target: query}, is_new=False)

    # so you can do corpus.interrogate('features/postags/wordclasses/lexicon')
    if target == 'features':
        target = 'v'
        query = r'.*'
        countmode = True

    if regex_nonword_filter:
        is_a_word = re.compile(regex_nonword_filter)
    else:
        is_a_word = re.compile(r'.*')

    # convert cql-style queries---pop for the sake of multiprocessing
    #cql = kwargs.pop('cql', None)
    #if cql:
    #    from corpkit.cql import to_corpkit
    #    search, _ = to_corpkit(search)

    # set up pause method
    original_sigint = signal.getsignal(signal.SIGINT)
    paralleling = kwargs.get('paralleling', None) is not None

    def signal_handler(signal, _):
        """
        Allow pausing and restarting whn not in GUI
        """
        import signal
        import sys
        from time import localtime, strftime
        signal.signal(signal.SIGINT, original_sigint)
        thetime = strftime("%H:%M:%S", localtime())
        INPUTFUNC('\n\n%s: Paused. Press any key to resume, or ctrl+c to quit.\n' % thetime)
        time = strftime("%H:%M:%S", localtime())
        print('%s: Interrogation resumed.\n' % time)
        signal.signal(signal.SIGINT, signal_handler)

    if paralleling is None:
        original_sigint = signal.getsignal(signal.SIGINT)
        try:
            signal.signal(signal.SIGINT, signal_handler)
        except ValueError:
            pass

    results = []
    df_bits = []
    
    try:
        nam = get_ipython().__class__.__name__
        if nam == 'ZMQInteractiveShell':
            in_notebook = True
        else:
            in_notebook = False
    except (ImportError, AttributeError, NameError, TraitError):
        in_notebook = False

    cname = getattr(corpus, 'name', kwargs.get('corpus_name'))

    # make the iterable, which should be very simple now
    # if the user passed in a df, it is a complete loadedcorpus
    corpus_is_loaded = type(corpus) == LoadedCorpus
    corpus_is_result = type(corpus) == Results
    corpus_is_df = type(corpus) == pd.DataFrame
    
    comp_tgrep = str(query) if target == 't' else False
    tgrep_string = str(query) if target == 't' else False

    # todo: wrong in the case of getting something from store
    # corpus_is_df might be a bad solution
    prog_bar_here = True
    if corpus_is_loaded or corpus_is_result or corpus_is_df:
        if target in ['t' ,'d', 'c']:
            prog_bar_here = False

    # here we will need to guess what to do with df searches...
    if isinstance(corpus, pd.DataFrame) and not corpus_is_loaded and not corpus_is_result:
        if getattr(corpus, 'reference', False) is False:
            corpus_is_loaded = True
        elif df is not False:
            corpus_is_result = True
        else:
            corpus_is_result = True

    # split anything if we are multiprocessing
    if multiprocess is not False:
        corpus_iter = partition(corpus, multiprocess)
    else:
        # if it has files, get those
        if isinstance(corpus, Corpus):
            corpus_iter = list(corpus.filepaths)
        elif isinstance(corpus, pd.DataFrame):
            corpus_iter = [corpus]
        else:
            corpus_iter = corpus

    if comp_tgrep:
        from nltk.tgrep import tgrep_compile
        comp_tgrep = tgrep_compile(comp_tgrep)
    
    # if the user added any fancy modifiers onto the end of depgrep, add them to search
    depgrep_string, search, offset = preprocess_depgrep(target, query, case_sensitive)

    if target == 'v':
        from corpkit.process import make_compiled_statsqueries
        comp_tgrep = make_compiled_statsqueries()

    running_count = 0
    running_len = 0

    if multiprocess:
        from joblib import Parallel, delayed
        basic_multi_dict = dict(target=target,
                                query=query,
                                multiprocess=False,
                                corpus_name=cname,
                                no_store=no_store,
                                just_index=just_index,
                                low_memory=low_memory,
                                case_sensitive=case_sensitive,
                                coref=coref,
                                mp=True)
        print('\n')
        print('\n' * len(corpus_iter))
        if len(corpus_iter) < multiprocess:
            multiprocess = len(chunks)
        res = Parallel(n_jobs=multiprocess)(delayed(interrogator)(corpus=d, paralleling=-i, **basic_multi_dict) for i, d in enumerate(corpus_iter))
        # make our final big df
        res = [i for i in res if i is not None]
        df = [x for x, y in res]
        results = [y for x, y in res]
        if no_store or low_memory:
            df = False
        else:
            df = pd.concat(df, copy=False) if len(df) > 1 else df[0]
        results = pd.concat(results, copy=False) if len(results) > 1 else results[0]
        
        # review this
        if isinstance(df, pd.DataFrame):
            df = df.copy()
            results = results.copy()

        # do not store the whole df again
        if corpus_is_loaded:
            reference = False
        interro = Results(matches=results, path=getattr(corpus, 'path', False), reference=df)
        return interro

    else:

        if prog_bar_here:
            t = tqdm(total=len(corpus_iter),
                     desc="Searching corpus",
                     position=kwargs.get('paralleling', 0),
                     ncols=120,
                     unit="file")
        fname = False

        for i, f in enumerate(corpus_iter, start=1):
            subc = get_subc(f, cname)
            # load in the full df now
            if isinstance(f, (Corpus, File, str)):
                fname = os.path.basename(getattr(f, 'name', f))
                f = path_to_df(getattr(f, 'path', f),
                               corpus_name=cname,
                               corp_folder=subc,
                               v2=kwargs.get('v2', 'auto'),
                               skip_morph=kwargs.get('skip_morph'),
                               add_gov=kwargs.get('add_gov', False),
                               usecols=cols,
                               drop=kwargs.get('drop', False),
                               cur_len=running_len,
                               just=just,
                               skip=skip)
                running_len += len(f)

            elif isinstance(f, (LoadedCorpus, pd.DataFrame)):
                if just is not False:
                    bools = []
                    for k, v in just.items():
                        bools.append(f[k].str.contains(v, case=False))
                    bools = pd.concat(bools, axis=1)
                    f = f[bools.any(axis=1)]

                if skip is not False:
                    bools = []
                    for k, v in skip.items():
                        bools.append(f[k].str.contains(v, case=False))
                    bools = pd.concat(bools, axis=1)
                    f = f[~bools.any(axis=1)]

            if search.get('d'):
                from corpkit.query import depgrep_compile
                to_comp = df if df is not False else f
                search['d'] = depgrep_compile(depgrep_string[:offset], df=to_comp,
                                              case_sensitive=case_sensitive)

            #if cols is not False and cols is not None:
            #    tc = cols + ['_n', 'sent_len']
            #    if 'parse' in f.columns and search.get('t', False):
            #        tc.append('parse')
            #    f = f[tc]
            res = pipeline(df=f,
                           search=search,
                           searchmode=searchmode,
                           case_sensitive=case_sensitive,
                           no_punct=no_punct,
                           no_closed=no_closed,
                           coref=coref,
                           countmode=countmode,
                           is_a_word=is_a_word,
                           corpus=corpus,
                           comp_tgrep=comp_tgrep,
                           depgrep_string=depgrep_string,
                           corpus_result=corpus_is_result,
                           corpus_loaded=corpus_is_loaded,
                           **kwargs)



            if inverse:
                res = f.drop(res.index)
                #res = f.loc[~f.index]
                #res = f.loc[list(set(f.index) - set(res.index))]

            if no_store or corpus_is_loaded:
                f = None
            
            if low_memory:
                # reduce the whole df to just the items in the ngram
                if '_gram' in f:
                    ixes = []
                    splt = res._gram.apply(lambda x: pd.Series(x.split(','))).fillna(0)
                    for i, d in splt.iterrows():
                        for v in d.values:
                            if not int(v):
                                continue
                            made = (i[0], i[1], int(v))
                            ixes.append(made)

                    f = f.loc[ixes]
                    f = f.drop_duplicates()
                else:
                    # what should this reduce to?
                    raise NotImplementedError

            if f is not None:
                df_bits.append(f)

            if prog_bar_here:
                n = len(res) if res is not None else 0
                running_count += n
                kwa = dict(results=format(running_count, ','))
                if fname is not False:
                    kwa['f'] = fname
                t.set_postfix(**kwa)
                t.update()

            # if no results, just skip
            pand = (pd.Series, pd.DataFrame)
            if res is None or not len(res) or (isinstance(res, pd.DataFrame) and res.empty):
                continue
            results.append(res)

    if prog_bar_here:
        t.close()

    if results is None or not len(results):
        try:
            signal.signal(signal.SIGINT, original_sigint)
        except ValueError:
            pass
        return

    # searching all done. remember what we did:
    querybits = dict(search=search,
                     searchmode=searchmode,
                     depgrep_string=depgrep_string,
                     tgrep_string=tgrep_string,
                     inverse=inverse,
                     case_sensitive=case_sensitive)

    # make our final big df if need be, or inherit it
    if corpus_is_loaded:
        df = corpus
    else:
        df = getattr(corpus, 'reference', None)
    if not no_store and not corpus_is_loaded and df is None:
        df = pd.concat(df_bits) if len(df_bits) > 1 else df_bits[0]

    # join results
    results = pd.concat(results) if len(results) > 1 else results[0]

    # invert the results it need be --- not sure if optimised

    if just_index:
        if '_gram' in results.columns:
            results = results[['w', '_gram']]
        else:
            results = results[['w']]
    
    if no_store:
        try:
            df = Corpus(corpus.path)
        except (TypeError, AttributeError):
            df = False

    # make interrogation here, or, if mulitprocessing, just send the result back
    if paralleling:
        return df, results

    try:
        signal.signal(signal.SIGINT, original_sigint)
    except ValueError:
        pass

    # add an _n attribute
    #if isinstance(df, pd.DataFrame):
    #    if list(df.index) != list(range(len(df))):
    #        df = df.copy()
    #    if not corpus_is_loaded:
    #        results = results.copy()
    
    if search.get('d'):
        qstring = depgrep_string 
    elif search.get('t'):
        qstring = tgrep_string
    else:
        qstring = False

    interro = Results(results, reference=df, path=getattr(corpus, 'path', False), qstring=qstring)

    return interro


def get_subc(f, cname):
    """
    Try to determine what the subcorpus name is
    """
    import os
    subc = getattr(f, '_subcorpus', None)
    if subc is None:
        f = getattr(f, 'path', f)
        try:
            subc = os.path.basename(os.path.dirname(f))
        except TypeError:
            return False
        if subc == cname:
            subc = False
    return subc
