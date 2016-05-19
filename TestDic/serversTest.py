#!/usr/bin/env python
# encoding: utf-8

#import NovaUtil.TomcatInstanceUtil
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from opsdkUtil.getClientUtil import GetClientUtil
from NovaUtil.FlavorUtil import FlavorUtil
from NovaUtil.InstanceUtil import InstanceUtil
from DBUtil.UsingInstancesDBUtil import UsingInstancesDBUtil
#nova = GetClientUtil.getNovaClient()
#instance = nova.servers.list(search_opts = {'name':'sjyvm-1'})
#print instance
#smallFlavor = FlavorUtil.findFlavorByName('m1.small')
#print 'get' + smallFlavor.name
#instance = nova.servers.create('sjy-x', 'skvmModel', smallFlavor)
#print nova.servers.ips(nova)
#instance = TomcatInstanceUtil.createTomcatInstance()

#instance = InstanceUtil.findInstaceByName('sjyvm-e2c9f0ce-b8fd-11e5-9899-00e04c680ae0')
#instance = InstanceUtil.findInstanceById('3c366418-8a4e-440a-b474-cf4dacd5e6c3')
#print dir(instance)
#print instance.availability-zone


print TomcatInstanceUtil.migrate('34223c71-33b5-4616-a818-2027812dc83b', 'az4')
