#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.PlacementComponent import PlacementComponent
from ACRCUtil import topoFilePath
from ACRCUtil import analyseJsonFormatConfigFile
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from operator import attrgetter
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from LoggingUtil import getLogUtil
from ACRCUtil.SLAHandler import SLAHandler
import logging

#不传参数默认日志级别是info
logger = getLogUtil('ACRCPlacementComponent', logging.DEBUG)

class ACRCPlacementComponent(PlacementComponent):
    def __init__(self, topoFile=topoFilePath, slaHandler=SLAHandler()):
        self.topoFilePath = topoFilePath
        self.slaHandler = slaHandler
        self.updateCloudInfo(topoFilePath)

    def calculateSubTreeInvalidProbability(self, treeNode):
        if not treeNode.children:
            return 1 - treeNode.availability
        else:
            subTreesInvalidProbability = []

            for subTree in treeNode.children:
                subTreesInvalidProbability.append(self.calculateSubTreeInvalidProbability(subTree))

            allSubTreesInvalidProbability = 1.0

            for sip in subTreesInvalidProbability:
                allSubTreesInvalidProbability *= sip

            return (1 - treeNode.availability) + treeNode.availability * allSubTreesInvalidProbability


    def calculateAvailability(self):
        if not self.cloudRoot:
            raise Exception('no topo tree')

        return 1 - self.calculateSubTreeInvalidProbability(self.cloudRoot)

    #在已经有vm的AZ里scaleUp, 不影响可用性
    def scaleUpInAZWithVMs(self, amount):
        createdCount = 0
        for az in self.azList:
            if az.holdVMs and len(az.holdVMs) < az.maxVMCount:
                vmsLaunchCount = min(az.maxVMCount - len(az.holdVMs), amount)
                TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(vmsLaunchCount, az.name)
                self.updateCloudInfo(self.topoFilePath)
                amount -= vmsLaunchCount
                createdCount += vmsLaunchCount

                if amount == 0:
                    break
        return createdCount

    #在还没有vm的AZ里scaleup, 提高可用性
    def scaleUpInAZWithoutVMs(self, amount, comd):
        createdCount = 0
        for az in self.azList:
            if not az.holdVMs and az.distance >= comd:
                vmsLaunchCount = min(az.maxVMCount, amount)
                TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(vmsLaunchCount, az.name)
                self.updateCloudInfo(self.topoFilePath)
                amount -= vmsLaunchCount
                createdCount += vmsLaunchCount
                if amount == 0:
                    break
        return createdCount


    def scaleDownInAZWithVMs(self, amount):
        totalDownCount = 0
        for az in self.azList:
            if az.holdVMs:
                #留一台不能全部关，所以-1
                vmsDownCount = min(len(az.holdVMs) - 1, amount)

                #本az只剩下一台机器了，在本函数中不能继续往下减，由后面的工作完成
                if vmsDownCount == 0:
                    continue

                #有几次出错，调试用
                logger.debug('scaleDownInAZWithVMs: downNumber:' + str(vmsDownCount) + ' az:'  + az.name + ' len az.holdVMs:' + str(len(az.holdVMs)) +  ' amount:' + str(amount))

                TomcatInstanceUtil.deleteSpecifyNumberInstancesWithSpecifyAZ(vmsDownCount, az.name)
                self.updateCloudInfo(self.topoFilePath)
                amount -= vmsDownCount
                totalDownCount += vmsDownCount

                if amount == 0:
                    break
        return totalDownCount

    #由于现在az里只有一个虚拟机了，这个函数看把这个az里的最后一个虚拟机拿掉可用性是否能满足要求
    def canScaleDownOnlyVMInAZOrNot(self, az):
        az.regionTreeNode.children.remove(az.azTreeNode)
        if not az.regionTreeNode.children:
            az.regionTreeNode.availability = 0
        avNow = self.calculateAvailability()
        if avNow >= self.slaHandler.getAvailabilitySLA():
            return True
        else:
            return False

    #由于执行了self.updateCloudInfo以后树和azList已经重新构建了，所以原来的azList没用了，只能用名字从最新的azList里找到最新的对应az
    def findNewAZWithAZName(self, azName):
        for az in self.azList:
            if az.name == azName:
                return az

        return None

    def scaleDownMakesAZEmpty(self, amount):
        totalDownCount = 0
        #按distance由大到小排列，从通讯开销最大的开始尝试，直到可用性不满足要求，或者需要scale down的数目已经满足
        reversedAzList = sorted(self.azList, key=attrgetter('distance'), reverse=True)

        azNameList = []
        for az in reversedAzList:
            azNameList.append(az.name)

        for azn in azNameList:
            az = self.findNewAZWithAZName(azn)
            if az.holdVMs:
                # No matter the result is true or false, the structure of the TopoTree has been changed after
                # this function call, so following updateCloudInfo() should be invoked anyway.
                if self.canScaleDownOnlyVMInAZOrNot(az):
                    logger.debug('scale down the only vm in ' + az.name)
                    TomcatInstanceUtil.deleteSpecifyNumberInstancesWithSpecifyAZ(1, az.name)
                    amount -= 1
                    totalDownCount += 1

                self.updateCloudInfo(self.topoFilePath)

                if amount == 0:
                    break

        return totalDownCount

    def getPlacementScheme(self, amount, isUp):
        avNow = self.calculateAvailability()

        #在本算法中，该变量只在可用性不足且scale up时使用，为了快速收敛
        communicationDegree = 0

        vmsShouldBeScaled = amount
        while amount > 0:
            #scale up
            if isUp:
                logger.info('scale up ' + str(vmsShouldBeScaled) + ' vms')

                #一会写SLAHandler替换self.slaHandler.getAvailabilitySLA()
                #可用性够
                if avNow >= self.slaHandler.getAvailabilitySLA():
                    logger.debug('availability now is ' + str(avNow) + ' , meeting availability sla ' + str(self.slaHandler.getAvailabilitySLA()))

                    createdCount = self.scaleUpInAZWithVMs(amount)
                    logger.debug('scale up ' + str(createdCount) + ' vms in az with vms!')

                    amount -= createdCount
                    if amount > 0:
                        #若在已有虚拟机的az里，已经无法启动amount台虚拟机了
                        #此时，在没有az里启动剩余的虚拟机
                        #交互度（communicationDegree)参数设为0
                        #因为此时可用性已经满足，所以只要启足够的虚拟机就行
                        #了，所以不考虑交互度，同时self.az是按distance由小
                        #到大排的，因此最先肯定也是考虑distance小的开始
                        createdCount = self.scaleUpInAZWithoutVMs(amount, 0)
                        logger.debug('scale up ' + str(createdCount) + ' vms in az without vms!')
                        amount -= createdCount

                        if amount > 0:
                            raise Exception('could not launch ' + str(vmsShouldBeScaled) + ' vms, left ' + str(amount) + ' not to be launched!')
                    return True
                #可用性不够, 一台一台加，尽量加在近的地方communicationDegree小，communicationDegree越大，对可用性的增加越高，communicationDegree自增是为了快速收敛
                else:
                    logger.debug('availability now is ' + str(avNow) + ' , not meeting availability sla ' + str(self.slaHandler.getAvailabilitySLA()))

                    createdCount = self.scaleUpInAZWithoutVMs(1, communicationDegree)
                    if not createdCount:
                        raise Exception('Could not launch vms in AZ without vms, so could not meet availability SLA!')
                    communicationDegree += 1
                    amount -= 1
            #scale down
            else:
                logger.info('scale down ' + str(vmsShouldBeScaled) + ' vms')

                downCount = self.scaleDownInAZWithVMs(amount)
                amount -= downCount

                if amount > 0:
                    logger.debug('now all az with vms only have one vm!')

                    downCount = self.scaleDownMakesAZEmpty(amount)
                    amount -= downCount

                    if amount > 0:
                        logger.warning('Could not scale down ' + str(vmsShouldBeScaled) + ' vms because of availability sla! we only scale down ' + str(vmsShouldBeScaled - amount) + ' vms!')
                        return True
            avNow = self.calculateAvailability()

        logger.info('scale successfully, the availability now is ' + str(self.calculateAvailability()))

    def updateCloudInfo(self, topoFilePath):
        if not topoFilePath:
            raise Exception('no topoFile')

        topoDic = analyseJsonFormatConfigFile(topoFilePath)

        assert topoDic, 'no cloud topo infomation'

        #获取Region和AZ的availability

        nodeAvailabilityFilePath = '/home/sk/openstackPythonSDKTest/ConfigDic/NodeAvailability'
        naf = open(nodeAvailabilityFilePath)
        exec naf
        naf.close()

        cloudRoot = TopoTreeNode('cloudRoot', TopoTreeNodeAvailability)
        azList = []
        for regionName in topoDic:
            regionTreeNode = TopoTreeNode(regionName, RegionAvailability)
            cloudRoot.children.append(regionTreeNode)
            regionAZs = topoDic[regionName]


            for az in regionAZs:
                vmsInAz = UsingInstancesDBUtil.getUsingInstancesByAZName(az['azName'])

                if vmsInAz:
                    azTreeNode = TopoTreeNode(az['azName'], AZAvailability)
                    regionTreeNode.children.append(azTreeNode)
                    newAZ = AvailabilityZone(az['azName'], az['distance'], regionName, azTreeNode, regionTreeNode)
                    newAZ.holdVMs = vmsInAz
                else:
                    newAZ = AvailabilityZone(az['azName'], az['distance'], regionName)

                azList.append(newAZ)

            #如果region下面的az都没有vm，则说明本application还没有部署到本region下的az里，本region对于本application的可用性为0
            if not regionTreeNode.children:
                regionTreeNode.availability = 0

        self.cloudRoot = cloudRoot
        self.azList = sorted(azList, key=attrgetter('distance'))

class AvailabilityZone(object):
    def __init__(self, name, distance, region, azTreeNode=None, regionTreeNode=None, maxVMCount=6):
        self.name = name
        self.distance = distance
        #用默认参数会导致所有实例共享一个列表
        self.holdVMs = []
        self.region = region
        self.azTreeNode = azTreeNode
        self.regionTreeNode = regionTreeNode
        self.maxVMCount = maxVMCount


class TopoTreeNode(object):
    def __init__(self, name, availability):
        self.name = name
        self.availability = availability
        self.children = []



