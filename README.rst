==============================
ZenPacks.community.CiscoPluggableOptics README.rst
==============================

About
=====

This ZenPack provides Cisco pluggable optics module monitoring of bias current,
supply voltage, temperature, transmit and receive optical signal levels for
modules that respond via the CISCO-ENTITY-SENSOR-MIB

Also included is a script to set a threshold for monitoring of receive optical
signal levels 3 dBm below the current value.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, 3.2 and 4.2.4.


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `CiscoPluggableOptics ZenPack <http://wiki.zenoss.org/ZenPack:CiscoPluggableOptics>`_.
Install the zenpack through the zenoss GUI and restart zenoss, or copy the .egg file to your Zenoss server and run the following commands as the zenoss user.

    ::

        zenpack --install ZenPacks.community.CiscoPluggableOptics-1.0.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the
CiscoPluggableOptics ZenPack you should clone the git
`repository <https://github.com/kb8u/CiscoPluggableOptics>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/kb8u/CiscoPluggableOptics.git
        zenpack --link --install ZenPacks.community.CiscoPluggableOptics
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Modeler Plugins
---------------

- **community.snmp.CiscoPluggableOpticsMap** - Pluggable Optics Sensor
  modeler plugin.

Monitoring Templates
--------------------

- Devices/CiscoPluggableOpticsSensorAmperes
- Devices/CiscoPluggableOpticsSensorCelcius
- Devices/CiscoPluggableOpticsSensorDbm
- Devices/CiscoPluggableOpticsSensorVoltsdc

Command
------

- Update_optical_power_threshold
Create rrd template local copy and/or update the threshold for receive
optical power on all Cisco Pluggable Optic Modules so that they will
generate a Error level alert if the optical signal degrades 3 dB from
the current value.
