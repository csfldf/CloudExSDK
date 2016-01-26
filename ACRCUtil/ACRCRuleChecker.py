#!/usr/bin/env python
# encoding: utf-8

import shelve
from DBUtil.PerformanceDBUtil import PerformanceDBUtil

fiboDataFile = '/home/sk/image/cloudExData/fiboData.db'
foboData = 'FIBODATA'

class ACRCRuleChecker(object):
    @staticmethod
    def getNextAddedVMs():
        PerformanceDBUtil.getNewestPerformanceData()

