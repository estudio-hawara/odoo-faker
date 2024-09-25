{
    'name': 'Faker',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Carlos Capote',
    'category': 'Administration',
    'description': 'Provides support to dynamically generate demo data',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/faker_target_views.xml',
        'views/menu_items.xml'
    ],
    'extenal_dependencies': {
        'python': [
            'Faker'
        ]
    }
}