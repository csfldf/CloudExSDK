#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
from uuid import uuid1 as genUUID

pmAndAZTableName = 'PMAndAZ'

class PMAndAZDBUtil(object):
    @staticmethod
    def createPMAndAZTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id VARCHAR(40) PRIMARY KEY,
                pmName CHAR(10) UNIQUE NOT NULL,
                innerIP VARCHAR(16) UNIQUE NOT NULL,
                azName VARCHAR(10) UNIQUE NOT NULL,
                upperThreshold DOUBLE(10,2) NOT NULL,
                lowerThreshold DOUBLE(10,2) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % pmAndAZTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.close()

    @staticmethod
    def addPMAndAZ(resourceId, pmName, innerIP, azName, upperThreshold, lowerThreshold):
        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(id, pmName, innerIP, azName, upperThreshold, lowerThreshold)
            VALUES('%s', '%s', '%s', '%s', %lf, %lf);
        ''' % (pmAndAZTableName, resourceId, pmName, innerIP, azName, upperThreshold, lowerThreshold)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def deletePMAndAZByResourceId(resourceId):
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DELETE FROM %s
            WHERE id='%s'
        ''' % (pmAndAZTableName, resourceId)
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()


    @staticmethod
    def getAllPMsInfo():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT id, upperThreshold, lowerThreshold
            FROM %s
        ''' % pmAndAZTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        pmsInfoList = []
        for pm in dbcur:
            rid = pm[0]
            upperThreshold = pm[1]
            lowerThreshold = pm[2]
            pmInfo = {'id':rid, 'upper_threshold':upperThreshold, 'lower_threshold':lowerThreshold}
            pmsInfoList.append(pmInfo)
        dbcur.close()
        dbcon.close()
        return pmsInfoList


    @staticmethod
    def dropPMAndAZTable():
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DROP TABLE %s
        ''' % pmAndAZTableName
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getAZNameByResourceId(resourceId):
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT azName
            FROM %s
            WHERE id = '%s'
        ''' % (pmAndAZTableName, resourceId)

        dbcur = dbcon.cursor()
        affectedRow = dbcur.execute(selectStat)
        if affectedRow == 0:
            dbcur.close()
            dbcon.close()
            return None

        azInfo = dbcur.fetchone()

        dbcur.close()
        dbcon.close()
        return azInfo[0]

    @staticmethod
    def modifyUpperThreshold(resourceId, targetValue):
        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET upperThreshold = %lf
            WHERE id = '%s'
        ''' % (pmAndAZTableName, targetValue, resourceId)

        dbcur = dbcon.cursor()
        dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()


    @staticmethod
    def modifyLowerThreshold(resourceId, targetValue):
        dbcon = getDBConwithCloudExDB()
        updateStat = '''
            UPDATE %s
            SET lowerThreshold = %lf
            WHERE id = '%s'
        ''' % (pmAndAZTableName, targetValue, resourceId)

        dbcur = dbcon.cursor()
        dbcur.execute(updateStat)
        dbcur.close()
        dbcon.commit()

    @staticmethod
    def isPMId(tarId):
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT COUNT(*)
            FROM %s
            WHERE id = '%s'
        ''' % (pmAndAZTableName, tarId)

        dbcur = dbcon.cursor()
        affectedRow = dbcur.execute(selectStat)

        res = dbcur.fetchone()

        dbcur.close()
        dbcon.close()

        if res[0] == 0:
            return False
        else:
            return True

    @staticmethod
    def getInnerIPByPMId(tarId):
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT innerIP
            FROM %s
            WHERE id = '%s'
        ''' % (pmAndAZTableName, tarId)

        dbcur = dbcon.cursor()
        affectedRow = dbcur.execute(selectStat)

        res = dbcur.fetchone()

        dbcur.close()
        dbcon.close()

        if affectedRow == 0:
            return None
        else:
            return res[0]



if __name__ == '__main__':
    #PMAndAZDBUtil.createPMAndAZTable()
    #for prefix, azName in zip(['50', '60', '70', '80', '210', '220', '230', '240'], ['az5', 'az6', 'az7', 'az8', 'az1', 'az2', 'az3', 'az4']):
    #    PMAndAZDBUtil.addPMAndAZ(str(genUUID()), 'ubuntu-' + prefix, '192.168.0.' + prefix, azName, 80.0, 20.0)
    #PMAndAZDBUtil.modifyUpperThreshold('05aa91c8-1a8f-11e6-a93b-00e04c680ae0', 80.0)
    #PMAndAZDBUtil.modifyLowerThreshold('05aa91c8-1a8f-11e6-a93b-00e04c680ae0', 20.0)
    #print PMAndAZDBUtil.isPMId('05add7fc-1a8f-11e6-a93b-00e04c680ae0')
    #print PMAndAZDBUtil.getAZNameByResourceId('05add7fc-1a8f-11e6-a93b-00e04c680ae0')
    #print  PMAndAZDBUtil.getInnerIPByPMId('aa')
    PMAndAZDBUtil.addPMAndAZ(str(genUUID()), 'ubuntu-50', '192.168.0.50', 'az5', 80.0, 20.0)
    #PMAndAZDBUtil.modifyUpperThreshold('05add7fc-1a8f-11e6-a93b-00e04c680ae0', 60)
    #PMAndAZDBUtil.modifyLowerThreshold('05add7fc-1a8f-11e6-a93b-00e04c680ae0', 30)
