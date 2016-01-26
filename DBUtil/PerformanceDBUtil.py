#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

performanceDataTableName = 'PerformanceData'

import MySQLdb

class PerformanceDBUtil(object):
    @staticmethod
    def createPerformanceDataTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE IF NOT EXISTS %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT UNIQUE NOT NULL,
                minResponseTime DOUBLE NOT NULL,
                maxResponseTime DOUBLE NOT NULL,
                avgResponseTime DOUBLE NOT NULL,
                breakSLAPercent DOUBLE NOT NULL,
                avgCpuUtil DOUBLE NOT NULL,
                avgMemoryUtil DOUBLE NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % performanceDataTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addPerformanceDataToSpecificPeriod(periodNo, performanceData):
        if not periodNo or not performanceData:
            raise Exception('no periodNo or real performanceData')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, minResponseTime, maxResponseTime, avgResponseTime, avgCpuUtil, avgMemoryUtil, breakSLAPercent)
            VALUES(%d, %f, %f, %f, %f, %f, %f);
        ''' % (performanceDataTableName, periodNo, performanceData['minResponseTime'], performanceData['maxResponseTime'], performanceData['avgResponseTime'], performanceData['avgCpuUtil'], performanceData['avgMemoryUtil'], performanceData['breakSLAPercent'])
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()


    @staticmethod
    def getPerformanceDataCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % performanceDataTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def dropPerformanceDataTable():
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DROP TABLE %s
        ''' % performanceDataTableName
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def clearPerformanceDataTable():
        dbcon = getDBConwithCloudExDB()
        clearStat = '''
            DELETE FROM %s
        ''' % performanceDataTableName
        dbcur = dbcon.cursor()
        dbcur.execute(clearStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getNewestPerformanceData():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT periodNo, minResponseTime, maxResponseTime, avgResponseTime, breakSLAPercent, avgCpuUtil, avgMemoryUtil
            FROM %s
            WHERE periodNo = (
                SELECT MAX(periodNo)
                FROM %s
            )
        ''' % (performanceDataTableName, performanceDataTableName)
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        pd = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if pd:
            return {'periodNo':pd[0], 'minResponseTime':pd[1], 'maxResponseTime':pd[2], 'avgResponseTime':pd[3], 'breakSLAPercent':pd[4], 'avgCpuUtil':pd[5], 'avgMemoryUtil':pd[6]}
        else:
            return None
