from AnalysisBackend.mapping.maprep import MapMakingVectors
from inputs import InputScan
import numpy as np
import healpy as hp
import pylab as pl
import util_CMB

# def set_param(func):
#     def wrapper(*args, **kwargs):
#         res = func(*args, **kwargs)


# m = MapMakingVectors.load('additional_files/SO_full.hdf5')
# epsilons = [0., 0.2, 0.24]
# for pos, epsilon in enumerate(epsilons):
#     w = util_CMB.partial2full(
#         util_CMB.qu_weight_mineig(m.cc*1e3, m.cs*1e3, m.ss*1e3, epsilon=epsilon, verbose=True),
#         m.mapinfo.obspix,
#         m.mapinfo.nside)
#
#     mask = w > 0
#     w[~mask] = np.nan
#     hp.gnomview(w, rot = [0., -57.5], xsize=800, reso=6.8, sub=int('13%d' % (pos + 1)))
# pl.show()

exps = ['deep', 'shallow']

fig, ax = pl.subplots(1,2,figsize=(10,5))
for pos, exp in enumerate(exps):
    m = InputScan.load('SO_%s_large_aperture_v2/masks/SO_%s_large_aperture_v2.hdf5' % (exp, exp))
    mask = m.cc > 0.#0.5 * np.max(m.cc)
    tr = m.w[mask]

    ax[pos].scatter(m.cc[mask]/tr, m.cs[mask]/tr,marker='.',alpha=0.1,s=1)
    ax[pos].axvline(0.5, color='orange',ls='--')
    ax[pos].axhline(0., color='orange',ls='--')

    epsilons = [0., 0.2, 0.24]
    colors = ['black', 'black', 'black']
    ls = ['--', ':', '-']
    for pos_eps, epsilon in enumerate(epsilons):
        radius = np.sqrt(0.25 - epsilon)
        lab = '%.2f'%epsilon
        circ=pl.Circle((0.5,0.),radius=radius, color=colors[pos_eps], fill=False, lw=2, ls=ls[pos_eps],label='$\epsilon =$ ' + lab)
        ax[pos].add_patch(circ)
    ax[pos].set_xlim(0,1)
    ax[pos].set_ylim(-0.5,0.5)

    ax[pos].set_title('%s survey' % exp,fontsize=18)
    if pos == 0:
        ax[pos].set_ylabel('Off-diagonal element',fontsize=18)
    ax[pos].set_xlabel('Diagonal element',fontsize=18)
    leg=pl.legend(loc='upper right')
    # leg.get_frame().set_alpha(0.0)
    # pl.savefig('selection_criterion.pdf')
pl.savefig('plots/polarised_pixel_variance.png')
pl.show()


# m = MapMakingVectors.load('additional_files/SO_full.hdf5')
# mask = m.cc > 0.#0.5 * np.max(m.cc)
# tr = m.w[mask]
#
# def mask_it(data_in, data_out, threshold, epsilon):
#     mask = data_in < threshold
#     data_out[mask] += epsilon
#     return data_out
#
# data_out = np.zeros_like(m.cc)
# data_in = (m.cc[mask]/tr - 0.5)**2 + (m.cs[mask]/tr)**2
# epsilons = np.linspace(0.0,0.25,4)
# print epsilons
# for epsilon in epsilons:
#     radius = 0.25 - epsilon
#     data_out = mask_it(data_in, data_out, radius, epsilon)
# data = util_CMB.partial2full(data_out, m.mapinfo.obspix[mask], m.mapinfo.nside)
# hp.gnomview(data, rot = [0., -57.5], xsize=800, reso=6.8)
# pl.show()
#
# # ax.scatter(m.cc[mask]/tr, m.cs[mask]/tr,marker='.',alpha=0.1,s=1)
# # ax.axvline(0.5, color='orange',ls='--')
# # ax.axhline(0., color='orange',ls='--')
#
# epsilons = [0., 0.2, 0.24]
# colors = ['black', 'black', 'black']
# ls = ['--', ':', '-']
# for pos, epsilon in enumerate(epsilons):
#     radius = np.sqrt(0.25 - epsilon)
#     lab = '%.2f'%epsilon
#     circ=pl.Circle((0.5,0.),radius=radius, color=colors[pos], fill=False, lw=2, ls=ls[pos],label='$\epsilon =$ ' + lab)
#     ax.add_patch(circ)
# ax.set_xlim(0,1)
# ax.set_ylim(-0.5,0.5)
#
# ax.set_title('Polarised pixel variance',fontsize=18)
# ax.set_ylabel('Off-diagonal element',fontsize=18)
# ax.set_xlabel('Diagonal element',fontsize=18)
# leg=pl.legend(loc='upper right')
# # leg.get_frame().set_alpha(0.0)
# # pl.savefig('selection_criterion.pdf')
# pl.savefig('selection_criterion.png')
# pl.show()
