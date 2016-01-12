#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil

class ImageUtil(object):
    @staticmethod
    def findImageByName(imageName):
        nova = GetClientUtil.getNovaClient()
        imageList = nova.images.list()
        for image in imageList:
            if image.name == imageName:
                return image
        return None

