import icalendar

def get_hashable_field(vevent, key):
    """ Transforms a icalendar field into something hashable
    """
    v = vevent.get(key)
    if isinstance(v, icalendar.prop.vDDDTypes):
        return v.dt
    else:
        return str(v)
