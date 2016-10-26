#!/usr/bin/env python
# encoding: utf-8

import math
import numpy as np

from ACRCUtil.ACRCRuleChecker import ACRCRuleChecker
from ACRCUtil.ProvisionComponent import ProvisionComponent
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
from DBUtil.WorkloadDBUtil import WorkloadDBUtil
from LoggingUtil import getLogUtil
from NormalUtil import *
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from PredictUtil import *
from PredictUtil.ACRCPredictUtil import ACRCPredictUtil

# 不传参数默认日志级别是info
logger = getLogUtil('ACRCProvisionComponent')


class EACRCProvisionComponent(ProvisionComponent):
    def __init__(self, predictor=ACRCPredictUtil(), ruleChecker=ACRCRuleChecker()):
        super(EACRCProvisionComponent, self).__init__(predictor, ruleChecker)

    def getNumberOfVMsShouldBeScaled(self):
        if not self.predictor or not self.ruleChecker:
            raise Exception('no predictor or ruleChecker')

        newestHD = WorkloadDBUtil.getNewestWorkload()

        if not newestHD:
            raise Exception('Can not get newest workload')

        addWLToACRCWindow(newestHD['realWL'])
        predictWL = self.predictor.getNextPeriodWorkload()
        addPWLToACRCWindow(predictWL)

        # 预测写入Workload表
        periodNoDB = shelve.open(periodRecoderFile)
        periodNo = periodNoDB.get(periodRecoder, None)
        if not periodNo:
            raise Exception('Can not get periodNo')

        # do linear regression in given windowSize
        # TODO: temporarily use default windowSize = sys.maxint
        pairs = WorkloadDBUtil.getRealWorkloadAndRealTotalCalculationInPairs()
        wl = pairs[0]
        tc = pairs[1]
        # TODO: do not fix the interception temporarily, might let the line cross the origin later
        regression = np.polyfit(wl, tc, 1)
        k = float(regression[0])
        b = float(regression[1])

        if k < 0:
            # actually k should be positive, here to eliminate corner case when there's not much log
            new_k = tc[-1] / wl[-1]
            logger.warning("k = " + str(k) + " is negative, using k = " + str(new_k) + " instead")
            predictTC = new_k * predictWL
        else:
            predictTC = k * predictWL + b

        WorkloadDBUtil.addPredictWorkloadAndPredictTotalCalculationToSpecificPeriod(periodNo, predictWL, predictTC)

        predictVMNumbers = math.ceil(predictTC / TomcatInstanceUtil.getCalculationCapacityPerInstance())

        # 记录供给的虚拟机数目的分布
        provisionInfoDB = shelve.open(provisionInfoFile)

        provisionInfoDB[predictProvisionVMNumbers] = predictVMNumbers

        logger.info('PredictWorkload:' + str(predictWL) + ' predictVMNumbers:' + str(predictVMNumbers)
                    + ' predictTC: ' + str(predictTC))

        addedVMNumbers = self.ruleChecker.getNextAddedVMs()

        provisionInfoDB[reactiveProvisionVMNumbers] = addedVMNumbers

        logger.info('addedVMNumbers:' + str(addedVMNumbers))

        provisionInfoDB.close()

        nextPeriodVMNumbers = predictVMNumbers + addedVMNumbers

        usingInstancesCount = UsingInstancesDBUtil.getUsingInstancesCount()
        gab = abs(usingInstancesCount - nextPeriodVMNumbers)

        if usingInstancesCount > nextPeriodVMNumbers:
            rt = {'vmNumbers': gab, 'isUp': False}
        elif usingInstancesCount < nextPeriodVMNumbers:
            rt = {'vmNumbers': gab, 'isUp': True}
        else:
            rt = {'vmNumbers': gab}

        logger.info('return with:' + str(rt))

        return rt
