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

    buyer_id = fields.Many2one('res.partner', string='Buyer')
    # date = fields.Date(string='Appointment Date')

    def create_appointment(self):
        print("xyz")
        x = {
            'buyer_id': self.buyer_id
        }
        self.env['real_estate.order'].create(x)