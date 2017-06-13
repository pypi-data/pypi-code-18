"""
corpkit: `Interrogation and Interrogation-like classes
"""

from __future__ import print_function
from collections import OrderedDict
import pandas as pd
from corpkit.constants import STRINGTYPE, CONLL_COLUMNS
from corpkit.views import _table, _sort, _conc
from corpkit.interrogator import interrogator
from corpkit.plotter import plotter, multiplotter
from corpkit.process import classname

class Results(pd.DataFrame):
    """
    Search results, a record of matching tokens in a Corpus
    """
    # temporary properties
    _internal_names = pd.DataFrame._internal_names + ['is_new'] # qstring?
    _internal_names_set = set(_internal_names)

    # normal properties
    _metadata = ['reference', 'path', 'qstring']

    @property
    def _constructor(self):
        return Results

    def __init__(self, matches, reference=False, path=False, qstring=False):
        super(Results, self).__init__(matches)
        self.reference = reference
        self.path = path
        self.qstring = qstring

    def __repr__(self):
        return pd.DataFrame.__repr__(pd.DataFrame(self))

        #super(Results, self).__repr__()

    def __bool__(self):
        return bool(len(self))

    def __nonzero(self):
        return bool(len(self))

    #def __invert__(self):
    #    if not isinstance(self.reference, bool):
    #        return self.reference[~self.reference._n.isin(self._n)]
    
    #def __str__(self):
    #    fmt = (classname(self), format(len(self), ','))
    #    return "<%s instance: %s total>" % fmt

    def keyness(self, *args, **kwargs):
        """
        Calculate keyness for each subcorpus

        Return:
            DataFrame
        """
        from corpkit.keys import keywords
        return keywords(self, *args, **kwargs)

    def visualise(self, **kwargs):
        """Visualise corpus interrogations.

        Keyword args:

           title (str): A title for the plot
           x_label (str): A label for the x axis
           y_label (str): A label for the y axis
           kind (str): The kind of chart to make
           style (str): Visual theme of plot
           figsize (tuple of dimensions): Size of plot
           save (bool/str): If bool, save with *title* as name; if str, use str as name
           legend_pos (str): Where to place legend
           reverse_legend (bool): Reverse the order of the legend
           num_to_plot (int/`'all'`): How many columns to plot
           tex (bool): Use TeX to draw plot text
           colours (str): Colourmap for lines/bars/slices
           cumulative (bool): Plot values cumulatively
           pie_legend (bool): Show a legend for pie chart
           partial_pie (bool): Allow plotting of pie slices only
           show_totals (str: `legend`/`plot`): Print sums in plot where possible
           transparent (bool): Transparent .png background
           output_format (str): File format for saved image
           black_and_white (bool): Create black and white line styles
           show_p_val (bool): Attempt to print p values in legend if contained in df
           stacked (bool): When making bar chart, stack bars on top of one another
           filled (bool): For area and bar charts, make every column sum to 100
           legend (bool): Show a legend
           rot (int): Rotate x axis ticks by *rot* degrees
           subplots (bool): Plot each column separately
           layout (tuple): Grid shape to use when *subplots* is True
           interactive: Experimental interactive options
           
        Return:
           matplotlib figure
        """
        return plotter(self, **kwargs)

    def multiplot(self, main_params={}, sub_params={}, **kwargs):
        """
        Plot a figure and subplots together

        Keyword args:

           main_params (dict): arguments for Results.visualise(), used to draw the large figure
           sub_params (dict): arguments for Results.visualise(), used to draw the sub figures.
              if a key is `data`, use its value as secondary data to plot.
           layout (int/float): a number between 1 and 16, corresponding to number of subplots.
              some numbers have an alternative layout accessible with floats (e.g. 3.5).
           kwargs (dict): arguments to pass to both figures
        """
        from corpkit.plotter import multiplotter
        return multiplotter(self, main_params=main_params, sub_params=sub_params, **kwargs)

    def tabview(self, decimals=3, **kwargs):
        import tabview
        kwargs['align_right'] = [False] * len(self.index.names) + [True] * len(self.columns)
        tabview.view(self.round(decimals=decimals), **kwargs)

    def save(self, **kwargs):
        from corpkit.other import save
        save(self, savename, **kwargs)

    def format(self, *args, **kwargs):
        print(pd.DataFrame(self))

    def calculate(self, **kwargs):
        from corpkit.process import interrogation_from_conclines
        return interrogation_from_conclines(self)

    def top(self, **kwargs):
        max_row = pd.options.display.max_rows
        max_col = pd.options.display.max_columns
        return self.iloc[:max_row, :max_col]

    def table(self, subcorpora='file', *args, **kwargs):
        """
        Create a spreadsheet-like table, showing one or more features by one or more others

        Args:
           subcorpora (str/list): which metadata or word feature(s) to put on the y axis
           show (str/list): word or metadata features to put on the x axis
           relative (bool/DataFrame): calculate relative frequencies using self or passed data
           keyness (bool/DataFrame):calculate keyness frequencies using self or passed data

        Return:
           pd.DataFrame

        """
        if 'df' not in kwargs:
            kwargs['df'] = self.reference
        return _table(self, subcorpora, *args, **kwargs)

    def conc(self, *args, **kwargs):
        """
        Generate a concordance

        Args:
            show (list of strs): how to display concordance matches
            n (int): number to show
            shuffle (bool): randomise order

        Return:
            pd.DataFrame: generated concordance lines
        """

        if 'df' not in kwargs:
            kwargs['df'] = self.reference
        from corpkit.corpus import LoadedCorpus
        kwargs['is_new'] = type(self) == LoadedCorpus
        return _conc(self, *args, **kwargs)

    def sort(self, **kwargs):
        return _sort(self, **kwargs)

    def search(self, *args, **kwargs):
        """
        Equivalent to `corpus.search()`
        """
        kwargs['df'] = self.reference
        return interrogator(self, *args, **kwargs)

    def deps(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('d', query)`
        """
        return interrogator(self, 'd', *args, **kwargs)

    def trees(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('t', query)`
        """
        return interrogator(self, 't', *args, **kwargs)

    def lemmas(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('l', query)`
        """
        return interrogator(self, 'l', *args, **kwargs)

    def pos(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('p', query)`
        """
        return interrogator(self, 'l', *args, **kwargs)

    def xpos(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('x', query)`
        """
        return interrogator(self, 'l', *args, **kwargs)

    def lemmas(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('l', query)`
        """
        return interrogator(self, 'l', *args, **kwargs)

    def words(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('w', query)`
        """
        return interrogator(self, 'w', *args, **kwargs)

    def functions(self, *args, **kwargs):
        """
        Equivalent to `corpus.search('w', query)`
        """
        return interrogator(self, 'f', *args, **kwargs)

    def collapse(self, feature, values, name=False):
        """
        Merge result on entries or metadata

        Returns:
           Results (subset)
        """
        res = self.copy()
        # allow regex
        if isinstance(values, list) and len(values) == 1:
            raise ValueError("Need more than one item to collapse, or pass in a regex str.")
        if isinstance(values, str):
            if not name:
                raise ValueError("New name needed.")
            res[feature] = res[feature].astype(str).str.replace(values, replace_name)
        else:
            replace_name = name if name else values.pop(0)
            for i in values:
                res[feature] = res[feature].astype(str).str.replace(i, replace_name)

        return Results(matches=res, reference=self.reference)

    def just(self, dct, mode='any'):
        """
        Reduce a DataFrame by string matching
        """
        import pandas as pd
        bools = []
        for k, v in just.items():
            bools.append(self[k].str.contains(v, case=False))
        bools = pd.concat(bools, axis=1)
        if mode == 'any':
            self = self[bools.any(axis=1)]
        elif mode == 'all':
            self = self[bools.all(axis=1)]
        return self

    def skip(self, dct):
        """
        Reduce a DataFrame by inverse string matching
        """
        import pandas as pd
        bools = []
        for k, v in dct.items():
            bools.append(self[k].str.contains(v, case=False))
        bools = pd.concat(bools, axis=1)
        if mode == 'any':
            self = self[~bools.any(axis=1)]
        elif mode == 'all':
            self = self[~bools.all(axis=1)]
        return self

    def top(self, n=50, feature='w'):
        """
        Get the top n most common results by column

        Args:

           n (int): number of most common results to show
           feature (str): which feature to count

        Returns:
            Results (subset)
        """
        ws = self[feature].str.lower().value_counts().head(n)
        return self[self[feature].isin(ws.index)]

    def save(self, savename, savedir='saved_interrogations', **kwargs):
        """
        Save an interrogation as pickle to ``savedir``.

        Example:
        
        >>> o = corpus.interrogate(W, 'any')
        ### create ./saved_interrogations/savename.p
        >>> o.save('savename')
        
            savename (`str`): A name for the saved file
            savedir (`str`): Relative path to directory in which to save file
            print_info (`bool`): Show/hide stdout
        """
        from corpkit.other import save
        save(self, savename, savedir=savedir, **kwargs)

    def store_as_hdf(self, **kwargs):
        """
        Store a result within an HDF5 file.
        """
        from corpkit.process import store_as_hdf
        return store_as_hdf(self, **kwargs)