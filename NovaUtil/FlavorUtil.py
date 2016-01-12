#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil

class FlavorUtil(object):
    @staticmethod
    def deleteFlavorByName(flavorName):
        flavor = FlavorUtil.findFlavorByName(flavorName)
        if flavor:
            flavor.delete()

    @staticmethod
    def findFlavorByName(flavorName):
        nova = GetClientUtil.getNovaClient()
        flavorList = nova.flavors.list()
        for flavor in flavorList:
            if flavor.name == flavorName:
                return flavor
        return None
