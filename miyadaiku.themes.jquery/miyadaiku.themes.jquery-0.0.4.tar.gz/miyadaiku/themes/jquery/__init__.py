from miyadaiku.core.contents import get_content_from_package, bin_loader
from miyadaiku.core import config

JQUERY_MIN = 'jquery-3.2.1.min.js'
JQUERY = 'jquery-3.2.1.js'
DEST_PATH = 'static/jquery/'

def load_package(site):
    f = site.config.get('/', 'jquery_compressed')
    f = config.to_bool(f)
    jquery = JQUERY_MIN if f else JQUERY
    src_path = 'externals/'+jquery
    
    content = get_content_from_package(site, __name__, src_path, DEST_PATH+jquery, bin_loader)
    site.contents.add(content)
    site.config.add('/', {'jquery_path': DEST_PATH+jquery})
