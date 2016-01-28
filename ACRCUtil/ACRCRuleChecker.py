#!/usr/bin/env python
# encoding: utf-8

import shelve
from DBUtil.PerformanceDBUtil import PerformanceDBUtil
#from ACRCUtil.SLAHandler import SLAHandler
from LoggingUtil import getLogUtil

fiboDataFile = '/home/sk/image/cloudExData/fiboData.db'
fiboDataName = 'FIBODATA'

# 不传参数默认日志级别是info
logger = getLogUtil('ACRCRuleChecker')


class ACRCRuleChecker(object):
    def __init__(self, slaHandler=None):
        if not slaHandler:
            from ACRCUtil.SLAHandler import SLAHandler
            self.slaHandler = SLAHandler()
        else:
            self.slaHandler = slaHandler

    # 是否违反了时延违反百分比
    def isBreakRTPercentSLA(self, rtPercent):
        if rtPercent > self.slaHandler.getSLABreakPercent():
            return True
        else:
            return False

    def isBreakCpuUpperLimitSLA(self, cpuUtil):
        if cpuUtil > self.slaHandler.getCpuUpperLimitSLA():
            return True
        else:
            return False

    def isBreakMemoryUpperLimitSLA(self, memoryUtil):
        if memoryUtil > self.slaHandler.getMemoryUpperLimitSLA():
            return True
        else:
            return False

    def getNextAddedVMs(self):
        newestPD = PerformanceDBUtil.getNewestPerformanceData()

        rtPercent = newestPD['breakSLAPercent']
        cpuUtil = newestPD['avgCpuUtil']
        memoryUtil = newestPD['avgMemoryUtil']
        periodNo = newestPD['periodNo']

        if not rtPercent or not cpuUtil or not memoryUtil or not periodNo:
            raise Exception('Can not get Performance Data correctly')

        fiboDB = shelve.open(fiboDataFile)
        fiboData = fiboDB.get(fiboDataName, None)

        if not fiboData:
            fiboData = [0, 1]

        breakFlag = False
        if self.isBreakRTPercentSLA(rtPercent):
            breakFlag = True
            logger.info('period ' + str(periodNo) + ': rtBreakPercent is ' + str(rtPercent * 100) + ', Break SLA ' + str(self.slaHandler.getSLABreakPercent) + '!')
        if self.isBreakCpuUpperLimitSLA(cpuUtil):
            breakFlag = True
            logger.info('period ' + str(periodNo) + ': avgCpuUtil is ' + str(cpuUtil * 100) + ', Break SLA ' + str(self.slaHandler.getCpuUpperLimitSLA) + '!')
        if self.isBreakMemoryUpperLimitSLA(memoryUtil):
            breakFlag = True
            logger.info('period ' + str(periodNo) + ': avgMemoryUtil is ' + str(memoryUtil * 100) + ', Break SLA ' + str(self.slaHandler.getMemoryUpperLimitSLA) + '!')

        if breakFlag:
            newTarget = fiboData[0] + fiboData[1]
            fiboData.pop(0)
            newTarget.append(newTarget)
        else:
            if fiboData[0] != 0:
                newTarget = fiboData[1] - fiboData[0]
                fiboData = [newTarget, fiboData[0]]

        fiboDB[fiboDataName] = fiboData
        return fiboData[0]
