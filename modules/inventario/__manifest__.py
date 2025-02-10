{
    'name': 'inventario',
    'version': '1.0',
    'description': 'Estoy solito',
    'summary': ' Mi modulo de practica para aprender',
    'author': 'Abel Noguera',
    'depends': [
        'base'
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/lote_views'
            'views/productos_view.xml',
            'views/ubicacion_view.xml',
            'views/menus.xml',
            
             
        
    ],
    
    'installable':True,
    'application': True,
    
}