{
    'name': 'factura',
    'version': '1.0',
    'description': 'facturo',
    'summary': 'modulo de facturacion',
    'author': 'Abel Noguera',
    'depends': [
        'mi_modulo','account'
    ],
    'data': [
    'security/restablecer_borrador_security.xml',
    'views/account_move_view.xml',
],
    'installable': True,
    'application': True,
    
}