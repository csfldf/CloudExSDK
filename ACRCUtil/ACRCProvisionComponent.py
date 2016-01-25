#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.ProvisionComponent import ProvisionComponent
from PredictUtil import *
from DBUtil.WorkloadDBUtil import WorkloadDBUtil

class ProvisionComponent(ProvisionComponent):

    def getNumberOfVMsShouldBeScaled(self):
        if not self.predictor or not self.ruleChecker:
            raise Exception('no predictor or ruleChecker')

        newstHD = WorkloadDBUtil.getNewstWorkload()

        if not newstHD:
            raise Exception('Can not get newest workload')

        addWLToACRCWindow(wl)




