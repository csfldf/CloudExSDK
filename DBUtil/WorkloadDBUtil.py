#!/usr/bin/env python
# encoding: utf-8

import sys
from DBUtil import *

workloadTableName = 'WorkloadData'


class WorkloadDBUtil(object):
    @staticmethod
    def createWorkloadTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT UNIQUE NOT NULL,
                realWL INT,
                predictWL INT,
                realTC DOUBLE,
                predictTC DOUBLE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addRealWorkloadAndRealTotalCalculationToSpecificPeriod(periodNo, realWL, realTC):
        if not periodNo or not realWL:
            raise Exception('no periodNo or real workload')

        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET realWL = %d, realTC = %f
            WHERE periodNo = %d
        ''' % (workloadTableName, realWL, realTC, periodNo)
        dbcur = dbcon.cursor()
        afl = dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()
        if afl == 0:
            raise Exception("add real workload to period that wasn't been predicted")

    @staticmethod
    def addFirstPeriodRealWorkloadAndRealTotalCalculation(realWL, realTC):
        if not realWL:
            raise Exception('no periodNo or real workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, realWL, predictWL, realTC, predictTC)
            VALUES(%d, %d, %d, %f, %f);
        ''' % (workloadTableName, 1, realWL, -1, realTC, -1.0)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addPredictWorkloadAndPredictTotalCalculationToSpecificPeriod(periodNo, predictWL, predictTC):
        if not periodNo or not predictWL:
            raise Exception('no periodNo or predict workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, predictWL, predictTC)
            VALUES(%d, %d, %f);
        ''' % (workloadTableName, periodNo, predictWL, predictTC)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getWorkloadCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def getAllWorkloadInfo():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT realWL, predictWL
            FROM %s
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        workloadList = []
        for wk in dbcur:
            workloadList.append((wk[0], wk[1]))
        dbcur.close()
        dbcon.close()
        return workloadList

    @staticmethod
    def dropWorkloadTable():
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DROP TABLE %s
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def clearWorkloadTable():
        dbcon = getDBConwithCloudExDB()
        clearStat = '''
            DELETE FROM %s
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(clearStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getNewestWorkload():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT periodNo, realWL
            FROM %s
            WHERE periodNo = (
                SELECT MAX(periodNo)
                FROM %s
            )
        ''' % (workloadTableName, workloadTableName)
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        wl = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if wl:
            return {'periodNo':wl[0], 'realWL':wl[1]}
        else:
            return None

    @staticmethod
    def getRealWorkloadAndRealTotalCalculationInPairs(windowSize=sys.maxint):
        # result is sorted by RealWorkload, which might have effect on the result of linear regression done by np
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT realWL, realTC
            FROM %s
            ORDER BY periodNo DESC
            LIMIT %d
        ''' % (workloadTableName, int(windowSize))
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        tmp = []
        for pair in dbcur:
            tmp.append((pair[0], pair[1]))
        dbcur.close()
        dbcon.close()

        if tmp.__len__() > 0:
            tmp.sort(lambda x, y: cmp(x[0], y[0]))
            wl = []
            tc = []
            for i in tmp:
                wl.append(i[0])
                tc.append(i[1])
            return [wl, tc]
        else:
            return None
