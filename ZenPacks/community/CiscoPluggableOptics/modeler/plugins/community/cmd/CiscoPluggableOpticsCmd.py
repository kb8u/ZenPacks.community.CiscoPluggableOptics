################################################################################
#
# This program is part of the CiscoPluggableOptics Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Log into a Cisco switch or router using telnet and issue commands
to locate pluggable optics modules.
"""

import re
#from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


#class CiscoPluggableOpticsCmd(CommandPlugin):
class CiscoPluggableOpticsCmd(PythonPlugin):
    "Map Cisco Entity sensors on intefaces to the python class for them"

    # The command to run.
    command = "terminal length 0\nsho int tran detail"

    modname = "ZenPacks.community.CiscoPluggableOptics.CiscoPluggableOptics"
    relname = "cards"
    compname = "hw"

    ######## delete this when changing to Command plugin!!!!
    def collect(self,device,log):
        log.info('Starting CiscoPluggableOpticsCmd modeler')
        to_add_file = '/home/zenoss/zenpacks/ZenPacks.community.CiscoPluggableOptics/ZenPacks/community/CiscoPluggableOptics/modeler/plugins/community/cmd/sample_output.txt'
        results = ''
        try:
            f = open(to_add_file)
            results = f.read()
            f.close()
        except IOError:
            log.error("Couldn't open %s" % to_add_file)
        return results


    def process(self, device, results, log):
        log.info("Starting process() for modeler CiscoPluggableOpticsCmd")
        log.info('got results: %s' % results)
        return

        objectmaps = []

        # process results (which contains output from command) and get
        # inteface names, etc.
        intfs = []
        sensorType = []
        sensorScale = []
        sensorPrecision = []

        rm = self.relMap()
        for intf in intfs:
            om = self.objectMap()
            om.id = self.prepId(intf)
            om.title = intf
            om.snmpindex = 0
            om.ifDescr = somethingortheother
            om.ifAlias = somethingelse
            om.ifIndex = 0
            om.entSensorType = sensorType['intf']
            om.entSensorScale = sensorScale['intf']
            om.entSensorPrecision = sensorPrecision['intf']
            om.monitor = True
            rm.append(om)
        return rm
            
