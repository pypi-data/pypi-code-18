

from ..utils import get_file_from_url


def NotMnist(datadir='./notmnist/'):

    url = 'http://yaroslavvb.com/upload/notMNIST/notMNIST_large.tar.gz'

    # url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    save_path = '{}/notMNIST_large.tar.gz'.format(datadir)
    datadir = get_file_from_url(save_path=save_path, origin=url, untar=True)
    # sav_dir = datadir + '/cifar-10-batches-py'


if __name__ == '__main__':
    NotMnist(datadir='./notmnist/')
