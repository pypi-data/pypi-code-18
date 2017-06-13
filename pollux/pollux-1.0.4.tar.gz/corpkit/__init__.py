"""
A toolkit for corpus linguistics
"""

from __future__ import print_function

#metadata
__version__ = "3.0.0"
__author__ = "Daniel McDonald"
__license__ = "MIT"

# probably not needed, anymore but adds corpkit to path for tregex.sh
import sys
import os
import inspect

# asterisk import
__all__ = [
    "load",
    "loader",
    "as_regex",
    "new_project",
    "Corpus",
    "File", "LoadedCorpus"]

corpath = inspect.getfile(inspect.currentframe())
baspat = os.path.dirname(corpath)
#dicpath = os.path.join(baspat, 'dictionaries')
for p in [corpath, baspat]:
    if p not in sys.path:
        sys.path.append(p)
    if p not in os.environ["PATH"].split(':'): 
        os.environ["PATH"] += os.pathsep + p

# import classes
from corpkit.corpus import Corpus, File, LoadedCorpus
from corpkit.interrogation import _table, _sort, Results, _conc
from corpkit.interrogator import interrogator
#from corpkit.model import MultiModel

from corpkit.other import (load, loader, as_regex, new_project)

from corpkit.lazyprop import lazyprop

# monkeypatch editing and plotting to pandas objects
import pandas as pd
from pandas import DataFrame, Series
pd.options.mode.chained_assignment = None

# monkey patch functions
def _plot(self, *args, **kwargs):
    from corpkit.plotter import plotter
    return plotter(self, *args, **kwargs)

def _save(self, savename, **kwargs):
    from corpkit.other import save
    save(self, savename, **kwargs)

def _format(self, *args, **kwargs):
    from corpkit.other import concprinter
    concprinter(self, *args, **kwargs)

def _texify(self, *args, **kwargs):
    from corpkit.other import texify
    texify(self, *args, **kwargs)

def _calculate(self, *args, **kwargs):
    from corpkit.process import interrogation_from_conclines
    return interrogation_from_conclines(self)

def _multiplot(self, main_params={}, sub_params={}, **kwargs):
    from corpkit.plotter import multiplotter
    return multiplotter(self, main_params=main_params, sub_params=sub_params, **kwargs)

def _perplexity(self):
    """
    Pythonification of the formal definition of perplexity.

    input:  a sequence of chances (any iterable will do)
    output: perplexity value.

    from https://github.com/zeffii/NLP_class_notes
    """
    def _perplex(chances):
        import math
        chances = [i for i in chances if i] 
        N = len(chances)
        product = 1
        for chance in chances:
            product *= chance
        return math.pow(product, -1/N)

    return self.apply(_perplex, axis=1)

def _entropy(self):
    """
    entropy(pos.edit(merge_entries=mergetags, sort_by='total').results.T
    """
    from scipy.stats import entropy
    import pandas as pd
    escores = entropy(self.edit('/', SELF).results.T)
    ser = pd.Series(escores, index=self.index)
    ser.name = 'Entropy'
    return ser

def _shannon(self):
    from corpkit.stats import shannon
    return shannon(self)


def _shuffle(self, inplace=False):
    import random
    index = list(self.index)
    random.shuffle(index)
    shuffled = self.ix[index]
    shuffled.reset_index()
    if inplace:
        self = shuffled
    else:
        return shuffled

def _top(self):
    """Show as many rows and cols as possible without truncation"""
    import pandas as pd
    max_row = pd.options.display.max_rows
    max_col = pd.options.display.max_columns
    return self.iloc[:max_row, :max_col]

def _tabview(self, decimals=3, **kwargs):
    import pandas as pd
    import tabview
    kwargs['align_right'] = [False] * len(self.index.names) + [True] * len(self.columns)
    tabview.view(self.round(decimals=decimals), **kwargs)

def _rel(self, relative=True, **kwargs):
    import pandas as pd
    if relative is True:
        return (self.T * 100.0 / self.sum(axis=1)).T
    elif isinstance(relative, (pd.Series, int, float)):
        return self * 100.0 / relative
    else:
        raise NotImplementedError

def _plain(df):
    return ' '.join(df['w'])

# monkey patching things

DataFrame.entropy = _entropy
DataFrame.perplexity = _perplexity
DataFrame.shannon = _shannon

DataFrame.rel = _rel
Series.rel = _rel

DataFrame.visualise = _plot
Series.visualise = _plot

DataFrame.tabview = _tabview

DataFrame.multiplot = _multiplot
Series.multiplot = _multiplot

DataFrame.save = _save
Series.save = _save

DataFrame.format = _format
Series.format = _format

Series.texify = _texify

DataFrame.calculate = _calculate
Series.calculate = _calculate

DataFrame.shuffle = _shuffle

DataFrame.top = _top

DataFrame.plain = _plain

DataFrame.table = _table
DataFrame.sort = _sort
DataFrame.conc = _conc

ANYWORD = r'[A-Za-z0-9:_]'

def _search(self, *args, **kwargs):
    return interrogator(self, *args, **kwargs)

DataFrame.search = _search

def _deps(self, *args, **kwargs):
    return interrogator(self, 'd', *args, **kwargs)

DataFrame.deps = _deps

def _keys(self, *args, **kwargs):
    from corpkit.keys import keywords
    return keywords(self, *args, **kwargs)

DataFrame.keyness = _keys