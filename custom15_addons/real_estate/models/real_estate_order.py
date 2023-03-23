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

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=False)
    date_availability = fields.Date(string='Available Date', required=True)
    expected_price = fields.Float(string='Expected Price', store=True, required=False)
    selling_price = fields.Float(string='Selling Price', store=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], copy=False, index=True, tracking=3, default='draft')
    property_type_id = fields.Many2one('property.type', string='Property Type')
    other_info = fields.Text(string='Other Info', required=False)
    salesman_id = fields.Many2one('res.partner', string='Salesman')
    buyer_id = fields.Many2one('res.users', string='Buyer')
    tag_id = fields.Many2many('property.tag', string='Property Tag')
    offer_ids = fields.One2many('property.offer', 'property_id', string='Offers')

    @api.onchange("garden")
    def onchange_garden(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_area = 10
                rec.garden_orientation = 'north'
            else:
                rec.garden_area = 0
                rec.garden_orientation = None