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

workbook = xlsxwriter.Workbook('../DataFile/acrc_predict.xlsx')


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
