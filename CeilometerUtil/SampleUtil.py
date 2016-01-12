#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil
from NormalUtil import *

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

