# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .sub_resource import SubResource


class ImageReference(SubResource):
    """The image reference.

    :param id: Resource Id
    :type id: str
    :param publisher: The image publisher.
    :type publisher: str
    :param offer: The image offer.
    :type offer: str
    :param sku: The image SKU.
    :type sku: str
    :param version: The image version. The allowed formats are
     Major.Minor.Build or 'latest'. Major, Minor and Build are decimal numbers.
     Specify 'latest' to use the latest version of the image.
    :type version: str
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'publisher': {'key': 'publisher', 'type': 'str'},
        'offer': {'key': 'offer', 'type': 'str'},
        'sku': {'key': 'sku', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
    }

    def __init__(self, id=None, publisher=None, offer=None, sku=None, version=None):
        super(ImageReference, self).__init__(id=id)
        self.publisher = publisher
        self.offer = offer
        self.sku = sku
        self.version = version
