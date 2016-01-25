#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.DailyPredictUtil import DailyPredictUtil
from PredictUtil.PeriodicPredictUtil import PeriodicPredictUtil
from PredictUtil.BasePredictUtil import BasePredictUtil

class ACRCPredictUtil(BasePredictUtil):
    def __init__(self, windowSize=acrcHistoryWindowSize, historyData=None, historyDataFile=historyDataFile, historyDataName=acrcHistoryData):
        super(ACRCPredictUtil, self).__init__(windowSize, historyData, historyDataFile, historyDataName)


    def adjustByAnalyseError(self, predictWorkload):
        pdDB = shelve.open(predictDataFile)
        acrcPD = pdDB.get(acrcPredictData, None)
        pdDB.close()


        if not acrcPD:
            raise Exception('no acrc predict data!')
        elif not self.historyData:
            raise Exception('no acrc history data!')
        elif len(acrcPD) != len(self.historyData):
            raise Exception('the length of acrc predict data and history data!')
        else:
            if acrcPD[0] == firstPeriodPredictData:
                begIndex = 1
                totalNumber = len(acrcPD) - 1

                #第一个周期
                if len(acrcPD) == 1:
                    return predictWorkload
            else:
                begIndex = 0
                totalNumber = len(acrcPD)

            indexList = range(begIndex, len(acrcPD))

            totalGab = 0
            gabList = []
            for ind in indexList:
                gab = self.historyData[ind] - acrcPD[ind] if self.historyData[ind] > acrcPD[ind] else 0
                gabList.append(gab)
                totalGab += gab

            #gabWorkload = totalGab / totalNumber + 1

            #max
            #gabWorkload = max(gabList)

            #%75
            gabList.sort()
            gl = len(gabList)
            tif = gl * 0.75
            if tif == int(tif):
                targetIndex = int(tif)
            else:
                targetIndex = int(tif) + 1
            gabWorkload = gabList[targetIndex - 1]

            return predictWorkload + gabWorkload


    def getNextPeriodWorkload(self):
        self.reloadHistoryData()

        if not self.historyData:
            raise Exception('no historyData!')

        ppu = PeriodicPredictUtil()
        dpu = DailyPredictUtil()

        periodicPredictWL = ppu.getNextPeriodWorkload()
        dailyPredictWL = dpu.getNextPeriodWorkload()
        addPWLToPeriodicWindow(periodicPredictWL)
        addPWLToDailyWindow(dailyPredictWL)

        hdLen = len(self.historyData)

        #debug
#        if self.historyData[hdLen - 1] >= 2289805 and self.historyData[hdLen - 1] <= 5112538:
#            print self.historyData[hdLen - 1] + 1
#            print 'period :' + str(periodicPredictWL)
#            print 'dailyPredictWL :' + str(dailyPredictWL)

        if hdLen == 1:
            return self.historyData[0]
        else:
            pdDB = shelve.open(predictDataFile)
            acrcPD = pdDB.get(acrcPredictData, None)
            pdDB.close()

            if len(acrcPD) != hdLen:
                raise Exception('the length of acrc predict data and history data not same!')

            combineTupleList = zip(self.historyData, acrcPD)

            if acrcPD[0] == firstPeriodPredictData:
                combineTupleList.pop(0)

            ctlLen = len(combineTupleList)
            count = 0
            for hd,pd in combineTupleList:
                if pd > hd:
                    count += 1

            targetPercent = 1.0 - float(count) / ctlLen

            #debug
#            if self.historyData[hdLen - 1] >= 2289805 and self.historyData[hdLen - 1] <= 5112538:
#                print targetPercent

            #防止过分减
            if targetPercent < 0.5:
                targetPercent = 0.5

            gab = abs(periodicPredictWL - dailyPredictWL)
            targetGab = int(gab * targetPercent) + 1

            originPWL = min(periodicPredictWL, dailyPredictWL) + targetGab

            return self.adjustByAnalyseError(originPWL)

