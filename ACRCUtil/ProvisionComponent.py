#!/usr/bin/env python
# encoding: utf-8

class ProvisionComponent(object):
    def __init__(self, predictor=None, ruleChecker=None):
        self.predictor = predictor
        self.ruleChecker = ruleChecker

    def getNumberOfVMsShouldBeScaled(self):
        pass
