# -*- coding: utf-8 -*-
{
    'name': "Framework Overrides",

    'summary': """
        Override the base framework definitions.""",

    'description': """
        Override the base framework definitions.
    """,

    'author': "Danny",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'SLR',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [
        'static/src/xml/base.xml',
    ],
}
