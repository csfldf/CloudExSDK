#!/usr/bin/env python
# encoding: utf-8

from NovaUtil.ImageUtil import ImageUtil
from NovaUtil.FlavorUtil import FlavorUtil
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from NovaUtil.InstanceUtil import InstanceUtil
from opsdkUtil.getClientUtil import GetClientUtil
from uuid import uuid1 as genUUID
import time
import sys

# TODO: all these parameters might be moved to a config file instead
instanceNamePrefix = 'sjyvm-'
flavorName = 'm1.small'
#imageName = 'svTomcat'
imageName = 'consolidationTem'
# TODO: should be replaced later
calculationCapacity = 1000.0


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
    def migrate(vmId, azName):
        if not vmId or not azName:
            return False

        nova = GetClientUtil.getNovaClient()
        targetInstance = InstanceUtil.findInstanceById(vmId)
        ips = nova.servers.ips(targetInstance.id)
        innerIP = TomcatInstanceUtil.getInnerIPFromIPInfo(ips)

        targetInstance.delete()

        oldStdout = sys.stdout
        nullFile = open('/dev/null', 'w')
        sys.stdout = nullFile

        while InstanceUtil.findInstanceById(vmId):
            time.sleep(2)

        sys.stdout = oldStdout
        nullFile.close()

        UsingInstancesDBUtil.deleteUsingInstanceByResourceId(targetInstance.id)

        newInstance = TomcatInstanceUtil.createTomcatInstance(azName, innerIP)

        if newInstance:
            while not InstanceUtil.isInstanceStatusActice(newInstance.id):
                time.sleep(2)
            return True
        else:
            return False

    @staticmethod
    def createTomcatInstance(azName='', fixedIp=''):
        nova = GetClientUtil.getNovaClient()
        targetInstanceName = instanceNamePrefix + TomcatInstanceUtil.getUUIDStr()
        targetImage = ImageUtil.findImageByName(imageName)
        targetFlavor = FlavorUtil.findFlavorByName(flavorName)
        if azName:
            if fixedIp:
                targetInstance = nova.servers.create(targetInstanceName, targetImage, targetFlavor,
                                                     availability_zone=azName,
                                                     nics=[{'net-id': netId, 'v4-fixed-ip': fixedIp}])
            else:
                targetInstance = nova.servers.create(targetInstanceName, targetImage, targetFlavor,
                                                     availability_zone=azName, nics=[{'net-id': netId}])

        else:
            if fixedIp:
                targetInstance = nova.servers.create(targetInstanceName, targetImage, targetFlavor,
                                                     nics=[{'net-id': netId, 'v4-fixed-ip': fixedIp}])
            else:
                targetInstance = nova.servers.create(targetInstanceName, targetImage, targetFlavor,
                                                     nics=[{'net-id': netId}])

        # print targetInstance.name
        ips = nova.servers.ips(targetInstance.id)
        while not ips:
            ips = nova.servers.ips(targetInstance.id)
        # print ips
        innerIP = TomcatInstanceUtil.getInnerIPFromIPInfo(ips)

        count = 0
        while True:
            try:
                targetInstance = nova.servers.get(targetInstance.id)
                realAZName = targetInstance.__dict__['OS-EXT-AZ:availability_zone']
            except KeyError:
                count += 1
                if count >= 50:
                    raise Exception('get az info failure!')
                else:
                    continue
            else:
                break

        UsingInstancesDBUtil.addUsingInstance(targetInstance.id, targetInstance.name, 1, innerIP, azName=realAZName)

        return targetInstance

    @staticmethod
    def deleteAllTestingInstance():
        nova = GetClientUtil.getNovaClient()
        instancesList = nova.servers.list()
        for instance in instancesList:
            if len(instance.name) > 20:
                instance.delete()
                UsingInstancesDBUtil.deleteUsingInstanceByResourceId(instance.id)

    @staticmethod
    def deleteSpecifyNumberInstances(no):
        if not no:
            return

        nova = GetClientUtil.getNovaClient()
        instancesList = nova.servers.list()
        count = 0
        for instance in instancesList:
            if len(instance.name) > 20:
                instance.delete()
                UsingInstancesDBUtil.deleteUsingInstanceByResourceId(instance.id)
                count += 1

            if count == no:
                break

    @staticmethod
    def deleteSpecifyNumberInstancesWithSpecifyAZ(no, azName):
        if not no:
            return

        holdVms = UsingInstancesDBUtil.getUsingInstancesByAZName(azName)
        holdVmsLen = len(holdVms)
        if no > holdVmsLen:
            raise Exception(
                'Could not down ' + str(no) + ' vms in ' + str(azName) + ', it only has ' + str(holdVmsLen) + ' vms!')

        nova = GetClientUtil.getNovaClient()

        count = 0
        for vm in holdVms:
            targetInstance = nova.servers.get(vm['id'])
            targetInstance.delete()
            UsingInstancesDBUtil.deleteUsingInstanceByResourceId(targetInstance.id)
            count += 1

            if count == no:
                break

    @staticmethod
    def createSpecifyNumberInstancesInAZ(no, azName=''):
        count = no
        while count > 0:
            TomcatInstanceUtil.createTomcatInstance(azName)
            count -= 1

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

    @staticmethod
    def getCalculationCapacityPerInstance():
        return calculationCapacity
