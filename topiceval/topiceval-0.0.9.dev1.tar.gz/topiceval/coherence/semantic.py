from __future__ import print_function
from __future__ import division


def semantic_coherence(model, topic_tuple, numwords=10):
    A = model.A_matrix
    for itup in topic_tuple[2:numwords]:
        for jtup in topic_tuple[1:numwords-1]:
            num = len(np.where())