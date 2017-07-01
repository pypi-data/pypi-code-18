import itertools

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def unique_everseen(iterable, key_extractor=None):
    seen = set()
    if key_extractor is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen.add(element)
            yield element
    else:
        for element in iterable:
            key = key_extractor(element)
            if key not in seen:
                seen.add(key)
                yield element
