import os.path as osp

import mxnet as mx
import numpy as np
from time import sleep
import models
import DataLoader
from Dataset import Dataset
import transforms


class TestDataset(Dataset):
    def __init__(self, root="../../data", transform=None, label_transform=None):
        super(TestDataset, self).__init__()

        self.root = root

        self.transform = transform
        self.label_transform = label_transform

        with open(osp.join(root, 'caltech-256-60-train.lst'), 'r') as fp:
            self.flist = [line.strip().split() for line in fp.readlines()]

    def __getitem__(self, index):
        label, id, path, = self.flist[index]
        data = self.pil_loader(osp.join(self.root, '256_ObjectCategories', path))

        if self.transform is not None:
            data = self.transform(data)
        if self.label_transform is not None:
            label = self.label_transform(label)
        return [data], [label]

    def __len__(self):
        return len(self.flist)


def mx_collate(batch):
    #  [((data1, ..., dataN), (label1, ..., labelN)),
    #   ((data1, ..., dataN), (label1, ..., labelN)),
    #    ....
    #   ((data1, ..., dataN), (label1, ..., labelN))]

    if isinstance(batch[0][0][0], mx.ndarray.NDArray):
        return batch
    raise TypeError(("batch must contain tensors, numbers, dicts or lists; found {}"
                     .format(type(batch[0]))))


if __name__ == "__main__":

    img_transform = transforms.Compose([
        transforms.Scale((512, 512)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(256),
        transforms.mx.ToNdArray()
    ])
    label_transform = transforms.Compose([
        transforms.Lambda(lambd=lambda x: mx.nd.array([x]))
    ])

    dst = TestDataset(root='../../data', transform=img_transform, label_transform=label_transform)


    def mx_collate(batch):
        return batch


    feedin_shapes = {
        'batch_size': 8,
        'data': [mx.io.DataDesc(name='data', shape=(32, 3, 128, 128), layout='NCHW')],
        'label': [mx.io.DataDesc(name='softmax_label', shape=(32,), layout='N')]
    }

    # from torchloader import DataLoader
    from DataLoader import BoxLoader

    loader = BoxLoader(dst, feedin_shapes, collate_fn=mx_collate, num_workers=1)
    import time

    net = models.alexnet(10)

    exit(0)
    start_time = time.time()
    for ind, each in enumerate(loader):
        new_start_time = time.time()
        elapsed_time = new_start_time - start_time
        start_time = new_start_time
        print ind, elapsed_time
