from django.conf import settings
import importlib
import re

def search_triggers(app):
    try:
        return importlib.import_module(app + '.triggers')
    except ImportError as e:
        re_app = re.sub('\.\w+$', '', app)
        if (app == re_app):
            return None
        # end if
        return search_triggers(re_app)
    # end try
# end def

def auto_triggers():
	for app in settings.INSTALLED_APPS:
	    search_triggers(app)
	# end for
# end def