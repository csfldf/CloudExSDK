#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from DBUtil.WorkloadDBUtil import WorkloadDBUtil
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from NovaUtil.InstanceUtil import InstanceUtil
from CeilometerUtil.SampleUtil import SampleUtil
from PredictUtil import *
from ACRCUtil import topoFilePath
from LoggingUtil import getLogUtil
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from copy import deepcopy


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

WorkloadDBUtil.addWorkload(1, 5000)
print WorkloadDBUtil.getWorkloadCount()
print WorkloadDBUtil.getAllWorkloadInfo()
WorkloadDBUtil.clearWorkloadTable()
print WorkloadDBUtil.getWorkloadCount()
