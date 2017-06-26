from __future__ import print_function
from __future__ import division

import numpy as np

from math import log


def semantic_coherence(model, topic_tuple, numwords=10):
    eps = 1e-12
    A = model.A_matrix
    pmi_semantic = 0.
    for i in range(1, numwords):
        itup = topic_tuple[i]
        iwordid = model.word2id_dict[itup[0]]
        for j in range(0, i):
            jtup = topic_tuple[j]
            jwordid = model.word2id_dict[jtup[0]]
            w1_docs = set(np.where(A[iwordid,:]>0)[0])
            w2_docs = set(np.where(A[jwordid,:]>0)[0])
            w1w2docs = w1_docs & w2_docs
            num = len(w1w2docs) + eps
            den = len(w2_docs)
            fraction = num/den
            pmi_semantic += log(fraction)
    return pmi_semantic
