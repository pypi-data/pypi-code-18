# -*- coding: utf-8 -*-

import re
import sys
from .base import AipBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote
from .base import Image
from .base import StringIO

class AipOcr(AipBase):
    """
        Aip OCR
    """

    __idcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/idcard'
    
    __bankcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard'
    
    __generalUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general'

    __basicGeneralUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

    __webImageUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage'

    __enhancedGeneralUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_enhanced'

    __drivingLicenseUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/driving_license'

    __vehicleLicenseUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_license'
    
    def idcard(self, image, isFront, options=None):
        """
            idcard ocr
        """

        options = options or {}
        data = {}
        data['image'] = image
        data['id_card_side'] = isFront and 'front' or 'back'

        data = dict(data, **options)

        return self._request(self.__idcardUrl, data)

    def bankcard(self, image):
        """
            bankcard ocr
        """
        
        data = {}
        data['image'] = image

        return self._request(self.__bankcardUrl, data)

    def general(self, image, options=None):
        """
            general ocr
        """

        options = options or {}
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__generalUrl, data)

    def basicGeneral(self, image, options=None):
        """
            basic general ocr
        """

        options = options or {}
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__basicGeneralUrl, data)

    def webImage(self, image, options=None):
        """
            web image ocr
        """

        options = options or {}
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__webImageUrl, data)

    def enhancedGeneral(self, image, options=None):
        """
            enhanced general ocr
        """

        options = options or {}
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__enhancedGeneralUrl, data)

    def vehicleLicense(self, image, options=None):
        """
            vehicleLicense
        """

        options = options or {}
        
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__vehicleLicenseUrl, data)

    def drivingLicense(self, image, options=None):
        """
            drivingLicense
        """

        options = options or {}
        
        data = {}
        data['image'] = image

        data = dict(data, **options)

        return self._request(self.__drivingLicenseUrl, data)

    def _validate(self, url, data):
        """
            validate
        """

        img = Image.open(StringIO(data['image']))

        format = img.format.upper()
        width, height = img.size

        # 图片格式检查
        if format not in ['JPEG', 'BMP', 'PNG']:
            return {
                'error_code': 'SDK109',
                'error_msg': 'unsupported image format',
            }

        # 图片大小检查
        if width < 15 or width > 4096 or height < 15 or height > 4096:
            return {
                'error_code': 'SDK101',
                'error_msg': 'image length error',
            }

        data['image'] = base64.b64encode(data['image'])

        # 编码后小于4m
        if len(data['image']) >= 4 * 1024 * 1024:
            return {
                'error_code': 'SDK100',
                'error_msg': 'image size error',
            }

        return True

