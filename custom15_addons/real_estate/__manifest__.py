# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate',
    'version': '',
    'category': 'Real Estate/Brokerage',
    'summary': '',
    'description': """""",
    'depends': ['mail', 'sale', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'security/real_estate_security.xml',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        'data/cron.xml',
        'wizard/property_appointment.xml',
        'wizard/sale_wizard.xml',
        'views/real_estate_views.xml',
        'views/property_type.xml',
        'views/property_tags.xml',
        'views/menu.xml',
        'views/res_users_views.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
}