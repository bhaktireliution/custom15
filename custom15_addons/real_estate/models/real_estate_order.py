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
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')
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
    total_area = fields.Integer(string='Total Area(sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Price', compute='_compute_best_offer')

    @api.depends('offer_ids.validity', 'offer_ids.date_deadline')
    def _compute_date(self):
        for rec in self:
            rec.date_deadline = rec.validity + rec.date_availability

    def _inverse_date(self):
        for rec in self:
            rec.validity = rec.date_availability + rec.validity


    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = 0
            for offer1 in range(len(rec.offer_ids)):
                for offer2 in range(offer1 + 1, len(rec.offer_ids)):
                    if rec.offer_ids[offer1].price < rec.offer_ids[offer2].price:
                        rec.best_offer = rec.offer_ids[offer2].price


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.onchange("garden")
    def onchange_garden(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_area = 10
                rec.garden_orientation = 'north'
            else:
                rec.garden_area = 0
                rec.garden_orientation = None