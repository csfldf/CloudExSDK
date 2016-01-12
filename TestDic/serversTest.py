#!/usr/bin/env python
# encoding: utf-8

#import NovaUtil.TomcatInstanceUtil
from NovaUtil.TomcatInstanceUtil import TomcatInstanceUtil
from opsdkUtil.getClientUtil import GetClientUtil
from NovaUtil.FlavorUtil import FlavorUtil

nova = GetClientUtil.getNovaClient()
#instance = nova.servers.list(search_opts = {'name':'sjyvm-1'})
#print instance
#smallFlavor = FlavorUtil.findFlavorByName('m1.small')
#print 'get' + smallFlavor.name
#instance = nova.servers.create('sjy-x', 'skvmModel', smallFlavor)
#print nova.servers.ips(nova)

instance = TomcatInstanceUtil.createTomcatInstance()
