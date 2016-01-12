#!/usr/bin/env python
# encoding: utf-8

from NovaUtil.ImageUtil import ImageUtil
from NovaUtil.FlavorUtil import FlavorUtil
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from NovaUtil.InstanceUtil import InstanceUtil
from opsdkUtil.getClientUtil import GetClientUtil
from uuid import uuid1 as genUUID
import time

instanceNamePrefix = 'sjyvm-'
flavorName = 'm1.small'
imageName = 'tomcatServer'


class TomcatInstanceUtil(object):
    @staticmethod
    def getInnerIPFromIPInfo(ips):
        innerIP = None
        for key in ips:
            ipInfo = ips[key][0]
            innerIP = ipInfo[u'addr']
            break
        return innerIP

    @staticmethod
    def getUUIDStr():
        uuidObj = genUUID()
        return str(uuidObj)

    @staticmethod
    def createTomcatInstance():
        nova = GetClientUtil.getNovaClient()
        targetInstanceName = instanceNamePrefix + TomcatInstanceUtil.getUUIDStr()
        targetImage = ImageUtil.findImageByName(imageName)
        targetFlavor = FlavorUtil.findFlavorByName(flavorName)
        targetInstance =  nova.servers.create(targetInstanceName, targetImage, targetFlavor)
        #print targetInstance.name
        ips = nova.servers.ips(targetInstance.id)
        while not ips:
            ips = nova.servers.ips(targetInstance.id)
        #print ips
        innerIP = TomcatInstanceUtil.getInnerIPFromIPInfo(ips)
        UsingInstancesDBUtil.addUsingInstance(targetInstance.id, targetInstance.name, 1, innerIP)
        return targetInstance

    @staticmethod
    def deleteAllTestingInstance():
        nova = GetClientUtil.getNovaClient()
        instancesList = nova.servers.list()
        for instance in instancesList:
            if len(instance.name) > 7:
                instance.delete()
                UsingInstancesDBUtil.deleteUsingInstanceByResourceId(instance.id)

    @staticmethod
    def deleteSpecifyNumberInstances(no):
        nova = GetClientUtil.getNovaClient()
        instancesList = nova.servers.list()
        count = 0
        for instance in instancesList:
            if len(instance.name) > 7:
                instance.delete()
                UsingInstancesDBUtil.deleteUsingInstanceByResourceId(instance.id)
                count += 1

            if count == no:
                break

    @staticmethod
    def resetAllUsingInstances():
        usingInstancesIds = UsingInstancesDBUtil.getAllUsingInstancesIds()
        for uiid in usingInstancesIds:
            InstanceUtil.rebootInstanceById(uiid)

    @staticmethod
    def ensureAllUsingInstancesActive():
        usingInstancesIds = UsingInstancesDBUtil.getAllUsingInstancesIds()
        while usingInstancesIds:
            for uiid in usingInstancesIds:
                if InstanceUtil.isInstanceStatusActice(uiid):
                    usingInstancesIds.remove(uiid)
            time.sleep(5)


