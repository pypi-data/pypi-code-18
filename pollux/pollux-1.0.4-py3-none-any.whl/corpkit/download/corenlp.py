def corenlp_downloader(custompath=False):
    """
    Very simple CoreNLP downloader

    :param custompath: A path where you want to put CoreNLP
    :type custompath: ``str``

    :Usage:
    python -m corpkit.download.corenlp
    """
    import os
    from corpkit.constants import CORENLP_URL, CORENLP_PATH
    from corpkit.build import download_from_url, extract_cnlp
    if not os.path.exists(os.path.expanduser('~/corenlp')):
        os.makedirs(os.path.expanduser('~/corenlp'))
    corenlp_fname = os.path.basename(CORENLP_URL)
    if custompath:
        CORENLP_PATH = custompath
    corenlp_fpath = os.path.join(CORENLP_PATH, corenlp_fname)

    download_from_url(CORENLP_URL, corenlp_fpath)
    return extract_cnlp(corenlp_fpath)

if __name__ == '__main__':
    import sys
    custompath = False if len(sys.argv) == 1 else sys.argv[-1]
    corenlp_downloader(custompath=custompath)
    