from __future__ import print_function
from corpkit.constants import STRINGTYPE, PYTHON_VERSION, INPUTFUNC

"""
This file contains a number of functions used in the corpus building process.
None of them is intended to be called by the user him/herself. A couple are deprecated, too.
"""

def download_large_file(proj_path, url, actually_download=True, root=False, **kwargs):
    """
    Download something to proj_path, unless it's CoreNLP, which goes to ~/corenlp
    """
    import os
    import shutil
    import glob
    import zipfile
    from time import localtime, strftime
    from corpkit.process import animator

    file_name = url.split('/')[-1]
    home = os.path.expanduser("~")
    customdir = kwargs.get('custom_corenlp_dir', False)
    # if it's corenlp, put it in home/corenlp
    # if that dir exists, check if for a zip file
    # if there's a zipfile and it works, move on
    # if there's a zipfile and it's broken, delete it
    if 'stanford' in url and not kwargs.get('model'):
        if customdir:
            downloaded_dir = customdir
        else:
            downloaded_dir = os.path.join(home, 'corenlp')
        if not os.path.isdir(downloaded_dir):
            os.makedirs(downloaded_dir)
        else:
            poss_zips = glob.glob(os.path.join(downloaded_dir, 'stanford-corenlp-full*.zip'))
            if poss_zips:
                fullfile = poss_zips[-1]
                from zipfile import BadZipfile
                try:
                    the_zip_file = zipfile.ZipFile(fullfile)                    
                    ret = the_zip_file.testzip()
                    if ret is None:
                        return downloaded_dir, fullfile
                    else:
                        os.remove(fullfile)
                except BadZipfile:
                    os.remove(fullfile)
            #else:
            #    shutil.rmtree(downloaded_dir)
    else:
        if not kwargs.get('model'):
            downloaded_dir = os.path.join(proj_path, 'temp')
        else:
            downloaded_dir = proj_path
        try:
            os.makedirs(downloaded_dir)
        except OSError:
            pass
    fullfile = os.path.join(downloaded_dir, file_name)

    if actually_download:
        import __main__ as main
        if not root and not hasattr(main, '__file__'):
            if not kwargs.get('model'):
                txt = 'CoreNLP not found. Download latest version (%s)? (y/n) ' % url
            else:
                txt = 'Language model not found. Download latest version (%s)? (y/n) ' % url
            
            selection = INPUTFUNC(txt)

            if 'n' in selection.lower():
                return None, None
        try:
            import requests
            # NOTE the stream=True parameter
            r = requests.get(url, stream=True, verify=False)
            file_size = int(r.headers['content-length'])
            file_size_dl = 0
            block_sz = 8192
            showlength = file_size / block_sz
            thetime = strftime("%H:%M:%S", localtime())
            print('\n%s: Downloading ... \n' % thetime)
            par_args = {'printstatus': kwargs.get('printstatus', True),
                        'length': showlength}
            if not root:
                tstr = '%d/%d' % (file_size_dl + 1 / block_sz, showlength)
                p = animator(None, None, init=True, tot_string=tstr, **par_args)
                animator(p, file_size_dl + 1, tstr)

            with open(fullfile, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_sz): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        file_size_dl += len(chunk)
                        #print file_size_dl * 100.0 / file_size
                        if kwargs.get('note'):
                            kwargs['note'].progvar.set(file_size_dl * 100.0 / int(file_size))
                        else:
                            tstr = '%d/%d' % (file_size_dl / block_sz, showlength)
                            animator(p, file_size_dl / block_sz, tstr, **par_args)
                        if root:
                            root.update()
        except Exception as err:
            import traceback
            print(traceback.format_exc())
            thetime = strftime("%H:%M:%S", localtime())
            print('%s: Download failed' % thetime)
            try:
                f.close()
            except:
                pass
            if root:
                root.update()
            return None, None

        if kwargs.get('note'):  
            kwargs['note'].progvar.set(100)
        else:    
            p.animate(int(file_size))
        thetime = strftime("%H:%M:%S", localtime())
        print('\n%s: Downloaded successully.' % thetime)
        try:
            f.close()
        except:
            pass
    return downloaded_dir, fullfile

def extract_cnlp(fullfilepath):
    """
    Extract corenlp zip file
    """
    import zipfile
    import os
    import shutil
    from corpkit.constants import CORENLP_PATH
    from corpkit.process import timestring
    timestring('Extracting CoreNLP files ...')
    from zipfile import BadZipfile
    try:
        with zipfile.ZipFile(fullfilepath) as zf:
            zf.extractall(CORENLP_PATH)
    except BadZipfile:
        shutil.rmtree(CORENLP_PATH)
        return False
    timestring('CoreNLP extracted.')
    return True

def check_jdk():
    """
    Check for a Java/OpenJDK
    """
    import corpkit
    import subprocess
    from subprocess import PIPE, STDOUT, Popen
    # add any other version string to here
    javastrings = ['java version "1.8', 'openjdk version "1.8']
    p = Popen(["java", "-version"], stdout=PIPE, stderr=PIPE)
    _, stderr = p.communicate()
    encoded = stderr.decode(encoding='utf-8').lower()

    return any(j in encoded for j in javastrings)

def corenlp_exists(corenlppath=False):
    import corpkit
    import os
    from corpkit.constants import CORENLP_VERSION
    important_files = ['stanford-corenlp-%s-javadoc.jar' % CORENLP_VERSION,
                       'stanford-corenlp-%s-models.jar' % CORENLP_VERSION,
                       'stanford-corenlp-%s-sources.jar' % CORENLP_VERSION,
                       'stanford-corenlp-%s.jar' % CORENLP_VERSION]
    if corenlppath is False:
        home = os.path.expanduser("~")
        corenlppath = os.path.join(home, 'corenlp')
    if os.path.isdir(corenlppath):
        find_install = [d for d in os.listdir(corenlppath) \
                   if os.path.isdir(os.path.join(corenlppath, d)) \
                   and os.path.isfile(os.path.join(corenlppath, d, 'jollyday.jar'))]

        if len(find_install) > 0:
            find_install = find_install[0]
        else:
            return False
        javalib = os.path.join(corenlppath, find_install)
        if len(javalib) == 0:
            return False
        if not any([f.endswith('-models.jar') for f in os.listdir(javalib)]):
            return False
        return True
    else:
        return False
    return True

def get_filepaths(a_path, ext='txt'):
    """
    Make list of txt files in a_path and remove non txt files
    """
    import os
    files = []
    if os.path.isfile(a_path):
        return [a_path]
    for (root, dirs, fs) in os.walk(a_path):
        for f in fs:
            if ext:
                if not f.endswith('.' + ext):
                    continue
            if 'Unidentified' not in f \
            and 'unknown' not in f \
            and not f.startswith('.'):
                files.append(os.path.join(root, f))
            #if ext:
            #    if not f.endswith('.' + ext):
            #        os.remove(os.path.join(root, f))
    return files

def get_all_metadata_fields(corpus, include_speakers=False):
    """
    Get a list of metadata fields in a corpus

    This could take a while for very little infor
    """
    from corpkit.corpus import Corpus
    from corpkit.constants import OPENER, PYTHON_VERSION, MAX_METADATA_FIELDS

    # allow corpus object
    if not isinstance(corpus, Corpus):
        corpus = Corpus(corpus, print_info=False)
    if not corpus.datatype == 'conll':
        return []

    path = getattr(corpus, 'path', corpus)

    fs = []
    import os
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fs.append(os.path.join(root, filename))

    badfields = ['parse', 'sent_id']
    if not include_speakers:
        badfields.append('speaker')

    fields = set()
    for f in fs:
        if PYTHON_VERSION == 2:
            from corpkit.process import saferead
            lines = saferead(f)[0].splitlines()
        else:
            with OPENER(f, 'rb') as fo:
                lines = fo.read().decode('utf-8', errors='ignore')
                lines = lines.strip('\n')
                lines = lines.splitlines()

        lines = [l[2:].split('=', 1)[0] for l in lines if l.startswith('# ') \
                 if not l.startswith('# sent_id')]
        for l in lines:
            if l not in fields and l not in badfields:
                fields.add(l)
        if len(fields) > MAX_METADATA_FIELDS:
            break
    return list(fields)

def get_names(filepath, speakid):
    """
    Get a list of speaker names from a file
    """
    import re
    from corpkit.process import saferead
    txt, enc = saferead(filepath)
    res = re.findall(speakid, txt)
    if res:
        return sorted(list(set([i.strip() for i in res])))

def get_meta_values(corpus, feature='speaker'):
    """
    Use regex to get speaker names from parsed data without parsing it
    """
    import os
    import re
    from corpkit.constants import MAX_METADATA_VALUES

    path = corpus.path if hasattr(corpus, 'path') else corpus
    
    list_of_files = []
    names = []

    # i am not really sure why we need multiline here
    # is it because start of line char is just matching
    speakid = re.compile(r'^# %s=(.*)' % re.escape(feature), re.MULTILINE)
    
    # if passed a dir, do it for every file
    if os.path.isdir(path):
        for (root, dirs, fs) in os.walk(path):
            for f in fs:
                list_of_files.append(os.path.join(root, f))
    elif os.path.isfile(path):
        list_of_files.append(path)

    for filepath in list_of_files:
        res = get_names(filepath, speakid)
        if not res:
            continue
        for i in res:
            if i not in names:
                names.append(i)
        if len(names) > MAX_METADATA_VALUES:
            break
    return list(sorted(set(names)))

def flatten_treestring(tree):
    """
    Turn bracketed tree string into something looking like English
    """
    import re
    reps = [(')', '')
            ('$ ', '$')
            ('`` ', '``')
            (' ,', ',')
            (' .', '.')
            ("'' ", "''")
            (" n't", "n't")
            (" 're","'re")
            (" 'm","'m")
            (" 's","'s")
            (" 'd","'d")
            (" 'll","'ll")
            ('  ', ' ')]
    tree = re.sub(r'\(.*? ', '', tree)
    for k, v in reps:
        tree = tree.raplce(k, v)
    return tree

def can_folderise(folder):
    """
    Check if corpus can be put into folders
    """
    import os
    from glob import glob
    if os.path.isfile(folder):
        return False
    fs = glob(os.path.join(folder, '*.txt'))
    if len(fs) > 1:
        if not any(os.path.isdir(x) for x in glob(os.path.join(folder, '*'))):
            return True
    return False

def folderise(folder):
    """
    Move each file into a folder
    """
    import os
    import shutil
    from glob import glob
    from corpkit.process import makesafe
    fs = glob(os.path.join(folder, '*.txt'))
    for f in fs:
        newname = makesafe(os.path.splitext(os.path.basename(f))[0])
        newpath = os.path.join(folder, newname)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        shutil.move(f, os.path.join(newpath))

def download_from_url(url, dst):
    """
    https://gist.github.com/wy193777/0e2a4932e81afc6aa4c8f7a2984f34e2
    """
    import requests
    import os
    from tqdm import tqdm, tqdm_notebook
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            tqdm = tqdm_notebook
    except:
        pass
    r = requests.get(url, stream=True, verify=False)
    file_size = int(r.headers.get('content-length', -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte, ncols=120,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size
