#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *

usingInstancesTableName = 'UsingInstances'

import MySQLdb
class UsingInstancesDBUtil(object):
    @staticmethod
    def createUsingInstancesTable():
        dbcon = getDBConwithCloudExDB()
        createTableStat = '''
            CREATE TABLE %s(
                id INT PRIMARY KEY AUTO_INCREMENT,
                resourceId VARCHAR(40) UNIQUE NOT NULL,
                name VARCHAR(50) UNIQUE NOT NULL,
                weight INT NOT NULL,
                innerIP VARCHAR(15) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % usingInstancesTableName
        dbcur = dbcon.cursor()
        dbcur.execute(createTableStat)
        dbcur.close()
        dbcon.close()

    @staticmethod
    def addUsingInstance(resourceId, name, weight, innerIP):
        dbcon = getDBConwithCloudExDB()
        insertStat = '''
            INSERT INTO %s(resourceId, name, weight, innerIP)
            VALUES('%s', '%s', %d, '%s');
        ''' % (usingInstancesTableName, resourceId, name, weight, innerIP)
        dbcur = dbcon.cursor()
        dbcur.execute(insertStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def deleteUsingInstanceByResourceId(resourceId):
        dbcon = getDBConwithCloudExDB()
        deleteStat = '''
            DELETE FROM %s
            WHERE resourceId='%s'
        ''' % (usingInstancesTableName, resourceId)
        dbcur = dbcon.cursor()
        dbcur.execute(deleteStat)
        dbcur.close()
        dbcon.commit()
        dbcon.close()

    @staticmethod
    def getUsingInstancesCount():
        dbcon = getDBConwithCloudExDB()
        countStat = '''
            SELECT COUNT(*)
            FROM %s
        ''' % usingInstancesTableName
        dbcur = dbcon.cursor()
        dbcur.execute(countStat)
        r = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        return r[0]

    @staticmethod
    def getAllUsingInstancesInfo():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT resourceId, weight, innerIP
            FROM %s
        ''' % usingInstancesTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        uiInfoList = []
        for ui in dbcur:
            rid = ui[0]
            weight = ui[1]
            innerIP = ui[2]
            url = innerIP + ':8080'
            uiInfo = {'url':url, 'weight':weight, 'id':rid}
            uiInfoList.append(uiInfo)
        dbcur.close()
        dbcon.close()
        return uiInfoList


    @staticmethod
    def getAllUsingInstancesIds():
        dbcon = getDBConwithCloudExDB()
        selectStat = '''
            SELECT resourceId
            FROM %s
        ''' % usingInstancesTableName
        dbcur = dbcon.cursor()
        dbcur.execute(selectStat)
        uiIdsList = []
        for ui in dbcur:
            uiIdsList.append(ui[0])
        dbcur.close()
        dbcon.close()
        return uiIdsList
