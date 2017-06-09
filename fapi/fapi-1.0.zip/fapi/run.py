import os
import sys
import json
import string
import pyperclip
import fapi
import urllib2
import progressbar
from optparse import OptionParser

# Arguments
parser = OptionParser()
parser.add_option('-u', '--username', type='string',
               help='Benutzen Sie hier Ihre Kundennummer', metavar='username')

parser.add_option('-p', '--password', type='string',
               help='Benutzen Sie hier Ihren PIN-Code', metavar='password')

parser.add_option('-f', '--folder', type='string',
               help='Ordner indem die heruntergeladenen Dateien gespeichert werden', metavar='folder')

(options, args) = parser.parse_args()
clipboard = pyperclip.paste()

try:
    # Check if account is valid
    account_status = fapi.get_account_status(options.username, options.password)

    # Convert FairUse status
    fairUse = (1 - account_status['fairuse_left']) * 100

    print 'Benutzerkonto %s (%s)' % (account_status['account_name'], account_status['type'])
    print 'Fair-Use Status: %s%%\n' % int(fairUse)

except Exception as err:
    print 'Es ist ein Problem mit dem Benutzerkonto aufgetreten: ' + str(err)
    sys.exit(0)


# Begin download urls
for url in string.split(clipboard, '\n'):
    try:
        data = fapi.getFile(url, options.username, options.password)

        filename = data['filename']
        filesize = int(data['filesize'])
        location = data['location']
        filepath = os.path.join(options.folder, filename)

        if os.path.exists(filepath):
            raise Exception('Die Datei (%s) existiert bereits' % filename)

        widgets = ['%s: ' % filename, progressbar.Percentage(), ' ',
                   progressbar.Bar(marker='0',left='[',right=']'),
                   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]

        pbar = progressbar.ProgressBar(widgets=widgets, maxval=filesize)
        pbar.start()

        u = urllib2.urlopen(location)
        f = open(filepath, 'wb')

        file_size_dl = 0
        block_sz = 8192

        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            pbar.update(file_size_dl)
        f.close()
        pbar.finish()

    except Exception as err:
        print str(err)

    except urllib2.HTTPError as err:
        print 'Die Datei (%s) konnte nicht heruntergeladen werden (%s)' % (data['filename'], err.code)
