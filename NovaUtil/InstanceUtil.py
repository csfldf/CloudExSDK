#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil
from novaclient.exceptions import NotFound

#Instance Status
activeStatus = 'ACTIVE'
rebootStatus = 'REBOOT'

class InstanceUtil(object):
    @staticmethod
    def deleteInstaceByName(instanceName):
        nova = GetClientUtil.getNovaClient()
        tartgetInstace = InstanceUtil.findInstaceByName(instanceName)
        if tartgetInstace:
            tartgetInstace.delete()

    @staticmethod
    def findInstaceByName(instanceName):
        nova = GetClientUtil.getNovaClient()
        tartgetInstances =  nova.servers.list({'name':instanceName})
        if len(tartgetInstances) == 1:
            return tartgetInstances[0]
        else:
            return None

    @staticmethod
    def findInstanceById(instanceId):
        nova = GetClientUtil.getNovaClient()
        try:
            targetInstance = nova.servers.get(instanceId)
        except NotFound, e:
            print e
            targetInstance = None
        return targetInstance

    @staticmethod
    def rebootInstanceById(instanceId):
        targetInstance = InstanceUtil.findInstanceById(instanceId)
        if targetInstance:
            targetInstance.reboot('SOFT')

    @staticmethod
    def isInstanceStatusActice(instanceId):
        targetInstance = InstanceUtil.findInstanceById(instanceId)
        if targetInstance and targetInstance.status == activeStatus:
            return True
        else:
            return False

