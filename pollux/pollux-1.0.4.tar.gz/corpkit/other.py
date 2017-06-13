from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION, INPUTFUNC

"""
In here are functions used internally by corpkit, but also
might be called by the user from time to time
"""

def _load(self=False, multiprocess=False, load_trees=False,
          path=False, name=False, **kwargs):
    import os
    import pandas as pd
    from corpkit.corpus import Corpus, File
    from corpkit.conll import path_to_df
    from corpkit.process import partition
    from corpkit.constants import CONLL_COLUMNS, DTYPES
    from corpkit.corpus import LoadedCorpus
    from tqdm import tqdm, tqdm_notebook
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            tqdm = tqdm_notebook
    except:
        pass

    dfs = []

    # arguments used when function is called recursively
    _data, _thread, _name, _tot = kwargs.get('_data', False), \
                                  kwargs.get('_thread', False), \
                                  kwargs.get('_name', False), \
                                  kwargs.get('_tot', False)

    # if multiprocessing, _data is the chunk we want to iterate over
    if _data:
        to_iter = _data
    # otherwise, we just want to iterate over the File objects
    else:
        if isinstance(self, File):
            to_iter = [self.path]
        elif isinstance(self, Corpus):
            to_iter = list(self.filepaths)
        _name = self.name

    size = 0

    # chunk data if multiprocessing, and then execute in parallel
    # this leaves us with a list of lists in dfs...
    if multiprocess:
        print('\n\n')
        from joblib import Parallel, delayed
        chunks = partition(to_iter, multiprocess)
        if len(chunks) < multiprocess:
            multiprocess = len(chunks)
        dfs = Parallel(n_jobs=multiprocess)(delayed(_load)(_data=b, 
                       _thread=i, name=_name, _tot=len(to_iter)) for i, b in enumerate(chunks, start=1))
    else:
        # parse and add to list
        kwa = dict(position=-_thread+1, ncols=120, unit="file", desc="Loading files", total=len(to_iter))
        t = tqdm(**kwa)
        fname = False
        for i, f in enumerate(to_iter, start=1):
            fname = getattr(f, 'name', os.path.basename(f))
            denom = _thread if _thread is not False else 1
            total = _tot if _tot is not False else len(to_iter)
            #print('Loading %d/%d\r' % (i*denom, total))
            df = path_to_df(getattr(f, 'path', f),
                            corpus_name=_name,
                            add_gov=kwargs.get('add_gov', False),
                            corp_folder=getattr(f, '_subcorpus', False),
                            v2=kwargs.get('v2', 'auto'),
                            just=kwargs.get('just', False),
                            skip=kwargs.get('skip', False),
                            usecols=kwargs.get('usecols', None),
                            load_trees=load_trees)
            if df is None:
                continue
            dfs.append(df)

            size += len(df)
            #kwa['tokens'] = format(size, ',')
            #if fname is not False:
            #    kwa['f'] = fname
            t.set_postfix({'tokens': format(size, ',')})
            t.update()
            
        t.close()
    # if we're paralleling, we have the _thread info in the output,
    if _data:
        return (_thread, dfs)
    else:
        if multiprocess:
            # make sure our dfs are in the right order
            # this is why _thread exists
            dfdat = []
            for i, d in sorted(dfs):
                dfdat.extend(d)
            dfs = dfdat
        if len(dfs) > 1:
            print('\nConcatenating %d frames ...' % len(dfs))
            # concat?
            dfs = pd.concat(dfs)
        else:
            dfs = dfs[0]
        
        for c in list(dfs.columns):
            if c in ['g', 'c', '_n', 'sent_len', 's', 'i']:
                if c == 'c':
                    dfs[c] = dfs[c].replace('_', 0)
                try:
                    dfs[c] = dfs[c].astype(int).fillna(0)
                except:
                    try:
                        dfs[c] = dfs[c].str.replace('^$|_', '0').fillna('0').astype(int).fillna(0)
                    except:
                        pass
            elif c in ['parse']:
                continue
            else:
                dfs[c] = dfs[c].astype('object').fillna('').astype('category')

        dfs = dfs.reset_index(drop=True)
        dfs.index.name = 'index'
        return LoadedCorpus(dfs, path=path)

def resize_by_window_size(df, window):
    df.is_copy = False
    if isinstance(window, int):
        df['left'] = df['left'].str.slice(start=-window, stop=None)
        df['left'] = df['left'].str.rjust(window)
        df['right'] = df['right'].str.slice(start=0, stop=window)
        df['right'] = df['right'].str.ljust(window)
        df['match'] = df['match'].str.ljust(df['match'].str.len().max())
    else:
        df['left'] = df['left'].str.slice(start=-window[0], stop=None)
        df['left'] = df['left'].str.rjust(window[0])
        df['right'] = df['right'].str.slice(start=0, stop=window[-1])
        df['right'] = df['right'].str.ljust(window[-1])
        df['match'] = df['match'].str.ljust(df['match'].str.len().max())
    return df

def concprinter(dataframe, kind='string', n=100,
                window=35, columns='all', metadata=True, **kwargs):
    """
    Print conc lines nicely, to string, latex or csv

    :param df: concordance lines from :class:``corpkit.corpus.Concordance``
    :type df: pd.DataFame 
    :param kind: output format
    :type kind: str ('string'/'latex'/'csv')
    :param n: Print first n lines only
    :type n: int/'all'
    :returns: None
    """

    df = dataframe.copy()

    if n > len(df):
        n = len(df)
    if not kind.startswith('l') and kind.startswith('c') and kind.startswith('s'):
        raise ValueError('kind argument must start with "l" (latex), "c" (csv) or "s" (string).')
    import pandas as pd

    # shitty thing to hardcode
    pd.set_option('display.max_colwidth', -1)

    if isinstance(n, int):
        to_show = df.head(n)
    elif n is False:
        to_show = df
    elif n == 'all':
        to_show = df
    else:
        raise ValueError('n argument "%s" not recognised.' % str(n))

    to_show.is_copy = False
    if window:
        to_show = resize_by_window_size(to_show, window)

    # if showing metadata to the right of lmr, add it here
    #cnames = list(to_show.columns)
    #ind = cnames.index('r')
    #if columns == 'all':
    #    columns = cnames[:ind+1]
    #if metadata is True:
    #    after_right = cnames[ind+1:]
    #    columns = columns + after_right
    #elif isinstance(metadata, list):
    #    columns = columns + metadata
#
    #to_show = to_show[columns]

    if kind.startswith('s'):
        functi = pd.DataFrame.to_string
    if kind.startswith('l'):
        functi = pd.DataFrame.to_latex
    if kind.startswith('c'):
        functi = pd.DataFrame.to_csv
        kwargs['sep'] = ','
    if kind.startswith('t'):
        functi = pd.DataFrame.to_csv
        kwargs['sep'] = '\t'

    # automatically basename subcorpus for show
    if 'c' in list(to_show.columns):
        import os
        to_show['c'] = to_show['c'].apply(os.path.basename)

    if 'f' in list(to_show.columns):
        import os
        to_show['f'] = to_show['f'].apply(os.path.basename)

    if 'file' in list(to_show.columns):
        import os
        to_show['file'] = to_show['file'].apply(os.path.basename)

    return_it = kwargs.pop('return_it', False)
    print_it = kwargs.pop('print_it', True)

    if return_it:
        return functi(to_show, header=kwargs.get('header', False), **kwargs)
    else:
        print('\n')
        print(functi(to_show, header=kwargs.get('header', False), **kwargs))
        print('\n')

def save(interrogation, savename, savedir='saved_interrogations', **kwargs):
    """
    Save an interrogation as pickle to *savedir*.

       >>> interro_interrogator(corpus, 'words', 'any')
       >>> save(interro, 'savename')

    will create ``./saved_interrogations/savename.p``

    :param interrogation: Corpus interrogation to save
    :type interrogation: corpkit interogation/edited result
    
    :param savename: A name for the saved file
    :type savename: str
    
    :param savedir: Relative path to directory in which to save file
    :type savedir: str
    
    :param print_info: Show/hide stdout
    :type print_info: bool
    
    :returns: None
    """

    try:
        import cPickle as pickle
    except ImportError:
        import pickle as pickle
    import os
    from time import localtime, strftime
    import corpkit
    from corpkit.process import makesafe, sanitise_dict

    from corpkit.interrogation import Interrogation
    from corpkit.corpus import Corpus

    print_info = kwargs.get('print_info', True)

    def make_filename(interrogation, savename):
        """create a filename"""
        if '/' in savename:
            return savename

        firstpart = ''
        if savename.endswith('.p'):
            savename = savename[:-2]    
        savename = makesafe(savename, drop_datatype=False, hyphens_ok=True)
        if not savename.endswith('.p'):
            savename = savename + '.p'
        if hasattr(interrogation, 'query') and isinstance(interrogation.query, dict):
            corpus = interrogation.query.get('corpus', False)
            if corpus:
                if isinstance(corpus, STRINGTYPE):
                    firstpart = corpus
                else:
                    if hasattr(corpus, 'name'):
                        firstpart = corpus.name
                    else:
                        firstpart = ''
        
        firstpart = os.path.basename(firstpart)

        if firstpart:
            return firstpart + '-' + savename
        else:
            return savename

    savename = make_filename(interrogation, savename)

    # delete unpicklable parts of query
    if hasattr(interrogation, 'query') and isinstance(interrogation.query, dict):
        iq = interrogation.query
        if iq:
            from types import ModuleType, FunctionType, BuiltinMethodType, BuiltinFunctionType
            interrogation.query = {k: v for k, v in iq.items() if not isinstance(v, ModuleType) \
                and not isinstance(v, FunctionType) \
                and not isinstance(v, BuiltinFunctionType) \
                and not isinstance(v, BuiltinMethodType)}
        else:
            iq = {}

    if savedir and not '/' in savename:
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        fullpath = os.path.join(savedir, savename)
    else:
        fullpath = savename

    while os.path.isfile(fullpath):
        selection = INPUTFUNC(("\nSave error: %s already exists in %s.\n\n" \
                "Type 'o' to overwrite, or enter a new name: " % (savename, savedir)))

        if selection == 'o' or selection == 'O':
            os.remove(fullpath)
        else:
            selection = selection.replace('.p', '')
            if not selection.endswith('.p'):
                selection = selection + '.p'
                fullpath = os.path.join(savedir, selection)

    if hasattr(interrogation, 'query'):
        interrogation.query = sanitise_dict(interrogation.query)

    try:
        del interrogation.corpus
        del interrogation.data.data
        del interrogation.data.corpus
        for i in interrogation.data:
            del i.parent
    except:
        pass

    with open(fullpath, 'wb') as fo:
        pickle.dump(interrogation, fo)
    
    time = strftime("%H:%M:%S", localtime())
    if print_info:
        print('\n%s: Data saved: %s\n' % (time, fullpath))

def load(savename, loaddir='saved_interrogations'):
    """
    Load saved data into memory:

        >>> loaded = load('interro')

    will load ``./saved_interrogations/interro.p`` as loaded

    :param savename: Filename with or without extension
    :type savename: str
    
    :param loaddir: Relative path to the directory containg *savename*
    :type loaddir: str
    
    :param only_concs: Set to True if loading concordance lines
    :type only_concs: bool

    :returns: loaded data
    """    
    try:
        import cPickle as pickle
    except ImportError:
        import pickle as pickle
    import os
    if not savename.endswith('.p'):
        savename = savename + '.p'

    if loaddir:
        if '/' not in savename:
            fullpath = os.path.join(loaddir, savename)
        else:
            fullpath = savename
    else:
        fullpath = savename

    with open(fullpath, 'rb') as fo:
        data = pickle.load(fo)
    return data

def loader(savedir='saved_interrogations'):
    """Show a list of data that can be loaded, and then load by user input of index"""
    import glob
    import os
    import corpkit
    from corpkit.other import load
    fs = [i for i in glob.glob(r'%s/*' % savedir) if not os.path.basename(i).startswith('.')]
    string_to_show = '\nFiles in %s:\n' % savedir
    most_digits = max([len(str(i)) for i, j in enumerate(fs)])
    for index, fname in enumerate(fs):
        string_to_show += str(index).rjust(most_digits) + ':\t' + os.path.basename(fname) + '\n'
    print(string_to_show)
    INPUTFUNC('Enter index of item to load: ')
    if ' ' in index or '=' in index:
        if '=' in index:
            index = index.replace(' = ', ' ')
            index = index.replace('=', ' ')
        varname, ind = index.split(' ', 1)
        globals()[varname] = load(os.path.basename(fs[int(ind)]))
        print("%s = %s. Don't do this again." % (varname, os.path.basename(fs[int(ind)])))
        return
    try:
        index = int(index)
    except:
        raise ValueError('Selection not recognised.')
    return load(os.path.basename(fs[index]))

def new_project(name, loc='.', **kwargs):
    """Make a new project in ``loc``.

    :param name: A name for the project
    :type name: str
    :param loc: Relative path to directory in which project will be made
    :type loc: str

    :returns: None
    """
    import corpkit
    import os
    import shutil
    import stat
    import platform
    from time import strftime, localtime

    root = kwargs.get('root', False)

    path_to_corpkit = os.path.dirname(corpkit.__file__)
    thepath, corpkitname = os.path.split(path_to_corpkit)
    
    # make project directory
    fullpath = os.path.join(loc, name)
    try:
        os.makedirs(fullpath)
    except:
        if root:
            thetime = strftime("%H:%M:%S", localtime())
            print('%s: Directory already exists: "%s"' %( thetime, fullpath))
            return
        else:
            raise
    # make other directories
    dirs_to_make = ['data', 'images', 'saved_interrogations', \
      'saved_concordances', 'dictionaries', 'exported', 'logs']
    #subdirs_to_make = ['dictionaries', 'saved_interrogations']
    for directory in dirs_to_make:
        os.makedirs(os.path.join(fullpath, directory))
    #for subdir in subdirs_to_make:
        #os.makedirs(os.path.join(fullpath, 'data', subdir))
    # copy the bnc dictionary to dictionaries

    def resource_path(relative):
        import os
        return os.path.join(os.environ.get("_MEIPASS2",os.path.abspath(".")),relative)

    corpath = os.path.dirname(corpkit.__file__)
    if root:
        corpath = corpath.replace('/lib/python2.7/site-packages.zip/corpkit', '')
    baspat = os.path.dirname(corpath)
    dicpath = os.path.join(corpath, 'dictionaries')
    try:
        shutil.copy(os.path.join(dicpath, 'bnc.p'), os.path.join(fullpath, 'dictionaries'))
    except:
        # find out why bnc not found!
        if root:
            try:
                shutil.copy(resource_path(os.path.join('dictionaries', 'bnc.p')), os.path.join(fullpath, 'dictionaries'))
            except:
                pass

    if not root:
        thetime = strftime("%H:%M:%S", localtime())
        print('\n%s: New project created: "%s"\n' % (thetime, name))

def texify(series, n=20, colname='Keyness', toptail=False, sort=False):
    """turn a series into a latex table"""
    import corpkit
    import pandas as pd
    if sort:
        df = pd.DataFrame(series.order(ascending=False))
    else:
        df = pd.DataFrame(series)
    df.columns = [colname]
    if not toptail:
        return df.head(n).to_latex()
    else:
        comb = pd.concat([df.head(n), df.tail(n)])
        longest_word = max([len(w) for w in list(comb.index)])
        tex = ''.join(comb.to_latex()).split('\n')
        linelin = len(tex[0])
        try:
            newline = (' ' * (linelin / 2)) + ' &'
            newline_len = len(newline)
            newline = newline + (' ' * (newline_len - 1)) + r'\\'
            newline = newline.replace(r'    \\', r'... \\')
            newline = newline.replace(r'   ', r'... ', 1)
        except:
            newline = r'...    &     ... \\'
        tex = tex[:n+4] + [newline] + tex[n+4:]
        tex = '\n'.join(tex)
        return tex

def as_regex(lst, boundaries='w', case_sensitive=False, inverse=False, compile=False):
    """Turns a wordlist into an uncompiled regular expression

    :param lst: A wordlist to convert
    :type lst: list

    :param boundaries:
    :type boundaries: str -- 'word'/'line'/'space'; tuple -- (leftboundary, rightboundary)
    
    :param case_sensitive: Make regular expression case sensitive
    :type case_sensitive: bool
    
    :param inverse: Make regular expression inverse matching
    :type inverse: bool

    :returns: regular expression as string
    """
    import corpkit

    import re
    if case_sensitive:
        case = r''
    else:
        case = r'(?i)'
    if not boundaries:
        boundary1 = r''
        boundary2 = r''
    elif isinstance(boundaries, (tuple, list)):
        boundary1 = boundaries[0]
        boundary2 = boundaries[1]
    else:
        if boundaries.startswith('w') or boundaries.startswith('W'):
            boundary1 = r'\b'
            boundary2 = r'\b'
        elif boundaries.startswith('l') or boundaries.startswith('L'):
            boundary1 = r'^'
            boundary2 = r'$'
        elif boundaries.startswith('s') or boundaries.startswith('S'):
            boundary1 = r'\s'
            boundary2 = r'\s'
        else:
            raise ValueError('Boundaries not recognised. Use a tuple for custom start and end boundaries.')
    if inverse:
        inverser1 = r'(?!'
        inverser2 = r')'
    else:
        inverser1 = r''
        inverser2 = r''

    if inverse:
        joinbit = r'%s|%s' % (boundary2, boundary1)
        as_string = case + inverser1 + r'(?:' + boundary1 + joinbit.join(sorted(list(set([re.escape(w) for w in lst])))) + boundary2 + r')' + inverser2
    else:
        as_string = case + boundary1 + inverser1 + r'(?:' + r'|'.join(sorted(list(set([re.escape(w) for w in lst])))) + r')' + inverser2 + boundary2
    if compile:
        return re.compile(as_string)
    else:
        return as_string

