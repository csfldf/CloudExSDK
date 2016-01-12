#!/usr/bin/python

from NovaUtil.FlavorUtil import FlavorUtil
from opsdkUtil.getClientUtil import GetClientUtil

nova = GetClientUtil.getNovaClient()
#FlavorUtil.deleteFlavorByName('custom2')

#nova.flavors.create('dzw', '2048', 1, '150', 'auto', 0)

#fl = nova.flavors.list()
#for f in fl:
#    print f.name

#f = FlavorUtil.findFlavorByName('dzw')
#f.name = 'aaa'
#f.set_keys({'name' : 'dzwCasco'})
print nova.flavors.resource_class

