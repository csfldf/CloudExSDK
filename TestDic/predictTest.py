#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
from PredictUtil import *
from NormalUtil import popNoneInList
from PredictUtil.PeriodicPredictUtil import PeriodicPredictUtil
from PredictUtil.MAPredictUtil import MAPredictUtil
from PredictUtil.DailyPredictUtil import DailyPredictUtil

clearAllData()

f = open('./DataFile/workload.txt')
realWL = []
for line in f:
#    print line
    l = re.split(r'\s+', line)
    realWL.append(int(l[1]))

f.close()

ppu = PeriodicPredictUtil()
mau = MAPredictUtil()
dpu = DailyPredictUtil()


for wl in realWL:
    #periodic
    #addWLToPeriodicWindow(wl)
    #predictWL = ppu.getNextPeriodWorkload()
    #addPWLToPeriodicWindow(predictWL)

    #ma
#    addWLToMAWindow(wl)
#    predictWL = mau.getNextPeriodWorkload()
#    addPWLToMAWindow(predictWL)

    #daily
    addWLToDailyWindow(wl)
    predictWL = dpu.getNextPeriodWorkload()
    addPWLToDailyWindow(predictWL)

    addPWLToStatWindow(predictWL)

pdDB = shelve.open(predictDataFile)
statPD = pdDB[statPredictData]
pdDB.close()

compareTuple = zip(realWL, statPD)
compareTuple.pop(0)
#periodic
#f = open('./DataFile/periodicCompare', 'w')

#ma
#f = open('./DataFile/maCompare', 'w')

#daily
f = open('./DataFile/dailyCOmpare', 'w')


for hd, pd in compareTuple:
    f.write('%d\t%d\n' % (hd, pd))

f.close()

relativeError = calculateRelativeError(compareTuple)
qualified = calculateQualified(compareTuple)

print relativeError, qualified
