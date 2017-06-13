def _conc(self,
          show=['w'],
          n=9999, 
          shuffle=False, 
          count=False, 
          low_memory=False,
          preserve_case=True, 
          is_new=False, 
          ngram=False,
          df=False,
          context=False,
          **kwargs):

    colours = kwargs.get('colour', False)
    if count:
        raise ValueError("Counted result has no data to concordance.")
    import pandas as pd
    from corpkit.constants import CONLL_COLUMNS, CORENLP_COREF_CATS, GOV_ATTRS
    from corpkit.process import apply_show, remove_punct_from_df

    if not isinstance(show, list):
        show = [show]

    #print('\n\n', self.head(), df.head())

    df, reference = make_df_and_reference(self, passed_in=df, subcorpora=[], show=show, is_new=is_new, conc=True)
    #print('\n\n', df.head(), reference.head())

    for i in show:
        if i.startswith(('+', '-')):
            df[i] = reference[i[2:]].shift(-int(i[1]))

    #if n is not False:
    #    print(df.head())
    #    df = df.head(n)
    #    reference = reference.head(n)

    if shuffle:
        import numpy as np
        df = df.reindex(np.random.permutation(df.index))

    if colours:
        # can we do another all_dat.update()
        formatted = add_colours(reference.copy(), colours, show, df.index)
        for col in list(formatted.columns):
            reference[col] = formatted[col]

    if is_new:
        if 'text' in df.columns:
            df['sentence'] = df['text']
        else:
            if 'i' not in df.columns:
                df['i'] = 1
            subdf = pd.DataFrame(df.reset_index()[['i', 'index', 'sent_len']])
            df['sentence'] = subdf.apply(_make_conc, axis=1, vals=reference['w'].values,
                                         raw=True, sent_mode=True, ngram=ngram)

        # this is a quick hack to color separators in word/lemma/pos
        if colours:
            df['sentence'] = df['sentence'].str.replace('</span>/<span', '/</span><span')
    else:
        if len(show) == 1 and show[0] in df.columns and ngram is False:
            df = df.copy()
            if preserve_case:
                df['match'] = df[show[0]]
            else:
                df['match'] = df[show[0]].str.lower()
        elif len(show) > 1 and all(i in df.columns for i in show) and ngram is False:
            df['match'] = df[show[0]].str.cat([df[x] for x in show[1:]], sep='/')
            if not preserve_case:
                df['match'] = df['match'].str.lower()
        else:
            #intshow = [reference.columns.get_loc(i) for i in show]
            positions = {y: x for x, y in enumerate(list(reference.columns))}
            df['match'] = df.apply(apply_show, axis=1, show=show, df=reference,
                               preserve_case=preserve_case, ngram=ngram, positions=positions)


        #subdf = pd.DataFrame(df[['i', '_n', 'sent_len',  'match']])
        subdf = pd.DataFrame(df.reset_index()[['i', 'index', 'sent_len', 'match']])
        #subdf = subdf.reset_index()
        l_r = subdf.apply(_make_conc, axis=1, vals=reference['w'].values, raw=True, context=context, ngram=ngram)
        df['left'], df['right'] = list(zip(*l_r))
        if colours:
            df['match'] = df['match'].str.replace('</span>/<span', '/</span><span')

    to_drop = ['parse', 'sent_len', 'text', 'head', 'e', 'n', 'x'] + CONLL_COLUMNS[1:]
    to_drop = to_drop + [i for i in list(df.columns) if i.startswith('_')] +  CORENLP_COREF_CATS + GOV_ATTRS
    df = df.drop(to_drop, axis=1, errors='ignore')
    df = conc_order(df, is_new)
    if 'corpus' in df.columns and not df['corpus'].any():
        df = df.drop('corpus', axis=1)

    return df

def _make_conc(row, vals, context=False, sent_mode=False, ngram=False):
    # row == i, n, sent_len, match
    nstart = ngram[0] if ngram is not False else 0
    nend = ngram[1] if ngram is not False else 0
    if context:
        match = context
        start = row[1] - context
        if start < 0:
            match -= abs(start)
            start = 0
        end = row[1] + context + 1
        if end > len(vals) - 1:
            end = len(vals) - 1
    else:
        start = row[1] - row[0] + 1
        end = start + row[2]
        match = row[0]
    sent = vals[int(start):int(end)]
    
    if sent_mode:
        return ' '.join(sent)
    else:
        return [' '.join(sent[:int(match)-1-nstart]), ' '.join(sent[int(match)+nend:])]

def _just_or_skip(self, skip=False, entries={}, metadata={}, mode='any',
                  case_sensitive=False):
    """
    Meta function for just or skip methods. If skip is True, the matches
    are inverted.

    #todo: case_sensitive

    Return:
        Results
    """
    from corpkit.conll import governor, dependents
    from corpkit.interrogation import Results
    import numpy as np

    # to skip, we invert the matches with numpy
    inverter = np.invert if skip else lambda x: x

    if mode != 'any':
        raise NotImplementedError
    
    rec = self.copy()
    if isinstance(entries, STRINGTYPE):
        entries = {'w': entries}

    ents = rec[CONLL_COLUMNS[1:]]
    for k, v in entries.items():
        obj, attrib = k[0], k[-1]
        
        if obj == 'g':
            maderows = ents.apply(governor, axis=1, df=self.reference)
            maderows = maderows[attrib]
        
        elif obj == 'd':
            raise NotImplementedError

        elif obj == attrib:
            maderows = rec[attrib]
        
        if isinstance(v, list):
            rec = rec[inverter(maderows.isin(v))]
        elif isinstance(v, STRINGTYPE):
            rec = rec[inverter(maderows.str.contains(v))]
        elif isinstance(v, int):
            rec = rec[inverter(maderows == v)]

    if isinstance(metadata, STRINGTYPE):
        metadata = {'w': metadata}

    for k, v in metadata.items():
        if isinstance(v, list):
            rec = rec[inverter(rec[k].isin(v))]
        elif isinstance(v, STRINGTYPE):
            rec = rec[inverter(rec[k].str.contains(v))]
        elif isinstance(v, int):
            rec = rec[inverter(rec[k] == v)]

    entries.update(metadata)
    querybits = {'search': entries,
                 'searchmode': mode,
                 'depgrep_string': False,
                 'tgrep_string': False,
                 'inverse': skip,
                 'case_sensitive': case_sensitive}
                 
    from corpkit.interrogation import Results
    return Results(rec, reference=self.reference)

def format(self, kind='string', n=100, window=35,
           print_it=True, columns='all', metadata=True, **kwargs):
    """
    Print concordance lines nicely, to string, LaTeX or CSV

    Keyword args:

        kind (`str`): output format: `string`/`latex`/`csv`
        n (`int`/`'all'`): Print first `n` lines only
        window (`int`): how many characters to show to left and right
        columns (`list`): which columns to show

    Example:

    >>> lines = corpus.concordance({T: r'/NN.?/ >># NP'}, show=L)
    ### show 25 characters either side, 4 lines, just text columns
    >>> lines.format(window=25, n=4, columns=[L,M,R])
        0                  we 're in  tucson     , then up north to flagst
        1  e 're in tucson , then up  north      to flagstaff , then we we
        2  tucson , then up north to  flagstaff  , then we went through th
        3   through the grand canyon  area       and then phoenix and i sp

    Return:
        None
    """
    from corpkit.other import concprinter
    if print_it:
        print(concprinter(self, kind=kind, n=n, window=window,
                       columns=columns, return_it=True, metadata=metadata, **kwargs))
    else:
        return concprinter(self, kind=kind, n=n, window=window,
                       columns=columns, return_it=True, metadata=metadata, **kwargs)

def tabview(self, window=(55, 55), df=False, **kwargs):
    """
    Show concordance in interactive cli view
    """
    from tabview import view
    import pandas as pd
    if isinstance(self.index, pd.MultiIndex):
        lsts = list(zip(*self.index.to_series()))
        widths = []
        for l in lsts:
            w = max([len(str(x)) for x in l])
            if w < 10:
                widths.append(w)
            else:
                widths.append(10)
    else:
        iwid = self.index.astype(str)[:100].str.len().max() + 1
        if iwid > 10:
            iwid = 10
        widths = [iwid]
    tot = len(self.columns) + len(self.index.names)
    aligns = [True] * tot
    truncs = [False] * tot
    if isinstance(window, int):
        window = [window, window]
    else:
        window = list(window)
    if window[0] > self['left'][:100].str.len().max():
        window[0] = self['left'][:100].str.len().max()
    if window[1] > self['right'][:100].str.len().max():
        window[1] = self['right'][:100].str.len().max()

    for i, c in enumerate(self.columns):
        if c == 'left':
            widths.append(window[0])
            truncs[i+len(self.index.names)] = True
        elif c == 'right':
            widths.append(window[1])
            aligns[i+len(self.index.names)] = False
        elif c == 'match':
            mx = self[c].astype(str)[:100].str.len().max() + 1
            if mx > 15:
                mx = 15
            widths.append(mx)
            aligns[i+len(self.index.names)] = False         
        else:
            mx = self[c].astype(str)[:100].str.len().max() + 1
            if mx > 10:
                mx = 10
            widths.append(mx)

    kwa = {'column_widths': widths, 'persist': True, 'trunc_left': truncs,
           'colours': kwargs.get('colours', False), 'df': self.reference}
    
    if 'align_right' not in kwargs:
        kwa['align_right'] = aligns

    view(pd.DataFrame(self), **kwa)

def _sort(df, by=False, keep_stats=False, remove_above_p=False):
    """
    Sort results, potentially using scipy's linregress
    """
    # translate options and make sure they are parseable
    stat_field = ix = ['_slope', '_intercept', '_r', '_p', '_stderr']
    easy_sorts = ['total', 'infreq', 'name', 'most', 'least', 'reverse']
    stat_sorts = ['increase', 'decrease', 'static', 'turbulent']

    options = stat_field + easy_sorts + stat_sorts

    # allow some alternative names
    by_convert = {'most': 'total', True: 'total', 'least': 'infreq'}
    by = by_convert.get(by, by)

    def lingres(ser, index):
        """
        Appliable stats calculation
        """
        from scipy.stats import linregress
        import pandas as pd
        ix = ['_slope', '_intercept', '_r', '_p', '_stderr']
        return pd.Series(linregress(index, ser.values), index=ix)

    if keep_stats or by in stat_field + stat_sorts:
        import numpy as np
        x = list(range(len(df)))
        # quick fix: do not have categorical index, because we might want to do regression on them
        try:
            df.index = df.index.astype(int)
        except:
            try:
                df.index = df.index.astype(object)
            except:
                pass
        stats = df.apply(lingres, axis=0, index=x)
        df = df.append(stats)
        df = df.replace([np.inf, -np.inf], 0.0)
    
    if by == 'name':
        # currently case sensitive
        df = df.reindex_axis(sorted(df.columns), axis=1)
        
    elif by in ['total', 'infreq']:
        df = df[list(df.sum().sort_values(ascending=by != 'total').index)]
    
    elif by == 'reverse':
        # performance tested
        df = df.loc[::,::-1]
    # sort by slope etc., or search by subcorpus name
    if by in stat_field or by not in options:
        df = df.T.sort_values(by=by, ascending=False).T
    
    if '_slope' in df.index:
        slopes = df.loc['_slope']
        if by == 'increase':
            std = slopes.sort_values(ascending=False)
            df = df[std.index]
        elif by == 'decrease':
            std = slopes.sort_values(ascending=True)
            df = df[std.index]
        elif by == 'static':
            std = slopes.abs().sort_values(ascending=True)
            df = df[std.index]
        elif by == 'turbulent':
            std = slopes.abs().sort_values(ascending=False)
            df = df[std.index]
        if remove_above_p > 0:
            df = df.T
            df = df[df['_p'] <= remove_above_p]
            df = df.T

    # remove stats field by default
    if not keep_stats:
        df = df.drop(stat_field, axis=0, errors='ignore')
    else:
        df.index = [i.lstrip('_') if i in stat_field else i for i in list(df.index)]

    return df

def df_denom(col, df=False):
    try:
        return col * 100.0 / df[col.name]
    except KeyError:
        return 100.0

def multiplot(self, leftdict={}, rightdict={}, **kwargs):
    from corpkit.plotter import multiplotter
    return multiplotter(self, leftdict=leftdict, rightdict=rightdict, **kwargs)

def colour_apply(row):
    html = '<span class="rounded" style="color:black;background-color:{};display:inline-block;margin-right:0px;">{}</span>'
    hex_col = row.pop('_colour')
    row = row.apply(lambda x: html.format(hex_col, x))
    return row

def add_colours(df, attr, show, ix):
    """
    Add HTML spans around tokens based on some attribute

    Args:
       df (DataFrame): records containing matches/sentences
       colours (str): attribute to colour
    """

    pastels = ['#ffb3ba',
               '#ffdfba',
               '#ffffba',
               '#baffc9',
               '#bae1ff',
               '#ffddba',
               '#babaff',
               '#cecece',
               '#ffb3b3',
               '#b3ffc2',
               '#b3d3ff',
               '#ffb3ff',
               '#b3f3ff',
               '#e4ffb3',
               '#d6ffb3']

    pos = ['nn',
           'vb',
           'jj',
           'rb',
           'in',
           'dt',
           'cc',
           'pr',
           'md',
           'wr',
           'rp',
           'to',
           'ex',
           'cd',
           'wp']

    ner = ['pe', 'or', 'lo', 'ti']

    mood = {# subject
            'csubj':   '#ffb3ba',
            'nsubj':   '#ffb3ba',
            # finite
            'aux':     '#ffdfba',
            # predicator
            'ccomp':   '#ffffba',
            'cop':     '#ffffba',
            'root':    '#ffffba',
            'compound:prt': '#ffffba',
            # below just don't work well
            ##complement
            #'acomp':   '#baffc9',
            #'dobj':    '#baffc9',
            #'iobj':    '#baffc9',
            ## adjunct
            #'agent':   '#bae1ff',
            #'advmo':   '#bae1ff',
            #'tmod':    '#bae1ff',
            #'advcl':   '#bae1ff',
            #'nmod_':   '#bae1ff',
            #'prep_':   '#bae1ff'
            }

    trans = {#participant
            'csubj':   '#ffb3ba',
            'nsubj':   '#ffb3ba',
            #process
            'ccomp':   '#ffffba',
            'cop':     '#ffffba',
            'root':    '#ffffba',
            'aux':     '#ffffba',
            #modifier/circumstance?
            }

    possible = {'p': pos, 'n': ner, 'm': mood, 't': trans,}
    if attr in ['t', 'm']:
        colour_dict = possible[attr]
        num = 5
        attr = 'f'
        default_colour = 'white'
    else:
        # fix the get
        colour_dict = {k: pastels[i] for i, k in enumerate(possible[attr])}
        num = 2
        default_colour = '#e5e5ff'
    
    # we just need the columns we'll show, plus the column telling us the format
    setcol = list(set(show + [attr]))

    # needed columns only
    dfx = df[setcol].copy()

    # needed rows only
    #needed_rows = dfx[dfx.index.droplevel('i').isin(ix.droplevel('i').unique())]
    needed_rows = dfx
    # add a column with the hex value
    needed_rows['_colour'] = needed_rows[attr].apply(lambda x: colour_dict.get(x.lower()[:num], default_colour))
    # remove the unneeded column
    needed_rows = needed_rows[show + ['_colour']]
    # make spans
    needed_rows = needed_rows.apply(colour_apply, axis=1)
    dfx.update(needed_rows)
    return dfx

def conc_order(df, is_new):
    """
    Reorder columns of a concordance
    """
    if is_new:
        start = ['sentence', 'file', 's', 'i']
    else:
        start = ['left', 'match', 'right', 'file', 's', 'i']
    dfcols = [i for i in df.columns if i not in start and not i.startswith('_')]
    allcols = start + dfcols
    df = df[allcols]
    df = df.reset_index(drop=True)
    df.index += 1
    df.index.name = '#'
    return df

def make_df_and_reference(corpus, passed_in=False, subcorpora=False, show=False, is_new=False, conc=False):
    import pandas as pd

    # if the user passed it in, it's good.
    reference = passed_in

    if reference is False:
        # if it's a dataframe, basically, then we need a reference passed in
        if not hasattr(corpus, 'reference'):
            reference = passed_in
        # if the reference corpus was never saved, it must be passed in
        elif getattr(corpus, 'reference', False) is False:
            reference = passed_in
        else:
            # otherwise, we should have a corpus
            reference = corpus.reference
    # if we don't, let's assume the corpus is the reference
    if reference is False:
        reference = corpus
    
    # get just the first word of each sent if new and return
    if is_new:
        corpus = reference[reference.i == 1]
        # way slower, possibly more accurate
        #corpus = reference.groupby('s').first()
        return corpus, reference
    
    # the hard bit: get all needed data from reference
    if not conc:
        extras = [i for i in ['sent_len', '_gram', 'file', 's', 'i'] if i in reference.columns]
        reference = reference[list(set(show+subcorpora+extras))]
    corpus = reference.loc[list(corpus.index)]

    return corpus, reference

def uncomma(row, df, df_show_col, gram_ix):
    n = row.name
    gramsize = str(row[gram_ix]).count(',')+1
    #if len(show) > 1:
    #    raise NotImplementedError
    try:
        rel = df[n:n+gramsize,df_show_col]
        #todo: if df_show_col is list, do slash sep
        form = ' '.join(rel)
        return form
    except:
        return ''

def _table(self,
           subcorpora,
           show=['w'],
           preserve_case=False,
           count=False,
           no_punct=True,
           sort='total',
           relative=False,
           keyness=False,
           ngram=False,
           is_new=False,
           df=False,
           top=-1,
           **kwargs):
    """
    Generate a result table view from Results, or a Results-like DataFrame
    """
    import pandas as pd
    from corpkit.corpus import Corpus, LoadedCorpus
    from corpkit.interrogation import Results
    from corpkit.process import remove_punct_from_df, apply_show
    from corpkit.constants import STATS_FIELDS

    if keyness is not False and relative is not False:
        return ValueError("You can either make relative frequencies or keyness calculations, not both.")

    if subcorpora == 'default' or subcorpora is False:
        subcorpora = 'file'

    if not isinstance(show, list):
        show = [show]
    if not isinstance(subcorpora, list):
        subcorpora = [subcorpora]

    df, reference = make_df_and_reference(self, passed_in=df, subcorpora=subcorpora, show=show)

    for i in show:
        if i.startswith(('+', '-')):
            df[i] = reference[i[2:]].shift(-int(i[1]))

    #if ngram:
        #0, 1
    #    for n in range(ngram[0], ngram[-1]+1):
    #        df['_n'+str(n)]

    # _match MUST be created below?

    # if count, the df is just sents, so it's all a bit different
    if count:
        # make the index and drop all metadata fields
        from corpkit.constants import STATS_FIELDS
        df = df.fillna({s: 'UNKNOWN' for s in subcorpora})
        #df.pivot_table(index, columns, values, aggfunc=sum)
        df = df.set_index(subcorpora, drop=False)
        df = df[STATS_FIELDS]
        df = df.groupby(df.index).sum()
        try:
            df.index = pd.MultiIndex.from_tuples(df.index, names=subcorpora)
        except (TypeError, ValueError):
            pass

    else:
        comma_ix = '_gram' in list(df.columns) and df._gram.values[0] is not False
        if all(i in df.columns for i in show) and ngram is False \
            and not comma_ix:
            if len(show) == 1:
                df['_match'] = df[show[0]].astype(object)
            else:
                cats = [df[i] for i in show[1:]]
                df['_match'] = df[show[0]].str.cat(others=cats, sep='/').str.rstrip('/')
        else:
            # make a minimal df for formatting
            # this bit of the code is performace critical, so it's really evil
            if ngram:
                positions = {y: x for x, y in enumerate(list(reference.columns))}
                df['_match'] = df.apply(apply_show, axis=1, show=show, df=reference,
                               preserve_case=preserve_case, ngram=ngram, positions=positions)
            elif comma_ix:
                df['_match'] = df.apply(uncomma,
                                        axis=1,
                                        raw=True,
                                        df=reference.values,
                                        df_show_col=list(reference.columns).index(show[0]),
                                        gram_ix=list(df.columns).index('_gram'))

        if not preserve_case:
            try:
                df['_match'] = df['_match'].str.lower()
            except:
                raise
                # ValueError: no match col           ['w'] Index([], dtype='object')
                raise ValueError("no match col" + str(show) + ' ' + str(df.columns))

        if top > 0:
            tops = df['_match'].str.lower().value_counts().head(top)
            df = df[df['_match'].isin(set(tops.index))]

        # for some unknown reason this is more stable than using len as aggfunc without values
        df['_count'] = 1
        df = pd.DataFrame(df).pivot_table(index=subcorpora, columns='_match', values='_count', aggfunc=sum)
        
        try:
            del df.columns.name
        except:
            pass

        df.index.names = [s.lstrip('_') for s in subcorpora]
        try:
            df = df.fillna(0.0)
        except:
            pass

    # relative of self
    if relative is True:
        df = df.T * 100.0 / df.sum(axis=1)
        df = df.T
    # relative of totals
    elif relative is not False and isinstance(relative, (pd.Series, int, float)):
        df = df.T * 100.0 / relative
        df = df.T
    else:
        if isinstance(relative, Corpus):
            # corpus needs to be in memory at least!
            relative = relative.load()
        if isinstance(relative, (Results, LoadedCorpus)):
            relative = relative.table(subcorpora=subcorpora).sum(axis=1)
            df = df.T * 100.0 / relative
            df = df.T
        elif isinstance(relative, pd.DataFrame):
            df = df.apply(df_denom, axis=0, df=relative)
    
    if keyness is not False and keyness is not None:
        sort = False
        from corpkit.keys import keywords
        df = keywords(df, reference_corpus=keyness, **kwargs)

    if sort:
        ks = kwargs.get('keep_stats', False)
        rap = kwargs.get('remove_above_p', False)
        df = _sort(df, by=sort, keep_stats=ks, remove_above_p=rap)

    # recast to int if possible
    # todo: add dtype check, or only do when
    try:
        if isinstance(df, pd.DataFrame) and \
            df.dtypes.all() == float and \
            df.applymap(lambda x: x.is_integer()).all().all():
            df = df.astype(int)
    except AttributeError:
        pass

    return df
