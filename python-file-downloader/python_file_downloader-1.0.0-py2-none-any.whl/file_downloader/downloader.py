"""
  It downloads pictures using multirpocessing.Pool and the Request api
"""
# pylint: skip-file
from mechanize import Request, urlopen
from constants import Constants


import multiprocessing
import time
import traceback
import exceptions
import six


verbose = False

def download(links, max_links=-1, num_processes=1):
    """
      Downloads the list of links in the parameter
    """
    if len(links) is 0:
        links = Constants.load_links(max_links)
    start = time.time()

    pool = multiprocessing.Pool(processes=num_processes)

    results = pool.map(doDownload, links)
    pool.close()
    pool.join()
    
    failed = filter( lambda r: r[0] == False, results)

    print("Download with {} processes and {} links took {}, failed {} "
          .format(num_processes, len(links), (time.time() - start), len(failed)))

    if not any(failed):
        raise exceptions.OSError("Failed {}".format(len(failed)))


def doDownload(url, serialize=Constants.picture_serialization):
    """
        Download the given url and serialize depending on the parameter
    """
    try:
        if url is None or not isinstance(url, six.types.StringTypes):
            return False, "No url was given to download"
        if verbose:
            print(u"[Process: {}] - Downl. url {} "
                  .format(multiprocessing.current_process(), url))
        req = Request(url)
        web_file = urlopen(req)
        if serialize:
            with open(Constants.get_output_for_url(url), "wb") as handle:
                handle.write(web_file.read())
        else:
            # For performance measurements
            web_file.read()
        return True,
    except Exception as e:
        return False

def main() :
    print("Downloader main method")

if __name__ == "__main__":
    print("Main method of file ", __file__)