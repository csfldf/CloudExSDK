#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil import slaConfFilePath
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent

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
        self.acrcPlacementComponent = ACRCPlacementComponent()
        self.slaBreakPercent = slaBreakPercent

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

    def getInitialScheme(self):
        pass
