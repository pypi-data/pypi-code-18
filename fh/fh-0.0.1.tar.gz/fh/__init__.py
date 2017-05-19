#!/usr/bin/env python3
import os
from .feed import fetch
from .annotations import MHFolder, MHFile
from .util import run, RunError

def feedrow(line):
    if 1 <= line.count(':'):
        identifier, url = line.split(':', 1)
        return (identifier.strip(), url.strip())
    else:
        raise ValueError('Invalid feed line: %r' % line)

def feedlocal(subfolder):
    try:
        stdout = run('scan', subfolder, '-format', '%{X-Feed-Link}')
    except RunError:
        return set()
    else:
        return set(stdout.strip().split('\n'))

def fh(folder: MHFolder='+feeds',
       feedsfile: MHFile=MHFile('feedaliases'),
       rcvstore='/usr/local/libexec/rcvstore'):
    '''
    :param folder: Root MH Folder to store feeds in
    :param feedsfile: File with feeds, with one feed per row, each row
        containing the feed identifier, a colon, then the URL. This format is a
        subset of mh-alias foramt. The URL may include "${page}", which will be
        substituted for page numbers to download multiple pages.
    :param rcvstore: rcvstore executable
    '''
    with open(feedsfile) as fp:
        for line in fp:
            identifier, url = feedrow(line)
            subfolder = os.path.join(folder, identifier)
            for message in fetch(url, feedlocal(subfolder)):
                message['X-Feed-Id'] = identifier
                run(rcvstore, subfolder, stdin=message.as_bytes())
                yield '%(X-Feed-Id)s    %(Subject)s' % message
            break

def main():
    import horetu
    horetu.cli(fh)
