#!/usr/bin/env python
# encoding: utf-8

from ACRCUtil.ACRCPlacementComponent import ACRCPlacementComponent

a = ACRCPlacementComponent()
a.getPlacementScheme(1, False)
print a.calculateAvailability()
