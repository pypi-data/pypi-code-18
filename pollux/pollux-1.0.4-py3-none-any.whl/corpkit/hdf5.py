import os
import re
import pandas as pd
import numpy as np
from corpkit.query import preprocess_depgrep

def determine_corpus(name_or_df,
                     search=False,
                     is_new=False,
                     matches=False,
                     need_sents=False,
                     store_path='~/corpora/corpora.h5',
                     case_sensitive=False):
    """
    Give the user the minimum-memory object from which they can search,
    but return a high-memory object if it was passed in
    
    Return: DataFrame to search from
    """
    # if we were given a corpus and don't have to cut it down
    if not isinstance(name_or_df, str) and matches is False:
        return name_or_df
    # cut down an in memory corpus and return it
    elif not isinstance(name_or_df, str) and matches is not False:
        return name_or_df.iloc[matches.index]

    # otherwise, we have to go to the store
    storepath = os.path.expanduser(store_path)
    try:
        hdf = pd.HDFStore(storepath)
    except ImportError:
        raise ValueError("You need HDF5 installed for this.")

    # not sure we should ever get here, for for new corpora, return each sentence once
    if is_new:
        return hdf.select(name_or_df, 'i=1')

    # if we are dep searching, we try to cut down by inspecting the query, getting
    # the first part, and returning only those sents
    if search and search.get('d'):
        depgrep_string, search, offset = preprocess_depgrep(search, case_sensitive)
    
    if matches is not False:
        if not search:
            search = {}
        if 'd' not in search and not need_sents:
            mats = list(matches.index)
            return hdf.select(name_or_df, 'index in mats')

        # revise this, faster mask needed
        fsi = hdf.select(name_or_df, columns=['file', 's', 'i']).set_index(['file', 's', 'i'])
        if need_sents or 'd' in search:
            mask = fsi.droplevel('i').isin(set(matches.index.droplevel('i')))
        else:
            mask = fsi.isin(set(matches.index))
        return hdf.select(name_or_df, where=mask)

    if search is False:
        return hdf[name_or_df]

    ob, att = next((k, v) for k, v in search.items() if k != 'd')

    # get a list of the relevant categories
    try:
        poss_vals = list(hdf.select(name_or_df, 'columns=ob')[ob].cat.categories)
    except AttributeError:
        poss_vals = list(set(hdf.select(name_or_df, 'columns=ob')[ob]))
    if isinstance(search, list):
        good_ones = [i for i in poss_vals if i in att]
    else:
        good_ones = [i for i in poss_vals if re.search(att, i)]

    # get sents, cut down
    if 'd' in search or need_sents:
        ix = hdf.select(name_or_df, columns=["file", "s", "i"]).index
        fs = ix.droplevel('i')
        matches = hdf.select(name_or_df, '%r=good_ones' % ob, columns=['file', 's', 'i', ob])
        matches = matches.index.droplevel('i').unique()
        mask = fs.isin(set(matches))
        return hdf.select(name_or_df, where=mask)
    else:
        return hdf.select(name_or_df, '%r=good_ones' % ob)

def make_all(table=True, do_json=True, colmax={}, **kwargs):

    import os
    import json
    import gc
    import pandas as pd
    from pollux.config import CORPUS_DIR, TOP_RESULTS, COLLAPSE_TREE_PUNCTUATION

    from corpkit.corpus import Corpus
    from corpkit.constants import DTYPES
    from corpkit.jsons import make_all_views_for

    import numpy as np

    #CORPUS_DIR = os.path.expanduser('~/corpora')
    USER = False
    UPLOAD_FOLDER = os.path.join(CORPUS_DIR, 'uploads')
    storepath = os.path.join(CORPUS_DIR, 'corpora.h5')
    jsonpath = os.path.join(CORPUS_DIR, 'views.json')

    from nltk.tree import ParentedTree

    corpus_json = {}
    dicts = []

    try:
        os.remove(storepath)
    except OSError:
        pass

    hdf_ok = True

    try:
        store = pd.HDFStore(storepath)
    except ImportError:
        hdf_ok = False
        print("\n\nWARNING: HDF5 not installed. This will slow things down.\n\n")

    projects = [os.path.join(CORPUS_DIR, d) for d in os.listdir(CORPUS_DIR)
                if os.path.isdir(os.path.join(CORPUS_DIR, d)) and d not in ['uploads', '_tmp']]

    # add user projects
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    if USER is not False:
        user_dirs = [os.path.join(UPLOAD_FOLDER, USER)]
    else:
        user_dirs = [d for d in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, d))]

    for d in user_dirs:
        userdir = os.path.join(UPLOAD_FOLDER, d)
        user_corp = [os.path.join(userdir, d) for d in os.listdir(userdir) if os.path.isdir(os.path.join(userdir, d)) and d.endswith('-parsed')]
        for i in user_corp:
            projects.append(i)

    # turn each project into a dict for the table
    for xx, parsed in enumerate(projects):

        corpus = Corpus(parsed)
        path = corpus.path
        nfiles = len(corpus.files)
        lang = corpus.metadata.get('lang', 'English')
        desc = corpus.metadata.get('desc', "No description")
        name = os.path.basename(corpus.path.replace('-parsed', ''))
        print('Starting: %s' % name)
        corpus = corpus.load(load_trees=not table, v2='auto', multiprocess=3)

        print("Creating store for %s ..." % name)

        kwargs = {'corpus_name': name, 'corpus': False, 'TOP_RESULTS': TOP_RESULTS,
                  'COLLAPSE_TREE_PUNCTUATION': COLLAPSE_TREE_PUNCTUATION}

        print("COLS:", corpus.columns)

        if do_json:
            corpus_json[name] = make_all_views_for(corpus, is_new=True,
                corp=corpus, cols=corpus.columns, **kwargs)
            
            cdict = {'name': name,
                     'path': path,
                     'lang': lang,
                     'desc': desc,
                     'parsed': "True",
                     'nsents': format(0, ','),
                     'nfiles': format(nfiles, ',')}

            dicts.append(cdict)
            print("JSON generated for %s" % name)

        if hdf_ok:

            print("Corpus prepared")
            corpus.store_as_hdf(path=storepath, name=name, colmax=colmax, **kwargs)
            corpus = None
            del corpus
            gc.collect()

    if do_json:
        from corpkit.jsons import JEncoder
        tup = [dicts, corpus_json]
        with open(jsonpath, 'w') as outfile:
            print("Writing JSON ... ")
            json.dump(tup, outfile, cls=JEncoder)
