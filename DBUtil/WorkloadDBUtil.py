#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

workloadTableName = 'Workload'

import MySQLdb

class WorkloadDBUtil(object):
    @staticmethod
    def createWorkloadTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT UNIQUE NOT NULL,
                workload INT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addWorkload(periodNo, workload):
        if not periodNo or not workload:
            raise Exception('no periodNo or workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, workload)
            VALUES(%d, %d);
        ''' % (workloadTableName, periodNo, workload)
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
            SELECT workload
            FROM %s
        ''' % workloadTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        workloadList = []
        for wk in dbcur:
            workloadList.append(wk[0])
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
            SELECT workload
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
            return wl[0]
        else:
            return None
