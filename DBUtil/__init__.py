#!/usr/bin/env python
# encoding: utf-8

import MySQLdb

dbUser = 'root'
dbUserPasswd = '123'
dbHost = '202.120.40.20'
dbPort = 43306
dbName = 'CloudEx'


def test():
    dbcon = getDBConwithNoDB()


def getDBConwithCloudExDB():
    return MySQLdb.connect(user=dbUser, passwd=dbUserPasswd, host=dbHost, port=dbPort, db=dbName)

def getDBConwithNoDB():
    return MySQLdb.connect(user=dbUser, passwd=dbUserPasswd, host=dbHost, port=dbPort)

def dropCloudExDB():
    dbcon = getDBConwithNoDB()
    dbcur = dbcon.cursor()
    dropDBStat = '''
        DROP DATABASE IF EXISTS %s;
    ''' % dbName
    dbcur.execute(dropDBStat)
    dbcur.close()
    dbcon.close()

def createCloudExDB():
    dbcon = getDBConwithNoDB()
    dbcur = dbcon.cursor()
    createDBStat = '''
        CREATE DATABASE IF NOT EXISTS %s;
    ''' % dbName
    dbcur.execute(createDBStat)
    dbcur.close()
    dbcon.close()

