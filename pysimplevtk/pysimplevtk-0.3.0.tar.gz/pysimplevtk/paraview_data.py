# -*- coding: utf-8 -*-
from xml.etree.ElementTree import ElementTree, Element, SubElement


class _DataSet(object):

    def __init__(self, file, timestep=0, group='', part=0):
        self.file = file
        self.timestep = timestep
        self.group = group
        self.part = part


class ParaViewData(object):

    def __init__(self):
        self.type = 'Collection'
        self.version = '0.1'
        self.byte_order = 'LittleEndian'
        self.compressor = 'vtkZLibDataCompressor'

        self.datasets = []

    def add_dataset(self, file, timestep=0, group='', part=0):
        self.datasets.append(
            _DataSet(
                file=file,
                timestep=timestep,
                group=group,
                part=part))

    def dump(self, file_or_filename):
        root = Element(
            'VTKFile',
            attrib={
                'type': self.type,
                'version': self.version,
                'byte_order': self.byte_order,
                'compressor': self.compressor
            })
        collection = SubElement(
            root,
            'Collection')
        for dataset in self.datasets:
            SubElement(
                collection,
                'DataSet',
                attrib={
                    'file': str(dataset.file),
                    'timestep': str(dataset.timestep),
                    'group': str(dataset.group),
                    'part': str(dataset.part)
                })

        tree = ElementTree(root)
        tree.write(file_or_filename)
