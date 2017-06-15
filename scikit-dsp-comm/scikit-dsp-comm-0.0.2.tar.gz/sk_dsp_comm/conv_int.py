import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
    plt.plot(x,y)
