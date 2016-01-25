#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

workloadTableName = 'WorkloadData'

import MySQLdb

class WorkloadDBUtil(object):
    @staticmethod
    def createWorkloadTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT UNIQUE NOT NULL,
                realWL INT,
                predictWL INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addRealWorkloadToSpecificPeriod(periodNo, realWL):
        if not periodNo or not realWL:
            raise Exception('no periodNo or real workload')

        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET realWL = %d
            WHERE periodNo = %d
        ''' % (workloadTableName, realWL, periodNo)
        dbcur = dbcon.cursor()
        dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()


    @staticmethod
    def addFirstPeriodRealWorkload(realWL):
        if not realWL:
            raise Exception('no periodNo or real workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, realWL, predictWL)
            VALUES(%d, %d, %d);
        ''' % (workloadTableName, 1, realWL, -1)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addPredictWorkloadToSpecificPeriod(periodNo, predictWL):
        if not periodNo or not predictWL:
            raise Exception('no periodNo or predict workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, predictWL)
            VALUES(%d, %d);
        ''' % (workloadTableName, periodNo, predictWL)
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
    def getNewstWorkload():
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
