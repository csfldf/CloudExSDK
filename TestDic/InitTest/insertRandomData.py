#!/usr/bin/env python
# encoding: utf-8

from DBUtil.PerformanceDBUtil import PerformanceDBUtil
from DBUtil.WorkloadDBUtil import WorkloadDBUtil


WorkloadDBUtil.addFirstPeriodRealWorkload(5000)
WorkloadDBUtil.addPredictWorkloadToSpecificPeriod(2, 300)
WorkloadDBUtil.addRealWorkloadToSpecificPeriod(3, 305)
print WorkloadDBUtil.getAllWorkloadInfo()



performanceData = {'minResponseTime':105.8, 'maxResponseTime':13.2, 'avgResponseTime':22.3, 'breakSLAPercent':0.2, 'avgCpuUtil':0.3, 'avgMemoryUtil':0.6}
PerformanceDBUtil.addPerformanceDataToSpecificPeriod(6, performanceData)

performanceData = {'minResponseTime':205.3, 'maxResponseTime':13.2, 'avgResponseTime':22.3, 'breakSLAPercent':0.2, 'avgCpuUtil':0.3, 'avgMemoryUtil':0.6}
PerformanceDBUtil.addPerformanceDataToSpecificPeriod(5, performanceData)

print PerformanceDBUtil.getPerformanceDataCount()


