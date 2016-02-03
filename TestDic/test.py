#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from DBUtil.WorkloadVMMapDBUtil import WorkloadVMMapDBUtil
from DBUtil.WorkloadDBUtil import WorkloadDBUtil
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from NovaUtil.InstanceUtil import InstanceUtil
from CeilometerUtil.SampleUtil import SampleUtil
from PredictUtil import *
from ACRCUtil import topoFilePath
from LoggingUtil import getLogUtil
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from copy import deepcopy
from NormalUtil import *
from DBUtil.PerformanceDBUtil import PerformanceDBUtil
from ACRCUtil.SLAHandler import SLAHandler

#dropCloudExDB()
#createCloudExDB()
#UsingInstancesDBUtil.createUsingInstancesTable()
#TomcatInstanceUtil.deleteAllTestingInstance()
#c = UsingInstancesDBUtil.getUsingInstancesCount()
#print c

#UsingInstancesDBUtil.getAllUsingInstancesInfo()
#InstanceUtil.findInstanceById('c9b4d1d0-00df-4b7e-b6bc-08aae56ef818')
#InstanceUtil.findInstanceById('1')
#a = SampleUtil.getCpuUtilListByResourceId('c9b4d1d0-00df-4b7e-b6bc-08aae56ef818')
#print a

#TomcatInstanceUtil.resetAllUsingInstances()

#l = UsingInstancesDBUtil.getAllUsingInstancesIds()
#print l

#a = 24 * 9 + 1
#for i in range(1, a + 1):
#    addPredictWorkload(i)

#clearPredictData()

#ppd = getPeriodicPD()
#dpd = getDailyPD()
#spd = getStatPD()

#print ppd
#print ''
#print dpd
#print ''
#print spd

#clearHistoryData()
#dhd = getDailyHD()
#phd = getPeriodicHD()
#print len(dhd)
#print len(phd)

#clearAllData()

#instance = InstanceUtil.findInstaceByName('sjywin')
#print instance.__dict__['OS-EXT-AZ:availability_zone']

#TomcatInstanceUtil.createTomcatInstance('az4')


#WorkloadDBUtil.createWorkloadTable()

#WorkloadDBUtil.addFirstPeriodRealWorkload(5000)
#print WorkloadDBUtil.getAllWorkloadInfo()

#WorkloadDBUtil.addPredictWorkloadToSpecificPeriod(2, 300)
#WorkloadDBUtil.addRealWorkloadToSpecificPeriod(3, 305)
#print WorkloadDBUtil.getAllWorkloadInfo()

#print WorkloadDBUtil.getNewstWorkload()

#print WorkloadDBUtil.getAllWorkloadInfo()

#WorkloadDBUtil.clearWorkloadTable()
#print WorkloadDBUtil.getAllWorkloadInfo()

#print WorkloadDBUtil.getNewstWorkload()
#WorkloadDBUtil.dropWorkloadTable()


#PerformanceDBUtil.dropPerformanceDataTable()
PerformanceDBUtil.createPerformanceDataTable()


performanceData = {'minResponseTime':105.8, 'maxResponseTime':13.2, 'avgResponseTime':22.3, 'breakSLAPercent':0.2, 'avgCpuUtil':0.3, 'avgMemoryUtil':0.6, 'availability':0.88, 'vmNumbers':3}
PerformanceDBUtil.addPerformanceDataToSpecificPeriod(6, performanceData)

performanceData = {'minResponseTime':205.3, 'maxResponseTime':13.2, 'avgResponseTime':22.3, 'breakSLAPercent':0.2, 'avgCpuUtil':0.3, 'avgMemoryUtil':0.6, 'availability':0.88, 'vmNumbers':5}
PerformanceDBUtil.addPerformanceDataToSpecificPeriod(5, performanceData)

print PerformanceDBUtil.getPerformanceDataCount()

print PerformanceDBUtil.getNewestPerformanceData()

PerformanceDBUtil.clearPerformanceDataTable()

print PerformanceDBUtil.getPerformanceDataCount()


#print SampleUtil.getAllUsingInstancesPeriodAVGMemoryUtil()
#print SampleUtil.getAllUsingInstancesPeriodAVGCpuUtil()

#print WorkloadVMMapDBUtil.getLevelStep()
#print WorkloadVMMapDBUtil.getTargetVMsToSpecificLevel(200)
#print WorkloadVMMapDBUtil.getworkloadVMMapCount()

#TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(1, 'az1')
#TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(1, 'az2')
#TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(1, 'az3')
#TomcatInstanceUtil.createSpecifyNumberInstancesInAZ(1, 'az4')
