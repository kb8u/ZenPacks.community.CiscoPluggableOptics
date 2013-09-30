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
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


class CiscoPluggableOpticsCMD(CommandPlugin):
    "Map Cisco Entity sensors on intefaces to the python class for them"

    # The command to run.
    command = "sho int tran detail"

    modname = "ZenPacks.community.CiscoPluggableOptics.CiscoPluggableOptics"
    relname = "cards"
    compname = "hw"


    def process(self, device, results, log):
        log.info("Starting process() for modeler CiscoPluggableOpticsCmd")

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
            
