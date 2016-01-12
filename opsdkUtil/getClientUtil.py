#!/usr/bin/python
from opsdkUtil.credential import *
from novaclient import client as novaclientProxy
import ceilometerclient.client

class GetClientUtil(object):
    @staticmethod
    def getNovaClient(version=NOVA_VERSION, userName=USER_NAME, userPassword=USER_PASSWORD, projectId=PROJECT_ID, authUrl=AUTH_URL):
        return novaclientProxy.Client(version, userName, userPassword, projectId, authUrl)

    @staticmethod
    def getCeilometerClient(version=CEILOMETER_VERSION, userName=USER_NAME, userPassword=USER_PASSWORD, projectId=PROJECT_ID, authUrl=AUTH_URL):
        return ceilometerclient.client.get_client(version, os_username=userName, os_password=userPassword, os_tenant_name=projectId, os_auth_url=authUrl)

