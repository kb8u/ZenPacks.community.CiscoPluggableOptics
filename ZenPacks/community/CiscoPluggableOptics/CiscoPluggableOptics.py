################################################################################
#
# This program is part of the CiscoPluggableOptics Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoPluggableOptics

CiscoPluggableOptics is used to measure temperature, supply voltage, bias
current, transmit power and receiver power on Cisco pluggable optical
modules.
"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS, ZEN_VIEW_HISTORY

from Products.ZenModel.ExpansionCard import ExpansionCard

import logging
log = logging.getLogger('CiscoPluggableOptics')


class CiscoPluggableOptics(ExpansionCard, ManagedEntity):
    """CiscoPluggableOptics object"""

    portal_type = meta_type = 'CiscoPluggableOptics'

    # set default _properties
    ifDescr = 'Not set by modeler'   # from IF-MIB ifEntry table
    ifAlias = ''                     # from IF-MIB ifXEntry table
    physDescr = 'Not set by modeler' # entPhysicalDescr from entPhysicalTable
    ifIndex = -1                    # index for above
    # the following are from the entSensorValues table
    entSensorType = 'unknown' # like amperes, celsius, dBm, voltsDC
    entSensorScale = 1        # a power of 10
    entSensorPrecision = 1

    _properties = (
        {'id': 'ifDescr', 'type':'string', 'mode':''},
        {'id': 'ifAlias', 'type':'string', 'mode':''},
        {'id': 'physDescr', 'type':'string', 'mode':''},
        {'id': 'ifIndex', 'type':'int', 'mode':''},
        {'id': 'entSensorType','type': 'string','mode':''},
        {'id': 'entSensorScale','type': 'float','mode':''},
        {'id': 'entSensorPrecision','type': 'int','mode':''},
    )

    factory_type_information = (
        {
            'id'             : 'CiscoPluggableOptics',
            'meta_type'      : 'CiscoPluggableOptics',
            'description'    : "Sensor monitoring of optical modules",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCiscoPluggableOptics',
            'immediate_view' : 'viewCiscoPluggableOptics',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCiscoPluggableOptics'
                , 'permissions'   : (ZEN_VIEW)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_HISTORY)
                },
            )
          },
        )

    def viewName(self):
        return self.physDescr
    name = viewName

    def getRRDTemplateName(self):
        return 'CiscoPluggableOpticsSensor' + self.entSensorType.capitalize()

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete Component
        """
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())


InitializeClass(CiscoPluggableOptics)

