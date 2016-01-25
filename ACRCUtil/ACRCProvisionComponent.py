#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.ProvisionComponent import ProvisionComponent

class ProvisionComponent(ProvisionComponent):

    def getNumberOfVMsShouldBeScaled(self):
        if not self.predictor or not self.ruleChecker:
            raise Exception('no predictor or ruleChecker')


