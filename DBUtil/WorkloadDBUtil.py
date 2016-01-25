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

