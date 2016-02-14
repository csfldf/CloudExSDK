#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
from math import ceil

workloadVMMapTableName = 'WorkloadVMMap'

class WorkloadVMMapDBUtil(object):

    @staticmethod
    def getworkloadVMMapCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % workloadVMMapTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def getLevelStep():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT workloadLevel
            FROM %s
            WHERE vmNumbers = 0
        ''' % workloadVMMapTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        stepContent = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if not stepContent:
            raise Exception('can not get level step infomation!')
        return stepContent[0]

    @staticmethod
    def getTargetVMsToSpecificLevel(level):
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT vmNumbers
            FROM %s
            WHERE workloadLevel = %d
        ''' % (workloadVMMapTableName, level)
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        vmn = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if not vmn:
            raise Exception('can not get vmNumbers to level %d' % level)
        else:
            return vmn[0]

    @staticmethod
    def getTargetVMsToSpecificWorkload(workload):
        levelStep = WorkloadVMMapDBUtil.getLevelStep()
        level = ceil(workload / float(levelStep))
        return WorkloadVMMapDBUtil.getTargetVMsToSpecificLevel(level)
