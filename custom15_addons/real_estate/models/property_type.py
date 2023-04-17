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

class propertytype(models.Model):
    _name = "property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(string='name')
    property_ids = fields.One2many('real_estate.order', 'property_type_id', string="Properties")
    sequence = fields.Integer(string='Sequence')
    offer_ids = fields.One2many('property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer count', compute='_compute_offer_count')



    def preview_offers(self):
        print("test")

    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    # @api.model
    # def create(self, vals):
    #     res = super().create(vals)
    #     if self.env.user.has_group('real_estate.group_estate_group_user'):
    #         raise AccessError(_('Real estate agents are not allowed to create new property types or tags.'))
    #     return res