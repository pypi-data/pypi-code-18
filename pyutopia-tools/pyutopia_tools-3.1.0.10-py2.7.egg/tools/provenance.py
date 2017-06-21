import datetime



def hasprovenance(value):
    return hasattr(value, '_provenance') and type(value._provenance) == dict

def provenance(value):
    try:
        return value._provenance
    except AttributeError:
        raise RuntimeError('No associated provenance found for this value')

def wrap_provenance(value, **kwargs):
    kwargs.setdefault('when', datetime.datetime.now())
    if isinstance(kwargs['when'], datetime.datetime):
        kwargs['when'] = kwargs['when'].isoformat()
    class sourced(type(value)):
        _provenance = kwargs
    sourced = sourced(value)
    return sourced
