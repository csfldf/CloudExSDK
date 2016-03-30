#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.BasePredictUtil import BasePredictUtil
from math import floor

class DailyPredictUtil(BasePredictUtil):

    def __init__(self, windowSize=dailyHistoryWindowSize, historyData=None, historyDataFile=historyDataFile, historyDataName=dailyHistoryData, highPercent=0.9):
        if not historyData and historyDataFile:
            hdDB = shelve.open(historyDataFile)
            historyData = hdDB[dailyHistoryData]
            hdDB.close()
        super(DailyPredictUtil, self).__init__(windowSize, historyData, historyDataFile, dailyHistoryData)
        self.highPercent = highPercent

    def predictUsingMA(self, singleHistoryData):
        return MAUtil(singleHistoryData)

    def predictUsingTimeHour(self):
        dailyHDLen = len(self.historyData)
        latestDay = self.historyData[dailyHDLen - 1]
        targetHour = len(latestDay)

        hourHDWindow = []
        if targetHour == 24:
            for day in self.historyData:
                hourHDWindow.append(day[23])
        else:
            for day in self.historyData:
                try:
                    hourHDWindow.append(day[targetHour])
                except IndexError:
                    break

        hourHDWindow.sort()

#        print hourHDWindow

        hhdLen = len(hourHDWindow)
        targetIndex = int(hhdLen * self.highPercent)
        return hourHDWindow[targetIndex]

    #由于DailyHDWindow里面的元素是天（列表），每个元素有24个元素代表
    #该天24小时的请求数目，本函数的作用是从DailyHDwindow中取出最后
    #dailyPredictWindowSize个history data
    def getHourHDWindowForDailyHDWindow(self):
        dhd = self.historyData

        if not dhd:
            return None
        else:
            dhdLen = len(dhd)

            retWindow = []
            if dhdLen == 1:
                singleHDWindowLen = len(dhd[0])
                if singleHDWindowLen >= dailyPredictWindowSize:
                    index = singleHDWindowLen - 1
                    count = 0
                    while count < dailyPredictWindowSize:
                        retWindow.insert(0, dhd[0][index])
                        count += 1
                        index -= 1
                else:
                    for hour in dhd[0]:
                        retWindow.append(hour)

            else:
                latestHDWindow = dhd[dhdLen - 1]
                latestHDWindowLen = len(latestHDWindow)

                if latestHDWindowLen >= dailyPredictWindowSize:
                    index = latestHDWindowLen - 1
                    count = 0
                    while count < dailyPredictWindowSize:
                        retWindow.insert(0, latestHDWindow[index])
                        count += 1
                        index -= 1
                else:
                    for hour in latestHDWindow:
                        retWindow.append(hour)

                    secondaryHDWindow = dhd[dhdLen - 2]
                    secondaryHDWindowLen = len(secondaryHDWindow)

                    index = secondaryHDWindowLen - 1
                    count = latestHDWindowLen

                    while count < dailyPredictWindowSize:
                        retWindow.insert(0, secondaryHDWindow[index])
                        count += 1
                        index -= 1

            return retWindow

    def adjustByAnalyseError(self, predictWorkload):
        pdDB = shelve.open(predictDataFile)
        dpd = pdDB.get(dailyPredictData, None)
        pdDB.close()

        hourHD = self.getHourHDWindowForDailyHDWindow()

        if not dpd:
            raise Exception('no daily predict data!')
        elif not hourHD:
            raise Exception('no hour history data!')
        elif len(dpd) != len(hourHD):
            raise Exception('the length of daily predict data and hour history data!')
        else:
            if dpd[0] == firstPeriodPredictData:
                begIndex = 1
                totalNumber = len(dpd) - 1

                #第一个周期
                if len(dpd) == 1:
                    return predictWorkload
            else:
                begIndex = 0
                totalNumber = len(dpd)

            indexList = range(begIndex, len(dpd))

            totalGab = 0
            gabList =[]
            for ind in indexList:
                gab = hourHD[ind] - dpd[ind] if hourHD[ind] > dpd[ind] else 0
                gabList.append(gab)
                totalGab += gab
            #avg
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
        else:
            dailyHDLen = len(self.historyData)
            if dailyHDLen == 1:
                firstDay = self.historyData[0]

                if not firstDay:
                    raise Exception('no firstDay history data!')

                if len(firstDay) == 1:
                    return firstDay[0]
                else:
                    originPWL = self.predictUsingMA(self.historyData[0])
            else:
                originPWL = self.predictUsingTimeHour()
            return originPWL


