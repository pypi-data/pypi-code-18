"""
In here are functions used internally by corpkit,  
not intended to be called by users.
"""

from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION, INPUTFUNC

def is_number(s):
    """
    Check if str can be can be made into float/int
    """
    try:
        float(s) # for int, long and float
        return True
    except ValueError:
        try:
            complex(s) # for complex
            return True
        except ValueError:
            return False
    except TypeError:
        return False

def timestring(input):
    """print with time prepended"""
    from time import localtime, strftime
    thetime = strftime("%H:%M:%S", localtime())
    print('%s: %s' % (thetime, input.lstrip()))

def makesafe(variabletext, drop_datatype=True, hyphens_ok=False):
    import re
    from corpkit.process import is_number
    if hyphens_ok:
        variable_safe_r = re.compile(r'[^A-Za-z0-9_-]+', re.UNICODE)
    else:
        variable_safe_r = re.compile(r'[^A-Za-z0-9_]+', re.UNICODE)
    try:
        txt = variabletext.name.split('.')[0]
    except AttributeError:
        txt = variabletext.split('.')[0]
    if drop_datatype:
        txt = txt.replace('-parsed', '')
    txt = txt.replace(' ', '_')
    if not hyphens_ok:
        txt = txt.replace('-', '_')
    variable_safe = re.sub(variable_safe_r, '', txt)
    if is_number(variable_safe):
        variable_safe = 'c' + variable_safe
    return variable_safe
    
def get_corenlp_path(corenlppath):
    """
    Find a working CoreNLP path.
    Return a dir containing jars
    """

    import os
    import sys
    import re
    import glob
    
    cnlp_regex = re.compile(r'stanford-corenlp-[0-9\.]+\.jar')

    # if something has been passed in, find that first
    if corenlppath:
        # if it's a file, get the parent dir
        if os.path.isfile(corenlppath):
            corenlppath = os.path.dirname(corenlppath)
            if any(re.search(cnlp_regex, f) for f in os.listdir(corenlppath)):
                return corenlppath
        # if it's a dir, check if dir contains jar
        elif os.path.isdir(corenlppath):
            if any(re.search(cnlp_regex, f) for f in os.listdir(corenlppath)):
                return corenlppath
            # if it doesn't contain jar, get subdir by glob
            globpath = os.path.join(corenlppath, 'stanford-corenlp*')
            poss = [i for i in glob.glob(globpath) if os.path.isdir(i)]
            if poss:
                poss = poss[-1]
                if any(re.search(cnlp_regex, f) for f in os.listdir(poss)):
                    return poss

    # put possisble paths into list
    pths = ['.', 'corenlp',
            os.path.expanduser("~"),
            os.path.join(os.path.expanduser("~"), 'corenlp')]
    if isinstance(corenlppath, STRINGTYPE):
        pths.append(corenlppath)
    possible_paths = os.getenv('PATH').split(os.pathsep) + sys.path + pths
    # remove empty strings
    possible_paths = set([i for i in possible_paths if os.path.isdir(i)])

    # check each possible path
    for path in possible_paths:
        if any(re.search(cnlp_regex, f) for f in os.listdir(path)):
            return path
    # check if it's a parent
    for path in possible_paths:
        globpath = os.path.join(path, 'stanford-corenlp*')
        cnlp_dirs = [d for d in glob.glob(globpath)
                     if os.path.isdir(d)]
        for cnlp_dir in cnlp_dirs:
            if any(re.search(cnlp_regex, f) for f in os.listdir(cnlp_dir)):
                return cnlp_dir
    return

def classname(cls):
    """Create the class name str for __repr__"""
    return '.'.join([cls.__class__.__module__, cls.__class__.__name__])

def canpickle(obj):
    """
    Determine if object can be pickled

    :returns: `bool`

    """
    import os
    try:
        from cPickle import UnpickleableError as unpick_error
        import cPickle as pickle
        from cPickle import PicklingError as unpick_error_2
    except ImportError:
        import pickle
        from pickle import UnpicklingError as unpick_error
        from pickle import PicklingError as unpick_error_2

    mode = 'w' if PYTHON_VERSION == 2 else 'wb'
    with open(os.devnull, mode) as fo:
        try:
            pickle.dump(obj, fo)
            return True
        except (unpick_error, TypeError, unpick_error_2, AttributeError) as err:
            return False

def sanitise_dict(d):
    """
    Make a dict that works as query attribute---remove nesting and unpicklable
    """
    if not isinstance(d, dict):
        return
    newd = {}
    if d.get('kwargs') and isinstance(d['kwargs'], dict):
        for k, v in d['kwargs'].items():
            if canpickle(v) and not isinstance(v, type):
                newd[k] = v
    for k, v in d.items():
        if canpickle(v) and not isinstance(v, type):
            newd[k] = v
    return newd

def saferead(path):
    """
    Read a file with detect encoding
    
    :returns: text and its encoding
    """
    import chardet
    import sys
    if sys.version_info.major == 3:
        enc = 'utf-8'
        try:
            with open(path, 'r', encoding=enc) as fo:
                data = fo.read()
        except:
            with open(path, 'rb') as fo:
                data = fo.read().decode('utf-8', errors='ignore')
        return data, enc
    else:
        with open(path, 'r') as fo:
            data = fo.read()
        try:
            enc = 'utf-8'
            data = data.decode(enc)
        except UnicodeDecodeError:
            enc = chardet.detect(data)['encoding']
            data = data.decode(enc, errors='ignore')
        return data, enc

def urlify(s):
    """
    Turn plot title into filename for saving
    """
    import re
    s = s.lower()
    s = re.sub(r"[^\w\s-]", '', s)
    s = re.sub(r"\s+", '-', s)
    s = re.sub(r"-(textbf|emph|textsc|textit)", '-', s)
    return s

def dictformat(d, query=False, metadata=False):
    """
    Format a dict search query for printing

    :returns: `str`
    """
    from corpkit.constants import transshow, transobjs
    if isinstance(d, STRINGTYPE) and isinstance(query, dict):
        newd = {}
        for k, v in query.items():
            newd[k] = fix_search({d: v}, metadata=metadata)
        return dictformat(newd, metadata=metadata)
        if query:
            sformat = dictformat(query, metadata=metadata)
            return sformat
        else:
            return d
    if all(isinstance(i, dict) for i in d.values()):
        sformat = '\n'
        for k, v in d.items():
            sformat += '             ' + k + ':'
            sformat += dictformat(v, metadata=metadata)
        return sformat
    if len(d) == 1 and d.get('v'):
        return 'Features'
    sformat = '\n'
    for k, v in d.items():
        if k in ['t', 'd', 'c']:
            dratt = ''
        else:
            dratt = transshow.get(k, k)
        if k == 't':
            drole = 'Trees'
        elif k == 'd':
            drole = 'Dependencies'
        elif k == 'c':
            drole = 'CQL'
        else:
            drole = ''
        vform = getattr(v, 'pattern', v)
        sformat += '                 %s %s: %s\n' % (drole, dratt.lower(), vform)
    return sformat

def make_name_to_query_dict(existing={}, cols=False, dtype=False):
    """
    Make or add to dict of longhand and shorthand search bits
    """
    from corpkit.constants import transshow, transobjs
    if dtype and dtype != 'conll':
        return {'None': 'None'}
    
    for l, o in transobjs.items():
        if cols and l in ['g', 'd'] and l not in cols:
            continue
        if o == 'Match':
            o = ''
        else:
            o = o + ' '
        for m, p in sorted(transshow.items()):
            if cols:
                fixed = m.replace('x', 'p')
                if fixed in ['n', 't', 'a']:
                    pass
                else:
                    if fixed not in cols:
                        continue
            if m in ['n', 't']:
                continue
            if p != 'POS' and o != '' and o != 'NER':
                p = p.lower()
            existing['%s%s' % (o, p)] = '%s%s' % (l, m)
    return existing

def auto_usecols(search, exclude, show, usecols, coref=False):
    """
    Figure out if we can speed up conll parsing based on search,
    exclude and show. the return value is passed to pandas.read_csv
    so that only relevant columns are parsed.

    If usecols isn't None, the user has specified needed cols.

    todo: coref
    """
    if usecols:
        return usecols
    from corpkit.constants import CONLL_COLUMNS

    # get all objs from search, exclude and show
    needed = []

    for i in search.keys():
        if 'g' in i or i == 'g':
            needed.append('d')
        elif 'd' in i or i == 'd':
            needed.append('g')
        elif 'h' in i or i == 'h':
            needed.append('c')
        elif 'r' in i or i == 'r':
            needed.append('c')
        # features mode:
        elif i == 'v':
            needed.append('f')
            needed.append('w')
            needed.append('p')
            continue
        needed.append(i)
    if isinstance(exclude, dict):
        for i in exclude.keys():
            needed.append(i)
    if isinstance(show, list):
        for i in show:
            if i.endswith('a'):
                needed.append('g')
            if i.startswith('r') or i.startswith('h'):
                needed.append('c')
            i = i.replace('a', 'f').replace('x', 'p')
            needed.append(i)
    else:
        needed.append(show)

    if coref:
        needed.append('c')
    # get the obj and attr from these
    stcols = []
    for i in needed:
        stcols.append(i[-1])
        try:
            stcols.append(i[-2])
        except:
            pass
    # word class is pos
    #stcols = ['p' if i == 'x' else i for i in stcols]
    # we always get word right now, but could remove '2' in the future
    # we add one to the index because conll_columns does not have 's', yet it
    # is there in the df
    out = [0, 1, 2]
    for n, c in enumerate(CONLL_COLUMNS, start=1):
        if c in stcols and n not in out:
            out.append(n)
    return out

def make_dotfile(metapath, corpuspath, return_json=False, data_dict=False):
    """
    Generate a dotfile in the data directory containing corpus information
    Right now, this information is the metadata fields and their values
    """
    import os
    import json
    from corpkit.build import get_all_metadata_fields, get_meta_values
    from corpkit.constants import OPENER, CONLL_COLUMNS
    
    if data_dict:
        json_data = data_dict
    else:
        json_data = {'fields': {}}
        fields = get_all_metadata_fields(corpuspath, include_speakers=True)
        for field in fields:
            vals = get_meta_values(corpuspath, field)
            json_data['fields'][field] = vals
        #df = get_first_df(path)
        json_data['columns'] = ['s'] + CONLL_COLUMNS
        json_data['v2'] = True
    
    with OPENER(metapath, 'w', encoding='utf-8') as fo:
        fo.write(json.dumps(json_data))
    if return_json:
        return json_data

def get_metadata_filepath(path):
    """
    Make metadata filename from path
    """
    import os
    dotname = '.%s.json' % os.path.basename(path)
    dotpath = os.path.dirname(path)
    return os.path.join(dotpath, dotname)
    
def get_corpus_metadata(path, generate=False):
    """
    Return a dict containing corpus metadata, or None if not done yet
    """
    import os
    import json
    from corpkit.corpus import Corpus
    from corpkit.constants import OPENER

    met_file = get_metadata_filepath(path)

    if not os.path.isfile(met_file):
        if generate:
            return make_dotfile(met_file, path, return_json=True)
        else:
            return
    else:
        with OPENER(met_file, 'r') as fo:
            data = fo.read()
            if data:
                return json.loads(data)
            else:
                return make_dotfile(met_file, path, return_json=True)

def make_df_json_name(typ, subcorpora=False):
    """
    Obsolete now?
    """
    if subcorpora:
        if isinstance(subcorpora, list):
            subcorpora = '-'.join(subcorpora)
        return '%s-%s' % (typ, subcorpora)
    else:
        return typ

def add_df_to_dotfile(path, df, typ='features', subcorpora=False):
    """
    Add some Pandas data to corpus metadata
    """
    import pandas as pd
    from corpkit.interrogation import Results
    from corpkit.corpus import LoadedCorpus
    if isinstance(df, (pd.Series, pd.DataFrame, Results, LoadedCorpus)):
        name = make_df_json_name(typ, subcorpora)
    else:
        name = typ
    md = get_corpus_metadata(path, generate=True)
    if name not in md:
        if isinstance(df, (pd.Series, pd.DataFrame, Results, LoadedCorpus)):
            df.index = df.index.astype(object)
            md[name] = df.astype(object).drop(['file', 's', 'i'], axis=1, errors='ignore').reset_index().to_json()
        else:
            md[name] = df
        metapath = get_metadata_filepath(path)
        make_dotfile(metapath, path, data_dict=md)

def delete_files_and_subcorpora(corpus, skip, just):
    """
    Remake a Corpus object without some files or folders
    """
    import re
    from corpkit.corpus import Corpus, File
    
    # we use type here because subcorpora don't have subcorpora, but Subcorpus
    # inherits from Corpus
    if not isinstance(corpus, Corpus):
        return corpus, skip, just
        
    if not skip and not just:
        return corpus, skip, just

    sd = skip.pop('folders', None) if isinstance(skip, dict) else None
    sf = skip.pop('files', None) if isinstance(skip, dict) else None
    jd = just.pop('folders', None) if isinstance(just, dict) else None
    jf = just.pop('files', None) if isinstance(just, dict) else None
    sd = str(sd) if isinstance(sd, (int, float)) else sd
    sf = str(sf) if isinstance(sf, (int, float)) else sf
    jd = str(jd) if isinstance(jd, (int, float)) else jd
    jf = str(jf) if isinstance(jf, (int, float)) else jf

    if not any([sd, sf, jd, jf]):
        return corpus, skip, just

    # now, the real processing begins
    # the code has to be this way, sorry.

    if sd not in [None, False, {}]:
        todel = set()
        if isinstance(sd, list):
            for i, sub in enumerate(corpus.subcorpora):
                if sub.name in sd:
                    todel.add(i)
        else:
            for i, sub in enumerate(corpus.subcorpora):
                if re.search(sd, sub.name, re.IGNORECASE):
                    todel.add(i)

        for i in sorted(todel, reverse=True):
            del corpus.subcorpora[i]

    if sf not in [None, False, {}]:
        if not getattr(corpus, 'subcorpora', False):
            todel = set()
            if isinstance(sf, list):
                for i, sub in enumerate(corpus.files):
                    if sub.name in sf:
                        todel.add(i)
            else:
                for i, sub in enumerate(corpus.files):
                    if re.search(sf, sub.name, re.IGNORECASE):
                        todel.add(i)

            for i in sorted(todel, reverse=True):
                del corpus.files[i]

        else:
            for sc in corpus.subcorpora:
                todel = set()
                if isinstance(sf, list):
                    for i, sub in enumerate(corpus.files):
                        if sub.name in sf:
                            todel.add(i)

                else:
                    for i, sub in enumerate(sc.files):
                        if re.search(sf, sub.name, re.IGNORECASE):
                            todel.add(i)

                for i in sorted(todel, reverse=True):
                    del sc.files[i]

    if jd not in [None, False, {}]:
        todel = set()
        if isinstance(jd, list):
            for i, sub in enumerate(corpus.subcorpora):
                if sub.name not in jd:
                    todel.add(i)
        else:
            for i, sub in enumerate(corpus.subcorpora):
                if not re.search(jd, sub.name, re.IGNORECASE):
                    todel.add(i)

        for i in sorted(todel, reverse=True):
            del corpus.subcorpora[i]

    if jf not in [None, False, {}]:
        if not getattr(corpus, 'subcorpora', False):
            todel = set()
            if isinstance(jf, list):
                for i, sub in enumerate(corpus.files):
                    if sub.name not in jf:
                        todel.add(i)
            else:
                for i, sub in enumerate(corpus.files):
                    if not re.search(jf, sub.name, re.IGNORECASE):
                        todel.add(i)

            for i in sorted(todel, reverse=True):
                del corpus.files[i]

        else:
            for sc in corpus.subcorpora:
                todel = set()
                if isinstance(jf, list):
                    for i, sub in enumerate(corpus.files):
                        if sub.name not in jf:
                            todel.add(i)

                else:
                    for i, sub in enumerate(sc.files):
                        if not re.search(jf, sub.name, re.IGNORECASE):
                            todel.add(i)

                for i in sorted(todel, reverse=True):
                    del sc.files[i]

    return corpus, skip, just

def timestring(inputx, blankfirst=0):
    """
    Print with time prepended

    Args:
        intputx (str): a string to print
        blankfirst (int): blank lines to prepend to the print string
    """
    from time import localtime, strftime
    thetime = strftime("%H:%M:%S", localtime())
    blankfirst = '\n' * blankfirst
    print('%s%s: %s' % (blankfirst, thetime, inputx.lstrip()))

def make_tree(path):
    """
    Represent a corpus path's directory structure visually in a terminal
    """
    import os
    s = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        s += '{}{}/'.format(indent, os.path.basename(root)) + '\n'
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.endswith('.txt') and not f.endswith('.conll'):
                continue
            s += '{}{}'.format(subindent, f) + '\n'
    return s

def make_filelist(path):
    """
    Make a list of absolute paths to every file in the corpus
    """
    import os
    all_files = []
    for root, ds, fs in os.walk(path):
        for f in fs:
            if not f.endswith('.txt') and not f.endswith('.conll'):
                continue
            fp = os.path.join(root, f)
            all_files.append(fp)
    return all_files

def format_text_from_df(df, f, s, middlestring):
    """
    Create a string of text from a pandas.DataFrame and a concordance line string

    Returns:
        str: the entire new text
        int: line number of the concordance in this string
    """
    linenum = 0
    # get just file data with sent num and word
    fdata = df['w'].xs([f])
    forelines = fdata.loc[:s-1].str.cat(sep=' ')
    postlines = fdata.loc[s+1:].str.cat(sep=' ')

    return "\n\n".join([forelines, middlestring, postlines]), linenum

def filter_df(row, k=False, v=False):
    if isinstance(v, list):
        return getattr(row['entry'], k) in v
    else:
        return getattr(row['entry'], k).astype(str).str.contains(v)

def apply_show(row, show=False, df=False, preserve_case=False, ngram=False, positions=False):
    """
    Format a match based on "show" criteria

    Args:
        ngram (tuple): a tuple of two ints, denoting indexes relative to the match (0)
    """
    # if we don't have multiple tokens, it's pretty easy.
    gram = row.get('_gram', False)
    if not gram and not ngram:
        if len(show) == 1:
            out = row[show[0]].rstrip('/')
            return out.lower() if not preserve_case else out
        else:
            out = '/'.join(row[show]).rstrip('/')
            return out.lower() if not preserve_case else out
        
    n = row.name
    i = row.i
    
    # we might need the whole sent ...
    if ngram:
        ran = [x+n for x in range(ngram[0], ngram[-1]+1)]
    elif gram:
        ran = [n-i+int(q) for q in gram.split(',')]

    if len(show) == 1:
        out = ' '.join(df.loc[ran,show[0]]).rstrip('/')
        return out.lower() if not preserve_case else out
    else:
        df = df.loc[ran]
        cols = [df[x] for x in show[1:]]
        df = df[show[0]].str.cat(cols, sep='/').str.rstrip('/')
        out = df.str.cat(sep=' ').rstrip('/')
        return out.lower() if not preserve_case else out


def partition(lst, n):
    """
    Divide a lst into n chunks
    """
    import pandas as pd
    if isinstance(lst, pd.DataFrame):
        import numpy as np
        return np.array_split(lst, n)
    from corpkit.corpus import Corpus
    if isinstance(lst, Corpus):
        lst = lst.filepaths
    q, r = divmod(len(lst), n)
    indices = [q*i + min(i, r) for i in range(n+1)]
    chunks = [lst[indices[i]:indices[i+1]] for i in range(n)]
    divved = [i for i in chunks if len(i)]
    return divved

def remove_punct_from_df(df, countmode):
    """
    Drop punctuation tokens, based on a regular expression
    """
    if countmode:
        return df
    df = df[~df['w'].isnull()]
    return df[~df['w'].str.contains(r'^-.*B-$|^[^A-Za-z0-9]*$')]

def make_compiled_statsqueries():
    """
    Stats mode involves many queries, which can take a while to compile.
    This compiles then all early

    Returns:
        dict: {name, query}
    """
    from nltk.tgrep import tgrep_compile
    tregex_qs = {#'Imperative': r'ROOT < (/(S|SBAR)/ < (VP !< VBD !< VBG !$ NP !$ SBAR < NP !$-- S '\
                 #'!$-- VP !$ VP)) !<< (/\?/ !< __) !<<\' /-R.B-/ !<<, /(?i)^(-l.b-|hi|hey|hello|oh|wow|thank|thankyou|thanks|welcome)$/',
                 'Open interrogative': r"ROOT < SBARQ <<' (/\?/ !< __)", 
                 #'Closed interrogative': r"ROOT < ((SQ < (NP $, VP)) << (/\?/ !< __)) | < ((/S|SBAR/ < (VP $, NP)) <<' (/\?/ !< __)))",
                 'Unmodalised declarative': r"ROOT < (S < (/NP|SBAR|VP/ $, (VP !< MD)))",
                 'Modalised declarative': r"ROOT < (S < (/NP|SBAR|VP/ $, (VP < MD)))",
                 'Clauses': r"/^S/ < __",
                 'Interrogative': r"ROOT << (/\?/ !< __)",
                 'Processes': r"/VB.*/ >-1 VP"}
    out = {}
    for k, v in sorted(tregex_qs.items()):
        out[k] = tgrep_compile(v)
    return out

def add_adj_for_ngram(show, gramsize):
    """
    If there's a gramsize of more than 1, remake show for ngramming
    """
    if gramsize == 1:
        return show
    out = []
    for i in show:
        out.append(i)
    for i in range(1, gramsize):
        for bit in show:
            out.append('+%d%s' % (i, bit))
    return out

def format_sent_string(sent, f=None, s=None, i=None, is_new=False, show=False, cols=False):
    """
    Nicely format a sentence DF as a string

    If f, s and i are provided, format them too.
    """
    from corpkit.constants import nospace_before, nospace_after, tok_trans

    # if conll-u v2, plaintext is stored in metadata, so we can just grab it and go.
    if cols is not False and 'text' in cols:
        n = list(cols).index('text')
        return sent[0,:n].rstrip('\n').replace(r'\n', ' ')

    #if 'text' in sent.columns and show in [False, ['w'], 'w']:
    #    return sent.iloc[0]['text'].rstrip('\n').replace(r'\n', ' ')
    # to mark matches
    if not isinstance(i, (list, tuple)):
        i = [i]
    # our string as it develops. can't use join because we may or may not have spaces
    text = []

    show = show[0] if show else 'w'
    show = list(cols).index(show)
    w = list(cols).index('w')
    f = list(cols).index('f')
    previous_row = False
    # iterate over each token in the sentence
    for ix, row in enumerate(sent, start=1):
        # get just the i if index is fsi
        #if isinstance(ix, tuple):
        #    ix = ix[-1]
        tok = tok_trans.get(row[w], row[show])
        form_tok = '<%s>' % tok if ix in i and not is_new else tok
        if previous_row is False:
            text.append(form_tok)
        else:
            if row[f] == 'punct' and not previous_row[f] == 'punct':
                pass
            elif tok in nospace_before:
                pass
            elif previous_row[show] in nospace_after:
                pass
            else:
                form_tok = ' ' + form_tok
            text.append(form_tok)
        previous_row = row
    text = ''.join(text).rstrip('\n').replace(r'\n', ' ')
    if f is not None:
        return '%s (%s, #%d)' % (text, f, int(s))
    else:
        return text

def store_as_hdf(self, path=False, append=True, name=False, colmax={}, **kwargs):
    """
    Create an HDF5-stored corpus from Corpus or LoadedCorpus
    """
    import os
    import pandas as pd
    import numpy as np
    from corpkit.corpus import Corpus

    # get name of corpus
    if name is False:
        name = getattr(self, 'name', os.path.basename(self.path))

    # generate a path to the file if need be
    appending = False
    if not path:
        appending = True
        path = os.path.join(self.path, name + '.h')

    # if the file exists, delete this table from it
    if os.path.isfile(path):
        store = pd.HDFStore(path)
        if name in [i.lstrip('/') for i in store.keys()]:
            del store[name]

    # load corpus ... perhaps not ideal :)
    if isinstance(self, Corpus):
        corpus = self.load(**kwargs)
    else:
        corpus = self

    # where our data will go
    store = pd.HDFStore(path)

    # remove bad fields
    corpus = corpus.drop(["d"], axis=1, errors='ignore')

    # remake the index as string for some reason?
    ix = list(corpus.index)
    #tup_ix = [tuple([str(f), int(s), int(i)]) for f, s, i in ix]
    #corpus.index = pd.MultiIndex.from_tuples(tup_ix)
    #corpus.index.names = ["file", "s", "i"]

    min_itemsize = {}
    corpsize = len(corpus)

    # convert some columns because of problems with categoricals
    for c in corpus.columns:
        if c in ['s', 'i', 'sent_len', '_n', 'number', 'year',
                 'g', 'c', 'postgroup', 'totalposts', 'postnum', 'postid']:
            corpus[c] = pd.to_numeric(corpus[c], errors='coerce')
        else:
            try:
                pd.to_numeric(corpus[c], errors='raise')
            except:
                corpus[c] = corpus[c].astype(object).fillna('')
                mx = corpus[c].str.len().max()
                #corpus[c] = corpus[c].str.pad(mx, side='right')
                if np.isnan(mx):
                    continue
                min_itemsize[c] = mx+1
                print("convert ", c, mx)

    if colmax:
        for k, v in colmax.items():
            if k in corpus.columns:
                try:
                    corpus[k] = corpus[k].str.slice(0,v-1)
                    print("cut %s to %d on %s." % (k, v, name))
                    min_itemsize[k] = v+1
                except:
                    print("colmax %s failed on %s." % (k, name))

    dcs = [i for i in ['file', 's', 'i', 'text'] if i in corpus.columns]
    if not all(i in corpus.columns for i in ['file', 's', 'i', 'w']):
        raise ValueError("Missing columns")
    chunksize = kwargs.get('chunksize', 80000)   
    if len(corpus) > chunksize:
        corpus = np.array_split(corpus, (corpsize // chunksize))
    else:
        corpus = [corpus]

    print("MIN ITEMSIZES", min_itemsize)


    t = False
    if len(corpus) > 1:
        from tqdm import tqdm, tqdm_notebook
        try:
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                tqdm = tqdm_notebook
        except:
            pass
        t = tqdm(total=len(corpus),
                 desc="Saving %s" % name,
                 #position=kwargs.get('paralleling', 0),
                 ncols=120,
                 unit="chunk")

    for i, d in enumerate(corpus, start=1):
        store.append(name,
                     pd.DataFrame(d),
                     format='table',
                     data_columns=dcs,
                     chunksize=chunksize,
                     expectedrows=corpsize,
                     min_itemsize=min_itemsize,
                     index=False)
        if t is not False:
            t.update()

    if t is not False:
        t.close()

    print("Stored as %s in %s" % (name, path))
    store.close()
    return store


def cmd_line_to_kwargs(args):
    """
    Turn bash-style command lin arguments into Python kwarg dict
    """
    trans = {'true': True,
         'false': False,
         'none': None}

    kwargs = {}
    for index, item in enumerate(args):
        if item.startswith('-'):
            item = item.lstrip('-').replace('-', '_')
            if 'bank' not in item:
                item = item.lower()
            if '=' in item:
                item, val = item.split('=', 1)
            else:
                try:
                    val = args[index+1]
                except IndexError:
                    val = 'true'
            if val.startswith('-'):
                val = 'true'
            val = val.strip()
            if val.isdigit():
                val = int(val)
            if isinstance(val, str):
                if val.startswith('-'):
                    continue
                val = trans.get(val.lower(), val)
            kwargs[item] = val
    return kwargs