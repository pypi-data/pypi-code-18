import tensorflow as tf
import numpy as np
from scipy.misc import imread, imresize
from imagenet_classes import class_names
import vgg16
from vgg16 import *


def get_embedding_x(img):
    '''
            Args    : Numpy Image Vector
            Returns : Embedded feature vector of length 4096
    '''
    sess = tf.Session()
    imgs = tf.placeholder(tf.float32, [None, 224, 224, 3])
    vgg = vgg16(imgs, 'vgg16_weights.npz', sess)
    img = imresize(img, (224, 224))
    img = np.array(img)
    emb = sess.run(vgg.emb, feed_dict={vgg.imgs: [img]})
    return emb


def get_embedding_X(img):
    '''
            Args 	: Numpy Images vector
            Returns : Embedded Matrix of length Samples, 4096
    '''
    sess = tf.Session()
    imgs = tf.placeholder(tf.float32, [None, 224, 224, 3])
    vgg = vgg16(imgs, 'vgg16_weights.npz', sess)

    img = [imresize(img_x, (224, 224)) for img_x in img]
    img = np.array(img)
    emb = sess.run(vgg.emb, feed_dict={vgg.imgs: img})
    return emb


img1 = imread('laska.png', mode='RGB')
print get_embedding_x(img1).shape

imgs = [img1, img1, img1]
print get_embedding_X(imgs).shape
