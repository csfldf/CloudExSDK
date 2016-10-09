#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

PMCPUTableName = 'PMCPU'


class PMCPUDBUtil(object):
    @staticmethod
    def createPMCPUTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT NOT NULL,
                realUtil DOUBLE(10, 2),
                predictUtil DOUBLE(10, 2),
                pmId VARCHAR(40) NOT NULL,
                FOREIGN KEY (pmId) REFERENCES PMAndAZ(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % PMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addRealPMCPUToSpecificPeriod(periodNo, tarId, realPMCPU):
        if not periodNo or not realPMCPU:
            raise Exception('no periodNo or real pm util')

        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET realUtil = %lf
            WHERE periodNo = %d AND pmId = '%s'
        ''' % (PMCPUTableName, realPMCPU, periodNo, tarId)
        dbcur = dbcon.cursor()
        afl = dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()
        if afl == 0:
            raise Exception("add real pm cpu util to period that wasn't been predicted")

    @staticmethod
    def addFirstPeriodRealPMCPU(realPMCPU, pmId):
        if not realPMCPU:
            raise Exception('no periodNo or real pm util')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, realUtil, predictUtil, pmId)
            VALUES(%d, %lf, %lf, '%s');
        ''' % (PMCPUTableName, 1, realPMCPU, -1, pmId)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addPredictPMCPUToSpecificPeriod(periodNo, predictPMCPU, pmId):
        if not periodNo or not predictPMCPU:
            raise Exception('no periodNo or predict workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, predictUtil, pmId)
            VALUES(%d, %lf, '%s');
        ''' % (PMCPUTableName, periodNo, predictPMCPU, pmId)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getPMCPUCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % PMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def getAllPMCPUInfo():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT realUtil, predictUtil
            FROM %s
        ''' % PMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        utilList = []
        for u in dbcur:
            utilList.append((u[0], u[1]))
        dbcur.close()
        dbcon.close()
        return utilList

    @staticmethod
    def dropPMCPUTable():
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DROP TABLE %s
        ''' % PMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def clearPMCPUTable():
        dbcon = getDBConwithCloudExDB()
        clearStat = '''
            DELETE FROM %s
        ''' % PMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(clearStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getNewestPMCPU():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT periodNo, realUtil
            FROM %s
            WHERE periodNo = (
                SELECT MAX(periodNo)
                FROM %s
            )
        ''' % (PMCPUTableName, PMCPUTableName)
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        nu = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if nu:
            return {'periodNo':nu[0], 'realPMCPU':nu[1]}
        else:
            return None

if __name__ == '__main__':
    #PMCPUDBUtil.createPMCPUTable()
    PMCPUDBUtil.dropPMCPUTable()
    PMCPUDBUtil.createPMCPUTable()
    PMCPUDBUtil.addFirstPeriodRealPMCPU(80.28, '05aa91c8-1a8f-11e6-a93b-00e04c680ae0')
    PMCPUDBUtil.addPredictPMCPUToSpecificPeriod(2, 80.28, '05aa91c8-1a8f-11e6-a93b-00e04c680ae0')
    PMCPUDBUtil.addRealPMCPUToSpecificPeriod(2, 80.29)
    print PMCPUDBUtil.getAllPMCPUInfo()
    print PMCPUDBUtil.getNewestPMCPU()
    print PMCPUDBUtil.getPMCPUCount()

    PMCPUDBUtil.clearPMCPUTable()
    print PMCPUDBUtil.getAllPMCPUInfo()
    print PMCPUDBUtil.getPMCPUCount()

