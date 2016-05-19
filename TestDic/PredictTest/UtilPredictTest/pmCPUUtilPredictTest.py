#!/usr/bin/env python
# encoding: utf-8

from PredictUtil import *
from PredictUtil.PMCPUPredictUtil import PMCPUPredictUtil
from PredictUtil.VMCPUPredictUtil import VMCPUPredictUtil
import shelve

clearAllData()

pvList = []

pi = PMCPUPredictUtil()
vi = VMCPUPredictUtil()
for util in [0.5, 0.8, 0.7, 0.6, 0.7, 0.7, 0.5]:
    addPMCPUUtilToPeriodicWindow('111', util)
    pv = pi.getNextPeriodWorkload('111')

    #pdDB = shelve.open(utilHistoryDataFile)
    #print 'historyData:',
    #print pdDB[pmCPUUtilHistoryData]
    #pdDB.close()

    #pdDB = shelve.open(utilPredictDataFile)
    #print 'predictData:',
    #print pdDB[pmCPUUtilPredictData]
    #pdDB.close()


    #print pv
    addPredictPMCPUUtilToPeriodicWindow('111', pv)

    #addVMCPUUtilToPeriodicWindow('192.168.9.44', util)



    #pdDB = shelve.open(utilHistoryDataFile)
    #print 'historyData:',
    #print pdDB[vmCPUUtilHistoryData]
    #pdDB.close()

    #pv = vi.getNextPeriodWorkload('192.168.9.44')
    #addPredictVMCPUUtilToPeriodicWindow('192.168.9.44', pv)
    pvList.append(pv)

pvList.pop()
print pvList
print [0.8, 0.7, 0.6, 0.7, 0.7, 0.5]



