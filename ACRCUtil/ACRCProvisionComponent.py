#!/usr/bin/env python
# encoding: utf-8

import shelve
from PredictUtil import *
from NormalUtil import *
from DBUtil.WorkloadDBUtil import WorkloadDBUtil
from ACRCUtil.ProvisionComponent import ProvisionComponent
from DBUtil.WorkloadVMMapDBUtil import WorkloadVMMapDBUtil
from PredictUtil.ACRCPredictUtil import ACRCPredictUtil
from ACRCUtil.ACRCRuleChecker import ACRCRuleChecker
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil


class ACRCProvisionComponent(ProvisionComponent):
    def __init__(self, predictor=ACRCPredictUtil, ruleChecker=ACRCRuleChecker):
        super(ACRCProvisionComponent, self).__init__(predictor, ruleChecker)


    def getNumberOfVMsShouldBeScaled(self):
        if not self.predictor or not self.ruleChecker:
            raise Exception('no predictor or ruleChecker')

        newestHD = WorkloadDBUtil.getNewestWorkload()

        if not newestHD:
            raise Exception('Can not get newest workload')


        addWLToACRCWindow(newestHD['realWL'])
        predictWL = self.predictor.getNextPeriodWorkload()
        addPWLToACRCWindow(predictWL)

        #预测写入Workload表
        periodNoDB = shelve.open(periodRecoderFile)
        periodNo = periodNoDB.get(periodRecoder, None)
        if not periodNo:
            raise Exception('Can not get periodNo')
        WorkloadDBUtil.addPredictWorkloadToSpecificPeriod(periodNo, predictWL)

        #查询需要的VM
        levelStep = WorkloadVMMapDBUtil.getLevelStep()
        level = predictWL / levelStep
        predictVMNumbers = WorkloadVMMapDBUtil.getTargetVMsToSpecificLevel(level)
        addedVMNumbers = self.ruleChecker.getNextAddedVMs()

        nextPeriodVMNumbers = predictVMNumbers + addedVMNumbers

        usingInstancesCount = UsingInstancesDBUtil.getUsingInstancesCount()
        gab = abs(usingInstancesCount - nextPeriodVMNumbers)

        if usingIntancesCount > nextPeriodVMNumbers:
            return {'vmNumbers':gab, 'isUp':False}
        elif usingIntancesCount < nextPeriodVMNumbers:
            return {'vmNumbers':gab, 'isUp':True}
        else:
            return {'vmNumbers':gab}

