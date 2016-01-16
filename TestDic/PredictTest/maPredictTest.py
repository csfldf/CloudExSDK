#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
from PredictUtil import *
from NormalUtil import popNoneInList
from PredictUtil.MAPredictUtil import MAPredictUtil

clearAllData()

f = open('../DataFile/workload.txt')
realWL = []
for line in f:
    l = re.split(r'\s+', line)
    realWL.append(int(l[1]))

f.close()
mau = MAPredictUtil()

for wl in realWL:
    #ma
    addWLToMAWindow(wl)
    predictWL = mau.getNextPeriodWorkload()
    addPWLToMAWindow(predictWL)
    addPWLToStatWindow(predictWL)

pdDB = shelve.open(predictDataFile)
statPD = pdDB[statPredictData]
pdDB.close()

compareTuple = zip(realWL, statPD)
compareTuple.pop(0)

#ma
f = open('../DataFile/maCompare.xls', 'w')

f.write('%s\t%s\n' % ('Real', 'Predicted'))

for hd, pd in compareTuple:
    f.write('%d\t%d\n' % (hd, pd))


relativeError = calculateRelativeError(compareTuple)
qualified = calculateQualified(compareTuple)

relativeError = round(relativeError * 100, 2)
qualified = round(qualified * 100, 2)

f.write('%f\t%f\n' % (relativeError, qualified))

f.close()
print relativeError, qualified
