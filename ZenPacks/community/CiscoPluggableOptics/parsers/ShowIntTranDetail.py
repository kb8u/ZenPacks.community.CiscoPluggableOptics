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
to collect optical performance measurements.
"""
import re
import pprint
import logging
from Products.ZenRRD.CommandParser import CommandParser


logger = logging.getLogger('.'.join(['zen', __name__]))

# see http://wiki.zenoss.org/Developing_a_Command_Parser-Based_ZenPack
class ShowIntTranDetail(CommandParser):

    def processResults(self, cmd, result):
        log.debug('In processResults, got output: %s' %
                  pprint.pformat(cmd.result.output))
