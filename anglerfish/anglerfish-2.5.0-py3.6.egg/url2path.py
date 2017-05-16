#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Download accelerator with multiple concurrent downloads for 1 file."""


import logging as log
import os
import ssl
import threading

from datetime import datetime
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

try:
    from make_autochecksum import autochecksum
    from bytes2human import bytes2human
    from seconds2human import timedelta2human
    from get_human_datetime import get_human_datetime
except ImportError:
    from anglerfish import (autochecksum, bytes2human,
                            timedelta2human, get_human_datetime)


def _get_context():
    """Return a context for the downloaders."""
    _context = ssl.create_default_context()
    _context.check_hostname = False  # Do NOT Check server Hostnames
    _context.verify_mode = ssl.CERT_NONE  # Do NOT Check server SSL Certificate
    return _context


def _download_simple(url, data, timeout, cafile, capath, filename):
    """Download without multiple concurrent downloads for the same file."""
    with urlopen(url, data=data, timeout=timeout, cafile=cafile, capath=capath,
                 context=_get_context()) as urly, open(filename, 'wb') as fyle:
        fyle.write(urly.read())
        return filename


def _calculate_ranges(value, numsplits):
    """Calculate the number of ranges of bytes, return a list of ranges."""
    lst = []
    for i in range(numsplits):
        lst.append('{0}-{1}'.format(
            i if i == 0 else int(round(1 + i * value / (numsplits * 1.0), 0)),
            int(round(1 + i * value / (numsplits * 1.0) +
                      value / (numsplits * 1.0) - 1, 0))))
    return tuple(lst)


def _get_size(url, data, timeout, cafile, capath):
    """Get the file Size in bytes from a remote URL."""
    with urlopen(url, data=data, timeout=timeout, cafile=cafile, capath=capath,
                 context=_get_context()) as urly:
        size = int(urly.headers.get('content-length', None))
    if size:
        log.info("{0}({1}Bytes) download".format(bytes2human(size, "m"), size))
    else:
        log.info("File size to download cant be determined from HTTP Headers.")
    return size


def _download_a_chunk(idx, irange, dataDict, url,
                      data, timeout, cafile, capath):
    req = Request(url)
    req.headers['Range'] = 'bytes={0}'.format(irange)
    print("Thread {0} is downloading {1}".format(idx, req.headers['Range']))
    with urlopen(req, data=data, timeout=timeout, cafile=cafile, capath=capath,
                 context=_get_context()) as urly:
        dataDict[idx] = urly.read()


def url2path(url, data=None, timeout=None, cafile=None, capath=None,
             filename=None, suffix=None, name_from_url=False,
             concurrent_downloads=5, force_concurrent=False, checksum=False):
    if not url.lower().startswith(("https:", "http:", "ftps:", "ftp:")):
        return url  # URL is a file path?.
    start_time, dataDict = datetime.now(), {}
    if not filename and bool(name_from_url):  # Get the filename from the URL.
        filename = url.split('/')[-1]
    if not filename:  # Create a temporary file as the filename.
        filename = NamedTemporaryFile(suffix=suffix, prefix="angler_").name
    log.info("Angler download accelerator start.")
    log.info("From: {0}.\nTo: {1}.\nTime: {2} ({3}).".format(
        url, filename, get_human_datetime(start_time), start_time))
    sizeInBytes = _get_size(url, data=data, timeout=timeout,
                            cafile=cafile, capath=capath)
    # if sizeInBytes=0,Resume is not supported by server,use _download_simple()
    # if sizeInBytes < 1 Gigabytes,file is small,use _download_simple()
    if not int(sizeInBytes / 1024 / 1024 / 1024) >= 1 and not force_concurrent:
        log.info("Resume is Not supported by the server or file is too small.")
        filename = _download_simple(
            url, data=data, timeout=timeout,
            cafile=cafile, capath=capath, filename=filename)
        if checksum and autochecksum:
            log.info("Generating Anglers Auto-CheckSum for downloaded file.")
            filename = autochecksum(filename, update=True)
        return filename
    splitBy = concurrent_downloads if concurrent_downloads in range(11) else 10
    ranges = _calculate_ranges(int(sizeInBytes), int(splitBy))
    log.info("Using {0} async concurrent downloads for 1 file".format(splitBy))
    # multiple concurrent downloads for the same file.
    downloaders = [threading.Thread(
        target=_download_a_chunk,
        args=(idx, irange, dataDict, url, data, timeout, cafile, capath), )
                   for idx, irange in enumerate(ranges)]
    for th in downloaders:
        th.start()
    for th in downloaders:
        th.join()
    with open(filename, 'wb') as fh:  # Reassemble file in correct order.
        for _idx, chunk in tuple(sorted(dataDict.items())):
            fh.write(chunk)
    if checksum and autochecksum:
        log.info("Generating Anglers Auto-CheckSum for downloaded file.")
        filename = autochecksum(filename, update=True)
    # Log some nice info.
    fl_size, fl_time = os.path.getsize(filename), datetime.now() - start_time
    log.info("Downloaded {0} binary data chunks total.".format(len(dataDict)))
    log.info("Finished writing downloaded output file: {0}.".format(filename))
    log.info('Size:{0} ({1} Bytes)'.format(bytes2human(fl_size, "m"), fl_size))
    log.info("Time: {0} ({1}).".format(timedelta2human(fl_time), fl_time))
    log.info("Finished:{0} ({1})".format(get_human_datetime(), datetime.now()))
    return filename
