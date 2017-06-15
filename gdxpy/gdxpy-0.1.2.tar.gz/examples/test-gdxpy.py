import gdxpy as gp

a = gp.gload('c2co2','test{1,2}.gdx', returnfirst=True)
print('ccdccd', a)

import gdxpy as gp
import os

# Create a GDX object
gdxpath = os.path.join(gp.__gdxpy_gamsdir__, 'testlib_ml', 'trnsport.gdx')
tdata = gp.gdxfile(gdxpath)

# Suggested way to programmatically load symbols
a = tdata.a()  # or...
a
b = tdata.query('b') # or...
b
c = gp.gload('@c', gdxpath)
c