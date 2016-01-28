#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.ACRCProvisionComponent import ACRCProvisionComponent
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil


class ACRController(object):
    def __init__(self, provisionComponent=ACRCProvisionComponent(), placementComponent=ACRCPlacementComponent()):
        self.provisionComponent = provisionComponent
        self.placementComponent = placementComponent

    def autonomicPeriodHandler(self):
        scaleContent = self.provisionComponent.getNumberOfVMsShouldBeScaled()

        if scaleContent['vmNumbers'] != 0 and scaleContent['isUp']:
            TomcatInstanceUtil.resetAllUsingInstances()
            self.placementComponent.getPlacementScheme(scaleContent['vmNumbers'], scaleContent['isUp'])
        else:
            if scaleContent['vmNumbers'] == 0:
                TomcatInstanceUtil.resetAllUsingInstances()
            else:
                self.placementComponent.getPlacementScheme(scaleContent['vmNumbers'], scaleContent['isUp'])
                TomcatInstanceUtil.resetAllUsingInstances()
