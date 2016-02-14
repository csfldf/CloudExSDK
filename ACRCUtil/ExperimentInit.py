#!/usr/bin/env python
# encoding: utf-8

import shelve
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

initUsingInstancesNumbers = 3


class ExperimentInit(object):
    def __init__(self):
        self.acrcPlacementComponent = ACRCPlacementComponent()

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
