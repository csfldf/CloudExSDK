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

periodicu = PeriodicPredictUtil()

periodicPredictList = []

for wl in realWL:
    addWLToPeriodicWindow(wl)

    periodicPredictWL = periodicu.getNextPeriodWorkload()

    addPWLToPeriodicWindow(periodicPredictWL)

    periodicPredictList.append(periodicPredictWL)



realWL.pop(0)
periodicPredictList.pop()

periodicCompareTuple = zip(realWL, periodicPredictList)



index = range(len(realWL))

workbook = xlsxwriter.Workbook('../DataFile/periodic_predict.xlsx')

periodicSheet = workbook.add_worksheet('periodic')

bold = workbook.add_format({'bold': 1})

headings = ['index', 'Real', 'Predicted']


periodicSheet.write_row('A1', headings, bold)
periodicSheet.write_column('A2', index)
periodicSheet.write_column('B2', realWL)
periodicSheet.write_column('C2', periodicPredictList)




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


workbook.close()
