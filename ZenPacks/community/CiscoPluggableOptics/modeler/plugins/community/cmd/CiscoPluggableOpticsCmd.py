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
import pprint
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

        # lines that match these indicate a sensor type change
        temperature_re = re.compile('celsius',re.IGNORECASE)
        voltage_re = re.compile('volt',re.IGNORECASE)
        transmit_re = re.compile('transmit',re.IGNORECASE)
        receive_re = re.compile('receive',re.IGNORECASE)
        intf_re = re.compile(r'^(g[ie]*\d+\S+)',re.IGNORECASE)

        # loop over lines from device & find ports with various types of sensors
        sensor = {}
        current_sensor = None
        for line in results.split('\n'):
            if temperature_re.search(line):
               log.debug('changed current_sensor: %s' % current_sensor)
               current_sensor = 'cmdCelsius'
               sensor[current_sensor] = []
            if voltage_re.search(line):
               log.debug('changed current_sensor: %s' % current_sensor)
               current_sensor = 'cmdVoltsdc'
               sensor[current_sensor] = []
            if transmit_re.search(line):
               log.debug('changed current_sensor: %s' % current_sensor)
               current_sensor = 'cmdTxDbm'
               sensor[current_sensor] = []
            if receive_re.search(line):
               log.debug('changed current_sensor: %s' % current_sensor)
               current_sensor = 'cmdRxDbm'
               sensor[current_sensor] = []

            line.strip(' \n')
            if intf_re.search(line):
                intf = intf_re.search(line).groups()[0]
                log.debug('found intf: %s' % intf)
                if current_sensor:
                    sensor[current_sensor].append(intf)

        # loop over lines to find column positions of description
        next_line_has_column_headers = False
        descr_pos = 0
        for line in results.split('\n'):
            if line.endswith('show interface description'):
                next_line_has_column_headers = True
            if next_line_has_column_headers:
                columns = line.split()
                for column in columns:
                    if re.match(r'^descr',re.IGNORECASE):
                        descr_pos = line.find(column)

        # loop over lines and find interface description
        intf_descr = {}
        for line in results.split('\n'):

        log.debug(pprint.pformat(sensor))
        return       
        
        rm = self.relMap()
        for sensor_type in sensor:
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
            
