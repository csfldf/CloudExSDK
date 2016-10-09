#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

VMCPUTableName = 'VMCPU'


class VMCPUDBUtil(object):
    @staticmethod
    def createVMCPUTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                periodNo INT NOT NULL,
                realUtil DOUBLE(10, 2),
                predictUtil DOUBLE(10, 2),
                vmIP VARCHAR(16) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % VMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addRealVMCPUToSpecificPeriod(periodNo, realVMCPU, vmIP):
        if not periodNo or not realVMCPU:
            raise Exception('no periodNo or real pm util')

        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET realUtil = %lf
            WHERE periodNo = %d AND vmIP = '%s'
        ''' % (VMCPUTableName, realVMCPU, periodNo, vmIP)
        dbcur = dbcon.cursor()
        afl = dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()
        if afl == 0:
            raise Exception("add real pm cpu util to period that wasn't been predicted")

    @staticmethod
    def addFirstPeriodRealVMCPU(realVMCPU, vmIP):
        if not realVMCPU:
            raise Exception('no periodNo or real pm util')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, realUtil, predictUtil, vmIP)
            VALUES(%d, %lf, %lf, '%s');
        ''' % (VMCPUTableName, 1, realVMCPU, -1, vmIP)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def addPredictVMCPUToSpecificPeriod(periodNo, predictVMCPU, vmIP):
        if not periodNo or not predictVMCPU:
            raise Exception('no periodNo or predict workload')

        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(periodNo, predictUtil, vmIP)
            VALUES(%d, %lf, '%s');
        ''' % (VMCPUTableName, periodNo, predictVMCPU, vmIP)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getVMCPUCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % VMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def getAllVMCPUInfo():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT realUtil, predictUtil
            FROM %s
        ''' % VMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        utilList = []
        for u in dbcur:
            utilList.append((u[0], u[1]))
        dbcur.close()
        dbcon.close()
        return utilList

    @staticmethod
    def dropVMCPUTable():
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DROP TABLE %s
        ''' % VMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def clearVMCPUTable():
        dbcon = getDBConwithCloudExDB()
        clearStat = '''
            DELETE FROM %s
        ''' % VMCPUTableName
        dbcur = dbcon.cursor()
        dbcur.execute(clearStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getNewestVMCPU():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT periodNo, realUtil
            FROM %s
            WHERE periodNo = (
                SELECT MAX(periodNo)
                FROM %s
            )
        ''' % (VMCPUTableName, VMCPUTableName)
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        nu = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        if nu:
            return {'periodNo':nu[0], 'realVMCPU':nu[1]}
        else:
            return None

if __name__ == '__main__':
    #VMCPUDBUtil.createVMCPUTable()
    VMCPUDBUtil.dropVMCPUTable()
    VMCPUDBUtil.createVMCPUTable()
    VMCPUDBUtil.addFirstPeriodRealVMCPU(80.28, '192.168.9.44')
    VMCPUDBUtil.addPredictVMCPUToSpecificPeriod(2, 80.28, '192.168.9.44')
    VMCPUDBUtil.addRealVMCPUToSpecificPeriod(2, 80.29)
    print VMCPUDBUtil.getAllVMCPUInfo()
    print VMCPUDBUtil.getNewestVMCPU()
    print VMCPUDBUtil.getVMCPUCount()

    VMCPUDBUtil.clearVMCPUTable()
    print VMCPUDBUtil.getAllVMCPUInfo()
    print VMCPUDBUtil.getVMCPUCount()

