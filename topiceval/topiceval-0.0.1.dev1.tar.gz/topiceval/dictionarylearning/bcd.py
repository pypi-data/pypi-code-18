from __future__ import division
from __future__ import print_function

from topiceval.basemodel import BaseModel
import topiceval.dictionarylearning.sparse_coding as sparse_coding
import topiceval.dictionarylearning.sparse_dictionary as sparse_dictionary
import topiceval.utils as utils

import logging
import sys
import os

import numpy as np


def softinit(K, D):
    H_sofinit = np.random.random_sample((K, D))
    for k in range(K):
        Hk = H_sofinit[k, :]
        assert (Hk.shape == (D,)), "hk has wrong shape"
        H_sofinit[k, :] = Hk / np.linalg.norm(Hk, ord=2)
        assert (0.99 < np.linalg.norm(H_sofinit[k, :], ord=2) ** 2 < 1.01), "Hk norm is not near 1"
    return H_sofinit


def normalize_X(X, N, D):
    for n in range(N):
        Xn = X[n, :]
        assert (Xn.shape == (D, )), "Xn has wrong shape"
        X[n, :] = Xn / np.linalg.norm(Xn, ord=2)
        assert (0.99 < np.linalg.norm(X[n, :], ord=2) ** 2 < 1.01), "Xn norm is not near 1"
    return X


class BCD(BaseModel):
    def __init__(self, datasetname, learn_model=True, X_matrix_path=None, A_matrix_path=None, id2word_dict=None,
                 id2word_dict_path=None, corpus=None, corpus_path=None, vocab_filepath=None, docword_filepath=None,
                 vocab_size=None, num_docs=None, num_topics=None, H_matrix_path=None, W_matrix_path=None,
                 evaluation_mode=False, bcd_iters=15, H_init=None, reconstruction_error_lim=1e2, gamma_frac=0.3,
                 nu_frac=0.15):
        # TODO: If A/X matrix path is given, it may be is being revaluated in basemodel, check that
        # TODO: Make hyperparameters file
        self.modelname = "bcd"
        super(BCD, self).__init__(datasetname=datasetname, id2word_dict=id2word_dict,
                                  id2word_dict_path=id2word_dict_path, corpus=corpus,
                                  corpus_path=corpus_path, vocab_filepath=vocab_filepath,
                                  docword_filepath=docword_filepath, vocab_size=vocab_size, num_docs=num_docs,
                                  evaluation_mode=evaluation_mode,
                                  Amatrix_needed=(X_matrix_path is None and A_matrix_path is None))
        self.num_topics = num_topics
        if X_matrix_path is not None:
            self.X_matrix = np.load(X_matrix_path)
        elif A_matrix_path is not None:
            self.X_matrix = np.load(A_matrix_path).T
        else:
            self.X_matrix = self.A_matrix.T
        if self.num_docs is not None:
            assert (self.X_matrix.shape[0] == self.num_docs), "X shape does not agree with num_docs"
        self.num_docs = self.X_matrix.shape[0]
        if vocab_size is not None:
            assert (self.X_matrix.shape[1] == vocab_size), "X shape does not agree with num_docs"

        if not learn_model and (H_matrix_path is None or W_matrix_path is None):
            raise ValueError("Learn model option is off and H and W matrix paths havent been provided.")

        if learn_model:
            if self.num_topics is None:
                raise ValueError("Num_topics not provided (learn_model option is on)")
            if H_matrix_path is not None or W_matrix_path is not None:
                logging.warning("User given filepath for H/W discarded in favor of learn_model=True")
            logging.info("Starting BCD learning for num_topics = %d, num_iters = %d, gamma=%0.2f*K, "
                         "nu=%0.2f*D, reconstruction_error_lim = %0.2f"
                         % (num_topics, bcd_iters, gamma_frac, nu_frac, reconstruction_error_lim))
            self.H_matrix, self.W_matrix = \
                self.block_coordinate_descent(num_iters=bcd_iters, H_init=H_init,
                                              reconstruction_error_lim=reconstruction_error_lim)
            assert (self.H_matrix.shape[0] == self.num_topics and self.H_matrix.shape[1] == self.vocab_size), \
                "H matrix learned has wrong dimenstions"
            assert (self.W_matrix.shape[0] == self.num_docs and self.W_matrix.shape[1] == self.num_topics), \
                "W matrix learned has wrong dimensions"
        else:
            if H_matrix_path is None or W_matrix_path is None:
                raise ValueError("If learn_model option is off, both H and W matrix paths need to be given")
            utils.verify_filename(H_matrix_path)
            utils.verify_filename(W_matrix_path)
            self.H_matrix = np.load(H_matrix_path)
            self.W_matrix = np.load(W_matrix_path)
            if self.num_topics is not None:
                assert (self.num_topics == self.H_matrix.shape[0] and self.num_topics == self.W_matrix.shape[1]), \
                    "Given num_topics do not match with H and W dimensions"
            else:
                assert (self.H_matrix.shape[0] == self.W_matrix.shape[1]), \
                    "W and H matrix don't exhibit same num_topics"
                self.num_topics = self.H_matrix.shape[0]
        self.representative_topic_tuples = self.get_representative_topic_tuples()
        return

    def block_coordinate_descent(self, num_iters, H_init, reconstruction_error_lim):
        K = self.num_topics
        N = self.X_matrix.shape[0]
        D = self.X_matrix.shape[1]
        logging.info("N=%d, D=%d, K=%d" % (N, D, K))
        X = normalize_X(X=self.X_matrix, N=N, D=D)

        if H_init is not None:
            H = H_init
        else:
            H = softinit(K, D)
        assert (H.shape == (K, D)), "H sofinit has wrong shape"
        W = np.zeros((N, K))

        R_old = sys.maxsize
        convergence_lim = N/2500
        for iter_num in range(num_iters):
            logging.info("BCD ITERATION NUMBER: %d" % iter_num)
            W = sparse_coding.learn(X=X, W=W, H=H, gamma=int(0.4*K), parallelization=True)
            X_reconstructed = W.dot(H)
            assert (X_reconstructed.shape == X.shape), "X_reconstructed and X don't agree shapewise"
            reconstruction_error = np.linalg.norm(X - X_reconstructed, ord='fro') ** 2
            logging.info("Reconstruction Error after sparse coding phase %d: %f"
                         % (iter_num, reconstruction_error))
            if reconstruction_error < reconstruction_error_lim:
                logging.info("Reconstruction error limit reached, stopping...")
                break

            H = sparse_dictionary.learn(X=X, H=H, W=W, nu_param=int(0.25*D))
            X_reconstructed = W.dot(H)
            assert (X_reconstructed.shape == X.shape), "x_reconstructed and x don't agree shapewise"
            reconstruction_error = np.linalg.norm(X - X_reconstructed, ord='fro') ** 2
            logging.info("Reconstruction Error after dict learning phase %d: %f"
                         % (iter_num, reconstruction_error))
            if reconstruction_error < reconstruction_error_lim:
                logging.info("Reconstruction error limit reached, stopping...")
                break
            if R_old - reconstruction_error < convergence_lim:
                logging.info("Convergence, stopping BCD early...")
                break
            R_old = reconstruction_error
        return H, W

    def save_H_matrix(self, H_matrix_path):
        np.save(H_matrix_path, self.H_matrix)
        return

    def save_W_matrix(self, W_matrix_path):
        np.save(W_matrix_path, self.W_matrix)
        return

    def get_topic_tuples(self, topicid_list=None, wordspertopic=10):
        if topicid_list is None:
            logging.debug("Using all topics as topicid_list is none")
            topicid_list = range(self.num_topics)
        topic_tuples = []
        for topicid in topicid_list:
            topicid = int(topicid)
            topic_topword_indices = np.argsort(self.H_matrix[topicid, :])[::-1][:int(wordspertopic)]
            topic_tuples.append([(self.id2word_dict[int(idx)].strip('\r'), self.H_matrix[topicid, int(idx)])
                                 for idx in topic_topword_indices])
        return topic_tuples, topicid_list

    def plot_topic_topwords(self, topicid_list=None, wordspertopic=10, cmaps=None):
        topic_tuples, topicid_list = self.get_topic_tuples(topicid_list=topicid_list, wordspertopic=wordspertopic)
        super(BCD, self).plot_topic_topwords_base(topic_tuples=topic_tuples, cmaps=cmaps,
                                                  title='Dictionary Leanring')
        return

    def plot_dominant_topic_document_distribution(self, upper_threshold=0.4, lower_threshold=0.3,
                                                  kind='vbar'):
        super(BCD, self).plot_dominant_topic_document_distribution_base(W_matrix=self.W_matrix.T,
                                                                        upper_threshold=upper_threshold,
                                                                        lower_threshold=lower_threshold, kind=kind)
        return

    def plot_entropy_distribution(self, all_topics=True, topics=None, *args, **kwargs):
        if all_topics:
            if topics is not None:
                logging.warning("bcd.plot_entropy_distribution: User given topic list discarded as all_topics=True")
            topics = range(self.num_topics)
        else:
            assert (topics is not None), "If all_topics option is switched off, list of topics to print must be given"
        distributions = [self.H_matrix[topic_id, :] for topic_id in topics]
        super(BCD, self).plot_entropy_distribution_base(distributions, *args, **kwargs)
        return

    def plot_topic_entropy_colormap(self):
        distributions = [self.H_matrix[topic_id, :] for topic_id in range(self.num_topics)]
        super(BCD, self).plot_topic_entropy_colormap(distributions)
        return

    def save_topic_top_words(self, filename, datasetname, num_topics, wordspertopic=10, separator=","):
        if num_topics > self.num_topics or num_topics == -1:
            if num_topics > self.num_topics:
                logging.warning("Given num_topics > num_topics of model, selecting all topics")
            topicid_list = range(self.num_topics)
        else:
            topicid_list = np.random.choice(self.num_topics, num_topics, replace=False)
        topic_tuples, _ = self.get_topic_tuples(topicid_list=topicid_list, wordspertopic=wordspertopic)
        super(BCD, self).save_topic_top_words(word_weight_list=topic_tuples, filename=filename,
                                              separator=separator, datasetname=datasetname)
        return

    def get_representative_topic_tuples(self, num_topics=None, wordspertopic=30):
        if num_topics is None:
            num_topics = self.num_topics
        topicid_list = np.random.choice(self.num_topics, num_topics, replace=False)
        topic_tuples, _ = self.get_topic_tuples(topicid_list=topicid_list, wordspertopic=wordspertopic)
        for i, topic_tuple in enumerate(topic_tuples):
            for j, tup in enumerate(topic_tuple):
                topic_tuples[i][j] = (tup[0], tup[1] * tup[1])
        # filename = dirname + "bcd_topics.npy"
        # logging.debug("Saving BCD topic tuples at %s" % filename)
        # np.save(filename, topic_tuples)
        return topic_tuples

    def save_topic_images(self, dirname):
        dirname = dirname + "bcd/"
        if not os.path.exists(dirname):
            logging.debug("Creating directory %s" % dirname)
            os.makedirs(dirname)
        for i, topic_tuple in enumerate(self.representative_topic_tuples):
            new_topic_tuple = []
            for j, tup in enumerate(topic_tuple):
                new_topic_tuple.append((tup[0], tup[1]*tup[1]))
            super(BCD, self).plot_topic_topwords_base(topic_tuples=[new_topic_tuple], cmaps='Uniform',
                                                      title='BCD', save=True, show=False,
                                                      filename=dirname+"topic%d" % i, show_weight=True)
        return

# x = np.array([[0.3, 0.5, sqrt(0.66)], [0.8, 0.2, sqrt(0.32)]])
# h, w = block_coordinate_descent(x, num_topics=4, num_iters=15, H_init=None)
# print(w)
# print(h)
# print(w.dot(h))
# print(x)
