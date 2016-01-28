#!/usr/bin/env python
# encoding: utf-8

import shelve
from ACRCUtil import slaConfFilePath
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from DBUtil.PerformanceDBUtil import PerformanceDBUtil
from DBUtil.WorkloadDBUtil import WorkloadDBUtil
from NormalUtil import periodRecoderFile
from NormalUtil import periodRecoder
from ACRCUtil.ACRCRuleChecker import fiboDataFile
from ACRCUtil.ACRCRuleChecker import fiboDataName
from PredictUtil import clearAllData
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil

initUsingInstancesNumbers = 1

class SLAHandler(object):
    def __init__(self, confFilePath=slaConfFilePath):
        self.confFilePath = confFilePath
        confF = open(self.confFilePath)
        exec confF
        confF.close()

        self.availability = availability
        self.responseTimeDelay = responseTimeDelay
        self.cpuUpperLimit = cpuUpperLimit
        self.memoryUpperLimit = memoryUpperLimit
        self.slaBreakPercent = slaBreakPercent
        self.acrcPlacementComponent = ACRCPlacementComponent()

    def getAvailabilitySLA(self):
        return self.availability

    def getResponseTimeDelaySLA(self):
        return self.responseTimeDelay

    def getCpuUpperLimitSLA(self):
        return self.cpuUpperLimit

    def getMemoryUpperLimitSLA(self):
        return self.memoryUpperLimit

    def getSLABreakPercent(self):
        return self.slaBreakPercent

    @staticmethod
    def getInitialScheme(self):
        periodDB = shelve.open(periodRecoderFile)
        periodDB[periodRecoder] = None
        periodDB.close()

        fiboDB = shelve.open(fiboDataFile)
        fiboDB[fiboDataName] = None
        fiboDB.close()

        clearAllData()

        PerformanceDBUtil.clearPerformanceDataTable()
        WorkloadDBUtil.clearWorkloadTable()


        uiCount = UsingInstancesDBUtil.getUsingInstancesCount()

        if uiCount < initUsingInstancesNumbers:
            TomcatInstanceUtil.resetAllUsingInstances()
            self.acrcPlacementComponent.getPlacementScheme(initUsingInstancesNumbers - uiCount, True)
        elif uiCount > initUsingInstancesNumbers:
            self.acrcPlacementComponent.getPlacementScheme(uiCount - initUsingInstancesNumbers, False)
            TomcatInstanceUtil.resetAllUsingInstances()
        else:
            TomcatInstanceUtil.resetAllUsingInstances()

