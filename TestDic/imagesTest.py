#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil


nova = GetClientUtil.getNovaClient()

imageList = nova.images.list()
for image in imageList:
#    print image.name
    print nova.images.resource_class


