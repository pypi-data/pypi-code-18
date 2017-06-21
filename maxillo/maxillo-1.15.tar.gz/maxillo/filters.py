import arrow

def humanize(value):
    dt = arrow.get(value)
    return dt.humanize()

def nosha(value):
    index = value.find('@sha')
    if index > 0:
        return value[:index]
    return value

FILTERS = {
    'humanize'  : humanize,
    'nosha'     : nosha,
}
