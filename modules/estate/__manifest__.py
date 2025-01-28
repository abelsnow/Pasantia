# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'estate',
    'version' : '1.0',
    'category': 'bienes y raices',
    'sequence': 15,
    'summary':"",
    'website':"",
    'depends': ['base'],
    'demo': [],
    'installable': True,
    'application': True,
    'assets':{},
    'license':'',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
