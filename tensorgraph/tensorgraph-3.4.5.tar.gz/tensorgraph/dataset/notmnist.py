
import glob
from ..utils import get_file_from_url
from scipy.misc import imread
import numpy as np


def NotMnist(datadir='./notmnist/'):

    url = 'http://yaroslavvb.com/upload/notMNIST/notMNIST_large.tar.gz'

    # url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    save_path = '{}/notMNIST_large.tar.gz'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=url, untar=True)
    classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    images = []
    labels = []
    for i, clss in enumerate(classes):
        print('..constructing class: ', i)
        clss_dir = '{}/notMNIST_large/{}'.format(datadir, clss)
        images = glob.glob('{}/*png'.format(clss_dir))
        # import pdb; pdb.set_trace()
        img_arr = []
        for img in images:
            try:
                arr = imread(img)
                img_arr.append(arr)
            except:
                print('{} not readable'.format(img))
        img_arr = np.concatenate(img_arr)
        images.append(img_arr)
        labels.append(np.ones(len(img_arr)) * i)
        print('len of class {}: {}'.format(i, len(img_arr)))
    images = np.concatenate(images)
    labels = np.concatenate(labels)
    import pdb; pdb.set_trace()


    print('datadir:', datadir)
    # sav_dir = datadir + '/cifar-10-batches-py'


if __name__ == '__main__':
    NotMnist(datadir='./notmnist/')
