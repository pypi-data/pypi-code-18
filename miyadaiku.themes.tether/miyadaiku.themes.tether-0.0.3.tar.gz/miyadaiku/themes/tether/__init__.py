from miyadaiku.core.contents import get_content_from_package, bin_loader
from miyadaiku.core import config

TETHER_MIN = 'tether.min.js'
TETHER = 'tether.js'
DEST_PATH = '/static/tether/'

def load_package(site):
    f = site.config.get('/', 'tether_compressed')
    f = config.to_bool(f)
    tether = TETHER_MIN if f else TETHER
    src_path = 'externals/js/'+tether
    
    content = get_content_from_package(site, __name__, src_path, DEST_PATH+tether, bin_loader)
    site.contents.add(content)
    site.config.add('/', {'tether_path': DEST_PATH+tether})
