#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
from PredictUtil import *
from NormalUtil import popNoneInList
from PredictUtil.PeriodicPredictUtil import PeriodicPredictUtil

clearAllData()

f = open('../DataFile/workload.txt')
realWL = []
for line in f:
    l = re.split(r'\s+', line)
    realWL.append(int(l[1]))

f.close()

ppu = PeriodicPredictUtil()

for wl in realWL:
    #periodic
    addWLToPeriodicWindow(wl)
    periodicPredictWL = ppu.getNextPeriodWorkload()
    addPWLToPeriodicWindow(periodicPredictWL)
    addPWLToStatWindow(periodicPredictWL)

pdDB = shelve.open(predictDataFile)
statPD = pdDB[statPredictData]
pdDB.close()

compareTuple = zip(realWL, statPD)
compareTuple.pop(0)

#periodic
f = open('../DataFile/periodicCompare.xls', 'w')

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
