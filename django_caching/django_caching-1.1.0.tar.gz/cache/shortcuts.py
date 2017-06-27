from django.shortcuts import Http404


def get_cached_object_or_404(cls, **kwargs):
    try:
        obj = cls.cached_objects.get(**kwargs)
    except:
        raise Http404

    return obj
