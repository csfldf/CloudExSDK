#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from PredictUtil.BasePredictUtil import BasePredictUtil

class MAPredictUtil(BasePredictUtil):
    def __init__(self, windowSize=maHistoryWindowSize, historyData=None, historyDataFile=historyDataFile, historyDataName=maHistoryData):
        if not historyData and historyDataFile:
            hdDB = shelve.open(historyDataFile)
            historyData = hdDB[historyDataName]
            hdDB.close()
        super(MAPredictUtil, self).__init__(windowSize, historyData, historyDataFile, historyDataName)


    def getNextPeriodWorkload(self):
        self.reloadHistoryData()

        if not self.historyData:
            raise Exception('no historyData!')

        return MAUtil(self.historyData)
