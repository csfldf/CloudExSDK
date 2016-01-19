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
periodicu = PeriodicPredictUtil()

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
    periodicPredictWL = periodicu.getNextPeriodWorkload()
    dailyPreidictWL = dailyu.getNextPeriodWorkload()

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
periodicCompareTuple = zip(realWL, periodicPredictList)
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

maChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
maChart.add_series({
        'name': '=ma!$B$1',
        'categories': '=ma!$A$2:$A$' + str(1 + len(index)),
        'values': '=ma!$B$2:$B$' + str(1 + len(index))})

maChart.add_series({
        'name': '=ma!$C$1',
        'categories': '=ma!$A$2:$A$' + str(1 + len(index)),
        'values': '=ma!$C$2:$C$' + str(1 + len(index))})

maRelativeError = calculateRelativeError(maCompareTuple)
maQualified = calculateQualified(maCompareTuple)

maRelativeError = round(maRelativeError * 100, 2)
maQualified = round(maQualified * 100, 2)

print 'ma: RelativeError: %f, Qualified: %f' % (maRelativeError, maQualified)

maChart.set_size({'width': 1400, 'height': 800})

maChart.set_title({'name': 'ma RelativeError:' + str(maRelativeError) + '% PassRate:' + str(maQualified) + '%'})
maSheet.insert_chart('E1', maChart)


periodicChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
periodicChart.add_series({
        'name': '=periodic!$B$1',
        'categories': '=periodic!$A$2:$A$' + str(1 + len(index)),
        'values': '=periodic!$B$2:$B$' + str(1 + len(index))})

periodicChart.add_series({
        'name': '=periodic!$C$1',
        'categories': '=periodic!$A$2:$A$' + str(1 + len(index)),
        'values': '=periodic!$C$2:$C$' + str(1 + len(index))})


periodicRelativeError = calculateRelativeError(periodicCompareTuple)
periodicQualified = calculateQualified(periodicCompareTuple)

periodicRelativeError = round(periodicRelativeError * 100, 2)
periodicQualified = round(periodicQualified * 100, 2)

print 'periodic: RelativeError: %f, Qualified: %f' % (periodicRelativeError, periodicQualified)

periodicChart.set_size({'width': 1400, 'height': 800})

periodicChart.set_title({'name': 'periodic RelativeError:' + str(periodicRelativeError) + '% PassRate:' + str(periodicQualified) + '%'})
periodicSheet.insert_chart('E1', periodicChart)



dailyChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
dailyChart.add_series({
        'name': '=daily!$B$1',
        'categories': '=daily!$A$2:$A$' + str(1 + len(index)),
        'values': '=daily!$B$2:$B$' + str(1 + len(index))})

dailyChart.add_series({
        'name': '=daily!$C$1',
        'categories': '=daily!$A$2:$A$' + str(1 + len(index)),
        'values': '=daily!$C$2:$C$' + str(1 + len(index))})

dailyRelativeError = calculateRelativeError(dailyCompareTuple)
dailyQualified = calculateQualified(dailyCompareTuple)

dailyRelativeError = round(dailyRelativeError * 100, 2)
dailyQualified = round(dailyQualified * 100, 2)

print 'daily: RelativeError: %f, Qualified: %f' % (dailyRelativeError, dailyQualified)

dailyChart.set_size({'width': 1400, 'height': 800})


dailyChart.set_title({'name': 'daily RelativeError:' + str(dailyRelativeError) + '% PassRate:' + str(dailyQualified) + '%'})
dailySheet.insert_chart('E1', dailyChart)


#acrc
clearAllData()

f = open('../DataFile/workload.txt')
realWL = []
for line in f:
    l = re.split(r'\s+', line)
    realWL.append(int(l[1]))
f.close()

acrcu = ACRCPredictUtil()
acrcPredictList = []

for wl in realWL:
    #acrc
    addWLToACRCWindow(wl)
    acrcPredictWL = acrcu.getNextPeriodWorkload()
    addPWLToACRCWindow(acrcPredictWL)
    acrcPredictList.append(acrcPredictWL)


realWL.pop(0)
acrcPredictList.pop()

acrcCompareTuple = zip(realWL, acrcPredictList)

index = range(len(realWL))


acrcSheet = workbook.add_worksheet('acrc')

bold = workbook.add_format({'bold': 1})

headings = ['index', 'Real', 'Predicted']

acrcSheet.write_row('A1', headings, bold)
acrcSheet.write_column('A2', index)
acrcSheet.write_column('B2', realWL)
acrcSheet.write_column('C2', acrcPredictList)


acrcChart = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth_with_markers'})
acrcChart.add_series({
        'name': '=acrc!$B$1',
        'categories': '=acrc!$A$2:$A$' + str(1 + len(index)),
        'values': '=acrc!$B$2:$B$' + str(1 + len(index))})

acrcChart.add_series({
        'name': '=acrc!$C$1',
        'categories': '=acrc!$A$2:$A$' + str(1 + len(index)),
        'values': '=acrc!$C$2:$C$' + str(1 + len(index))})

acrcRelativeError = calculateRelativeError(acrcCompareTuple)
acrcQualified = calculateQualified(acrcCompareTuple)

acrcRelativeError = round(acrcRelativeError * 100, 2)
acrcQualified = round(acrcQualified * 100, 2)

print 'acrc: RelativeError: %f, Qualified: %f' % (acrcRelativeError, acrcQualified)

acrcChart.set_size({'width': 1400, 'height': 800})

acrcChart.set_title({'name': 'acrc RelativeError:' + str(acrcRelativeError) + '% PassRate:' + str(acrcQualified) + '%'})
acrcSheet.insert_chart('E1', acrcChart)

workbook.close()
