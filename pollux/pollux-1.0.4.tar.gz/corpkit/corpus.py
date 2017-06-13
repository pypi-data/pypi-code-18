import os
from corpkit.lazyprop import lazy_property
from corpkit.interrogation import Results
from corpkit.process import classname
import collections

class Corpus(collections.MutableSequence):
    """
    Model a parsed or unparsed corpus with arbitrary depth of subfolders
    """

    def __new__(self, path_or_data, **kwargs):
        if isinstance(path_or_data, str) and path_or_data.endswith('.h'):
                import pandas as pd
                store = pd.HDFStore(path_or_data)
                data = store[os.path.basename(path_or_data)[:-2]]
                store.close()
                return LoadedCorpus(data=data, path=path_or_data)
        else:
            return super().__new__(self)

    def __init__(self, path_or_data, **kwargs):
        # in here we'll put the corpus files
        fs = []
        
        # defaults
        self.singlefile = False
        self.path = False
        self.datatype = 'conll'
        self._trees = {}
        self._subcorpus = kwargs.get('in_subcorpus', False)
        self._sliced = kwargs.get('sliced', False)
        self._id = 0
        self._hdf5 = False

        # these make it possible to cut the corpus short quickly
        self.just = kwargs.pop('just', None)
        self.skip = kwargs.pop('skip', None)

        if not len(path_or_data):
            raise ValueError("Corpus cannot be empty.")

        # if path wasn't passed in as a kwarg, this must be it
        if not kwargs.get('path'):
            self.path = path_or_data
        else:
            # i want this to raise an error if not there
            self.path = kwargs.pop('path', '')
            # for when files are passed in (i.e. slicing)
            fs = path_or_data

        self.name = os.path.basename(self.path)

        # get singlefile, datatype
        if isinstance(self.path, str):
            self.singlefile = os.path.isfile(self.path)
            if self.singlefile:
                if self.path.endswith('conll'):
                    self.datatype = 'conll'
                else:
                    self.datatype = 'plaintext'
            else:
                if self.path.endswith('-parsed'):
                    self.datatype = 'conll'
                else:
                    self.datatype = 'plaintext'
            
        # prepend 'data' if corpus can't be found at path
        if isinstance(self.path, str) and \
            not os.path.isdir(self.path) and \
            not self.singlefile:
            self.path = os.path.join('data', self.path)

        # if the user gave a path to a corpus, make a list of File objs
        if not fs and not self.singlefile:
            for root, dirnames, filenames in os.walk(self.path):
                for filename in filenames:
                    if not filename.endswith(('conll', 'conllu', 'txt')):
                        continue
                    subc = os.path.basename(root)
                    subc = False if subc == self.name else subc
                    fs.append(File(os.path.join(root, filename), corpus_name=self.name, in_subcorpus=subc))

        self.list = list()
        self.extend(fs)

        if not os.path.exists(self.path):
            raise FileNotFoundError("Corpus not found at %s" % self.path)

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        import re
        # get from subcorpora, unless there are none, in which case, get from files
        #to_iter = self.subcorpora if os.path.isdir(self.path) and len(self.subcorpora) else self.list
        to_iter = self.list
        if isinstance(i, str):
            # dict style lookup of files when there are no subcorpora
            return next((s for s in to_iter if s.name.split('.', 1)[0] == i), None)
        # allow user to pass in a regular expression and get all matching names
        elif isinstance(i, re._pattern_type):
            return Corpus([s for s in to_iter if re.search(i, s.name.split('.', 1)[0])], path=self.path, sliced=True)
        # normal indexing and slicing
        elif isinstance(i, slice):
            return Corpus(to_iter[i], path=self.path, sliced=True)
        else:
            return to_iter[i]

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        self.list[i] = v

    def insert(self, i, v):
        self.list.insert(i, v)

    def __str__(self):
        return str(self.list)

    def __getattr__(self, name):
        name = name.split('.', 1)[0]
        return self.__getitem__(name)

    @lazy_property
    def files(self):
        """
        A list of File objects within the corpus
        """
        return [i for i in self.list]

    @lazy_property
    def filepaths(self):
        """
        A list of filepaths within the corpus
        """
        return [i.path for i in self.list]

    def store_as_hdf(self, **kwargs):
        """
        Store a corpus in an HDF5 file for faster loading
        """
        from corpkit.process import store_as_hdf
        return store_as_hdf(self, **kwargs)

    @lazy_property
    def subcorpora(self):
        """
        A list of immediate subcorpora, also modelled as Corpus objects.
        """
        subs = [Corpus(os.path.join(self.path, x))
                for x in os.listdir(self.path)
                if os.path.isdir(os.path.join(self.path, x))]
        return subs

    def load(self, multiprocess=False, load_trees=True, **kwargs):
        """
        Load corpus into memory (i.e. create one large `pd.DataFrame`)

        Keyword args:
            multiprocess (int): how many threads to use
            load_trees (bool): Parse constituency trees if present
            add_gov (bool): pre-load each token's governor
            cols (list): list of columns to be loaded (can improve performance)
            just (dict): restrict load to lines with feature key matching
                regex value (case insensitive)
            skip (dict): the inverse of `just`

        Returns:
            :class:`corpkit.corpus.LoadedCorpus`
        """
        from corpkit.other import _load
        return _load(self, multiprocess=multiprocess, load_trees=load_trees,
                      path=self.path, name=self.name, **kwargs)

    def search(self, target, query, **kwargs):
        """
        Search a corpus for some linguistic or metadata feature

        Args:
            target (str): The name of the column or feature to search

               - `'w'`: words
               - `'l'`: lemmas
               - `'x'`: XPOS
               - `'p'`: POS
               - `'f'`: dependency function
               - `'year'`, `speaker`, etc: arbitrary metadata categories
               - `'t'`: Constitutency trees via TGrep2 syntax
               - `'d'`: Dependency graphs via depgrep

            query (str/list): regular expression, Tgrep2/depgrep string to match, or
                list of strings to match against

        Keyword Args:
            inverse (bool): get non-matches 
            multiprocess (int): number of parallel threads to start
            no_store (bool): do not store reference corpus in Results object
            just_index (bool): return only pointers to matches, not actual data
            cols (list): list of columns to be loaded (can improve performance)
            just (dict): restrict load to lines with feature key matching
                regex value (case insensitive)
            skip (dict): the inverse of `just`

        Returns:
            :class:`corpkit.interrogation.Results`: search result
        """
        from corpkit.interrogator import interrogator
        return interrogator(self, target, query, **kwargs)

    def trees(self, query, **kwargs):
        """Equivalent to `.search('t', query)`"""
        return self.search('t', query, **kwargs)

    def deps(self, query, **kwargs):
        """Equivalent to `.search('d', query)`"""
        return self.search('d', query, **kwargs)

    def cql(self, query, **kwargs):
        """Equivalent to `.search('c', query)`"""
        return self.search('c', query, **kwargs)

    def words(self, query, **kwargs):
        """Equivalent to `.search('w', query)`"""
        return self.search('w', query, **kwargs)

    def lemmas(self, query, **kwargs):
        """Equivalent to `.search('l', query)`"""
        return self.search('l', query, **kwargs)

    def pos(self, query, **kwargs):
        """Equivalent to `.search('p', query)`"""
        return self.search('p', query, **kwargs)

    def pos(self, query, **kwargs):
        """Equivalent to `.search('x', query)`"""
        return self.search('p', query, **kwargs)

    def functions(self, query, **kwargs):
        """Equivalent to `.search('f', query)`"""
        return self.search('f', query, **kwargs)

    def parse(self, parser='corenlp', lang='english',
              multiprocess=False, **kwargs):
        """
        Parse a plaintext corpus

        Keyword Args:
            parser (str): name of the parser (only 'corenlp' accepted so far)
            lang (str): language for parser (`english`, `arabic`, `chinese`, 
                        `german`, `french` or `spanish`)
            multiprocess (int): number of parallel threads to start
            memory_mb (int): megabytes of memory to use per thread (default 2024)

        Returns:
            :class:`corpkit.corpus.Corpus`: parsed corpus

        """
        if self.name.endswith('-parsed'):
            raise ValueError("Corpus is already parsed.")
        from corpkit.parse import Parser
        parser = Parser(parser=parser, lang=lang)
        return parser.run(self, multiprocess=multiprocess, **kwargs)

    # for backward compatibility only
    def interrogate(self, search, **kwargs):
        target, query = search.popitem()
        return self.search(target=target, query=query, **kwargs)

    def __str__(self):
        from corpkit.process import make_tree
        return str(self.files)

    def __repr__(self):
        # not always nice, should use abspath sometimes ...
        relat = os.path.relpath(self.path).split('/')[1:]
        usr = next((i for i, x in enumerate(relat) if x.lower() == 'users'), 0)
        path = ' -> '.join(relat[usr:])
        return '<%s: %s --- %ss/%sf>' % (self.__class__.__name__, 
            path, format(len(self.subcorpora), ','), format(len(self), ','))

    def fsi(self, ix):
        """
        Get a slice of a corpus as a DataFrame

        Args:
            ix (iterable): if len(ix) == 1, filename to get
                           if len(ix) == 2, get sent from filename
                           if len(ix) == 3, get token from sent from filename

        Return:
            pd.DataFrame
        """
        if not isinstance(ix, (list, tuple)):
            ix = [ix]
        # allow the user to pass in somthing nested
        if isinstance(ix[0], (list, tuple)):
            import pandas as pd
            dfs = [self.fsi(i) for i in ix]
            return pd.concat(dfs)
        ix = list(ix)
        if isinstance(ix[0], int):
            ix[0] = self.files[ix[0]].name.split('.', 1)[0]
        if len(ix) == 1:
            f, s, i = ix[0], None, None
        elif len(ix) == 2:
            f, s, i = ix[0], ix[1], None
        elif len(ix) == 3:
            f, s, i = ix[0], ix[1], ix[2]
        else:
            raise NotImplementedError
        # if the user deliberately gave no filename, we have to load all
        if f is None:
            df = self.load()
        else:
            fobj = next((s for s in self.files if s.name.split('.', 1)[0] == f), None)
            if not fobj:
                return ValueError("File not found.")
            df = fobj.document
        if s is None and i is None:
            return df
        elif s is None and i is not None:
            df = df.xs(i, level=['i'], drop_level=False)
        elif i is not None:
            df = df.xs((s, i), level=['s', 'i'], drop_level=False)
        else:
            df = df.xs([s], level=['s'], drop_level=False)
        return df

    def features(self, subcorpora=False):
        """
        Generate and show basic stats from the corpus, including number of 
        sentences, clauses, process types, etc.
        
        Example:

        >>> corpus.features
            SB  Characters  Tokens  Words  Closed class words  Open class words
            01       26873    8513   7308                4809              3704
            02       25844    7933   6920                4313              3620
            03       18376    5683   4877                3067              2616
            04       20066    6354   5366                3587              2767
        """
        if 'features' in self.metadata:
            import pandas as pd
            feat = pd.read_json(self.metadata['features'])
            #feat = feat.set_index(['file', 's'])
            #todo: make into interrogation object?
            if subcorpora:
                return feat.pivot_table(index=subcorpora, aggfunc=sum)
            else:
                return feat
        from corpkit.interrogator import interrogator
        from corpkit.process import add_df_to_dotfile
        feat = interrogator(self, 'features')
        if not self._sliced:
            add_df_to_dotfile(self.path, feat, typ='features', subcorpora=False)
        else:
            print("Corpus is a slice, and thus will not be added to metadata")
        if subcorpora:
            return feat.table(subcorpora=subcorpora)
        else:
            return feat

    @lazy_property
    def wordclasses(self):
        """
        Generate and show basic stats from the corpus, including number of 
        sentences, clauses, process types, etc.
        
        Example:

        >>> corpus.wordclasses
            SB   Verb  Noun  Preposition   Determiner ...
            01  26873  8513         7308         5508 ...
            02  25844  7933         6920         3323 ...
            03  18376  5683         4877         3137 ...
            04  20066  6354         5366         4336 ...
        """
        from corpkit.features import _get_postags_and_wordclasses
        postags, wordclasses = _get_postags_and_wordclasses(self)
        return wordclasses

    @lazy_property
    def postags(self):
        """
        Generate and show basic stats from the corpus, including number of 
        sentences, clauses, process types, etc.
        
        Example:

        >>> corpus.postags
            SB      NN     VB     JJ     IN     DT 
            01   26873   8513   7308   4809   3704  ...
            02   25844   7933   6920   4313   3620  ...
            03   18376   5683   4877   3067   2616  ...
            04   20066   6354   5366   3587   2767  ...
        """
        from corpkit.features import _get_postags_and_wordclasses
        postags, wordclasses = _get_postags_and_wordclasses(self)
        return postags

    @lazy_property
    def lexicon(self, **kwargs):

        """
        Get a lexicon/frequency distribution from a corpus. Store it in metadata.
        
        Returns:
            a `DataFrame` of tokens and counts
        """
        from corpkit.features import lexicon
        return lexicon(self)

    def sample(self, n, level='f'):
        """
        Get a sample of the corpus

        :param n: amount of data in the the sample. If an ``int``, get n files.
                  if a ``float``, get float * 100 as a percentage of the corpus
        :type n: ``int``/``float``
        :param level: sample subcorpora (``s``) or files (``f``)
        :type level: ``str``
        Returns:
            a Corpus object
        """
        import random
        if level.startswith('f'):
            return Corpus(random.sample(list(self), n), self.path)
        else:
            return Corpus(random.sample(list(self.subcorpora), n), self.path)

    def delete_metadata(self):
        """
        Delete metadata for corpus. May be needed if corpus is changed
        """
        import os
        os.remove(os.path.join('data', '.%s.json' % self.name))

    @lazy_property
    def metadata(self):
        """
        Get metadata for a corpus
        """
        if isinstance(self, File):
            self = self.mainpath
        #if not self.name.endswith('-parsed'):
        #    return {}
        from corpkit.process import get_corpus_metadata
        absp = os.path.abspath(self.path)
        return get_corpus_metadata(absp, generate=True)

    def tokenise(self, postag=True, lemmatise=True, *args, **kwargs):
        """
        Tokenise a plaintext corpus, saving to disk

        Returns:
            The newly created :class:`corpkit.corpus.Corpus`
        """

        from corpkit.make import make_corpus
        #from corpkit.process import determine_datatype
        #dtype, singlefile = determine_datatype(self.path)
        if self.datatype != 'plaintext':
            raise ValueError(
                'parse method can only be used on plaintext corpora.')
        kwargs.pop('parse', None)
        kwargs.pop('tokenise', None)

        c = make_corpus(self.path,
                        parse=False,
                        tokenise=True,
                        postag=postag,
                        lemmatise=lemmatise,
                        *args,
                        **kwargs)
        return Corpus(c)

    def annotate(self, interro, annotation, dry_run=True):
        """
        Annotate a corpus

        Args:
            interro (:class:`corpkit.Interrogation`): Search matches
            annotation (str/dict): a tag or field: value dict. If a dict, the key
                is the name of the annotation field, and the value is, well, the
                value. If the value string matches one of the column names seen
                when concordancing, the content of that string will be used. If
                the value is a list, the middle column will be formatted, as per
                the `show` arguments for Interrogation.table() and
                Interrogation.conc().
            dry_run (bool): Show the annotations to be made, but don't do them

        """
        conc = self.concordance
        from corpkit.annotate import annotator
        annotator(conc, annotation, dry_run=dry_run)
        # regenerate metadata afterward---could be a bit slow?
        if not dry_run:
            self.delete_metadata()
            from corpkit.process import make_dotfile
            make_dotfile(self)

    def unannotate(annotation, dry_run=True):
        """
        Delete annotation from a corpus

        Args:
            annotation (str/dict): just as in `corpus.annotate()`.
            dry_run (bool): Show the changes to be made, but don't do them
        """
        from corpkit.annotate import annotator
        annotator(self, annotation, dry_run=dry_run, deletemode=True)

class File(Corpus):
    """
    Models a corpus file for reading, interrogating, concordancing.

    Methods for interrogating, concordancing and configurations are the same as
    :class:`corpkit.corpus.Corpus`, plus methods for accessing the file contents 
    directly as a `str`, or as a Pandas DataFrame.
    """

    def __init__(self, path, **kwargs):
        super(File, self).__init__(path)
        self.corpus_name = kwargs.get('corpus_name')
        self._subcorpus = kwargs.get('in_subcorpus', False)

    def __repr__(self):
        return "<%s instance: %s>" % (classname(self), self.name)

    def __str__(self):
        return self.path

    def __bool__(self):
        return True
 
    def read(self, **kwargs):
        """
        Get contents of file as string
        """
        from corpkit.constants import OPENER
        with OPENER(self.path, 'r', **kwargs) as fo:
            return fo.read()

    @lazy_property
    def document(self):
        """
        `pd.DataFrame` containing tokens and their attributes and metadata
        """
        if self.datatype == 'conll':
            from corpkit.conll import path_to_df
            return path_to_df(self.path, corpus_name=self.corpus_name)
        else:
            from corpkit.process import saferead
            return saferead(self.path)[0]
    
    @lazy_property
    def trees(self):
        """
        Get list of parse trees in a File
        """
        from nltk.tree import ParentedTree
        dat = self.read()
        dat = [i.split('=')[1].strip() for i in dat if i.startswith(('# parse =', '# parse='))]
        return [ParentedTree.fromstring(t) for t in dat]

    @lazy_property
    def plain(self):
        """
        Show the sentences in a File as plaintext
        """
        dat = self.read()
        dat = [i.split('=')[1].strip() for i in dat if i.startswith(('# text =', '# text='))]
        if not dat:
            return
        else:
            return dat

class LoadedCorpus(Results):
    """
    Store a corpus in memory as a DataFrame.

    This class has all the same methods as a Results object. The only real
    difference is that slicing it will do some reindexing to speed up searches.
    """

    @property
    def _constructor(self):
        import pandas as pd
        pd.options.mode.chained_assignment = None
        #self.loc[:,'_n'] = list(range(len(self)))
        return LoadedCorpus

    def __init__(self, data, path=False):
        super(LoadedCorpus, self).__init__(data, path=path)
