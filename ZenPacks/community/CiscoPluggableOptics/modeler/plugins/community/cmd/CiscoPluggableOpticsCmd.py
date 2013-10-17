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
    """Map Cisco Entity sensors on intefaces to the python class for them.
Assumes data that looks like file sample_output.txt"""


    # The command to run.
    command =   "terminal length 0\n" \
              + "terminal width 254\n" \
              + "sho int tran detail\n" \
              + "show interface description\n"

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
        bias_re = re.compile('\s+\(mA\)\s+')
        transmit_re = re.compile('transmit',re.IGNORECASE)
        receive_re = re.compile('receive',re.IGNORECASE)
        intf_re = re.compile(r'^(g[ie]*\d+\S+)',re.IGNORECASE)

        # loop over lines from device & find ports with various types of sensors
        log.debug('Pass 1 on results, checking for sensors...')
        sensor = {}
        current_sensor = None
        for line in results.split('\n'):
            log.debug('Processing line %s' % line)
            if temperature_re.search(line):
               current_sensor = 'cmdCelsius'
               sensor[current_sensor] = []
               log.debug('changed current_sensor: %s' % current_sensor)
            if voltage_re.search(line):
               current_sensor = 'cmdVoltsdc'
               sensor[current_sensor] = []
               log.debug('changed current_sensor: %s' % current_sensor)
            if bias_re.search(line):
               current_sensor = 'cmdMilliamps'
               sensor[current_sensor] = []
               log.debug('changed current_sensor: %s' % current_sensor)
            if transmit_re.search(line):
               current_sensor = 'cmdTxDbm'
               sensor[current_sensor] = []
               log.debug('changed current_sensor: %s' % current_sensor)
            if receive_re.search(line):
               current_sensor = 'cmdRxDbm'
               sensor[current_sensor] = []
               log.debug('changed current_sensor: %s' % current_sensor)

            line.strip(' \n')
            if intf_re.search(line):
                intf = intf_re.search(line).groups()[0]
                log.debug('found intf: %s' % intf)
                if current_sensor:
                    sensor[current_sensor].append(intf)

            # no more sensors in output once next command starts
            if line.endswith('show interface description'):
                break

        if not sensor:
            log.info("Couldn't find any optical sensors on interfaces")
            return 
        else:
            log.debug('found sensors: %s' % pprint.pformat(sensor))

        # loop over lines to find column positions of interface & description
        log.debug('Pass 2 on results, finding column positions...')
        saw_column_headers = False
        interface_pos = 0
        descr_pos = 0
        for line in results.split('\n'):
            log.debug('Processing line %s' % line)
            if line.endswith('show interface description'):
                saw_column_headers = True
                continue
            if saw_column_headers:
                columns = line.split()
                for column in columns:
                    if re.match(r'^descr',column,re.IGNORECASE):
                        descr_pos = line.find(column)
                    if re.match(r'^int',column,re.IGNORECASE):
                        interface_pos = line.find(column)
                break
        log.debug('interface_pos %d descr_pos %d' % (interface_pos,descr_pos))

        # loop over lines and find interface description.
        # This code assumes description comes last and interfaces names do
        # not have whitespace in them.  If that's not the case, more position
        # finding will be necessary
        intf_descr = {}
        if descr_pos == 0:
            log.info("Can't determine interface descriptions")
        else:
            log.debug('Pass 3 on results, checking for interface descriptions')
            saw_column_headers = False
            for line in results.split('\n'):
                log.debug('Processing line %s' % line)
                if line.endswith('show interface description'):
                    saw_column_headers = True
                    continue
                if saw_column_headers:
                    intf = line[interface_pos:].split()[0]
                    log.debug('found intf %s' % intf)
                    if len(line) > descr_pos:
                        intf_descr[intf]  = line[descr_pos:]
                    else:
                        intf_descr[intf] = ''
                    log.debug('interface description: "%s"' % intf_descr[intf])
                # no more interfaces in output once next command starts
                if line.endswith('>'):
                    break
            if not intf_descr:
                log.info('No interface descriptions found')
            else:
                log.debug('interface descriptions: %s' % \
                          pprint.pformat(intf_descr))
            

        rm = self.relMap()
        for sensor_type in sensor:
            sensor_title = ''
            if sensor_type == 'cmdCelsius':
                sensor_title = 'Module Temperature Sensor'
            elif sensor_type == 'cmdVoltsdc':
                sensor_title = 'Supply Voltage Sensor'
            elif sensor_type == 'cmdMilliamps':
                sensor_title = 'Bias Current Sensor'
            elif sensor_type == 'cmdRxDbm':
                sensor_title = 'Receive Power Sensor'
            elif sensor_type == 'cmdTxDbm':
                sensor_title = 'Transmit Power Sensor'
            else:
                log.info('Unknown sensor type %s' % sensor_type)
                continue

            for intf in sensor[sensor_type]:
                om = self.objectMap()
                om.id = self.prepId("%s %s" % (intf,sensor_type))
                om.title = intf + ' ' + sensor_title
                om.snmpindex = 0
                om.ifDescr = intf
                if intf in intf_descr:
                    om.ifAlias = intf_descr[intf]
                else:
                    log.info('No description found for interface %s' % intf)
                    om.ifAlias = ''
                om.physDescr  = "%s %s" % (intf,sensor_type)
                om.ifIndex = 0
                om.entSensorType = sensor_type
                om.entSensorScale = 0
                om.entSensorPrecision = 0
                om.monitor = True
                rm.append(om)
        return rm
