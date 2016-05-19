#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.BasePredictUtil import BasePredictUtil

class VMCPUPredictUtil(BasePredictUtil):
    #errorRatio在上一个周期的错误和之前的错误的平均值两者之间加权算错误用
    def __init__(self, windowSize=periodicHistoryWindowSize, historyData=None, historyDataFile=utilHistoryDataFile, historyDataName=vmCPUUtilHistoryData, errorRatio=0.5):
        if not historyData and historyDataFile:
            hdDB = shelve.open(historyDataFile)
            historyData = hdDB[historyDataName]
            hdDB.close()
        super(VMCPUPredictUtil, self).__init__(windowSize, historyData, historyDataFile, historyDataName)
        self.errorRatio = errorRatio

    def calculateB(self, vmIP):
        pdDB = shelve.open(utilPredictDataFile)
        ppd = pdDB.get(vmCPUUtilPredictData, None)

        edDB = shelve.open(utilErrorDataFile)
        epd = edDB.get(vmCPUUtilErrorData, None)

        #print ppd, epd

        if not ppd or not epd or vmIP not in ppd or vmIP not in epd:
            raise Exception('no predictData or not epd!')

        hl = len(self.historyData[vmIP])
        pl = len(ppd[vmIP])


        if hl != pl:
            raise Exception('the length of historyData and predictData not same!')

        avgE = sum(epd[vmIP]) / len(epd[vmIP])

        newestHWL = self.historyData[vmIP][hl - 1]
        newestPWL = ppd[vmIP][pl - 1]

        newE = (1 - self.errorRatio) * abs(newestHWL - newestPWL) + self.errorRatio * avgE
        addDataToWindow(epd[vmIP], newE, errorParamWindowSize)
        edDB[vmCPUUtilErrorData] = epd

        maxE = max(epd[vmIP])
        B = 1 - newE / maxE

        pdDB.close()
        edDB.close()

        return B


    def adjustByAnalyseError(self, vmIP, predictWorkload):
        pdDB = shelve.open(utilPredictDataFile)
        ppd = pdDB.get(vmCPUUtilPredictData, None)
        pdDB.close()


        if not ppd or vmIP not in ppd or not ppd[vmIP]:
            raise Exception('no daily predict data!')
        elif vmIP not in self.historyData and not self.historyData[vmIP]:
            raise Exception('no periodic history data!')
        elif len(ppd[vmIP]) != len(self.historyData[vmIP]):
            raise Exception('the length of periodic predict data and history data!')
        else:
            if ppd[vmIP][0] == firstPeriodPredictData:
                begIndex = 1
                totalNumber = len(ppd[vmIP]) - 1

                #第一个周期
                if len(ppd[vmIP]) == 1:
                    return predictWorkload
            else:
                begIndex = 0
                totalNumber = len(ppd[vmIP])

            indexList = range(begIndex, len(ppd[vmIP]))

            totalGab = 0
            gabList = []
            for ind in indexList:
                gab = self.historyData[vmIP][ind] - ppd[vmIP][ind] if self.historyData[vmIP][ind] > ppd[vmIP][ind] else 0
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

    def getNextPeriodWorkload(self, vmIP):

        self.reloadHistoryData()

        if not self.historyData or vmIP not in self.historyData:
            raise Exception('no historyData!')

        hdLen = len(self.historyData[vmIP])

        if hdLen == 1:
            return self.historyData[vmIP][0]
        if hdLen == 2:
            pdDB = shelve.open(utilPredictDataFile)
            ppd = pdDB.get(vmCPUUtilPredictData, None)

            edDB = shelve.open(utilErrorDataFile)
            edpd = [self.errorRatio * abs(self.historyData[vmIP][1] - ppd[vmIP][1])]
            #print edDB[vmCPUUtilErrorData]
            edDB[vmCPUUtilErrorData] = {vmIP: edpd}
            edDB.close()
            pdDB.close()
            originPWL = MAUtilForUtil(self.historyData[vmIP])
        else:
            B = self.calculateB(vmIP)

            #debug
            #if self.historyData[vmIP][hdLen - 1] == 3790405 or self.historyData[vmIP][hdLen - 1] == 2289805:
            #    print B

            totalPastHWD = sum(self.historyData[vmIP]) - self.historyData[vmIP][hdLen - 1]
            totalAVG = totalPastHWD / (hdLen - 1) + 1

            originPWL = (1 - B) * self.historyData[vmIP][hdLen - 1] + B * totalAVG
            #print originPWL, self.adjustByAnalyseError(vmIP, originPWL)
        return self.adjustByAnalyseError(vmIP, originPWL)
