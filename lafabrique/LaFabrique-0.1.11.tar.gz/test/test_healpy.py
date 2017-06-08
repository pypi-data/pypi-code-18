from scipy import weave

c_code = r"""
t = ang2pix(2048,theta,phi);
"""
theta = 0.
phi = 0.
t = 0.
weave.inline(c_code, ["t", "theta", "phi"], headers=["<healpix_map.h>"])
print t
