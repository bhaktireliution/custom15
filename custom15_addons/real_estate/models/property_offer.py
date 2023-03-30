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

class Propertyoffer(models.Model):
    _name = "property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', string='Partner', required=False)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False, required=False)
    property_id = fields.Many2one('real_estate.order', string='Property')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', defaul='rec.create_date', compute='_compute_date', inverse='_inverse_date', store=True)


    @api.depends('create_date')
    def _compute_date(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date + timedelta(days=rec.validity)

    def _inverse_date(self):
        for rec in self:
            if rec.date_deadline:
                rec.validity = (fields.Datetime.to_datetime(rec.date_deadline) - rec.create_date).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True