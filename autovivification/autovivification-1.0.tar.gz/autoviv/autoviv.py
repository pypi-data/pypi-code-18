class AutoVivification(dict):
    """ Use: "if not h[a][b][c][d]: h[a][b][c][d] = int()" if you need to init an int for counting"""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def autoviv():
    return AutoVivification()


"""
h = AutoVivification()

for key in lists:
    a = key[4]
    b = key[0]
    c = key[1]
    d = key[2]
    e = key[3]
    if not h[a][b][c][d]:
        h[a][b][c][d] = int()
    h[a][b][c][d] += 1 

for x in h:
    for y in h[x]:
        for z in h[x][y]:
            for a in h[x][y][z]:
                print  x, y, z, a, h[x][y][z][a]
"""