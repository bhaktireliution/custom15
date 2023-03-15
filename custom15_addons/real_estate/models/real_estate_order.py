#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils

class realestateorder(models.Model):
    _name = "real_estate.order"
    _description = "Real Estate Order"
    _order = 'date_order desc, id desc'
    _check_company_auto = True

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    description = fields.Text(string='Description', required=True, readonly=True)
    postcode = fields.Char(string='Postcode', required=True, readonly=True)
    date_availability = fields.Date(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    expected_price = fields.Float(string='Expected Price', store=True)
    selling_price = fields.Float(string='Selling Price', store=True)
    bedrooms = fields.Integer(string='Bedrooms', compute='_get_invoiced')
    living_area = fields.Integer(string='Living Area', compute='_get_invoiced')
    facades = fields.Integer(string='Facades', compute='_get_invoiced')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
