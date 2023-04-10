# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate',
    'version': '',
    'category': '',
    'summary': '',
    'description': """""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_views.xml',
        'views/property_type.xml',
        'views/property_tags.xml',
        'views/menu.xml',
        'views/res_users_views.xml'
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
}