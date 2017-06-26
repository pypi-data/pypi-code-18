
import numpy as np
from tensorgraph.utils import make_one_hot
import struct
import numpy
import gzip

import tarfile, inspect, os, sys
from six.moves.urllib.request import urlretrieve
from ..progbar import ProgressBar
from ..utils import get_file_from_url
from .preprocess import global_contrast_normalize, zca_whiten


def ImageNet(flatten=False, onehot=True, contrast_normalize=False, whiten=False, datadir='./imagenet/'):

    train_url = 'http://www.image-net.org/challenges/LSVRC/2011/download/non-pub/ILSVRC2011_images_train.tar'
    save_path = '{}/ILSVRC2011_images_train.tar'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=train_url, untar=True)

    valid_url = 'http://www.image-net.org/challenges/LSVRC/2011/download/non-pub/ILSVRC2011_images_val.tar'
    save_path = '{}/ILSVRC2011_images_val.tar'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=valid_url, untar=True)

    test_url = 'http://www.image-net.org/challenges/LSVRC/2011/download/non-pub/ILSVRC2011_images_test.tar'
    save_path = '{}/ILSVRC2011_images_test.tar'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=test_url, untar=True)

    train_bbox_url = 'http://www.image-net.org/challenges/LSVRC/2011/download/non-pub/ILSVRC2011_bbox_train.v2.tar'
    save_path = '{}/ILSVRC2011_bbox_train.v2.tar'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=train_bbox_url, untar=True)

    valid_bbox_url = 'http://www.image-net.org/challenges/LSVRC/2011/download/non-pub/ILSVRC2011_bbox_val.v3.tar'
    save_path = '{}/ILSVRC2011_bbox_val.v3.tar'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=valid_bbox_url, untar=True)


    def make_data(batchnames):
        X = []
        y = []
        for data_batch in batchnames:
            fp = sav_dir + '/' + data_batch
            with open(fp, 'rb') as fin:
                # python2
                if sys.version_info.major == 2:
                    import cPickle
                    tbl = cPickle.load(fin)
                # python 3
                elif sys.version_info.major == 3:
                    import pickle
                    tbl = pickle.load(fin, encoding='bytes')

                else:
                    raise Exception('python version not 2 or 3')
                X.append(tbl[b'data'])
                y.append(tbl[b'labels'])
        X = np.concatenate(X, axis=0).astype('f4')
        y = np.concatenate(y, axis=0).astype('int')
        X /= 255.0
        return X, y

    X_train, y_train = make_data(['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5'])
    X_test , y_test = make_data(['test_batch'])


    if contrast_normalize:
        norm_scale = 55.0  # Goodfellow
        X_train = global_contrast_normalize(X_train, scale=norm_scale)
        X_test = global_contrast_normalize(X_test, scale=norm_scale)


    if whiten:
        zca_cache = os.path.join(datadir, 'cifar-10-zca-cache.pkl')
        X_train, X_test = zca_whiten(X_train, X_test, cache=zca_cache)


    if onehot:
        y_train = make_one_hot(y_train, 10)
        y_test = make_one_hot(y_test, 10)

    if not flatten:
        X_train = X_train.reshape((-1, 3, 32, 32)).swapaxes(1, 3)
        X_test = X_test.reshape((-1, 3, 32, 32)).swapaxes(1, 3)

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    X_train, y_train, X_test, y_test = ImageNet(flatten=False, onehot=False)
    from scipy.misc import imshow, imsave
    imsave('img.png', X_train[0])
    print('X_train:', X_train.shape)
    print('y_train:', y_train.shape)
    print('X_test:', X_test.shape)
    print('y_test:', y_test.shape)
