#!/usr/bin/env python
# encoding: utf-8
import urllib2

from opsdkUtil.getClientUtil import GetClientUtil
from NormalUtil import *
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil

class SampleUtil(object):
    @staticmethod
    def getCpuUtilListByResourceId(resourceId):
        ceilometer = GetClientUtil.getCeilometerClient()
        query = [dict(field='resource_id', op='eq', value=resourceId), dict(field='meter',op='eq',value='cpu_util')]
        sampleList = ceilometer.new_samples.list(q=query)
        retValueList = []
        for sample in sampleList:
            retValueList.append(round(sample.volume, 2))
        return retValueList

    @staticmethod
    def getMemoryUtilListByResourceId(resourceId):
        ceilometer = GetClientUtil.getCeilometerClient()
        query = [dict(field='resource_id', op='eq', value=resourceId), dict(field='meter',op='eq',value='memory.usage')]
        memoryUsageSampleList = ceilometer.new_samples.list(q=query)
        retValueList = []
        for muSample in memoryUsageSampleList:
            memoryAmount = muSample.metadata['flavor.ram']
            memoryUtil = muSample.volume / float(memoryAmount) * 100
            retValueList.append(round(memoryUtil, 2))
        return retValueList

    @staticmethod
    def getThreadInfoByResourceId(resourceId, jumper_server):
        innerIP = UsingInstancesDBUtil.getInnerIPByResourceId(resourceId)
        url = jumper_server + "/getSpecificThreadInfo?ip=" + str(innerIP)
        req = urllib2.Request(url)
        # TODO: retry mechanism might be added later
        infos = eval(urllib2.urlopen(req).read())
        # here simplify the model since our instance must has single cpu
        freq = infos[0][2]  # format => [[thread, freqStandard, freqReal]...]
        util = SampleUtil.getCpuUtilPeriodAVGByResourceId(resourceId)
        return {"cal": 1.0 * freq * util, "util": util}

    @staticmethod
    def getMemoryUtilPeriodAVGByResourceId(resourceId):
        memUtilList = SampleUtil.getMemoryUtilListByResourceId(resourceId)
        if memUtilList:
            return avgNumberList(memUtilList)
        else:
            return None

    @staticmethod
    def getCpuUtilPeriodAVGByResourceId(resourceId):
        cpuUtilList = SampleUtil.getCpuUtilListByResourceId(resourceId)
        if cpuUtilList:
            return avgNumberList(cpuUtilList)
        else:
            return None

    @staticmethod
    def getAllUsingInstancesPeriodAVGCpuUtil():
        allUiIds = UsingInstancesDBUtil.getAllUsingInstancesIds()

        uiAvgCpuList = []

        for uiId in allUiIds:
            uiAvgCpuList.append(SampleUtil.getCpuUtilPeriodAVGByResourceId(uiId))

        if uiAvgCpuList:
            return avgNumberList(uiAvgCpuList)
        else:
            return None

    @staticmethod
    def getAllUsingInstancesPeriodAVGMemoryUtil():
        allUiIds = UsingInstancesDBUtil.getAllUsingInstancesIds()

        uiAvgMemoryList = []

        for uiId in allUiIds:
            uiAvgMemoryList.append(SampleUtil.getMemoryUtilPeriodAVGByResourceId(uiId))

        if uiAvgMemoryList:
            return avgNumberList(uiAvgMemoryList)
        else:
            return None

    @staticmethod
    def getThreadInfosOverAllUsingInstances(jump_server):
        allUiIds = UsingInstancesDBUtil.getAllUsingInstancesIds()

        uiAvgCPUList = []
        totalCalculation = 0.0

        for uiId in allUiIds:
            tmp = SampleUtil.getThreadInfoByResourceId(uiId, jump_server)
            uiAvgCPUList.append(tmp["util"])
            totalCalculation += tmp["cal"]

        if uiAvgCPUList:
            return avgNumberList(uiAvgCPUList), totalCalculation
        else:
            return None