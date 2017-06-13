
import os

class Parser(object):
    """
    Create an object that can parse a Corpus.
    """

    def __init__(self, parser='corenlp', lang='english'):
        import os
        from corpkit.corpus import Corpus
        self.parser = parser
        self.lang = lang
        self.datapath = '.'
        #self.original_dir = os.getcwd()
        super(Parser, self).__init__()

    def unimplemented(self):
        """
        For things not yet done
        """
        raise NotImplementedError

    def prepare_parser(self):
        """
        Calls the correct preparation method
        """
        prepares = {'corenlp': self.corenlp_prepare, 'features': self.feature_prepare}
        return prepares.get(self.parser, self.corenlp_prepare)()
        #return prepares.get(self.parser, self.unimplemented)()

    def parse(self):
        """
        Calls the correct parser method
        """
        parse_funcs = {'corenlp': self.corenlp_parse, 'features': self.feature_parse}
        parse_funcs.get(self.parser, self.unimplemented)()

    def corenlp_prepare(self):
        """
        If working with CoreNLP, make sure we have it and the lang data
        """
        from corpkit.constants import (INPUTFUNC, CORENLP_VERSION, 
                                       CORENLP_URL, CORENLP_MODEL_URLS, CORENLP_PATH)
        # i.e. ~/corenlp
        self.corenlp_path = CORENLP_PATH
        # i.e stanford-corenlp-date.zip
        self.corenlp_fname = os.path.basename(CORENLP_URL)
        # i.e. ~/corenlp/stanford-corenlp-date.zip
        self.corenlp_fpath = os.path.join(self.corenlp_path, self.corenlp_fname)
        self.corenlp_subpath = os.path.splitext(self.corenlp_fpath)[0]

        # problem one: no directory
        if not os.path.isdir(self.corenlp_path):
            os.makedirs(self.corenlp_path)
            print("CoreNLP not found. Auto-installing CoreNLP v%s..." % CORENLP_VERSION)
        
        # problem two: no zip file and no dir (user may have deleted zip, but that's ok)
        if not os.path.isdir(self.corenlp_subpath) and not os.path.isfile(self.corenlp_fpath):
            from corpkit.build import download_from_url
            while True:
                if self.kwargs.get('notify', False):
                    import rumps
                    rumps.notification("Downloading and installing CoreNLP", "", "", data=self.kwargs['NSDictionary'],
                                        img=self.kwargs['iconpath'], sound=False)
                try:
                    download_from_url(CORENLP_URL, self.corenlp_fpath)
                    break
                except (KeyboardInterrupt, SystemExit):
                    import shutil
                    if os.path.exists(self.corenlp_path):
                        os.remove(self.corenlp_path)
                except:
                    import shutil
                    if os.path.exists(self.corenlp_path):
                        os.remove(self.corenlp_path)
                    stop = INPUTFUNC("Download failed. Retry? (y/n)")
                    if stop.lower().startswith('n'):
                        break

        # problem three: dir is not yet there (i.e. zip unextracted)
        if not os.path.isdir(self.corenlp_subpath):
            from corpkit.build import extract_cnlp
            success = extract_cnlp(self.corenlp_fpath)

        # problem four: extraction failed
        if not os.path.isdir(self.corenlp_subpath):
            raise ValueError("%s should exist." % self.corenlp_subpath)

        # problem five: no language-specific model
        url = CORENLP_MODEL_URLS.get(self.lang, False)
        if self.lang != 'english':
            if not url:
                self.unimplemented()
            if not os.path.basename(url) in os.listdir(self.corenlp_path):
                from corpkit.build import download_from_url, extract_cnlp
                fpath = os.path.join(self.corenlp_path, os.path.basename(url))
                download_from_url(url, fpath)
        
        success = [self.corenlp_path]

        if self.lang != 'english':
            success.append(self.corenlp_fname in os.listdir(self.corenlp_path))
        
        return all(success)

    def feature_prepare(self):
        #print("Initialising features")
        from grammar import Grammar
        g = Grammar(load=self.load_features)
        #print('grammar loaded')
        if g._model is False:
            g.model(path=self.training_data)
        self.feature_grammar = g
        return True

    def corenlp_filter_done_files(self, fs):
        """
        If restarting a parse job, remove files that are already done
        """
        parsed = set([os.path.splitext(i)[0] for i in os.listdir(self.parsed_path)
                      if i.endswith('.conll')])
        return [f for f in fs if os.path.basename(f) not in parsed]

    def corenlp_make_filelists(self):
        from corpkit.constants import OPENER, PYTHON_VERSION
        to_parse = self.stripped_corpus if self.stripped_corpus else self.plain_corpus
        fs = to_parse.filepaths
        abspath = os.path.abspath(os.getcwd())
        fs = [os.path.join(abspath, f) for f in fs]
        if self.restart:
            oldnum = len(fs)
            fs = self.corenlp_filter_done_files(fs)
            newnum = len(fs)
            print("Already done: %d/%d files." % (oldnum-newnum, oldnum))
            # this means all files are parsed
            if oldnum-newnum == oldnum:
                return
            # perhaps all files were moved to their dirs already
            # in this case, we check that it has no files in the
            # base dir, but at least one in a subdir
            if oldnum-newnum == 0:
                from corpkit.corpus import Corpus
                test = Corpus(self.parsed_path)
                if len(test.filepaths):
                    print("Files already moved into place.")
                    return


        if self.multiprocess:
            from corpkit.process import partition
            chunks = partition(fs, self.multiprocess)
        else:
            chunks = [fs]
        if len(chunks) < self.multiprocess:
            self.multiprocess = len(chunks)
        filelist_paths = []
        for i, chunk in enumerate(chunks, start=1):
            p = (to_parse.name, str(i).zfill(4))
            filelist_path = os.path.join(self.datapath, '%s-filelist-%s.txt' % p)
            with OPENER(filelist_path, 'w', encoding='utf-8') as fo:
                if PYTHON_VERSION == 2:
                    fo.write('\n'.join(chunk).encode('utf-8'))
                else:
                    fo.write('\n'.join(chunk))
            filelist_paths.append(filelist_path)
        return filelist_paths
    
    def corenlp_run_parser(self, filelists):
        # create the operations string
        if isinstance(self.operations, list):
            self.operations = ','.join([i.lower() for i in self.operations])
        elif self.operations is False:
            cof = ',dcoref' if self.coref else ''
            self.operations = 'tokenize,ssplit,pos,lemma,parse,ner' + cof

        kwarg = dict(jarpath=self.corenlp_subpath,
                    memory_mb=self.memory_mb,
                    parsed_path=self.parsed_path,
                    lang=self.lang,
                    operations=self.operations,
                    copula_head=self.copula_head)

        # todo: use notifier!
        if self.kwargs.get('notify', False):
            import rumps
            rumps.notification("Parsing corpus...", "", "", data=self.kwargs['NSDictionary'],
                                img=self.kwargs['iconpath'], sound=False)

        if len(filelists) == 1:
            corenlp_parse_filelist(filelists[0], **kwarg)
        elif self.multiprocess:
            from joblib import Parallel, delayed
            dfs = Parallel(n_jobs=self.multiprocess)(delayed(corenlp_parse_filelist)(filelist=f, thread=i, **kwarg) for i, f in enumerate(filelists, start=1))

    def corenlp_move_parsed_files(self):
        """
        Make parsed files follow existing corpus structure
        """
        import shutil
        import fnmatch
        dir_list = []
        # go through old path, make file list
        #os.chdir(self.original_dir)
        
        # make list of parsed filenames that haven't been moved already
        parsed_fs = [f for f in os.listdir(self.parsed_path) if f.endswith('.conll')]

        # make a dictionary of the right paths
        pathdict = {}
        for rootd, dirnames, filenames in os.walk(self.plain_corpus.path):
            for filename in fnmatch.filter(filenames, '*.txt'):
                pathdict[filename] = rootd

        # move each file
        for f in parsed_fs:
            noext = f.replace('.conll', '')
            right_dir = pathdict[noext].replace(self.plain_corpus.path,
                                                self.parsed_path)
            frm = os.path.join(self.parsed_path, f)
            tom = os.path.join(right_dir, f)
            # forgive errors on restart mode, because some files 
            # might already have been moved into place
            try:
                os.renames(frm, tom)
            except OSError:
                pass

    def feature_parse(self):
        """
        Do feature annotation with optional metadata. Nice!
        """
        import fnmatch
        from corpkit.conll import get_metadata, load_raw_data
        met_mode = self.stripped_corpus is not None
        to_parse = self.stripped_corpus if met_mode else self.plain_corpus
        # make a dictionary of the right paths
        pathdict = {}
        for rootd, dirnames, filenames in os.walk(self.plain_corpus.path):
            for filename in fnmatch.filter(filenames, '*.txt'):
                pathdict[filename] = rootd

        for f in to_parse.files:
            
            data = f.read()
            if met_mode or speaker_segmentation:
                with open(f.path.replace('-stripped', '', 1), 'r') as fo:
                    raw = fo.read()
                stripped = data
            else:
                raw = data
                stripped = None

            df = self.feature_grammar.process(data)
            df.index.names = ['s', 'i']
            #df = df.reset_index()
            outstring = []

            for ix, sent in df.groupby(level='s'):
                offsets = (sent['start'].values[0], sent['end'].values[0])
                metad = get_metadata(stripped,
                                     raw,
                                     offsets,
                                     metadata_mode=self.metadata,
                                     speaker_segmentation=self.speaker_segmentation)
                #text = stripped[start:end] if self.stripped_corpus else raw[start:end]

                output = '# sent_id = %d\n# sent_len = %d\n# parser = features\n' % (ix, len(sent))
                for k, v in sorted(metad.items()):
                    output += '# %s = %s\n' % (k, v)
                dat = sent.drop(['start', 'end'], axis=1).replace('_', '0').replace('', '_')
                dat.index = dat.index.droplevel('s')
                output += dat.to_csv(sep='\t', header=None).rstrip()
                outstring.append(output)
        outstring = '\n\n'.join(outstring)

        newpath = f.path.replace(self.plain_corpus.path,
                                 self.parsed_path) + '.conll'
        newpath = newpath.replace('-stripped', '', 1)
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        with open(newpath, 'w') as fo:
            fo.write(outstring)

    def corenlp_parse(self):
        from corpkit.conll import convert_json_to_conll
        filelist_paths = self.corenlp_make_filelists()
        if filelist_paths is not None:
            self.corenlp_run_parser(filelist_paths)
        self.corenlp_move_parsed_files()
        if filelist_paths is not None:
            for f in filelist_paths:
                os.remove(f)
        convert_json_to_conll(self.parsed_path,
                              speaker_segmentation=self.speaker_segmentation,
                              plain_path=self.plain_corpus.path,
                              coref=self.coref, metadata=self.metadata)
        if self.kwargs.get('notify', False):
            import rumps
            rumps.notification("Corpus ready to search!", "", "", data=self.kwargs['NSDictionary'],
                                img=self.kwargs['iconpath'], sound=False)

    def make_stripped(self):
        """
        Make a stripped version of the plain corpus
        """
        import re
        import shutil
        from corpkit.process import saferead
        from corpkit.corpus import Corpus
        from corpkit.constants import OPENER, MAX_SPEAKERNAME_SIZE, PYTHON_VERSION

        stripped_path = self.plain_corpus.path + '-stripped'

        # define regex broadly enough to accept timestamps, locations if need be
        idregex = re.compile(r'(^.{,%d}?):\s+(.*$)' % MAX_SPEAKERNAME_SIZE)

        # duplicate plain corpus
        if os.path.isdir(stripped_path) and self.restart:
            pass
        else:
            try:
                shutil.copytree(self.plain_corpus.path, stripped_path)
            except OSError:
                shutil.rmtree(stripped_path)
                shutil.copytree(self.plain_corpus.path, stripped_path)

        all_files = Corpus(stripped_path).filepaths

        for f in all_files:
            good_data = []
            fo, enc = saferead(f)
            data = fo.splitlines()
            # for each line in the file, remove speaker and metadata
            for datum in data:
                if self.speaker_segmentation:
                    matched = re.search(idregex, datum)
                    if matched:
                        datum = matched.group(2)
                if self.metadata:
                    splitmet = datum.rsplit('<metadata ', 1)
                    # for the impossibly rare case of a line that is '<metadata '
                    if not splitmet:
                        continue
                    datum = splitmet[0]
                if datum:
                    good_data.append(datum)

            with OPENER(f, "w") as fo:
                if PYTHON_VERSION == 2:
                    fo.write('\n'.join(good_data).encode('utf-8'))
                else:
                    fo.write('\n'.join(good_data))
        return stripped_path

    def run(self, corpus, multiprocess=False, speaker_segmentation=False,
            metadata=False, coref=False, memory_mb=2024, restart=False, **kwargs):
        """
        Run the whole parsing pipeline, including download of CoreNLP if necessary

        Args:
           corpus (Corpus): plain data to process
           multiprocess (int/bool): how many processes to use for parser

        Return:
            Corpus: parsed corpus
        """
        import os
        import shutil
        from corpkit.corpus import Corpus
        self.plain_corpus = corpus
        self.multiprocess = multiprocess
        self.speaker_segmentation = speaker_segmentation
        self.metadata = metadata
        self.coref = coref
        self.operations = kwargs.get('operations', False)
        self.memory_mb = str(memory_mb)
        self.copula_head = kwargs.get('copula_head', True)
        self.stripped_corpus = None
        self.corpus_name = corpus.name
        self.load_features = kwargs.get('load', True)
        self.training_data = kwargs.get('training_data', 'en-ud-train.conllu')
        # todo: fix this, it's terrible
        if self.training_data == 'en-ud-train.conllu' and not os.path.isfile('en-ud-train.conllu'):
            storedpath = os.path.expanduser('~/corpora/UD_English-parsed/en-ud-train.conllu')
            if os.path.isfile(storedpath):
                self.training_data = storedpath
            else:
                os.system('curl -O https://raw.githubusercontent.com/UniversalDependencies/UD_English/master/en-ud-train.conllu')
        # name for final corpus folder
        self.parsed_name = kwargs.pop('outname', corpus.name.replace('-stripped', '') + '-parsed')
        # dir to put parsed corpus in
        self.datapath = kwargs.pop('outpath', self.datapath)
        self.kwargs = kwargs
        # full path to final parsed corpus
        self.parsed_path = os.path.join(self.datapath, self.parsed_name)
        self.restart = restart

        if not self.restart:
            if not os.path.isdir(self.datapath):
                os.makedirs(self.datapath)
            shutil.copytree(self.plain_corpus.path, self.parsed_path,
                            ignore=shutil.ignore_patterns('*.*'))
        
        if speaker_segmentation or metadata:
            self.stripped_corpus = Corpus(self.make_stripped())

        prepared = self.prepare_parser()
        if not prepared:
            print("Error in preparation...")
        self.parse()
        return Corpus(self.parsed_path)


def corenlp_parse_filelist(filelist, jarpath, memory_mb, parsed_path,
    lang, operations, copula_head, thread=False):
    """
    The method in which java is actually called upon a filelist

    It unfortunately isn't a method because it can cause a multiprocess pickle error
    """
    import os
    import subprocess
    import sys
    import re
    from corpkit.constants import CORENLP_VERSION
    import time
    from tqdm import tqdm, tqdm_notebook
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            tqdm = tqdm_notebook
    except:
        pass

    # get set of filenames and number to parse
    with open(filelist, 'r') as fo:
        flist = set(fo.read().strip('\n').splitlines())
        num_to_parse = len(flist)
        if thread is False:
            flist = None
        else:
            flist = set(os.path.basename(f) + '.conll' for f in flist)
            #if thread is not False:
            

    jars = '%s' % os.path.join(jarpath, '*')

    arglist = ['java', '-cp', jars, 
               '-Xmx%sm' % memory_mb,
               'edu.stanford.nlp.pipeline.StanfordCoreNLP', 
               '-filelist', os.path.abspath(filelist),
               '-noClobber',
               '-outputExtension', '.conll',
               '-outputFormat', 'json',
               '-outputDirectory', os.path.abspath(parsed_path)]
    
    # todo: do not change dirs, this is terrible
    cwd = os.getcwd()
    #os.chdir(jarpath)

    if lang != 'english':
        import corpkit
        arglist += ['-props', os.path.join(os.path.dirname(corpkit.__file__),
                    'langprops', '%s.properties' % lang)]
    else:
        if copula_head:
            arglist += ['--parse.flags', ' -makeCopulaHead']
        arglist += ['-annotators', operations]

    if thread is False or thread == 1:
        print("Parsing with command: ", ' '.join(arglist) + '\n')

    kwa = dict(ncols=120,
               unit="file",
               desc="Parsing",
               total=num_to_parse)

    if thread is not False:
        kwa['position'] = -thread + 1

    if num_to_parse > 1:
        t = tqdm(**kwa)

    logname = parsed_path.replace('-parsed', '') + '.log'
    logfile = open(logname, "w")

    proc = subprocess.Popen(arglist, stdout=logfile, stderr=logfile)

    previous = 0
    #proc.kill()  
    pp = os.path.abspath(parsed_path)
    while proc.poll() is None:
        time.sleep(1)
        # all parsed filenames
        now_done = set(i for i in os.listdir(pp) if i.endswith('.conll'))
        if thread is False:
            now_done = len(now_done)
        else:
            # number of files in filelist and parsed
            now_done = len(now_done.intersection(flist))
        to_update = now_done - previous
        if to_update > 0 and num_to_parse > 1:
            t.update(to_update)
        previous = now_done

    if num_to_parse > 1:
        t.close()
        
    #os.chdir(cwd) 