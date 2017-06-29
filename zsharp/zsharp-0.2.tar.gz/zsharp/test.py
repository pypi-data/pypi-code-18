import numpy as np
from zsharp import numerical



x=np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
xgrid=[0,0.5,1]
y=x**2
numerical.BinGrid(x,y,xgrid,0)