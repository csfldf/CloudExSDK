#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.eACRCProvisionComponent import EACRCProvisionComponent
from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil


class ACRController(object):
    def __init__(self, provisionComponent=EACRCProvisionComponent(), placementComponent=ACRCPlacementComponent()):
        self.provisionComponent = provisionComponent
        self.placementComponent = placementComponent

    def autonomicPeriodHandler(self):
        scaleContent = self.provisionComponent.getNumberOfVMsShouldBeScaled()

        # re-organize the code, maintaining the logic
        if scaleContent['vmNumbers'] == 0:
            TomcatInstanceUtil.resetAllUsingInstances()
        elif scaleContent['isUp']:
            TomcatInstanceUtil.resetAllUsingInstances()
            self.placementComponent.getPlacementScheme(scaleContent['vmNumbers'], scaleContent['isUp'])
        else:
            self.placementComponent.getPlacementScheme(scaleContent['vmNumbers'], scaleContent['isUp'])
            TomcatInstanceUtil.resetAllUsingInstances()
