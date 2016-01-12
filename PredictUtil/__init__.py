#!/usr/bin/env python
# encoding: utf-8

import shelve

historyDataFile = '/home/sk/image/cloudExData/workloadData.db'
dailyHistoryData = 'DAILYHISTORYDATA'
periodicHistoryData = 'PERIODICHISTORYDATA'
maHistoryData = 'MAHISTORYDATA'
dailyHistoryWindowSize = 7
periodicHistoryWindowSize = 4
maHistoryWindowSize = periodicHistoryWindowSize

predictDataFile = '/home/sk/image/cloudExData/predictWorkload.db'
dailyPredictData = 'DAILYPREDICTDATA'
periodicPredictData = 'PERIODICPREDICTDATA'
maPredictData = 'MAPREDICTDATA'
statPredictData = 'STATPREDICTDATA'
dailyPredictWindowSize = 7
periodicPredictWindowSize = periodicHistoryWindowSize
maPredictWindowSize = maHistoryWindowSize
firstPeriodPredictData = -1

errorParamDataFile = '/home/sk/image/cloudExData/errorParam.db'
errorParamData = 'ERRORPARAMDATA'
errorParamWindowSize = periodicHistoryWindowSize

def addDataToWindow(targetList, newData, windowSize):
    windowLen = len(targetList)
    if windowLen == windowSize:
        targetList.pop(0)
        targetList.append(newData)
    else:
        targetList.append(newData)

def addWLToDailyWindow(workloadData):
    hdDB = shelve.open(historyDataFile)
    dailyHD = hdDB.get(dailyHistoryData, None)

    if not dailyHD:
        targetDay = [workloadData]
        dailyHD = [targetDay]
    else:
        windowLen = len(dailyHD)
        targetDay = dailyHD[windowLen - 1]
        hourWindowLen = len(targetDay)

        #要等dailyHistoryWindowSize + 1个元素都装满了24个hour才pop
        if hourWindowLen == 24 and windowLen == dailyHistoryWindowSize + 1:
            newHourWindow = [workloadData]
            dailyHD.pop(0)
            dailyHD.append(newHourWindow)
        elif hourWindowLen == 24 and windowLen < dailyHistoryWindowSize + 1:
            newHourWindow = [workloadData]
            dailyHD.append(newHourWindow)
        else:
            targetDay.append(workloadData)
    hdDB[dailyHistoryData] = dailyHD
    hdDB.close()

def addWLToPeriodicWindow(workloadData):
    hdDB = shelve.open(historyDataFile)
    periodicHD = hdDB.get(periodicHistoryData, None)

    if not periodicHD:
        periodicHD = [workloadData]
    else:
        addDataToWindow(periodicHD, workloadData, periodicHistoryWindowSize)

    hdDB[periodicHistoryData] = periodicHD
    hdDB.close()


def addWLToMAWindow(workloadData):
    hdDB = shelve.open(historyDataFile)
    maHD = hdDB.get(maHistoryData, None)

    if not maHD:
        maHD = [workloadData]
    else:
        addDataToWindow(maHD, workloadData, maHistoryWindowSize)

    hdDB[maHistoryData] = maHD
    hdDB.close()

def getDailyHD():
    hdDB = shelve.open(historyDataFile)
    dailyHD = hdDB.get(dailyHistoryData, None)
    hdDB.close()
    return dailyHD

def getPeriodicHD():
    hdDB = shelve.open(historyDataFile)
    periodicHD = hdDB.get(periodicHistoryData, None)
    hdDB.close()
    return periodicHD

def clearHistoryData():
    hdDB = shelve.open(historyDataFile)
    hdDB[dailyHistoryData] = []
    hdDB[periodicHistoryData] = []
    hdDB.close()

def addPWLToDailyWindow(predictWorkloadData):
    if not predictWorkloadData:
        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
    pdDB = shelve.open(predictDataFile)
    dailyPD = pdDB.get(dailyPredictData, None)

    if not dailyPD:
        dailyPD = [firstPeriodPredictData, predictWorkloadData]
    else:
        addDataToWindow(dailyPD, predictWorkloadData, dailyPredictWindowSize)

    pdDB[dailyPredictData] = dailyPD
    pdDB.close()

def addPWLToPeriodicWindow(predictWorkloadData):
    if not predictWorkloadData:
        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
    pdDB = shelve.open(predictDataFile)
    periodicPD = pdDB.get(periodicPredictData, None)

    if not periodicPD:
        periodicPD = [firstPeriodPredictData, predictWorkloadData]
    else:
        addDataToWindow(periodicPD, predictWorkloadData, periodicPredictWindowSize)

    pdDB[periodicPredictData] = periodicPD
    pdDB.close()


def addPWLToMAWindow(predictWorkloadData):
    if not predictWorkloadData:
        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
    pdDB = shelve.open(predictDataFile)
    maPD = pdDB.get(maPredictData, None)

    if not maPD:
        maPD = [firstPeriodPredictData, predictWorkloadData]
    else:
        addDataToWindow(maPD, predictWorkloadData, maPredictWindowSize)

    pdDB[maPredictData] = maPD
    pdDB.close()

def addPWLToStatWindow(predictWorkloadData):
    if not predictWorkloadData:
        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
    pdDB = shelve.open(predictDataFile)
    statPD = pdDB.get(statPredictData, None)

    if not statPD:
        statPD = [firstPeriodPredictData, predictWorkloadData]
    else:
        statPD.append(predictWorkloadData)

    pdDB[statPredictData] = statPD
    pdDB.close()

def getDailyPD():
    pdDB = shelve.open(predictDataFile)
    dailyPD = pdDB.get(dailyPredictData, None)
    pdDB.close()
    return dailyPD

def getPeriodicPD():
    pdDB = shelve.open(predictDataFile)
    periodicPD = pdDB.get(periodicPredictData, None)
    pdDB.close()
    return periodicPD

def getStatPD():
    pdDB = shelve.open(predictDataFile)
    statPD = pdDB.get(statPredictData, None)
    pdDB.close()
    return statPD

def clearPredictData():
    pdDB = shelve.open(predictDataFile)
    pdDB[dailyPredictData] = []
    pdDB[periodicPredictData] = []
    pdDB[statPredictData] = []
    pdDB.close()

def clearErrorData():
    edDB = shelve.open(errorParamDataFile)
    edDB[errorParamData] = []
    edDB.close()

def clearAllData():
    clearHistoryData()
    clearPredictData()
    clearErrorData()

#def addPredictWorkload(predictWorkloadData):
#    if not predictWorkloadData:
#        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
#    addPWLToDailyWindow(predictWorkloadData)
#    addPWLToPeriodicWindow(predictWorkloadData)
#    addPWLToStatWindows(predictWorkloadData)




def addHistoryWorkload(workloadData):
    if not workloadData:
        raise Exception('no workload data pass in function addHistoryWorkload!')
    addWLToDailyWindow(workloadData)
    addWLToPeriodicWindow(workloadData)

def MAUtil(targetList):
    sumL = sum(targetList)
    tlen = len(targetList)
    return sumL / tlen + 1

def calculateRelativeError(compareList):
    realWorkloadSum = 0
    errorSum = 0

    for hd, pd in compareList:
        realWorkloadSum += hd
        errorSum += abs(pd - hd)

    return float(errorSum) / realWorkloadSum

def calculateQualified(compareList):
    totalCount = len(compareList)
    qualifiedCount = 0

    for hd, pd in compareList:
        if pd >= hd:
            qualifiedCount += 1

    return float(qualifiedCount) / totalCount

