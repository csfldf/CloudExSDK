#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
import xlsxwriter
from PredictUtil import *
from NormalUtil import popNoneInList
from PredictUtil.MAPredictUtil import MAPredictUtil
from PredictUtil.ACRCPredictUtil import ACRCPredictUtil
from PredictUtil.DailyPredictUtil import DailyPredictUtil
from PredictUtil.PeriodicPredictUtil import PeriodicPredictUtil

clearAllData()

f = open('../DataFile/workload.txt')
realWL = []
for line in f:
    l = re.split(r'\s+', line)
    realWL.append(int(l[1]))
f.close()

mau = MAPredictUtil()
acrcu = ACRCPredictUtil()
dailyu = DailyPredictUtil()
PeriodicPredictUtil = PeriodicPredictUtil()

maPredictList = []
periodicPredictList = []
dailyPredictList = []
acrcPredictList = []

for wl in realWL:
    #ma
    addWLToMAWindow(wl)
    addWLToPeriodicWindow(wl)
    addWLToDailyWindow(wl)

    maPredictWL = mau.getNextPeriodWorkload()
    periodicPredictWL = PeriodicPredictUtil.getNextPeriodWorkload()
    dailyPreidictWL = DailyPredictUtil.getNextPeriodWorkload()

    addPWLToMAWindow(maPredictWL)
    addPWLToPeriodicWindow(periodicPredictWL)
    addPWLToDailyWindow(dailyPreidictWL)

    maPredictList.append(maPredictWL)
    periodicPredictList.append(periodicPredictWL)
    dailyPredictList.append(dailyPreidictWL)

#pdDB = shelve.open(predictDataFile)
#statPD = pdDB[statPredictData]
#pdDB.close()


realWL.pop(0)
maPredictList.pop()
dailyPredictList.pop()
periodicPredictList.pop()

maCompareTuple = zip(realWL, maPredictList)
dailyCompareTuple = zip(realWL, dailyPredictList)
periodicCompareTuple = zip(realWL, periodicPredictWL)
#statPD.pop(0)
#statPD.pop()

#if len(realWL) != len(statPD):
#    raise Exception('the length of realWL and statPD not same!')


#ma

index = range(len(realWL))

workbook = xlsxwriter.Workbook('../DataFile/total_predict.xlsx')

maSheet = workbook.add_worksheet('ma')
periodicSheet = workbook.add_worksheet('periodic')
dailySheet = workbook.add_worksheet('daily')

bold = workbook.add_format({'bold': 1})

headings = ['index', 'Real', 'Predicted']

maSheet.write_row('A1', headings, bold)
maSheet.write_column('A2', index)
maSheet.write_column('B2', realWL)
maSheet.write_column('C2', maPredictList)


dailySheet.write_row('A1', headings, bold)
dailySheet.write_column('A2', index)
dailySheet.write_column('B2', realWL)
dailySheet.write_column('C2', maPredictList)


periodicSheet.write_row('A1', headings, bold)
periodicSheet.write_column('A2', index)
periodicSheet.write_column('B2', realWL)
periodicSheet.write_column('C2', maPredictList)

chart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
chart.add_series({
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$' + str(1 + len(index)),
        'values': '=Sheet1!$B$2:$B$' + str(1 + len(index))})

chart.add_series({
        'name': '=Sheet1!$C$1',
        'categories': '=Sheet1!$A$2:$A$' + str(1 + len(index)),
        'values': '=Sheet1!$C$2:$C$' + str(1 + len(index))})



maRelativeError = calculateRelativeError(maCompareTuple)
maQualified = calculatemaQualified(maCompareTuple)

maRelativeError = round(maRelativeError * 100, 2)
maQualified = round(maQualified * 100, 2)

periodicRelativeError = calculateRelativeError(periodicCompareTuple)
periodicQualified = calculateperiodicQualified(periodicCompareTuple)

periodicRelativeError = round(periodicRelativeError * 100, 2)
periodicQualified = round(periodicQualified * 100, 2)


dailyRelativeError = calculateRelativeError(dailyCompareTuple)
dailyQualified = calculatedailyQualified(dailyCompareTuple)

dailyRelativeError = round(dailyRelativeError * 100, 2)
dailyQualified = round(dailyQualified * 100, 2)


chart.set_size({'width': 1400, 'height': 800})

chart.set_title({'name': 'ma RelativeError:' + str(maRelativeError) + '% PassRate:' + str(maQualified) + '%'})
maSheet.insert_chart('E1', chart)

chart.set_title({'name': 'periodic RelativeError:' + str(periodicRelativeError) + '% PassRate:' + str(periodicQualified) + '%'})
periodicSheet.insert_chart('E1', chart)

chart.set_title({'name': 'daily RelativeError:' + str(dailyRelativeError) + '% PassRate:' + str(dailyQualified) + '%'})
dailySheet.insert_chart('E1', chart)


workbook.close()

