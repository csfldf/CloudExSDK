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
            gab = abs(periodicPredictWL - dailyPredictWL)
            targetGab = int(gab * targetPercent) + 1

            return min(periodicPredictWL, dailyPredictWL) + targetGab

