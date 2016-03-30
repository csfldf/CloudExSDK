#!/usr/bin/env python
# encoding: utf-8

from DBUtil import *
import xlsxwriter

performanceDataTableName = 'PerformanceData'

def getVMsInfoTuple():
    dbcon = getDBConwithCloudExDB()
    selectStat = '''
        SELECT vmNumbers, shouldVMNumbers, periodNo
        FROM %s
    ''' % performanceDataTableName
    dbcur = dbcon.cursor()
    dbcur.execute(selectStat)
    real = []
    should = []
    index = []
    for item in dbcur:
        real.append(item[0])
        should.append(item[1])
        index.append(item[2] - 1)
    dbcur.close()
    dbcon.close()
    return real, should, index

real, should, index = getVMsInfoTuple()

print 'total: ' + str(len(index))

count = 0
for i in index:
    if real[i] >= should[i]:
        count += 1

print 'gou: ' + str(count)
print 'gou%: ' + str(float(count) / len(index))

