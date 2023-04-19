#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class PropertyAppointment(models.TransientModel):
    _name = "property.appointment"
    _description = "Property Appointment"

    property_type_id = fields.Many2one('property.type', string='Property Type')
    name = fields.Char(string="Name")
    # buyer_id = fields.Many2one('res.partner', string='Buyer')
    # date = fields.Date(string='Appointment Date')
    # postcode = fields.Char(string='Postcode')

    def create_appointment(self):
        x = {
            'property_type_id': self.property_type_id.id,
            'name': self.name
        }
        self.env['real_estate.order'].create(x)
