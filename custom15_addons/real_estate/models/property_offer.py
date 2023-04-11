# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json


from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils


class Propertyoffer(models.Model):
    _name = "property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', string='Partner', required=False)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False, required=False)
    property_id = fields.Many2one('real_estate.order', string='Property')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date', inverse='_inverse_date', store=True)
    property_type_id = fields.Many2one('property.type', string='Property Type', related="property_id.property_type_id",
                                       store=True)

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
        self.write({"status": "accepted"})
        self.property_id.write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer_id": self.partner_id})

    def action_refuse(self):
        return self.write({"status": "refused"})

    # def create(self, vals):
    #     res = super().create(vals)
    #     self.property_id.state = 'offer_received'
    #     return res

    # def write(self,vals):
    #     line =

    # @api.model
    # def create(self, vals):
    #     x = super().create(vals)
    #     print("offer:", x)
    #     # for rec in self:
    #     #     if rec.property_id:
    #     #         rec.property_id.state = 'offer_received'
    #     # return x

    # @api.model
    # def create(self, vals):
    #     x = super().create(vals)
    #     for rec in self:
    #         if rec.property_id:
    #             rec.property_id.state = 'offer_received'

