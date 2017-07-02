import exceptions
import multiprocessing
import time

from constants import Constants

verbose = False
serialize = False


def download(links=[], max_links=-1, num_processes=1):
    if len(links) is 0:
        links = Constants.load_links(max_links)
    start = time.time()

    pool = multiprocessing.Pool(processes=num_processes)

    results = pool.map(_doExecute, links)
    pool.close()
    pool.join()
    failed = filter(lambda r: r[0] is False, results)

    print("Download with {} processes and {} links took {}, failed {} "
          .format(num_processes, len(links), (time.time() - start), len(failed)))

    if len(failed):
        raise (exceptions.OSError("Failed {}".format(len(failed))))


def _doExecute(url):
    # TODO: implement downloading with hyper
    raise exceptions.NotImplementedError
    """
    try:
        if url is None or not isinstance(url, six.types.StringTypes):
            return False, "No url was given to download"
        if verbose:
            print("[Process: {}] - Downloading url {} ".format(multiprocessing.current_process(), url))

        url_p = urlparse.urlparse(url)
        target = "{}://{}?{}".format(url_p.scheme, url_p.hostname, url_p.query)
        conn = HTTPConnection(target)
        conn.request('GET', url_p.path)
        resp = conn.get_response()

        if Constants.picture_serialization:
            with open(Constants.get_output_for_url(url), "wb") as f:
                f.write(resp.read())
        else:
            # For performance measurement
            resp.read()
        return True,
    except Exception as e:
        return False,
    """