#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil

a = ACRCPlacementComponent()


countList = range(20)

for i in countList:
    a.getPlacementScheme(1, True)
    uic = UsingInstancesDBUtil.getUsingInstancesCount()
    print 'vm numbers:' + str(uic) + ' av:' + str(a.calculateAvailability())

for i in countList:
    a.getPlacementScheme(1, False)
    uic = UsingInstancesDBUtil.getUsingInstancesCount()
    print 'vm numbers:' + str(uic) + ' av:' + str(a.calculateAvailability())

