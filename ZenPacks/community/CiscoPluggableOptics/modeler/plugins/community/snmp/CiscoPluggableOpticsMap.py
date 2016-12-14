################################################################################
#
# This program is part of the CiscoPluggableOptics Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Walk IF-MIB ifEntry ifDescr to find names of interfaces, then
walk entSensorValueTable to find similar entries in entSensorMeasuredEntity
for temperature, bias current, voltage, transmit and receive optical power.
Exclude sensors that have entSensorStatus not equal to 1 (ok)
"""

import re
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap
from pprint import pprint

class CiscoPluggableOpticsMap(SnmpPlugin):
    "Map Cisco Entity sensors on intefaces to the python class for them"

    modname = "ZenPacks.community.CiscoPluggableOptics.CiscoPluggableOptics"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = ( GetTableMap('ifEntry',
                                     '1.3.6.1.2.1.2.2.1',
                                     { '.2' : 'ifDescr' }
                                    ),
                         GetTableMap('ifXEntry',
                                     '1.3.6.1.2.1.31.1.1.1',
                                     { '.18' : 'ifAlias' }
                                    ),
                         GetTableMap('entPhysicalEntry',
                                     '1.3.6.1.2.1.47.1.1.1.1',
                                     { '.2' : 'entPhysicalDescr' }
                                    ),
                         GetTableMap('entSensorValueEntry',
                                     '1.3.6.1.4.1.9.9.91.1.1.1.1',
                                     { '.1' : 'entSensorType',
                                       '.2' : 'entSensorScale',
                                       '.3' : 'entSensorPrecision',
                                       '.5' : 'entSensorStatus' }
                                    ),
                       )

    def process(self, device, results, log):
        """
Run SNMP queries, process returned values, find Cisco PluggableOptics sensors
        """
        log.info('Starting process() for modeler CiscoPluggableOpticsMap')

        # sensor names match if they contain an interface name append with:
        _sensor_regex = r'\s+.*(temperature|current|voltage|power)'

        # from CISCO-ENTITY-SENSOR-MIB
        _SensorDataType = {
          1  : 'other',
          2  : 'unkown',
          3  : 'voltsAC',
          4  : 'voltsDC',
          5  : 'amperes',
          6  : 'watts',
          7  : 'hertz',
          8  : 'celsius',
          9  : 'percentRH',
          10 : 'rpm',
          11 : 'cmm',
          12 : 'truthvalue',
          13 : 'specialEnum',
          14 : 'dBm' }
        _SensorDataScale = {
           7  : .000001,
           8  : .001,
           9  : 1,
           10 : 1000 }

        getdata, tabledata = results
        rm = self.relMap()
        # build dictionary of ifDescr,index and entPhysicalDescr,index
        ifDescrs = {}
        physDescrs = {}
        for index, ifDescr in tabledata.get("ifEntry").iteritems():
            ifDescrs[ifDescr['ifDescr']] = index
        for index, physDescr in tabledata.get("entPhysicalEntry").iteritems():
            physDescrs[physDescr['entPhysicalDescr']] = index

        if not ifDescrs:
            log.info('No ifDescrs found in ifEntry SNMP table')
            return
        if not physDescrs:
            log.info(
                'No entPhysicalDescrs found in entPhysicalEntry SNMP table')
            return

        entSensorValueEntry = tabledata.get('entSensorValueEntry')
        if not entSensorValueEntry:
            log.info('No data returned from entSensorValueEntry SNMP table')
            return
        
        # iterate over ifDescrs to find matching sensors
        for ifDescr, ifIndex in ifDescrs.iteritems():
            intfSlot = 'no ifDescr slot match'
            m = re.search(r"\D+([\d\/]+)(\/\d+)", ifDescr)
            if m:
                intfSlot = m.group(1) + m.group(2)
            for physDescr, physIndex in physDescrs.iteritems():
                physSlot = 'no physDescr slot match'
                m = re.search(r"slot\s+([\d\/]+)\s+transceiver.*\s+(\d+)\s+.*(temperature|current|voltage|power)", physDescr, re.IGNORECASE)
                if m:
                    physSlot = m.group(1) + '/' + m.group(2)
                if re.search(ifDescr + _sensor_regex, physDescr, re.IGNORECASE) or intfSlot == physSlot:
                    # give a friendlier name if the interface name did not match
                    if intfSlot == physSlot:
                        physDescr = re.sub(r'.*slot\s+([\d\/]+)\s+transceiver.*\s+(\d+)',ifDescr,physDescr)
                    try:
                      log.info('Found sensor %s' % physDescr)
                      if entSensorValueEntry[physIndex]['entSensorStatus'] != 1:
                          log.info(
                              '%s entSensorStatus != ok, skipping' % physDescr)
                          continue
                    except KeyError:
                      log.info(
                          "%s did not return it's status, skipping" % physDescr)
                      continue
                    om = self.objectMap()
                    om.id = self.prepId(physDescr)
                    om.title = physDescr
                    om.snmpindex = int(physIndex.strip('.'))
                    om.ifDescr = ifDescr
                    try:
                        om.ifAlias = tabledata.get(
                                         "ifXEntry")[ifIndex]['ifAlias']
                    except KeyError:
                        om.ifAlias = ''
                    om.physDescr = physDescr
                    om.ifIndex = int(ifIndex.strip('.'))
                    # don't create object if there's missing data
                    try:
                        om.entSensorType = _SensorDataType[int(
                           entSensorValueEntry[physIndex]['entSensorType'])]
                        om.entSensorScale = _SensorDataScale[int(
                           entSensorValueEntry[physIndex]['entSensorScale'])]
                        om.entSensorPrecision = int(
                           entSensorValueEntry[physIndex]['entSensorPrecision'])
                    except KeyError:
                        log.info('"%s" is missing entSensor values, skipping' %\
                            physDescr)
                        continue
                    om.monitor = True
                    rm.append(om)

        return rm
