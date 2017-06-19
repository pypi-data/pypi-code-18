from __future__ import division
from __future__ import print_function

import argparse
import logging

from topiceval import emailextraction as emailextraction
from topiceval.dictionarylearning.bcd import BCD
from topiceval.lda import LDA
from topiceval.thresholdedsvd.tsvd import TSVD
from topiceval.usereval import topiceval_application as application

FORMAT = "[%(asctime)s][%(filename)s - %(funcName)10s()] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%I:%M:%S")


def main():
    parser = argparse.ArgumentParser(description='topic-model-evaluation-package')
    parser.add_argument('-numtopics', help='specify number of topics to learn', type=int, default=20)
    parser.add_argument('-numtopicseval', help='specify number of topics to evaluate per model', type=int, default=10)
    parser.add_argument('-usethreads', help='whether to use threaded mails or single ones', type=int, default=0)
    parser.add_argument('-uselemmatization', help='whether to use lemmatization (nltk)', type=int, default=1)
    # parser.add_argument('-train', help='training data', type=str, default='data/train.txt')
    # parser.add_argument('-dev', help='development data', type=str, default='data/dev.txt')
    # parser.add_argument('-d', help='input dimension', type=int, default=500)
    # parser.add_argument('-cd', help='context dimension', type=int, default=200)
    # parser.add_argument('-dh', help='hidden dimension', type=int, default=100)
    # parser.add_argument('-cdh', help='context hidden dimension', type=int, default=100)
    # parser.add_argument('-deep', help='number of encoder layers, network depth = 2 deep - 1', type=int, default=1)
    # parser.add_argument('-pt', help='if pre-train the network', type=bool, default=True)
    # parser.add_argument('-lambda', help='context weight for backprop', type=float, default=.1)
    # parser.add_argument('-drop', help='dropout probability', type=float, default=0.1)
    # parser.add_argument('-rho', help='regularization weight', type=float, default=1e-4)
    # parser.add_argument('-batch_size', help='adagrad minibatch size.', type=int, default=25)
    # parser.add_argument('-num_epochs', help='number of training epochs', type=int, default=10)
    # parser.add_argument('-num_epochs_pt', help='number of pre-training epochs', type=int, default=7)
    # parser.add_argument('-adagrad_reset', help='reset sum of squared gradients after this number of epochs', type=int,
    #                     default=50)
    # parser.add_argument('-lr', help='adagrad initial learning rate', type=float, default=0.005)
    # parser.add_argument('-output', help='desired location of output model', default='models/params')

    args = vars(parser.parse_args())

    num_topics = args['numtopics']
    num_topics_eval = args['numtopicseval']
    threaded = args['usethreads']
    usenltk = args['uselemmatization']
    if threaded == 0:
        threaded = False
    else:
        threaded = True
    if usenltk == 0:
        usenltk = False
    else:
        usenltk = True
    dirname = emailextraction.extract_usermails(threaded=threaded)
    datasetname = dirname.strip("./data")
    ldamodel = LDA(datasetname=datasetname, id2word_dict_path=dirname+"id2word_dict.pickle",
                   corpus_path=dirname+"corpus.npy", num_topics=num_topics, evaluation_mode=True)
    tsvdmodel = TSVD(datasetname=datasetname, id2word_dict_path=dirname+"id2word_dict.pickle",
                     corpus_path=dirname+"corpus.npy", num_topics=num_topics, evaluation_mode=True)
    bcdmodel = BCD(datasetname=datasetname, id2word_dict_path=dirname+"id2word_dict.pickle",
                   corpus_path=dirname+"corpus.npy", num_topics=num_topics, evaluation_mode=True)
    models = [ldamodel, tsvdmodel, bcdmodel]
    # models = [bcdmodel]
    # for model in models:
    #     model.plot_topic_topwords(topicid_list=np.arange(int(num_topics/2)))
    #     model.save_topic_images(dirname=dirname)
    application.main(models=models, dirname=dirname, num_topics=num_topics_eval, threaded=threaded)
    # ldamodel.plot_topic_entropy_colormap()
    # tsvdmodel.plot_topic_entropy_colormap()
    # bcdmodel.plot_topic_entropy_colormap()
    # ldamodel.plot_dominant_topic_document_distribution(kind='colormap')
    # tsvdmodel.plot_dominant_topic_document_distribution(kind='colormap')
    # bcdmodel.plot_dominant_topic_document_distribution(kind='colormap')
    # ldamodel.plot_entropy_distribution()
    # tsvdmodel.plot_entropy_distribution()
    return

if __name__ == '__main__':
    main()
