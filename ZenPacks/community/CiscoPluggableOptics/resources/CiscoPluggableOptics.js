/*
###########################################################################
#
# This program is part of the CiscoPluggableOptics ZenPack
# Copyright 2013 by Russell Dwarshuis, Merit Network, Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}


ZC.CiscoPluggableOpticsPanel = Ext.extend(ZC.ComponentGridPanel, {
 constructor: function(config) {
 config = Ext.applyIf(config||{}, {
 componentType: 'CiscoPluggableOptics',
 autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'description'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'description',
                dataIndex: 'description',
                header: _t('Interface description'),
                sortable: true,
                width: 200
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.CiscoPluggableOpticsPanel.superclass.constructor.call(this, config);
    }
});


Ext.reg('CiscoPluggableOpticsPanel', ZC.CiscoPluggableOpticsPanel);
ZC.registerName(
    'CiscoPluggableOptics',
    _t('Pluggable Optics Sensor'),
    _t('Pluggable Optics Sensors'));

})();
