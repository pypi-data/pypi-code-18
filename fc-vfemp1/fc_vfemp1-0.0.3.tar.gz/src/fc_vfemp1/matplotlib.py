import numpy as np
import matplotlib.pyplot as plt
import fc_simesh_matplotlib.siMesh as siplt
from fc_tools.matplotlib import set_axes_equal,DisplayFigures
from fc_tools.colors import selectColors


def plot_order(res_order,Ch=0.1,Ch2=1.0,isPlot=2*[True]):
  Lh=res_order['Lh']
  Lu_errL2=res_order['Lu_errL2'];Lu_errH1=res_order['Lu_errH1']
  colors = selectColors(4)
  if isPlot[0]:
    plt.loglog(Lh,Lu_errL2,color=colors[0],label='$\|u_h-\pi_h(u)\|_{L^2}$')
  if isPlot[1]:
    plt.loglog(Lh,Lu_errH1,color=colors[1],label='$\|u_h-\pi_h(u)\|_{H^1}$')
  plt.loglog(Lh,Ch*Lh,color=(0,0,0),label='$O(h)$',ls=':',marker='s')
  plt.loglog(Lh,Ch2*Lh**2,color=(0,0,0),label='$O(h^2)$',ls='-.',marker='o')
  plt.legend(bbox_to_anchor=(0.05, 1), loc=2, borderaxespad=0.)
  plt.xlabel('$h$')