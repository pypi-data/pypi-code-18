"""
corpkit: process CONLL formatted data
"""
from nltk.tree import ParentedTree
import pandas as pd
from pandas import DataFrame, Series

def make_dict_from_meta(metastring, sent_num, meta={}, splitter=' = ', load_trees=False, leng=False):
    """
    Take a string which is the metadata for a sent
    and make a dict from it
    """
    try:
        d = dict(l.lstrip('# ').rstrip().split(splitter, 1) for l in metastring.splitlines())
    except:
        d = {}
        for l in metastring.splitlines():
            try:
                k, v = l.lstrip('# ').split(splitter, 1)
            except ValueError:
                continue
            # this is very strict, for bad data. key can't have a space!
            if not k or not v or ' ' in k.strip():
                continue
            d[k.lower().strip()] = v.strip()                
        
    d.pop('', None)
    d.update(meta)
    d['s'] = sent_num
    if leng is not False and 'sent_len' not in d:
        d['sent_len'] = leng
    if load_trees and 'parse' in d:
        d['parse'] = ParentedTree.fromstring(d['parse'])

    return d

def make_csv(raw_lines, fname, meta, meta_attr=False, splitter=' = ', lt=True):
    """
    Take one CONLL-U file and add all metadata to each row
    Return: str (CSV data) and list of dicts (sent level metadata)
    """
    import re
    real_lines = []
    tokens = []
    sent_num = 1
    slen = 0
    meta_dicts = []
    sent_dict = dict(meta)
    sents = raw_lines.strip()+'\n'
    gotlen = 'sent_len = ' in sents[:5000]
    sents = sents.strip().split('\n\n')
    splut = [re.split('\n([0-9])', x, 1) for x in sents]
    splut = [i for i in splut if len(i) == 3]
    try:
        meta_dicts = [make_dict_from_meta(n, s, sent_dict, splitter, load_trees=lt, leng=c.count('\n')+1)
                      for s, (n, o, c) in enumerate(splut, start=1)]
    except:
        splut = [i for i in splut if len(i) == 3]
        meta_dicts = [make_dict_from_meta(n, s, sent_dict, splitter, load_trees=lt, leng=c.count('\n')+1)
                      for s, (n, o, c) in enumerate(splut, start=1)]
    csvdat = '\n'.join([y + z for x, y, z in splut]).rstrip()
    
    return csvdat, meta_dicts

def path_to_df(path, corpus_name=False, corp_folder=False, v2="auto",
               skip_morph=False, add_gov=False, usecols=None, drop=False,
               cur_len=0, just=False, skip=False, load_trees=False):
    """
    Optimised CONLL-U reader for v2.0 data

    Args:
        path (str): the file to prepare

    Returns:
        pd.DataFrame: 3d array representation of file data

    """
    import os
    import re
    import pandas as pd
    from corpkit.constants import CONLL_COLUMNS, CONLL_COLUMNS_V2, \
                                  PYTHON_VERSION, DTYPES, CORENLP_COREF_CATS
    if PYTHON_VERSION == 2: 
        from StringIO import StringIO
    else:
        from io import StringIO

    with open(path, 'r') as fo:
        data = fo.read().strip('\n')

    # we will assume that data is conll, but if it's not, we still
    # want to be able to work with it
    is_conll = True

    if v2 == 'auto':
        v2 = 'sent_id = ' in data[:5000]
    features = 'parser = features' in data[:5000]

    splitter = ' = ' if v2 else '='

    fname = re.sub(r'.txt.conll$', '', path).replace('_', '-')
    if corpus_name:
        fname = re.sub(r'^.*?/?data/(%s/|)' % corpus_name, '', fname)
    else:
        fname = os.path.basename(fname)

    # metadata that applies filewide
    basedict = {'file': fname}

    if corp_folder:
        basedict['folder'] = corp_folder
    year = re.search(r'[12][0-9][0-9][0-9]', fname)
    if year:
        basedict['year'] = year.group(0)

    if '\n\n' not in data:
        if not re.search('^#', data):
            is_conll = False

    if is_conll:
        sents, metadata = make_csv(data, fname, basedict, meta_attr=False, splitter=splitter, lt=load_trees)
        sents = StringIO(sents)
    else:
        sents = StringIO(data)

    if v2 and is_conll:
        all_col_names = CONLL_COLUMNS_V2
    elif is_conll:
        all_col_names = CONLL_COLUMNS
    else:
        all_col_names = None

    if isinstance(usecols, (list, set)):
        needed = ['i']
        usecols = [i for i in usecols if i in all_col_names and i not in needed]
        usecols = ['i'] + usecols

    header = None if is_conll else True
    ixc = 0
    if features:
        usecols = None
        all_col_names = ['i', 'w', 'l', 'x', 'p'] + CORENLP_COREF_CATS
        header = None

    df = pd.read_csv(sents, sep="\t", header=header, names=all_col_names, quoting=3, memory_map=True,
                     index_col=ixc, engine='c', usecols=usecols, na_filter=False)
   
    if is_conll:
        # this sucks
        s = []
        current = 0
        for num in df.index:
            if num == 1 or num == '1' or (isinstance(num, str) and num.startswith(('1-', '1.'))):
                current += 1
            s.append(current)

        df['s'] = s
        df = df.set_index('s', append=True)
        # maybe does nothing:
        df = df.reorder_levels(['s', 'i'])

    if v2 and not skip_morph and not features:
        df['m'] = df['m'].fillna('')
        df['o'] = df['o'].fillna('')
        cats = CORENLP_COREF_CATS + ['c', 'n', 'head']
        cats = list(set([i for i in cats if i+'=' in data]))
        om = df['o'].str.cat(df['m'], sep='|').str.strip('|_')
        # this is a very slow list comp, but i can't think of a better way to do it.
        # the 'extractall' solution makes columns for not just the value, but the key...
        extra = [om.str.extract('%s=([^|$]+)' % cat.title(), expand=True) for cat in cats]
        if extra:
            extra = pd.concat(extra, axis=1)
            extra.columns = cats
            df = pd.concat([df, extra], axis=1)

    # make and join the meta df
    metadata = {i: d for i, d in enumerate(metadata, start=1)}
    metadata = pd.DataFrame(metadata).T
    metadata.index.name = 's'
    df = metadata.join(df, how='inner')

    badcols = ['o', 'm']
    if drop:
        badcols = badcols + drop
    df = df.drop(badcols, axis=1, errors='ignore')

    # some evil code to handle conll-u files where g col could be a string
    if 'g' in df.columns:
        df['g'] = df['g'].fillna(0)
        if df['g'].dtype in [object, str]:
            df['g'] = df['g'].str.replace('_|^$', '0').astype(int)
        df['g'] = df['g'].astype(int)
    df = df.fillna('_')

    for c in list(df.columns):
        if c == 'g' or df[c].dtype.name.startswith('date'):
            continue
        try:
            df[c] = df[c].astype(DTYPES.get(c, 'category'))
        except (ValueError, TypeError):
            pass

    if add_gov:
        df = add_governors_to_df(df)

    if just is not False:
        bools = []
        for k, v in just.items():
            try:
                bools.append(df[k].str.contains(v, case=False))
            except KeyError:
                pass
        if not bools:
            return
        elif len(bools) == 1:
            return df[bools[0]]
        else:
            bools = pd.concat(bools, axis=1)
            df = df[bools.any(axis=1)]
    if skip is not False:
        bools = []
        for k, v in skip.items():
            try:
                bools.append(df[k].str.contains(v, case=False))
            except KeyError:
                bools.append(df['w'].str.contains('.*', case=False))
        if not bools:
            return df
        elif len(bools) == 1:
            return df[~bools[0]]
        else:
            bools = pd.concat(bools, axis=1)
            df = df[~bools.any(axis=1)]

    df.index = df.index.droplevel('s')
    df = df.reset_index()
    df.index += cur_len
    return df

def remove_bad(df):
    """
    Delete sentences from DF that do not contain an alphanumeric character
    
    """
    # get alnum bool for every word
    bools = df['w'].str.isalnum()
    # get true for sents to keep, false for sents to discard
    sbool = bools.groupby(level=["f", "s"]).any()
    sbool = sbool[sbool==True]
    # remove false from index
    return df[df.index.droplevel('i').isin(list(sbool.index))]

def cut_df_by_metadata(df, metadata, criteria, coref=False,
                            feature='speaker', method='just'):
    """
    Keep or remove parts of the DataFrame based on metadata criteria
    """
    if not criteria:
        df._metadata = metadata
        return df
    # maybe could be sped up, but let's not for now:
    if coref:
        df._metadata = metadata
        return df
    import re
    good_sents = []
    new_metadata = {}
    from corpkit.constants import STRINGTYPE
    # could make the below more elegant ...
    for sentid, data in sorted(metadata.items()):
        meta_value = data.get(feature, 'none')
        lst_met_vl = meta_value.split(';')
        if isinstance(criteria, (list, set, tuple)):
            criteria = [i.lower() for i in criteria]
            if method == 'just':
                if any(i.lower() in criteria for i in lst_met_vl):
                    good_sents.append(sentid)
                    new_metadata[sentid] = data
            elif method == 'skip':
                if not any(i in criteria for i in lst_met_vl):
                    good_sents.append(sentid)
                    new_metadata[sentid] = data
        elif isinstance(criteria, (re._pattern_type, STRINGTYPE)):
            if method == 'just':
                if any(re.search(criteria, i, re.IGNORECASE) for i in lst_met_vl):
                    good_sents.append(sentid)
                    new_metadata[sentid] = data
            elif method == 'skip':
                if not any(re.search(criteria, i, re.IGNORECASE) for i in lst_met_vl):
                    good_sents.append(sentid)
                    new_metadata[sentid] = data

    df = df.loc[good_sents]
    df = df.fillna('')
    df._metadata = new_metadata
    return df

def cut_df_by_meta(df, just, skip):
    """
    Reshape a DataFrame based on filters
    """
    if df is not None:
        if just:
            for k, v in just.items():
                df = cut_df_by_metadata(df, df._metadata, v,
                                        feature=k)
        if skip:
            for k, v in skip.items():
                df = cut_df_by_metadata(df, df._metadata, v,
                                        feature=k, method='skip')
    return df

def maketree(tree):
    try:
        return ParentedTree.fromstring(tree)
    except:
        return

def custom_tgrep(pattern, df, countmode=False, is_interro=False, corpus_loaded=False, **kwargs):
    """
    Search all the parse strings in a DataFrame

    Returns:
        list: search matches
    """
    from nltk.tree import ParentedTree
    from corpkit.constants import STRINGTYPE

    if isinstance(pattern, (STRINGTYPE, bool)):
        from nltk.tgrep import tgrep_compile
        pattern = tgrep_compile(pattern)

    if corpus_loaded:
        from tqdm import tqdm, tqdm_notebook
        try:
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                tqdm = tqdm_notebook
        except:
            pass

    matches = []
    # get a parse tree for each sent
    # note that this searches whole trees, so it can be wrong when trying
    # to filter results...
    #df = df.drop('_n', axis=1, errors='ignore')
    #df['_n'] = list(range(len(df)))

    if corpus_loaded:
        tree_once = df['parse'][df.i==1]
        #tree_once = df[['parse', '_n']][df.index.get_level_values('i') == 1]
        #tree_once = df[['parse', '_n']].xs(1, level='i', drop_level=False)
    elif is_interro:
        tree_once = df.reset_index().groupby(['file', 's']).first()['parse']
        tree_once.name = 'parse'
    else:
        tree_once = df['parse'][df.i==1]
        #tree_once = df[['parse', '_n']][df.index.get_level_values('i') == 1]

    if isinstance(tree_once.values[0], str):
        tree_once = tree_once.apply(maketree)

    ser = []
    six = []

    if corpus_loaded:
        running_count = 0
        t = tqdm(total=len(tree_once),
                 desc="Searching trees",
                 position=kwargs.get('paralleling', 0),
                 ncols=120,
                 unit="tree")

    # broken
    # should do dropna or whatever on this
    for n, tree in tree_once.iteritems():
        if not tree:
            continue
        match_count = 0
        root_positions = tree.treepositions(order='leaves')
        positions = tree.treepositions()
        for position in positions:
            done = []
            if pattern(tree[position]):
                match_count += 1
                size = len(tree[position].leaves())
                first = tree[position].treepositions('leaves')[0]
                first = position + first
                pos = root_positions.index(first)
                form = ','.join([str(x) for x in range(pos+1, pos+size+1)])
                ser.append(form)
                six.append(n+pos)
                #ser.append((index[0], index[1], pos, form))
        if corpus_loaded:
            running_count += match_count
            kwa = dict(results=format(running_count, ','))
            t.set_postfix(**kwa)
            t.update()

    if corpus_loaded:
        t.close()

    return six, ser

def tgrep_searcher(df, comp_tgrep=False, corpus_loaded=False,
                   countmode=False, stats=False, **kwargs):
    """
    Search a DataFrame using tgrep. This is also called to search for processes
    during a stats query.
    """
    out = []
    if not stats:
        df['_gram'] = [False for i in range(len(df))]

    # if we're counting, we don't need all the different conll bits
    if countmode:
        from corpkit.conll import CONLL_COLUMNS
        df = df.drop(CONLL_COLUMNS[1:], axis=1, errors='ignore')

    isinto = kwargs.get('is_interro', False)
    six, ser = custom_tgrep(comp_tgrep, df, corpus_loaded=corpus_loaded, **kwargs)
    df = df.iloc[six].copy()
    df['_gram'] = ser
    return df

    #for root, position, (f, s, i) in all_matches:
    #    ixs = [e for e, x in enumerate(root, start=1) \
    #            if x[:len(position)] == position]
    #    #span = df.loc[f, s, slice(ixs[0], ixs[-1])]
#
    #    df.loc[(f,s,ixs[0]),'_gram'] = ','.join([str(n) for n in ixs])
    #    #df.loc[idx[f,s,ixs[0]],'_gram'] = tuple(ixs[1:])
    #    #out.append([f, s, i])
    if not stats:
        return df.dropna(subset=['_gram'])
    else:
        return df

def get_stats(df=False, comp_tgrep=False,
              countmode=False, **kwargs):
    """
    Get general statistics for a DataFrame
    """
    from nltk.tree import ParentedTree
    from corpkit.constants import STRINGTYPE, CONLL_COLUMNS
    from corpkit.dictionaries.process_types import processes
    import re
    from collections import defaultdict
    import pandas as pd
    res = defaultdict(dict)

    # make df with just each sent once
    dfc = df.copy()
    tree_once = dfc['parse'].xs(1, level='i', drop_level=False)
    # make series of trees with fsi index
    try:
        tree_once = tree_once.apply(maketree)
    except:
        pass
    # get the processes query and search it, returning a df? of matches
    procq = comp_tgrep.get('Processes')
    procr = tgrep_searcher(df, tree_once=tree_once, comp_tgrep=procq, stats=True, **kwargs)

    # todo
    #for ptype in ['mental', 'relational', 'verbal']:
    #    nname = ptype.title() + ' processes'
    #    reg = getattr(processes, ptype).lemmata.as_regex(boundaries='l')
    #    count = len([i for i in procr if re.search(reg, i['l'])])
    #    res.append((f,s,nname, count))

    # each tree is once per sentence. do each search on each tree
    # and sum the results, then add to our defaultdict
    for ix, tree in tree_once.iteritems():
        root_position = tree.root().treepositions(order='leaves')
        positions = tree.treepositions()
        for qname, pattern in comp_tgrep.items():
            if qname == 'Processes':
                continue
            count = sum([1 for position in positions if pattern(tree[position])])
            res[(f, s)][qname] = count

    # now we iterate over the sents using groupby to count dep stuff
    sents = df.groupby(['file', 's'])
    for ix, sent in sents:
        res[(f, s)]['Passives'] = sent['f'].str.count('nsubjpass').sum()
        res[(f, s)]['Tokens'] = len(sent)
        punct = sent['w'].str.count(r'^-.*B-$|^[^A-Za-z0-9]*$').sum()
        w = len(sent) - punct
        res[(f, s)]['Words'] = w
        res[(f, s)]['Characters'] = sent['w'].str.len().sum()
        oc = sent['p'].str.count(r'^[NJVR]').sum()
        res[(f, s)]['Open class'] = oc
        res[(f, s)]['Punctuation'] = punct
        res[(f, s)]['Closed class'] = w - oc
        cols = CONLL_COLUMNS[1:] + ['parse']
        meta = sent.iloc[0][sent.iloc[0].index.difference(cols)]
        res[(f, s)].update(meta.to_dict())

    # turn our defaultdict into a multiindex df
    df = pd.DataFrame(res).T
    df.index.names = ['file', 's']
    # sort by total
    #df = df[df.sum().sort_values(ascending=False).index]
    return df

def pipeline(df=False,
             search=False,
             searchmode='all',
             coref=False,
             just=False,
             skip=False,
             corpus_name=False,
             corpus=False,
             multiprocess=False,
             comp_tgrep=False,
             countmode=False,
             case_sensitive=False,
             corpus_loaded=False,
             **kwargs):
    """
    A basic pipeline for conll querying---some options still to do
    It is expensive, so the code is optimised where possible,
    and therefore a bit ugly and repetitive
    """
    from collections import Counter, defaultdict
    from corpkit.corpus import File, Corpus
    from corpkit.constants import CONLL_COLUMNS

    # if we're doing depgrep, try to take the first part of the query
    # so we can just boolean match against it (it's faster!)

    # todo: this could become obsolete
    corp_folder = False
    if getattr(df, 'parent', False):
        corp_folder = df.parent

    # now, we have either a single file or a whole corpus as df
    # determine which subsearcher to use
    searcher = False
    if 'v' in search:
        searcher = get_stats
    if 't' in search:
        searcher = tgrep_searcher

    # first column should always be strings!
    try:
        df['w'].str
    except AttributeError:
        raise AttributeError("CONLL data doesn't match expectations. " \
                             "Try the corpus.conll_conform() method to " \
                             "convert the corpus to the latest format.")
    except TypeError:
        return

    # strip out punctuation by regex if the user wants
    #if kwargs.get('no_punct', False):
    #    from corpkit.process import remove_punct_from_df
    #    df = remove_punct_from_df(df)

    # don't know if anybody ever wants to use this, but oh well.
    #if kwargs.get('no_closed'):
    #    from corpkit.dictionaries import wordlists
    #    crit = wordlists.closedclass.as_regex(boundaries='l', case_sensitive=False)
    #    df = df[~df['w'].str.contains(crit)]

    # a really super quick return or cut down of the df by boolean indexing
    nsearch = {}
    if searchmode == 'all':
        for k, v in search.items():
            # ignore tgrep et al
            if k in ['c', 't', 'd']:
                nsearch[k] = v
                continue
            # ignore anything else that isn't readily available
            v = getattr(v, 'pattern', v)
            if k not in list(df.columns):
                nsearch[k] = v
                continue
            if isinstance(v, list):
                if not case_sensitive:
                    v = [str(x).lower() for x in v]
                if case_sensitive:
                    df = df[df[k].isin(v)]
                else:
                    if str(df[k].dtype).startswith(('int', 'float')):
                        df = df[df[k].isin(v)]
                    else:
                        df = df[df[k].str.lower().isin(v)]
            else:
                if str(df[k].dtype).startswith(('int', 'float')):
                    op, x = getattr(v, 'pattern', v).strip().split(' ', 1)
                    try:
                        x = float(x)
                    except:
                        pass
                    if op.lstrip('!') in ['=', '==']:
                        crit = df[k] == x
                    if op.lstrip('!') == '<':
                        crit = df[k] < x
                    if op.lstrip('!') == '<=':
                        crit = df[k] <= x
                    if op.lstrip('!') == '>':
                        crit = df[k] > x
                    if op.lstrip('!') == '>=':
                        crit = df[k] >= x
                    if op.startswith('!'):
                        df = df[~crit]
                    else:
                        df = df[crit]
                else:
                    df = df[df[k].str.contains(v, case=case_sensitive)]
        search = nsearch
    # if that's everything, we can leave now
    if not search and searchmode == 'all':
        return df

    # call stats and tgrep searchers if need be
    if searcher:
        all_res = searcher(df, corpus_loaded=corpus_loaded,
                        comp_tgrep=comp_tgrep, countmode=countmode, **kwargs)
        if searcher == get_stats:
            return all_res
        # todo, don't return here, allow the user to search for more stuff too?
        elif searcher == tgrep_searcher:
            # when tgrep is a subsequent search, there might be nans left. remove.
            if kwargs.get('is_interro'):
                all_res = all_res.dropna(how='all')
            return all_res

    if 'd' in search:
        from corpkit.query import depgrep
        return depgrep(df, search['d'], df=df, corpus_loaded=corpus_loaded)

    # for any other weirdness...
    raise NotImplementedError

def load_raw_data(f, parsed_path=False, plain_path=False, just_raw=False, split_ext=True):
    """
    Loads the stripped and raw versions of a parsed file
    """
    import os
    from corpkit.constants import OPENER
    if split_ext:
        f = os.path.splitext(f)[0]

    # open the unparsed version of the file, read into memory
    if just_raw:
        stripped_txtdata = None
    else:
        if not plain_path:
            stripped_txtfile = f.replace('-parsed', '-stripped')
        else:
            stripped_txtfile = f.replace(parsed_path.rstrip('/'), plain_path.rstrip('/') + '-stripped').replace('.conll', '')

        with OPENER(stripped_txtfile, 'r') as fo:
            stripped_txtdata = fo.read()

    # open the unparsed version with speaker ids
    if not plain_path:
        id_txtfile = f.replace('-parsed', '')
    else:
        id_txtfile = f.replace(parsed_path.rstrip('/'), plain_path.rstrip('/')).replace('.conll', '')

    with OPENER(id_txtfile, 'r') as fo:
        id_txtdata = fo.read()

    return stripped_txtdata, id_txtdata

def get_metadata(stripped,
                 plain,
                 sent_offsets,
                 metadata_mode=False,
                 speaker_segmentation=False,
                 first_line=False,
                 has_fmeta=False):
    """
    Take offsets and get a speaker ID or metadata from them
    """
    if not stripped and not plain:
        return {}
    if stripped is None:
        stripped = plain
    if not first_line:
        start, end = sent_offsets
    else:
        start = 0
        try:
            end = stripped.index('\n')
        except:
            end = len(stripped) - 1
    # get the text from stripped
    sent = stripped[start:end]
    # get everything before this text
    cut_old_text = stripped[:start]
    # count which line the sent must be on from the old text
    line_index = cut_old_text.count('\n')
    if has_fmeta:
        line_index += 1
    # lookup this text
    with_id = plain.splitlines()[line_index]
    
    if first_line:
        meta_dict = {}
    else:
        meta_dict = {'text': sent.strip('\n \t\r').replace('\n', r'\n')}

    if metadata_mode:

        # split line on last appearance of '<metadata', get last bit with no >
        metad = with_id.strip().rstrip('>').rsplit('<metadata ', 1)
        
        import shlex
        from corpkit.constants import PYTHON_VERSION
        
        try:
            shxed = shlex.split(metad[-1].encode('utf-8')) if PYTHON_VERSION == 2 \
                else shlex.split(metad[-1])
        except:
            shxed = metad[-1].split("' ")
        for m in shxed:
            if PYTHON_VERSION == 2:
                m = m.decode('utf-8')
            # in rare cases of weirdly formatted xml:
            try:
                k, v = m.split('=', 1)
                v = v.replace(u"\u2018", "'").replace(u"\u2019", "'")
                v = v.strip("'").strip('"')
                meta_dict[k] = v
            except ValueError:
                continue

    if speaker_segmentation:
        split_line = with_id.split(': ', 1)
        # handle multiple tags?
        if len(split_line) > 1:
            speakerid = split_line[0]
        else:
            speakerid = 'UNIDENTIFIED'
        meta_dict['speaker'] = speakerid

    return meta_dict

def convert_json_to_conll(corpus,
                          speaker_segmentation=False,
                          coref=False,
                          metadata=False,
                          plain_path=False,
                          just_files=False):
    """
    take json corenlp output and convert to conll, with
    dependents, speaker ids and so on added.

    Path is for the parsed corpus, or a list of files within a parsed corpus
    Might need to fix if outname used?
    """

    import json
    import re
    from corpkit.build import get_filepaths
    from corpkit.corpus import Corpus
    from corpkit.constants import CORENLP_VERSION, OPENER, CORENLP_COREF_CATS
    
    from tqdm import tqdm, tqdm_notebook
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            tqdm = tqdm_notebook
    except:
        pass

    if not isinstance(corpus, Corpus):
        corpus = Corpus(corpus)

    files = corpus.filepaths
    
    t = tqdm(total=len(files),
             desc="Converting to CONLL-U",
             ncols=120,
             unit="file")

    for f in files:

        if speaker_segmentation or metadata:
            stripped, raw = load_raw_data(f, parsed_path=corpus.path, plain_path=plain_path)
        else:
            stripped, raw = load_raw_data(f, parsed_path=corpus.path, plain_path=plain_path, just_raw=True)

        fmeta = get_metadata(stripped, raw, False, metadata_mode=metadata, speaker_segmentation=False, first_line=True)

        main_out = ''
        # if the file has already been converted, don't worry about it
        # untested?
        with OPENER(f, 'r') as fo:
            try:
                data = json.load(fo)
            except ValueError:
                continue

        try:
            fo.close()
        except:
            pass

        corefs = reshape_coref(data.get('corefs')) if coref else {}

        for idx, sent in enumerate(data['sentences'], start=1):

            sent_corefs = corefs.get(idx, {})

            # get the parse tree
            tree = sent['parse'].replace('\n', '')
            tree = re.sub(r'\s+', ' ', tree)

            sent_offsets = (sent['tokens'][0]['characterOffsetBegin'], \
                            sent['tokens'][-1]['characterOffsetEnd'])

            # get the speaker, plaintext, and any other metadata            
            metad = get_metadata(stripped,
                                 raw,
                                 sent_offsets,
                                 metadata_mode=metadata,
                                 speaker_segmentation=speaker_segmentation,
                                 has_fmeta=bool(fmeta))

            if isinstance(fmeta, dict):
                fmeta.update(metad)
                metad = fmeta
                            
            # UD 2.0 officially demands sent_id = n
            output = '# sent_id = %d\n# parse = %s\n# sent_len = %d\n' % (idx, tree, len(sent['tokens']))
            #output = '# parse=%s\n' % tree
            for k, v in sorted(metad.items()):
                output += '# %s = %s\n' % (k, v)

            # now we go over each token in the sentence, formatting the lines
            for token in sent['tokens']:

                index = str(token['index'])
                # this got a stopiteration on rsc data
                governor, func = next(((i['governor'], i['dep']) \
                    for i in sent.get('enhancedPlusPlusDependencies',
                    sent.get('collapsed-ccprocessed-dependencies')) \
                    if i['dependent'] == int(index)), ('_', '_'))
                
                morphline = []
                miscline = []
                
                # add ner if it's in there
                ner = token.get('n', False)
                if ner:
                    miscline.append('n=%s' % ner)

                # add this spaceafter convention for ud 2.0
                if not token.get('after'):
                    miscline.append("SpaceAfter=No")
                
                # get any coref data for this token
                this_tok = sent_corefs.get(int(index), False)

                if this_tok is not False:

                    miscline.append('c=%d' % this_tok['id'])
                    is_head = int(index) == this_tok['headIndex']
                    if is_head:
                        miscline.append('head=%s' % str(is_head).lower())
                        repres = this_tok.get('Isrepresentativemention', '_')
                        miscline.append('Isrepresentativemention=%s' % str(repres).lower())

                        for key in CORENLP_COREF_CATS:
                            if key in this_tok:
                                val = this_tok[key]
                                val = str(val) if not isinstance(val, bool) else str(val).lower()
                                morphline.append('%s=%s' % (key.title(), val.strip('|').strip('=')))

                miscline = '|'.join(miscline) if miscline else '_'
                morphline = '|'.join(morphline) if morphline else '_'

                line = [index,
                        token.get('word', '_'),
                        token.get('lemma', '_'),
                        '_', #xpos
                        token.get('pos', '_'),
                        morphline,
                        governor,
                        func,
                        '_', # enhanced deps
                        miscline]

                # no ints
                line = [str(l) if isinstance(l, int) else l for l in line]
                # no empty spaces
                line = [l if l else '_' for l in line]

                from corpkit.constants import PYTHON_VERSION
                if PYTHON_VERSION == 2:
                    try:
                        lines = [unicode(l, errors='ignore') for l in line]
                    except TypeError:
                        pass

                # slash is changed because formatting of tokens can use slash: (i/be). by
                # keeping the number of slashes the same, we can make multiindex from them or whatever
                output += '\t'.join(line).replace('/', '-slash-') + '\n'
            main_out += output + '\n'

        stripped = None
        raw = None
   
        with OPENER(f, 'w', encoding='utf-8') as fo:
            main_out = main_out.replace(u"\u2018", "'").replace(u"\u2019", "'")
            fo.write(main_out)

        t.update()

    t.close()
    return

def _sentence(row, df):
    start = row.name + row.sent_len - row.i
    end = start + row.sent_len
    return df.iloc[start:end,:]

def sentence_df(row, df):
    if not isinstance(df, pd.DataFrame):
        return sentence(row, df)
    start = row.name - row.i
    end = start + row.sent_len
    return df.loc[start:end,:]

def sentence(row, df, start=False, positions=False):
    try:
        # get actual sent
        if positions and not hasattr(row, 'index'):
            #print("row", row, "positions", positionsq)
            rn = row.name
            if isinstance(rn, tuple):
                rn = row._n
            slen = row[positions['sent_len']]
        else:
            rn = row.name
            if isinstance(rn, tuple):
                rn = row._n
            slen = row.sent_len

        if not start:
            start = rn - slen + 1
            end = start + slen
        # get fuzzy sent
        else:
            start = rn - start
            end = rn + start
        return df[start:end]
    except:
        raise

def governor(row, df):
    """
    Get governor of row as row from df
    """
    if not row['g']:
        return "ROOT"
    else:
        i = row.name[2] if isinstance(row.name, tuple) else row['i']
        n = row['_n'] if isinstance(row.name, tuple) else row.name
        # n-1+g
        return [df[n-i+row['g']]]

def xgovernor(row, df):
    """
    Get governor of row as row from df
    """
    if not row['g']:
        return "ROOT"
    try:
        x = df[row._n-row.name[2]+row['g']]
        return [x]
    except:
        return []
        #todo: rethink this
        x = df[df[:,:3] == (row.name[0], row.name[1], row['g'])]
        return x

def dependents(row, df, positions):
    """
    Get list of dependents of row as rows from df
    """
    sent = sentence(row, df, positions=positions)
    i = row.name[2] if isinstance(row.name, tuple) else row['i']
    try:
        return sent[sent[:,positions['g']] == i]
    except:
        return sent[sent[:,positions['g']] == row[positions['i']]]
    #return d
    #return sent[sent['g'] == row.name[2]]

def governors(row, df):
    """
    Sometimes we need a list of governors, but only one is possible
    So, here we just return a one-item list
    """
    return governor(row, df)

def has_dependent(obj, df):
    """
    Check if dependents exist

    Return: bool
    """
    sent = sent = sentence(row, df)
    return sent[sent['g'] == row.name[2]].any()

def has_governor(obj):
    """
    Check if governor exists

    Return: bool
    """
    return obj['g'] not in ['_', '0', 0]

def sisters(row, df):
    """
    Give a list of tokens sharing a governor, but not row
    """
    sent = sentence(row, df)
    return sent[sent['g'] == row['g']].drop(getattr(row, 'name', tuple(row[:3])), errors='ignore')
    #return [samegov.loc[i] for i in samegov.index if i != row.name[2]]

def next_sent(row, df):
    # if sent, just get last row and add 1
    if isinstance(row, pd.DataFrame):
        start = row.iloc[-1,:].name + 1
    else:
        start = row.name + row.sent_len - row.i + 1
    end = df.iloc[start,'sent_len']
    return df.iloc[start:end,:]

def reshape_coref(coref):
    """
    corefs are a dict of incrementing-number: list of mentions
    each object in the list of mentions is a dict containing a lot
    of interesting information. but, we need to shape the dict so we can
    access by sentence instead of arbirary number

    Return: dict
    """
    from collections import defaultdict
    out = defaultdict(dict)
    for numstring, list_of_dicts in coref.items():
        for dct in list_of_dicts:
            if not dct:
                continue
            sent = dct.pop('sentNum')
            tok_indexes = range(dct['startIndex'], dct['endIndex']+1)
            for ix in tok_indexes:
                out[sent][ix] = dct
    return out

def add_governors_to_df(df):
    """
    Add governor info to a DF. Increases memory usage quite a bit.
    """
    # save the original index
    i = df.index.get_level_values('i')
    # add g
    dfg = df.set_index('g', append=True)
    # remove i
    dfg = dfg.reset_index('i')
    dfg = df.loc[dfg.index]
    dfg = dfg[['w', 'l', 'p', 'f']]
    dfg['i'] = i
    dfg = dfg.set_index('i', append=True)
    dfg.index.names = ['file', 's', 'g', 'i']
    dfg = dfg.reset_index('g', drop=True)
    for c in list(dfg.columns):
        try:
            dfg[c] = dfg[c].cat.add_categories(['ROOT'])
        except (AttributeError, ValueError):
            pass
    dfg = dfg.fillna('ROOT')
    dfg.columns = ['gw', 'gl', 'gp', 'gf']
    dfg = df.join(dfg, how="inner")
    return dfg


