#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.BasePredictUtil import BasePredictUtil
from LoggingUtil import getLogUtil

cpuLogger = getLogUtil('VMOrPMCPUUtilPredict')

class PMCPUPredictUtil(BasePredictUtil):
    #errorRatio在上一个周期的错误和之前的错误的平均值两者之间加权算错误用
    def __init__(self, windowSize=periodicHistoryWindowSize, historyData=None, historyDataFile=utilHistoryDataFile, historyDataName=pmCPUUtilHistoryData, errorRatio=0.5):
        if not historyData and historyDataFile:
            hdDB = shelve.open(historyDataFile)
            historyData = hdDB[historyDataName]
            hdDB.close()
        super(PMCPUPredictUtil, self).__init__(windowSize, historyData, historyDataFile, historyDataName)
        self.errorRatio = errorRatio

    def calculateB(self, pmId):
        pdDB = shelve.open(utilPredictDataFile)
        ppd = pdDB.get(pmCPUUtilPredictData, None)

        edDB = shelve.open(utilErrorDataFile)
        epd = edDB.get(pmCPUUtilErrorData, None)

        #print ppd, epd

        cpuLogger.info('pmId:' + pmId + ' epd:' + str(epd) + ' ppd:' + str(ppd))

        if not ppd or not epd or pmId not in ppd or pmId not in epd:
            raise Exception('no predictData or not epd!')

        hl = len(self.historyData[pmId])
        pl = len(ppd[pmId])


        if hl != pl:
            raise Exception('the length of historyData and predictData not same!')

        avgE = sum(epd[pmId]) / len(epd[pmId])

        newestHWL = self.historyData[pmId][hl - 1]
        newestPWL = ppd[pmId][pl - 1]

        newE = (1 - self.errorRatio) * abs(newestHWL - newestPWL) + self.errorRatio * avgE
        addDataToWindow(epd[pmId], newE, errorParamWindowSize)
        edDB[pmCPUUtilErrorData] = epd

        maxE = max(epd[pmId])

        if maxE == 0:
            B = 0
        else:
            B = 1 - newE / maxE

        pdDB.close()
        edDB.close()

        return B


    def adjustByAnalyseError(self, pmId, predictWorkload):
        pdDB = shelve.open(utilPredictDataFile)
        ppd = pdDB.get(pmCPUUtilPredictData, None)
        pdDB.close()


        if not ppd or pmId not in ppd or not ppd[pmId]:
            raise Exception('no daily predict data!')
        elif pmId not in self.historyData and not self.historyData[pmId]:
            raise Exception('no periodic history data!')
        elif len(ppd[pmId]) != len(self.historyData[pmId]):
            raise Exception('the length of periodic predict data and history data!')
        else:
            if ppd[pmId][0] == firstPeriodPredictData:
                begIndex = 1
                totalNumber = len(ppd[pmId]) - 1

                #第一个周期
                if len(ppd[pmId]) == 1:
                    return predictWorkload
            else:
                begIndex = 0
                totalNumber = len(ppd[pmId])

            indexList = range(begIndex, len(ppd[pmId]))

            totalGab = 0
            gabList = []
            for ind in indexList:
                gab = self.historyData[pmId][ind] - ppd[pmId][ind] if self.historyData[pmId][ind] > ppd[pmId][ind] else 0
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

    def getNextPeriodWorkload(self, pmId):

        self.reloadHistoryData()

        if not self.historyData or pmId not in self.historyData:
            raise Exception('no historyData!')

        hdLen = len(self.historyData[pmId])

        if hdLen == 1:
            return self.historyData[pmId][0]
        if hdLen == 2:
            pdDB = shelve.open(utilPredictDataFile)
            ppd = pdDB.get(pmCPUUtilPredictData, None)

            edDB = shelve.open(utilErrorDataFile)
            edpd = [self.errorRatio * abs(self.historyData[pmId][1] - ppd[pmId][1])]

            prev = edDB[pmCPUUtilErrorData]
            prev[pmId] = edpd
            edDB[pmCPUUtilErrorData] = prev
            edDB.close()
            pdDB.close()
            originPWL = MAUtilForUtil(self.historyData[pmId])
        else:
            B = self.calculateB(pmId)

            #debug
            #if self.historyData[pmId][hdLen - 1] == 3790405 or self.historyData[pmId][hdLen - 1] == 2289805:
            #    print B

            totalPastHWD = sum(self.historyData[pmId]) - self.historyData[pmId][hdLen - 1]
            totalAVG = totalPastHWD / (hdLen - 1) + 1

            originPWL = (1 - B) * self.historyData[pmId][hdLen - 1] + B * totalAVG
        #差这个！！
        return self.adjustByAnalyseError(pmId, originPWL)

