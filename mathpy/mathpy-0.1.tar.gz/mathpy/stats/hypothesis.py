"""
Module containing methods for performing common hypothesis tests such as t-tests
and ANOVA.

"""

# import numpy as np
#
# from mathpy._lib import _create_rec_arrays
# from mathpy.stats.variance import var
#
#
# def ttest(y1, y2=None, mu=None, names=None):
#     if names is not None:
#         cols = ','.join(list(names))
#     else:
#         cols = None
#
#     n1 = len(y1)
#     s1 = int(var(y1))
#     ybar1 = np.mean(y1)
#     y1 = _create_rec_arrays(y1)
#
#     if y2 is not None:
#         n2 = len(y2)
#         s2 = int(var(y2))
#         ybar2 = np.mean(y2)
#
#         t = (ybar1 - ybar2) / np.sqrt(s1 / n1 + s2 / n2)
#
#     else:
#         if mu is None:
#             return 'Must specify mu to test one-sample hypothesis'
#
#         t = (n1 - mu) / np.sqrt(s1 / n1)
#
#     return t
#
# def degrees_of_freedom(y1, y2=None):
#     n1 = len(y1)
#     s1 = var(y1)
#     v1 = n1 - 1
#
#     if y2 is not None:
#         n2 = len(y2)
#         s2 = var(y2)
#         v2 = n2 - 1
#
#         v = np.power((s1 / n1 + s2 / n2), 2) / (np.power((s1 / n1), 2) / v1 + np.power((s2 / n2), 2) / v2)
#     else:
#         v = v1
#
#     return v


# def anova(x, names=None, method=None):
#     if names is not None:
#         cols = ','.join(list(names))
#     else:
#         cols = None
#
#     x = _create_rec_arrays(x)
