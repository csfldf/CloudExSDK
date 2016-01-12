#!/usr/bin/env python
# encoding: utf-8

import shelve

class BasePredictUtil(object):
    def __init__(self, windowSize = 7, historyData = None, historyDataFile = None, historyDataName = None):
        self.windowSize = windowSize
        self.historyData = historyData
        self.historyDataFile = historyDataFile
        self.historyDataName = historyDataName

    def reloadHistoryData(self):
        if self.historyDataFile and self.historyDataName:
            hdDB = shelve.open(self.historyDataFile)
            targetData = hdDB[self.historyDataName]
            hdDB.close()
            self.historyData = targetData

    def getNextPeriodWorkload(self):
        pass
