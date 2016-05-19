#!/usr/bin/env python
# encoding: utf-8

import shelve

historyDataFile = '/home/sk/image/cloudExData/workloadData.db'
dailyHistoryData = 'DAILYHISTORYDATA'
periodicHistoryData = 'PERIODICHISTORYDATA'
maHistoryData = 'MAHISTORYDATA'
acrcHistoryData = 'ACRCHISTORYDATA'
dailyHistoryWindowSize = 7
periodicHistoryWindowSize = 4
maHistoryWindowSize = periodicHistoryWindowSize
acrcHistoryWindowSize = periodicHistoryWindowSize

predictDataFile = '/home/sk/image/cloudExData/predictWorkload.db'
dailyPredictData = 'DAILYPREDICTDATA'
periodicPredictData = 'PERIODICPREDICTDATA'
maPredictData = 'MAPREDICTDATA'
acrcPredictData = 'ACTCPREDICTDATA'
statPredictData = 'STATPREDICTDATA'
dailyPredictWindowSize = 7
periodicPredictWindowSize = periodicHistoryWindowSize
maPredictWindowSize = maHistoryWindowSize
acrcPredictWindowSize = acrcHistoryWindowSize
firstPeriodPredictData = -1

errorParamDataFile = '/home/sk/image/cloudExData/errorParam.db'
errorParamData = 'ERRORPARAMDATA'
errorParamWindowSize = periodicHistoryWindowSize

utilHistoryDataFile = '/home/sk/image/cloudExData/utilData.db'
pmCPUUtilHistoryData = 'PMCPUUTILHISTORYDATA'
vmCPUUtilHistoryData = 'VMCPUUTILHISTORYDATA'

utilPredictDataFile = '/home/sk/image/cloudExData/predictUtil.db'
pmCPUUtilPredictData = 'PMCPUUTILPREDICTDATA'
vmCPUUtilPredictData = 'VMCPUUTILPREDICTDATA'

utilErrorDataFile = '/home/sk/image/cloudExData/utilErrorData.db'
pmCPUUtilErrorData = 'PMCPUUTILERRORDATA'
vmCPUUtilErrorData = 'VMCPUUTILERRORDATA'



def addWLToPeriodicWindow(workloadData):
    hdDB = shelve.open(historyDataFile)
    periodicHD = hdDB.get(periodicHistoryData, None)

    if not periodicHD:
        periodicHD = [workloadData]
    else:
        addDataToWindow(periodicHD, workloadData, periodicHistoryWindowSize)

    hdDB[periodicHistoryData] = periodicHD
    hdDB.close()

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


def addPMCPUUtilToPeriodicWindow(pmId, pmCPUUtil):
    utilDB = shelve.open(utilHistoryDataFile)
    pmCPUUtilHD = utilDB.get(pmCPUUtilHistoryData, None)

    if not pmCPUUtilHD:
        pmCPUUtilHD = {}

    if pmId not in pmCPUUtilHD:
        pmCPUUtilHD[pmId] = [pmCPUUtil]
    else:
        addDataToWindow(pmCPUUtilHD[pmId], pmCPUUtil, periodicHistoryWindowSize)

    utilDB[pmCPUUtilHistoryData] = pmCPUUtilHD
    utilDB.close()

def addVMCPUUtilToPeriodicWindow(vmIP, vmCPUUtil):
    utilDB = shelve.open(utilHistoryDataFile)
    vmCPUUtilHD = utilDB.get(vmCPUUtilHistoryData, None)

    if not vmCPUUtilHD:
        vmCPUUtilHD = {}

    if vmIP not in vmCPUUtilHD:
        vmCPUUtilHD[vmIP] = [vmCPUUtil]
    else:
        addDataToWindow(vmCPUUtilHD[vmIP], vmCPUUtil, periodicHistoryWindowSize)

    utilDB[vmCPUUtilHistoryData] = vmCPUUtilHD
    utilDB.close()


def addWLToMAWindow(workloadData):
    hdDB = shelve.open(historyDataFile)
    maHD = hdDB.get(maHistoryData, None)

    if not maHD:
        maHD = [workloadData]
    else:
        addDataToWindow(maHD, workloadData, maHistoryWindowSize)

    hdDB[maHistoryData] = maHD
    hdDB.close()

def addWLToACRCWindow(workloadData):

    addWLToDailyWindow(workloadData)
    addWLToPeriodicWindow(workloadData)

    hdDB = shelve.open(historyDataFile)
    acrcHD = hdDB.get(acrcHistoryData, None)

    if not acrcHD:
        acrcHD = [workloadData]
    else:
        addDataToWindow(acrcHD, workloadData, acrcHistoryWindowSize)

    hdDB[acrcHistoryData] = acrcHD
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
    hdDB[acrcHistoryData] = []
    hdDB[maHistoryData] = []
    hdDB.close()

    utilhdDB = shelve.open(utilHistoryDataFile)
    utilhdDB[pmCPUUtilHistoryData] = {}
    utilhdDB[vmCPUUtilHistoryData] = {}
    utilhdDB.close()

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


def addPredictPMCPUUtilToPeriodicWindow(pmId, pv):
    if not pmId or not pv:
        raise Exception('no predictData or pmId pass in function addPredictWorkload!')
    pdDB = shelve.open(utilPredictDataFile)
    ppmutilData = pdDB.get(pmCPUUtilPredictData, None)

    if not ppmutilData or pmId not in ppmutilData:
        ppmutilData[pmId] = [firstPeriodPredictData, pv]
    else:
        addDataToWindow(ppmutilData[pmId], pv, periodicPredictWindowSize)

    pdDB[pmCPUUtilPredictData] = ppmutilData
    pdDB.close()


def addPredictVMCPUUtilToPeriodicWindow(vmIP, pv):
    if not vmIP or not pv:
        raise Exception('no predictData or vmIP pass in function addPredictWorkload!')
    pdDB = shelve.open(utilPredictDataFile)
    pvmutilData = pdDB.get(vmCPUUtilPredictData, None)

    if not pvmutilData or vmIP not in pvmutilData:
        pvmutilData[vmIP] = [firstPeriodPredictData, pv]
    else:
        addDataToWindow(pvmutilData[vmIP], pv, periodicPredictWindowSize)

    pdDB[vmCPUUtilPredictData] = pvmutilData
    pdDB.close()


def addPWLToMAWindow(predictWorkloadData):
    utilhdDB.close()
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


def addPWLToACRCWindow(predictWorkloadData):
    if not predictWorkloadData:
        raise Exception('no predictWorkloadData pass in function addPredictWorkload!')
    pdDB = shelve.open(predictDataFile)
    acrcPD = pdDB.get(acrcPredictData, None)

    if not acrcPD:
        acrcPD = [firstPeriodPredictData, predictWorkloadData]
    else:
        addDataToWindow(acrcPD, predictWorkloadData, acrcPredictWindowSize)

    pdDB[acrcPredictData] = acrcPD
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
    pdDB[acrcPredictData] = []
    pdDB[maPredictData] = []
    pdDB.close()

    utilpdDB = shelve.open(utilPredictDataFile)
    utilpdDB[pmCPUUtilPredictData] = {}
    utilpdDB[vmCPUUtilPredictData] = {}
    utilpdDB.close()

def clearErrorData():
    edDB = shelve.open(errorParamDataFile)
    edDB[errorParamData] = []
    edDB.close()

    utiledDB = shelve.open(utilErrorDataFile)
    utiledDB[pmCPUUtilErrorData] = {}
    utiledDB[vmCPUUtilErrorData] = {}
    utiledDB.close()


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

def MAUtilForUtil(targetList):
    return sum(targetList) / len(targetList)

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

