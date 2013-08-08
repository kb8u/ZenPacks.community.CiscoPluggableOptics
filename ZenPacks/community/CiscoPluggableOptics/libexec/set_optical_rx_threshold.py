#!/usr/bin/env python

################################################################################
#
# This program is part of the CiscoPluggableOptics Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

usage = '''
Create rrd template local copy and/or update the threshold for receive
optical power on all Cisco Pluggable Optic Modules so that they will
generate a Error level alert if the optical signal degrades 3 dB from
the current value.

set_optical_rx_threshold.py <device>
'''

import sys
import re
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

dmd = ZenScriptBase(connect=True).dmd

# find device on command line (either IP or device id will work)
if len(sys.argv) < 2:
    print usage
    print 'Error: no device specified on command line'
    sys.exit()

device = dmd.Devices.findDevice(sys.argv[1])

if device is None:
    print usage
    print 'Error: Device not found.'
    sys.exit()

for component in device.getMonitoredComponents():
    if component.__class__.__name__ != 'CiscoPluggableOptics':
        continue
    # Don't set a transmit threshold, only receive
    if re.search('receive',component.id,flags=re.IGNORECASE) is None:
        continue
    component.makeLocalRRDTemplate('CiscoPluggableOpticsSensorDbm')
    template = component.getRRDTemplateByName(
                   'CiscoPluggableOpticsSensorDbm')
    if template is None:
        continue

    # find 'Optical signal too low' threshold or continue to next component
    thresholds = template.thresholds()
    if len(thresholds) == 0:
        continue
    for threshold in thresholds:
        if threshold.id == 'Optical signal too low':
            break
    if threshold.id != 'Optical signal too low':
        continue

    # get current value from rrd
    current = component.getRRDValue('entSensorValue_entSensorValue')
    if current is None:
        print '%s threshold not changed:' % component.id
        print 'rrd file is missing or too new. Try again in 10 minutes.'
        continue
    new_minval = current - 30.0
    threshold.minval = str(new_minval)
    threshold.enabled = True

    commit()
    print 'Changed %s threshold to %.1f dBm' % \
                 (component.id,float(new_minval)/10)

print 'Command completed.'
