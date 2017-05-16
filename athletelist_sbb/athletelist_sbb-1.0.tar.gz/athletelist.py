def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return time_string
    (mins, secs) = time_string.split(splitter)
    return mins + '.' + secs


class AthleteList(list):
    def __init__(self, a_name, a_dob=None, a_time=[]):
        list.__init__([])
        self.extend(a_time)
        self.name = a_name
        self.dob = a_dob

    def top3(self):
        return (sorted(set([sanitize(t) for t in self])))[0:3]