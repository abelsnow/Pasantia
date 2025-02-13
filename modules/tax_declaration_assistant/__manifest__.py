# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'tax_declaration_assistant',
    'version': '0.1',
    'category': 'Accounting',
    'sequence': 15,
    'summary': '',
    'website': '',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tax_declaration_assistant_menus.xml',
        'views/tax_declaration_assistant_views.xml',
        
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': '',

}
