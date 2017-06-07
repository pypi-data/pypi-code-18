from django.conf import settings
import importlib
print "ok1"
def auto_triggers():
    for app in settings.INSTALLED_APPS:
        try:
           module = importlib.import_module(app + '.triggers')
        except ImportError as e:
            if str(e) != 'No module named triggers':
                raise e
            # end if
        # end try
    # end for
# end def