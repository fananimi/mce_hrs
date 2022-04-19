# -*- coding: utf-8 -*-
{
    'name': "McEasy HRIS",

    'summary': """
        McEasy HRIS module
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
        # data
        'data/res.country.state.csv',
        'data/res.country.city.csv',
        'data/res.country.district.csv',
        'data/res.country.subdistrict.csv',
        # 'data/mce_hr.employee.xlsx',
        # 'data/mce_hr.leave.xlsx',

        # security
        'security/mce_hr_security.xml',
        'security/ir.model.access.csv',

        # menuitem
        'views/mce_menu.xml',
        'views/mce_address_views.xml',
        'views/mce_employee_views.xml',
        'views/mce_leave_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
