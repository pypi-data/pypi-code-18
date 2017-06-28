# ===============================================================================
# Copyright 2017 GustavoJunior
# ===============================================================================

import os
import re
import sys
import math
import time
import urllib
import urllib2
import tarfile
from datetime import datetime, timedelta

import web_tools


class StationNotFoundError(Exception):
    pass


class InvalidSatelliteError(Exception):
    pass


def connect_earth_explorer(usgs):
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)

    data = urllib2.urlopen("https://ers.cr.usgs.gov").read()
    m = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data)
    if m:
        token = m.group(1)
    else:
        print "Error : CSRF_Token not found"
        # sys.exit(-3)

    params = urllib.urlencode(dict(username=usgs['account'], password=usgs['passwd'], csrf_token=token))
    request = urllib2.Request("https://ers.cr.usgs.gov/login", params, headers={})
    f = urllib2.urlopen(request)

    data = f.read()
    f.close()
    if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products') > 0:
        print "Authentification failed"
        # sys.exit(-1)
    return


def download_chunks(url, output_dir, image):
    """ Downloads large files in pieces
  """
    try:
        req = urllib2.urlopen(url)
        # if downloaded file is html
        if req.info().gettype() == 'text/html':
            print "error : file is in html and not an expected binary file"
            lines = req.read()
            if lines.find('Download Not Found') > 0:
                raise TypeError
            else:
                with open("error_output.html", "w") as f:
                    f.write(lines)
                    print "result saved in ./error_output.html"
                    # sys.exit(-1)
        # if file too small
        total_size = int(req.info().getheader('Content-Length').strip())

        if total_size < 50000:
            print "Error: The file is too small to be a Landsat Image"
            print url
            # sys.exit(-1)
        print image, total_size
        total_size_fmt = sizeof_fmt(total_size)

        # download
        downloaded = 0
        CHUNK = 1024 * 1024 * 8
        with open(output_dir + '/' + image, 'wb') as fp:
            start = time.clock()
            print('Downloading {0} ({1}):'.format(image, total_size_fmt))
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                done = int(50 * downloaded / total_size)
                sys.stdout.write('\r[{1}{2}]{0:3.0f}% {3}ps'
                                 .format(math.floor((float(downloaded)
                                                     / total_size) * 100),
                                         '=' * done,
                                         ' ' * (50 - done),
                                         sizeof_fmt((downloaded // (time.clock() - start)) / 8)))
                sys.stdout.flush()
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        if e.code == 500:
            print 'error code 500: file doesnt exist'
            pass
        else:
            print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return output_dir, image


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
            # num /= 1024.0


def unzip_image(tgzfile, outputdir):
    target_tgz = os.path.join(outputdir, tgzfile)
    if os.path.exists(target_tgz):
        print 'found tgs: {} \nunzipping...'.format(target_tgz)
        tfile = tarfile.open(target_tgz, 'r:gz')
        tfile.extractall(outputdir)
        print 'unzipped\ndeleting tgz: {}'.format(target_tgz)
        os.remove(target_tgz)
    else:
        raise NotImplementedError('Did not find download output directory to unzip...')
    return None


def get_credentials(usgs_path):
    with file(usgs_path) as f:
        (account, passwd) = f.readline().split(' ')
        if passwd.endswith('\n'):
            passwd = passwd[:-1]
        usgs = {'account': account, 'passwd': passwd}
        return usgs


def get_station_list_identifier(product):
    if product.startswith('LC8'):
        identifier = '12864'
        stations = ['LGN']
    elif product.startswith('LE7'):
        identifier = '3373'
        stations = ['EDC', 'SGS', 'AGS', 'ASN', 'SG1', 'CUB', 'COA']
    elif product.startswith('LT5'):
        identifier = '3119'
        stations = ['GLC', 'ASA', 'KIR', 'MOR', 'KHC', 'PAC',
                    'KIS', 'CHM', 'LGS', 'MGR', 'COA', 'MPS', 'CUB']
    else:
        raise NotImplementedError('Must provide valid product string...')

    return identifier, stations



def down_usgs_by_id(scene_id, output_dir, usgs_creds_txt):

    usgs_creds = get_credentials(usgs_creds_txt)
    connect_earth_explorer(usgs_creds)

    identifier, stations = get_station_list_identifier(scene_id)
    base_url = 'https://earthexplorer.usgs.gov/download/'
    tail_string = '{}/{}/STANDARD/EE'.format(identifier,scene_id)
    url = '{}{}'.format(base_url,tail_string)
    tgz_file = '{}.tgz'.format(scene_id)
    scene_dir = os.path.join(output_dir, scene_id)
    if not os.path.isdir(scene_dir):
	os.mkdir(scene_dir)
	download_chunks(url,scene_dir,tgz_file)
	print 'image {}'.format(os.path.join(scene_dir,tgz_file))
	unzip_image(tgz_file, scene_dir)
    else:
	raise NotImplementedError('This image already exists at {}'.format(output_dir))

    return None


if __name__ == '__main__':
    pass

# ===============================================================================
