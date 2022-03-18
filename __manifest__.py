# -*- coding: utf-8 -*-
{
    'name': "McEasy HRS",

    'summary': """
        McEasy HRS module
    """,

    'description': """
    """,

    'author': "McEasy",
    'website': "https://www.mceasy.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'muk_web_theme'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mce_menu.xml',
        'views/mce_employee_views.xml',
        'views/mce_leave_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
