#!/usr/bin/env python
# encoding: utf-8

from opsdkUtil.getClientUtil import GetClientUtil
from CeilometerUtil.SampleUtil import SampleUtil

#ceilometer = GetClientUtil.getCeilometerClient()
#query = [dict(field='resource_id', op='eq', value='9be7cd50-2c59-4851-bde6-789ec09be5b0'), dict(field='meter',op='eq',value='memory_util')]
#cul = ceilometer.new_samples.list(q=query)
#vl = []
#for sample in cul:
#    vl.append(round(sample.volume, 2))
#print vl

#query = [dict(field='resource_id', op='eq', value='9be7cd50-2c59-4851-bde6-789ec09be5b0'), dict(field='meter',op='eq',value='memory.usage')]
#ml = ceilometer.new_samples.list(q=query)
#print ml[0].metadata['flavor.ram']

cpuList = SampleUtil.getCpuUtilListByResourceId('3c366418-8a4e-440a-b474-cf4dacd5e6c3')
print len(cpuList)

