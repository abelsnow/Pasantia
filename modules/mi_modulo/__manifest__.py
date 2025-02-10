{
    'name' : 'mi_modulo',
    'version' : '1.0',
    'summary' : 'mi primer modulo',
    'author': 'Abel Noguera',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        
    ],

    'installable': True,
    'application': True,
 }