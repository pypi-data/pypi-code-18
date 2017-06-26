from __future__ import print_function
from __future__ import division

import os
import numpy as np


def verify_filename(filename):
    if not os.path.isfile(filename):
        raise ValueError("Given filepath doesn't exist.")
    return


def read_tsvd_M_hat_matrix(num_topics, vocab_size, avg_doc_size, datasetname, norm=True):
    """
    Read the topic-word distribution matrix M_hat_catch generated from TSVD
    and return normalized M
    Input: num_topics, vocab_size, norm <bool> whether to normalize to 0-1 range or not
    Output: Return normalized vocab_size x num_topics distribution
    """
    fname = "./data/tsvd_M_hat_catch_2" + datasetname
    Mt = np.zeros((num_topics, vocab_size))
    with open(fname, 'r') as f:
        for topic_num, line in enumerate(f):
            line.strip(' \n')
            line = line.split('\t')
            l = []
            for i, word in enumerate(line):
                try:
                    float(word)
                except ValueError:
                    del line[i]
                    word = word.strip(' \n')
                    if word == '':
                        continue
                    ws = word.split(' ')
                    for w in ws:
                        l.append(w)
            for w in l:
                line.append(w)
            for w in line:
                try:
                    float(w)
                except ValueError:
                    print('ERROR:', w)
            nums = [float(word) for word in line]
            Mt[topic_num, :] = nums

    M = Mt.transpose()
    if norm:
        M = M/avg_doc_size
    return M
