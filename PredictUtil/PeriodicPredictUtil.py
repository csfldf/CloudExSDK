#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.BasePredictUtil import BasePredictUtil

class PeriodicPredictUtil(BasePredictUtil):
    #errorRatio在上一个周期的错误和之前的错误的平均值两者之间加权算错误用
    def __init__(self, windowSize=periodicHistoryWindowSize, historyData=None, historyDataFile=historyDataFile, historyDataName=periodicHistoryData, errorRatio=0.5):
        if not historyData and historyDataFile:
            hdDB = shelve.open(historyDataFile)
            historyData = hdDB[periodicHistoryData]
            hdDB.close()
        super(PeriodicPredictUtil, self).__init__(windowSize, historyData, historyDataFile, historyDataName)
        self.errorRatio = errorRatio

    def calculateB(self):
        pdDB = shelve.open(predictDataFile)
        ppd = pdDB.get(periodicPredictData, None)

        edDB = shelve.open(errorParamDataFile)
        epd = edDB.get(errorParamData, None)

        hl = len(self.historyData)
        pl = len(ppd)

        if not ppd or not epd:
            raise Exception('no predictData or not epd!')

        if hl != pl:
            raise Exception('the length of historyData and predictData not same!')

        avgE = sum(epd) / len(epd)

        newestHWL = self.historyData[hl - 1]
        newestPWL = ppd[pl - 1]

        newE = (1 - self.errorRatio) * abs(newestHWL - newestPWL) + self.errorRatio * avgE
        addDataToWindow(epd, newE, errorParamWindowSize)
        edDB[errorParamData] = epd

        maxE = max(epd)
        B = 1 - newE / maxE

        pdDB.close()
        edDB.close()

        return B


    def adjustByAnalyseError(self, predictWorkload):
        pdDB = shelve.open(predictDataFile)
        ppd = pdDB.get(periodicPredictData, None)
        pdDB.close()


        if not ppd:
            raise Exception('no daily predict data!')
        elif not self.historyData:
            raise Exception('no periodic history data!')
        elif len(ppd) != len(self.historyData):
            raise Exception('the length of periodic predict data and history data!')
        else:
            if ppd[0] == firstPeriodPredictData:
                begIndex = 1
                totalNumber = len(ppd) - 1

                #第一个周期
                if len(ppd) == 1:
                    return predictWorkload
            else:
                begIndex = 0
                totalNumber = len(ppd)

            indexList = range(begIndex, len(ppd))

            totalGab = 0
            gabList = []
            for ind in indexList:
                gab = self.historyData[ind] - ppd[ind] if self.historyData[ind] > ppd[ind] else 0
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

        hdLen = len(self.historyData)

        if hdLen == 1:
            return self.historyData[0]
        if hdLen == 2:
            edDB = shelve.open(errorParamDataFile)
            pdDB = shelve.open(predictDataFile)
            ppd = pdDB.get(periodicPredictData, None)
            edpd = [self.errorRatio * abs(self.historyData[1] - ppd[1])]
            edDB[errorParamData] = edpd
            edDB.close()
            pdDB.close()
            originPWL = MAUtil(self.historyData)
        else:
            B = self.calculateB()

            #debug
            #if self.historyData[hdLen - 1] == 3790405 or self.historyData[hdLen - 1] == 2289805:
            #    print B

            totalPastHWD = sum(self.historyData) - self.historyData[hdLen - 1]
            totalAVG = totalPastHWD / (hdLen - 1) + 1

            originPWL = (1 - B) * self.historyData[hdLen - 1] + B * totalAVG
        return self.adjustByAnalyseError(originPWL)
